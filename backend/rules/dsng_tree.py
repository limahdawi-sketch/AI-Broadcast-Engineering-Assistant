"""
Deterministic diagnostic engine for the DSNG / Earth Station fault domains.

This is a direct, faithful port of the decision trees originally implemented
client-side in app/dsng-troubleshooter.html, moved to the backend so that:
  - the diagnostic logic has a single source of truth that can be unit tested,
  - future phases (evidence engine, confidence scoring, AI fallback) can call
    into it without re-implementing the trees in Python from scratch,
  - the frontend can eventually become a thin client over this API.

Design follows the "rules first" principle from ARCHITECTURE.md: this module
is 100% deterministic and contains no AI calls. Adding a new fault category
means adding data here -- it never requires touching the API layer.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Option:
    label: str
    next: str


@dataclass
class Node:
    id: str
    question: Optional[str] = None
    options: list[Option] = field(default_factory=list)
    is_result: bool = False
    severity: Optional[str] = None   # "critical" | "warning" | "info"
    title: Optional[str] = None
    steps: list[str] = field(default_factory=list)


@dataclass
class Category:
    id: str
    title: str
    description: str
    root: str


CATEGORIES: list[Category] = [
    Category("no_signal", "Total Signal Loss", "No carrier at all on the receiver", "ns1"),
    Category("poor_quality", "Poor Signal Quality / Dropouts", "Low Eb/No, bit errors, frozen picture", "pq1"),
    Category("cross_pol", "Poor Cross-Polarization", "Weak cross-pol isolation", "cp1"),
    Category("buc_hpa", "BUC / HPA Alarm", "Alarm on the power amplifier unit", "bh1"),
    Category("pointing", "Antenna Pointing Issues", "Difficulty finding the satellite or tracking loss", "ap1"),
    Category("encoding", "Encoding / Video Issues", "Picture breakup or freezing despite a healthy signal", "ev1"),
]

CATEGORY_BY_ID = {c.id: c for c in CATEGORIES}

# ---------------------------------------------------------------------------
# Node graph. Kept as plain dict literals (not classes) for compactness and
# to mirror the original JS `nodes` object 1:1, which makes future diffing
# against the frontend source straightforward.
# ---------------------------------------------------------------------------
_RAW_NODES = {
    # ---------------- NO SIGNAL ----------------
    "ns1": {"q": "Is the modulator/encoder actually transmitting (Tx Active / Carrier ON)?",
            "o": [("Yes", "ns2"), ("No", "ns_r1")]},
    "ns_r1": {"r": 1, "sev": "critical", "title": "No transmission from the modulator",
              "steps": ["Check the unit is powered and receiving mains power",
                        "Confirm the input cable from the camera/source is properly connected",
                        "Check the Carrier ON setting on the modulator interface"]},
    "ns2": {"q": "Does the BUC / HPA show a normal output power reading?",
            "o": [("Yes", "ns3"), ("No", "ns_r2")]},
    "ns_r2": {"r": 1, "sev": "critical", "title": "No output power from BUC/HPA",
              "steps": ["Check power supply and the 10MHz reference link between modulator and BUC",
                        "Check the fuse or protection breaker",
                        "Swap in a redundant unit if the unit will not recover"]},
    "ns3": {"q": "Has it been confirmed the antenna is pointed at the correct satellite "
                 "(beacon receiver or Az/El reading)?",
            "o": [("Yes", "ns4"), ("No", "ns_r3")]},
    "ns_r3": {"r": 1, "sev": "warning", "title": "Likely antenna pointing error",
              "steps": ["Run a peaking procedure using the target satellite's beacon",
                        "Verify the Az/El/Pol angles calculated for your location"]},
    "ns4": {"q": "Are all transmission parameters (uplink frequency, symbol rate, polarization) "
                 "an exact match for the satellite operator's booking?",
            "o": [("Yes", "ns_r5"), ("No", "ns_r4")]},
    "ns_r4": {"r": 1, "sev": "warning", "title": "Transmission settings mismatch",
              "steps": ["Review the technical booking sheet issued by the satellite operator",
                        "Match every setting precisely on the modulator interface"]},
    "ns_r5": {"r": 1, "sev": "info", "title": "Your equipment looks healthy -- coordination needed",
              "steps": ["Contact the satellite operator immediately to confirm carrier reception on their side",
                        "The fault is most likely on the receiving teleport side, not your equipment"]},

    # ---------------- POOR QUALITY ----------------
    "pq1": {"q": "Is the Eb/No or C/N value on the modulator below the usual normal range?",
            "o": [("Yes", "pq2"), ("No", "pq_r1")]},
    "pq_r1": {"r": 1, "sev": "info", "title": "Signal strength is healthy",
              "steps": ["The issue is likely not signal level but FEC/Modulation mismatch between ends",
                        "Check for an incorrect multiplexing assignment"]},
    "pq2": {"q": "Is it currently raining or heavily overcast at your site or at the receiving teleport?",
            "o": [("Yes", "pq_r2"), ("No", "pq3")]},
    "pq_r2": {"r": 1, "sev": "warning", "title": "Rain fade",
              "steps": ["Usually temporary -- monitor until conditions clear",
                        "If ATPC is supported, confirm it is enabled to auto-compensate",
                        "Avoid manually raising power beyond the allowed limit (adjacent-satellite interference risk)"]},
    "pq3": {"q": "Did a quick re-peak of the antenna noticeably improve the reading?",
            "o": [("Yes", "pq_r3"), ("No", "pq4")]},
    "pq_r3": {"r": 1, "sev": "warning", "title": "Slight antenna pointing drift",
              "steps": ["Redo a full peaking pass (Az/El/Pol) using the satellite beacon",
                        "Check the antenna base and drive mounts are properly tightened"]},
    "pq4": {"q": "Does the spectrum analyzer show any unusual carrier/pattern near your frequency?",
            "o": [("Yes", "pq_r4"), ("No", "pq_r5")]},
    "pq_r4": {"r": 1, "sev": "critical", "title": "RF interference",
              "steps": ["Capture a clear spectrum screenshot and log the affected frequency/bandwidth",
                        "Report to the satellite operator immediately to identify the source",
                        "Briefly stop your own transmission to confirm you are not the source"]},
    "pq_r5": {"r": 1, "sev": "warning", "title": "Likely receive-chain degradation",
              "steps": ["Swap in a spare LNB for comparison -- possible high noise figure",
                        "Inspect cables and connectors for corrosion or moisture",
                        "Confirm the feed is sealed and no water has entered it"]},

    # ---------------- CROSS POL ----------------
    "cp1": {"q": "Was Cross-pol Optimization performed when the antenna was first installed?",
            "o": [("Yes", "cp2"), ("No", "cp_r1")]},
    "cp_r1": {"r": 1, "sev": "warning", "title": "Polarization was never optimized",
              "steps": ["Perform Cross-pol Optimization using the satellite beacon",
                        "Or coordinate directly with teleport engineers to fine-tune the angle"]},
    "cp2": {"q": "Was the antenna exposed to strong wind, or moved/serviced recently?",
            "o": [("Yes", "cp_r2"), ("No", "cp3")]},
    "cp_r2": {"r": 1, "sev": "warning", "title": "Likely mechanical shift in polarization angle",
              "steps": ["Inspect the antenna and feed mechanical mounting",
                        "Redo Cross-pol Optimization from scratch"]},
    "cp3": {"q": "Does the feed / OMT look physically sound (no moisture or corrosion)?",
            "o": [("Yes", "cp_r4"), ("No", "cp_r3")]},
    "cp_r3": {"r": 1, "sev": "critical", "title": "Possible OMT/feed damage",
              "steps": ["Inspect the OMT closely for internal moisture or corroded connectors",
                        "Replace if needed -- it directly affects polarization isolation"]},
    "cp_r4": {"r": 1, "sev": "info", "title": "Equipment looks healthy -- external coordination needed",
              "steps": ["Coordinate with the satellite operator or teleport to verify from their side",
                        "The issue may be with the transponder itself or an adjacent-satellite conflict"]},

    # ---------------- BUC / HPA ----------------
    "bh1": {"q": "What type of alarm is showing on the BUC / HPA unit?",
            "o": [("Over Temperature", "bh_r1"), ("Over Current", "bh_r2"), ("General/unspecified Mute", "bh_r3")]},
    "bh_r1": {"r": 1, "sev": "warning", "title": "Unit overheating",
              "steps": ["Confirm cooling fans are running and vents are not obstructed",
                        "In extreme heat, temporarily reduce output power if the system allows"]},
    "bh_r2": {"r": 1, "sev": "critical", "title": "Overcurrent -- likely internal fault",
              "steps": ["Power the unit off immediately to prevent further damage",
                        "Do not re-power before a full technical inspection",
                        "Switch to the redundant unit if available"]},
    "bh_r3": {"r": 1, "sev": "warning", "title": "Unspecified general alarm",
              "steps": ["Perform a full power cycle of the unit",
                        "If the alarm recurs, set it aside for specialized maintenance and use the spare"]},

    # ---------------- ANTENNA POINTING ----------------
    "ap1": {"q": "Which best describes the situation?",
            "o": [("New antenna installation", "ap2"), ("Antenna was working, then stopped", "ap4")]},
    "ap2": {"q": "Have accurate GPS site coordinates been entered into the antenna controller (ACU)?",
            "o": [("Yes", "ap_r_ready"), ("No", "ap_r1")]},
    "ap_r1": {"r": 1, "sev": "warning", "title": "Site coordinates are inaccurate",
              "steps": ["Enter accurate GPS coordinates for the site first",
                        "Recompute Azimuth / Elevation / Polarization before starting pointing"]},
    "ap_r_ready": {"r": 1, "sev": "info", "title": "Ready to begin manual pointing",
                   "steps": ["Begin manual peaking using the satellite beacon signal",
                             "Slowly sweep Azimuth and Elevation to find the peak reading",
                             "Fine-tune polarization after finding the peak signal"]},
    "ap4": {"q": "Was there an exceptionally strong wind event, or any shock/vibration at the site recently?",
            "o": [("Yes", "ap_r2"), ("No", "ap5")]},
    "ap_r2": {"r": 1, "sev": "warning", "title": "Likely mechanical shift in pointing",
              "steps": ["Inspect the base and mechanical mounts for looseness",
                        "Re-peak the antenna on the satellite beacon"]},
    "ap5": {"q": "Does the drive actuator respond normally to commands from the antenna controller (ACU)?",
            "o": [("Yes", "ap_r4"), ("No", "ap_r3")]},
    "ap_r3": {"r": 1, "sev": "critical", "title": "Likely actuator or controller fault",
              "steps": ["Check actuator wiring and power supply",
                        "Check the ACU's error log",
                        "The actuator or controller may need replacement or service"]},
    "ap_r4": {"r": 1, "sev": "info", "title": "Likely lost calibration",
              "steps": ["Run a full system re-calibration from the ACU settings menu",
                        "Then perform a precise manual peak on the satellite beacon"]},

    # ---------------- ENCODING / VIDEO ----------------
    "ev1": {"q": "Is the video feeding the encoder (from the camera) clean on the local monitor?",
            "o": [("Yes", "ev2"), ("No", "ev_r1")]},
    "ev_r1": {"r": 1, "sev": "warning", "title": "The issue is upstream of the encoder",
              "steps": ["Check the SDI/HDMI cable and the camera output",
                        "Try a different video source to isolate the fault"]},
    "ev2": {"q": "Do the encoder's settings (bitrate, resolution, GOP) match what the "
                 "receiving decoder at master control expects?",
            "o": [("Yes", "ev3"), ("No", "ev_r2")]},
    "ev_r2": {"r": 1, "sev": "warning", "title": "Encoding settings mismatch",
              "steps": ["Coordinate with master control (MCR) to match bitrate/resolution/GOP/profile on both ends"]},
    "ev3": {"q": "Is there breakup or freezing in the picture even though the modulator's "
                 "Eb/No reading is normal?",
            "o": [("Yes", "ev_r3"), ("No", "ev_r4")]},
    "ev_r3": {"r": 1, "sev": "critical", "title": "Likely internal encoder fault or network saturation",
              "steps": ["Power-cycle the encoder",
                        "Check the unit's temperature and ventilation",
                        "Try a backup encoder if the issue persists"]},
    "ev_r4": {"r": 1, "sev": "info", "title": "Transmission looks healthy on your end",
              "steps": ["Coordinate with master control to confirm they are receiving good quality video",
                        "The issue is most likely on the receiving side or their internal distribution network"]},
}


def _build_nodes() -> dict[str, Node]:
    built: dict[str, Node] = {}
    for node_id, raw in _RAW_NODES.items():
        if raw.get("r"):
            built[node_id] = Node(id=node_id, is_result=True, severity=raw["sev"],
                                   title=raw["title"], steps=list(raw["steps"]))
        else:
            built[node_id] = Node(id=node_id, question=raw["q"],
                                   options=[Option(label=l, next=n) for l, n in raw["o"]])
    return built


NODES: dict[str, Node] = _build_nodes()


class UnknownNodeError(KeyError):
    pass


class UnknownCategoryError(KeyError):
    pass


def get_category(category_id: str) -> Category:
    try:
        return CATEGORY_BY_ID[category_id]
    except KeyError as e:
        raise UnknownCategoryError(category_id) from e


def get_node(node_id: str) -> Node:
    try:
        return NODES[node_id]
    except KeyError as e:
        raise UnknownNodeError(node_id) from e


def total_scenarios() -> int:
    """Number of terminal (result) nodes across all trees -- used for reporting/stats."""
    return sum(1 for n in NODES.values() if n.is_result)


def validate_tree_integrity() -> list[str]:
    """
    Sanity-check every category root exists and every option target exists.
    Returns a list of problems found (empty list == healthy).
    Intended to run in CI so a future content edit can never silently break
    the diagnostic graph (e.g. an option pointing at a typo'd node id).
    """
    problems: list[str] = []
    for cat in CATEGORIES:
        if cat.root not in NODES:
            problems.append(f"Category '{cat.id}' root '{cat.root}' does not exist")
    for node in NODES.values():
        if not node.is_result:
            for opt in node.options:
                if opt.next not in NODES:
                    problems.append(f"Node '{node.id}' option '{opt.label}' points to missing node '{opt.next}'")
    return problems
