# AI Broadcast Engineering Assistant

**AI-powered engineering support for Earth Station & DSNG troubleshooting**

A practical, vendor-neutral engineering support tool designed to help broadcast engineers standardize first-response diagnosis, preserve field knowledge, and prepare structured cases for optional external AI assistance.

> **Public MVP / Engineering Prototype**  
> Created by **Laith Mahdawi**

## Live Demo

**https://ai-broadcast-engineering-assistant.onrender.com/**

## Why this project exists

In field engineering, a large part of troubleshooting depends on experience: the order of checks, the questions asked first, the evidence collected, and the decision to escalate.

This project turns part of that experience into a reviewable digital workflow while keeping human engineering judgment at the center.

The goal is not to replace the engineer. The goal is to help engineers **diagnose more consistently, document better, and learn from one another**.

## What the MVP demonstrates

- Six major DSNG / Earth Station fault categories
- Deterministic decision-tree troubleshooting
- Probable diagnosis with recommended actions
- Engineering Knowledge Bank backed by a database
- Controlled knowledge validation workflow
- Vendor-neutral equipment profile foundation
- FastAPI backend
- Arabic and English interface
- Structured AI prompt preparation for difficult or uncovered cases
- Optional hand-off to the user's own ChatGPT or Claude account
- Word and PDF report generation
- Public deployment with automated checks

## Engineering workflow

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
Optional External AI Assistance
```

The deterministic troubleshooting logic remains the primary mechanism. Generative AI is intentionally optional and advisory.

## Knowledge Bank

The Knowledge Bank is designed around a controlled-learning principle:

```text
Field Observation
      ↓
Pending Contribution
      ↓
Technical Review
      ↓
Approved Knowledge
```

The intent is to capture field experience without automatically treating every observation as verified departmental knowledge.

## AI assistance model

The public MVP does **not** require the project owner's ChatGPT, Claude, or AI API credentials.

For cases outside the predefined troubleshooting trees, the backend prepares a structured engineering prompt. The user can then:

1. Copy the prompt.
2. Open ChatGPT using their own account.
3. Open Claude using their own account.
4. Continue the investigation using their own session and judgment.

This keeps external AI usage separated from the project owner's account and avoids embedding a shared AI API key in the public frontend.

## Technology

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL for hosted deployment
- SQLite for local development fallback
- HTML / CSS / JavaScript frontend
- GitHub Actions
- Render

## Architecture

```text
                    AI Broadcast Engineering Assistant
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
          Diagnostic Engine                   AI Gateway
                 │                                 │
           Decision Trees                 Engineering Prompt
                 │                                 │
         Diagnosis + Actions            ┌──────────┴──────────┐
                                        │                     │
                                   ChatGPT                Claude
                                        │                     │
                                  User account          User account

                 ┌───────────────────────────────────────────┐
                 │              Engineering Data              │
                 │ Knowledge Bank · Equipment Profiles       │
                 └───────────────────────────────────────────┘
```

## Safety and engineering principles

### Deterministic first

Operational troubleshooting should remain reviewable and predictable. The predefined diagnostic trees are therefore the primary troubleshooting path.

### Human in the loop

AI-generated content is advisory. Qualified engineering judgment, approved procedures, and safety requirements remain authoritative.

### Controlled learning

Field knowledge should be captured and reviewed before being treated as trusted departmental knowledge.

### Vendor neutral

Equipment information is represented as data where practical rather than being hard-coded into the diagnostic logic.

### Public safe

No private AI API credential is embedded in the public frontend, and local secrets are excluded from source control.

## Public MVP status

This release is intentionally an **MVP / engineering prototype** rather than a safety-critical production system.

### Verified in the current release

- Public web deployment
- Health endpoint
- Knowledge Bank API
- Database-backed knowledge persistence
- Six diagnostic categories
- Complete diagnostic paths
- Arabic / English UI
- AI prompt workflow
- Word / PDF reporting
- Automated repository checks

### Known MVP limitations

- Authentication and role-based access are not implemented yet.
- Expert Directory persistence is currently browser-local rather than a shared team database.
- The AI hand-off is intentionally external rather than a built-in paid AI service.
- Advanced audit logging, richer search / RAG, analytics, and enterprise governance remain future work.

## Local development

From the project root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open:

- `http://127.0.0.1:8000/` — application
- `http://127.0.0.1:8000/docs` — API documentation
- `http://127.0.0.1:8000/health` — health check
- `http://127.0.0.1:8000/api/knowledge` — Knowledge Bank API

## Testing

The repository includes automated tests covering API health, diagnostic categories and nodes, tree integrity, complete diagnostic paths, Knowledge Bank CRUD and review workflow, equipment profiles, and frontend integration.

The current repository reports a successful automated test result of **17 passed**.

## Contributing

This project is intentionally open to engineering learning and contribution.

If you have useful field knowledge, a better diagnostic question, a missing fault scenario, equipment-specific insight, a documentation improvement, or a safer troubleshooting workflow, contributions are welcome.

Please keep contributions:

- technically reasoned,
- reviewable,
- vendor-neutral where possible,
- respectful of operational and RF safety,
- clearly separated from unverified assumptions.

## A note about sharing knowledge

This project is also a small personal attempt at **sharing useful engineering knowledge openly**.

The idea is simple:

> What we learn through years of field work should not disappear when a shift ends or an engineer moves on.

May this project encourage someone to learn, another person to teach, and another engineer to document one useful lesson for the colleague who will face the same fault tomorrow.

**اللهم ارزقنا وارزق منا.**

## Disclaimer

This project is an engineering support and educational tool. It does not replace satellite operator requirements, equipment manufacturer procedures, approved departmental SOPs, or qualified engineering judgment.

Before performing any action that may affect an operational transmission, RF chain, power amplifier, antenna system, or other critical equipment, follow the applicable approved procedures and safety requirements.

## License

MIT License.

## Author

**Laith Mahdawi**  
AI Broadcast Engineering Assistant — Earth Station / DSNG Engineering Support

© 2026 Laith Mahdawi — AI Broadcast Engineering Assistant Public MVP