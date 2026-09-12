import uuid
from sqlalchemy import Column, String, Text
from .database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class EquipmentProfile(Base):
    """
    Minimal first slice of the vendor-neutral Equipment Profile framework
    described in ARCHITECTURE.md. Deliberately small for Phase 1/2: enough
    to prove the "equipment is data, not code" principle end-to-end, without
    building out the full parameters/measurements/alarms schema yet.

    A category (e.g. "Earth Station Antenna", "BUC/HPA") can have many
    profiles (specific makes/models); the diagnostic engine in rules/ never
    references a specific profile directly, keeping the two systems decoupled
    until Phase 5 hardware integration links them together.
    """
    __tablename__ = "equipment_profiles"

    id = Column(String, primary_key=True, default=_uuid)
    category = Column(String, nullable=False)      # e.g. "antenna", "buc_hpa", "modulator"
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    function = Column(Text, nullable=True)
    notes = Column(Text, nullable=True, default="")
