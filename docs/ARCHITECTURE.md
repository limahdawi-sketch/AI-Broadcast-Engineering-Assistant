# Architecture — AI Broadcast Engineering Assistant

## 1. Purpose

The AI Broadcast Engineering Assistant is a practical engineering support platform for Earth Station and DSNG troubleshooting.

The architecture is intentionally designed around five principles:

1. Deterministic diagnosis first.
2. Controlled capture and validation of field knowledge.
3. Vendor-neutral equipment modeling.
4. Optional external AI assistance.
5. Human engineering judgment remains authoritative.

The system is intended to reduce first-response troubleshooting time, standardize engineering practice, preserve field knowledge, and provide a foundation for future AI-assisted engineering workflows.

---

## 2. High-Level Architecture

```text
                         AI Broadcast Engineering Assistant
                                      │
                     ┌────────────────┴────────────────┐
                     │                                 │
              Deterministic Core                 AI Gateway
                     │                                 │
              Diagnostic Trees                 Prompt Preparation
                     │                                 │
             Diagnosis + Actions          ┌────────────┴────────────┐
                                           │                         │
                                      ChatGPT                    Claude
                                           │                         │
                                    User's account            User's account
```

The deterministic diagnostic engine is the primary troubleshooting path.

The AI Gateway is an optional fallback for cases that are not adequately represented in the predefined decision trees.

---

## 3. Frontend

The current user-facing application is the DSNG Troubleshooting Assistant.

The frontend provides:

* Fault category selection.
* Sequential diagnostic questions.
* Probable diagnosis.
* Severity classification.
* Recommended engineering actions.
* Knowledge Bank contribution.
* Equipment context.
* Optional AI assistance.
* Arabic and English interface support.

The existing frontend remains intentionally lightweight and browser-based.

The application communicates with the FastAPI backend for server-side functions.

---

## 4. Backend

The backend is implemented using FastAPI.

```text
backend/
├── api/
│   ├── diagnostic.py
│   ├── knowledge.py
│   ├── equipment.py
│   └── assistant.py
│
├── models/
│   ├── database.py
│   ├── knowledge.py
│   └── equipment.py
│
├── schemas/
│   ├── knowledge.py
│   ├── equipment.py
│   └── assistant.py
│
├── rules/
│   └── dsng_tree.py
│
├── tests/
├── data/
├── main.py
├── requirements.txt
├── .env.example
└── .env
```

The API layer is intentionally thin.

Business and diagnostic logic should not be duplicated inside individual route handlers.

---

## 5. Diagnostic Engine

The diagnostic engine contains the predefined DSNG troubleshooting decision trees.

Current coverage includes six major categories:

* Total signal loss.
* Poor signal quality / dropouts.
* Cross-polarization issues.
* BUC / HPA alarms.
* Antenna pointing issues.
* Encoding / video issues.

The current release contains 26 documented diagnostic scenarios.

Each category has a root node and a sequence of questions leading to a terminal diagnosis.

```text
Category
   ↓
Root Question
   ↓
Engineer Observation
   ↓
Next Question
   ↓
Terminal Diagnosis
   ↓
Severity + Recommended Actions
```

### Integrity

The tree is validated automatically.

The test suite checks that:

* Every referenced node exists.
* Every category root exists.
* Every category begins with a question.
* Unknown nodes fail safely.
* Unknown categories fail safely.
* Complete diagnostic paths can reach a valid terminal result.
* Scenario counts remain synchronized with the frontend.

The diagnostic tree therefore acts as a deterministic and reviewable source of truth.

---

## 6. Knowledge Bank

The Knowledge Bank captures field-discovered faults and fixes.

A knowledge contribution contains information such as:

```text
Title
Category
Probable Causes
Fix Steps
Notes
Author
Validation State
Created At
```

### Controlled Learning

New contributions are created with:

```text
validation_state = pending
```

They do not automatically become trusted departmental knowledge.

A reviewer can explicitly transition a contribution to:

```text
validation_state = approved
```

This provides a controlled-learning model:

```text
Field Observation
       ↓
Knowledge Contribution
       ↓
Pending Review
       ↓
Human Validation
       ↓
Approved Knowledge
```

This separation is intentional.

Generative AI output and field observations should not silently become authoritative engineering procedures.

---

## 7. Equipment Profiles

Equipment is modeled as structured data rather than embedded
