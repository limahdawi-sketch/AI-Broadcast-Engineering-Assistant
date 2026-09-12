# AI Broadcast Engineering Assistant

A practical engineering support tool for Earth Station / DSNG troubleshooting.

Built to standardize first-response diagnosis, preserve field knowledge, describe equipment in a vendor-neutral way, and prepare structured cases for optional external AI assistance.

> **Created by Laith Mahdawi**

## What this project does

The assistant combines a deterministic diagnostic engine with an engineering Knowledge Bank and equipment profiles.

It is designed around the way a broadcast engineer actually approaches a field fault:

```text
Observed Fault
     ↓
Diagnostic Category
     ↓
Decision Tree
     ↓
Probable Diagnosis
     ↓
Recommended Actions
     ↓
Knowledge / Equipment Context
     ↓
Optional AI Assistance
```

The deterministic diagnostic engine remains the primary troubleshooting mechanism. External AI is an optional fallback for cases that are not adequately covered by the predefined diagnostic trees.

## Current capabilities

* 6 major DSNG / Earth Station fault categories
* 26 documented diagnostic scenarios
* Server-side diagnostic decision trees
* Diagnostic tree integrity validation
* Engineering Knowledge Bank with database persistence
* Controlled knowledge validation workflow
* Vendor-neutral Equipment Profiles
* FastAPI backend
* SQLite persistence
* Interactive Swagger API documentation
* AI Gateway that prepares structured engineering prompts
* Copy Prompt functionality
* Open ChatGPT functionality
* Open Claude functionality
* Arabic and English interface support
* No AI API key embedded in the frontend
* Public-safe configuration using `.env.example`

## Architecture

```text
                    AI Broadcast Engineering Assistant
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
       Diagnostic Engine                         AI Gateway
              │                                       │
      Decision Trees                           Engineering Prompt
              │                                       │
      Diagnosis + Actions                  ┌──────────┴──────────┐
                                           │                     │
                                      ChatGPT                Claude
                                           │                     │
                                     User's account         User's account
```

### Backend

```text
backend/
├── api/
│   ├── diagnostic.py
│   ├── knowledge.py
│   ├── equipment.py
│   └── assistant.py
│
├── models/
├── schemas/
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

### Frontend

The original DSNG Troubleshooting Assistant interface is served by the FastAPI application and remains the main user-facing engineering tool.

## Run on Windows

From the project root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open:

* `http://127.0.0.1:8000/` — DSNG Troubleshooting Assistant
* `http://127.0.0.1:8000/docs` — Swagger API documentation
* `http://127.0.0.1:8000/health` — health check
* `http://127.0.0.1:8000/api/diagnostic/categories` — diagnostic categories
* `http://127.0.0.1:8000/api/diagnostic/stats` — diagnostic statistics

## AI assistance

The application does **not** require the project owner's ChatGPT, Claude, or API account.

When a case is not adequately covered by the deterministic troubleshooting trees, the AI Gateway prepares a structured engineering prompt.

The user can then:

1. Copy the prepared prompt.
2. Open ChatGPT using their own account.
3. Open Claude using their own account.
4. Paste the prepared engineering prompt into the selected assistant.

This design avoids embedding a shared API key in the public application and avoids charging external AI usage to the project owner.

## Environment configuration

The public repository includes:

```text
backend/.env.example
```

Example:

```env
AI_PROVIDER=external
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-6
```

The local file:

```text
backend/.env
```

is intentionally excluded from Git through `.gitignore`.

No secret, password, API key, or personal credential should be committed to the repository.

## Knowledge Bank

The Knowledge Bank allows engineers to document field-discovered faults and fixes.

Each contribution is initially created as:

```text
pending
```

A review endpoint can then transition the contribution to:

```text
approved
```

This controlled-learning approach is intended to prevent unreviewed field observations from automatically becoming trusted departmental knowledge.

## Equipment Profiles

Equipment is represented as data rather than hard-coded diagnostic logic.

This allows the system to remain vendor-neutral and provides a foundation for future equipment-aware troubleshooting.

Example profile fields include:

```text
Category
Manufacturer
Model
Function
Notes
```

## Testing

The project includes automated tests covering:

* API health
* Diagnostic categories
* Diagnostic node retrieval
* Invalid node handling
* Tree integrity
* Scenario counts
* Complete diagnostic paths
* Knowledge Bank CRUD
* Knowledge review workflow
* Knowledge validation
* Equipment Profile CRUD
* Frontend integration

Run:

```powershell
python -m pytest -v
```

The current verified result is:

```text
17 passed
```

## Design principles

### Deterministic first

Safety-critical or operational troubleshooting should not depend solely on a generative model.

The decision trees provide predictable, reviewable diagnostic logic.

### Controlled learning

Field knowledge should be captured and reviewed before becoming trusted departmental knowledge.

### Vendor neutral

Equipment information is stored as data instead of becoming embedded inside diagnostic rules.

### Public safe

The project should be publishable without exposing the owner's private API credentials or account.

### Human in the loop

AI-generated content is advisory. Engineering judgment, official procedures, and applicable safety requirements remain authoritative.

## Project status

This project is an evolving engineering MVP.

The current release demonstrates:

```text
Diagnostic Engine        ✅
Knowledge Bank           ✅
Knowledge Review         ✅
Equipment Profiles       ✅
AI Gateway               ✅
ChatGPT / Claude Fallback ✅
Arabic / English         ✅
Automated Tests          ✅ 17/17
Public-safe configuration ✅
```

Future work may include authentication, richer knowledge search, RAG, audit logging, expert escalation, analytics, and deeper equipment-aware diagnostics.

## Contributing

Engineering feedback, additional diagnostic scenarios, equipment knowledge, usability improvements, and documentation contributions are welcome.

Contributions should preserve the project's safety-oriented and reviewable engineering approach.

## Disclaimer

This project is an engineering support and educational tool.

It does not replace official satellite operator requirements, equipment manufacturer procedures, departmental SOPs, or qualified engineering judgment.

Before performing any action that may affect an operational transmission, RF chain, power amplifier, antenna system, or other critical equipment, follow the applicable approved procedures.

---

**AI Broadcast Engineering Assistant**
Earth Station / DSNG Engineering Support
Created by Laith Mahdawi
