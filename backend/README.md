# Backend — AI Broadcast Engineering Assistant

The backend provides the server-side foundation for the AI Broadcast Engineering Assistant.

It is built with FastAPI and currently provides:

* Server-side DSNG diagnostic decision trees.
* Diagnostic tree integrity validation.
* Persistent Engineering Knowledge Bank using SQLite.
* Controlled knowledge review workflow.
* Vendor-neutral Equipment Profiles.
* AI Gateway for preparing structured engineering prompts.
* API contracts documented through Swagger/OpenAPI.
* Automated integration and unit tests.

> **Created by Laith Mahdawi**

## Architecture

```text
Frontend
   │
   ├── Diagnostic workflow
   ├── Knowledge Bank UI
   ├── Equipment UI
   └── AI Assistant UI
   │
   ▼
FastAPI Backend
   │
   ├── Diagnostic API
   ├── Knowledge API
   ├── Equipment API
   └── AI Gateway
           │
           └── Prepared Engineering Prompt
                    │
                    ├── Copy
                    ├── ChatGPT
                    └── Claude
```

The backend does not require a project-owned AI API key for the current public MVP.

## Run locally

From the project root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open:

* `http://127.0.0.1:8000/` — main DSNG Troubleshooting Assistant
* `http://127.0.0.1:8000/docs` — Swagger / OpenAPI documentation
* `http://127.0.0.1:8000/health` — health check

SQLite persistence is created under:

```text
backend/data/app.db
```

## API modules

### Diagnostic

```text
GET /api/diagnostic/categories
GET /api/diagnostic/stats
```

The diagnostic engine is backed by:

```text
backend/rules/dsng_tree.py
```

The rules are deterministic and reviewable.

### Knowledge Bank

The Knowledge API provides persistent storage for field-discovered engineering knowledge and supports a controlled review workflow.

New contributions begin as pending knowledge and can be reviewed before being treated as approved knowledge.

### Equipment Profiles

Equipment is represented as structured data rather than hard-coded diagnostic logic.

This supports a vendor-neutral troubleshooting architecture.

### AI Gateway

```text
POST /api/assistant/diagnose
```

The current endpoint prepares a structured engineering prompt from the field case.

It does not call Anthropic or OpenAI directly.

The response contains:

```json
{
  "prompt": "...",
  "chatgpt_url": "...",
  "claude_url": "..."
}
```

The frontend uses the generated prompt to let the user:

* Copy the prompt.
* Open ChatGPT.
* Open Claude.

The external AI service is therefore used through the user's own account.

## Configuration

An example configuration is provided in:

```text
.env.example
```

A private local environment file may be stored as:

```text
.env
```

The private environment file is excluded from Git.

No secret or API key should be committed to the repository.

The current public MVP does not require an AI API key to run its deterministic troubleshooting features.

## Tests

Run:

```powershell
python -m pytest -v
```

The current verified test suite contains:

```text
17 passed
```

The tests cover:

* Health endpoint.
* Diagnostic categories.
* Diagnostic node retrieval.
* Invalid diagnostic nodes.
* Tree integrity.
* Category and scenario consistency.
* Complete diagnostic paths.
* Knowledge Bank CRUD.
* Knowledge validation workflow.
* Knowledge validation rules.
* Equipment Profile CRUD.
* Frontend integration.
* Backend API contracts.

## Project structure

```text
backend/
├── api/
│   ├── assistant.py
│   ├── diagnostic.py
│   ├── equipment.py
│   └── knowledge.py
│
├── models/
│   ├── database.py
│   ├── equipment.py
│   └── knowledge.py
│
├── schemas/
│   ├── assistant.py
│   ├── diagnostic.py
│   └── knowledge.py
│
├── rules/
│   └── dsng_tree.py
│
├── tests/
│   ├── test_api.py
│   ├── test_integration.py
│   └── test_rules.py
│
├── data/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Security and deployment

This backend is currently designed as a local/internal MVP.

Before exposing it as a production Internet service, additional controls should be implemented, including:

* Authentication.
* Authorization.
* Rate limiting.
* Audit logging.
* HTTPS.
* Production CORS policy.
* Secure secret management.
* Database backup and recovery.
* Additional API validation and monitoring.

The current configuration should not be treated as production Internet security.

## Engineering philosophy

The backend follows a deterministic-first approach.

The diagnostic tree provides predictable and reviewable engineering logic.

The Knowledge Bank provides controlled institutional learning.

Equipment Profiles provide vendor-neutral context.

The AI Gateway provides optional external reasoning assistance without making the project dependent on one AI provider or one project-owner account.

The system is therefore designed to support engineers, not replace engineering judgment.

## Status

Current backend capabilities:

```text
FastAPI Backend            ✅
Diagnostic Engine          ✅
Knowledge Bank             ✅
Knowledge Review           ✅
Equipment Profiles         ✅
AI Gateway                 ✅
ChatGPT / Claude Fallback  ✅
Automated Tests            ✅ 17/17
Public-safe Configuration  ✅
```
