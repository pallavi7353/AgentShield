<<<<<<< HEAD
# AI Agent Security Platform — CYBR-03

Full-stack project: FastAPI security/database backend + Member 1's
Gemma-powered AI Security Engine + a React frontend console.

```
CYBR03-Full-Project/
├── backend/     FastAPI app (auth, RBAC, audit, alerts, threat history, AI engine)
└── frontend/    React + Vite + Tailwind security console
```

## 1. Run the backend
=======
# AgentShield AI — AI Agent Security Platform (CYBR-03)

A full-stack security platform that sits in front of AI agents and screens
every prompt/response for **prompt injection attacks** and **sensitive data
leaks**, backed by role-based access control, a full audit trail, and a
real-time alerting dashboard.

---

## Project Overview

AgentShield AI is a defensive security layer designed to sit between users
and AI agents. As organizations increasingly deploy AI agents to handle
tasks involving sensitive data, those agents become a new attack surface —
vulnerable to prompt injection, jailbreak attempts, and unintentional data
leakage. This project provides real-time detection, logging, alerting, and
access control for exactly that problem, combining a fast rule-based
detector with a Gemma-powered semantic AI engine.

---

## Problem Statement

**CYBR-03: Securing Autonomous AI Agents Against Sensitive Data Exposure**

Design an AI Agent Security Platform that continuously monitors autonomous
AI agents, detects unauthorized access to sensitive information, enforces
least-privilege access, identifies prompt injection and data leakage
attempts, and alerts security teams before confidential data is exposed.

Develop an AI security platform that enables organizations to monitor
autonomous AI agents, prevent sensitive data exposure, detect prompt
injection attacks, enforce secure access controls, and provide transparent
auditing of AI actions. The solution should help enterprises adopt AI
safely by reducing the risks associated with autonomous agent behavior
while maintaining compliance and trust.

**How AgentShield AI addresses this:**
- Continuously screens every prompt/response in real time before it
  reaches or leaves the agent
- Detects prompt injection and data leakage attempts using a two-layer
  engine (rule-based + Gemma semantic detection)
- Scores risk and blocks dangerous requests automatically
- Enforces least-privilege access through role-based access control
  (RBAC), checked server-side on every request
- Provides transparent, tamper-evident auditing of every AI action and
  admin operation
- Alerts security teams in real time via a dedicated alerts dashboard

---

## Features

- **JWT-based authentication** with account lockout after repeated failed
  login attempts
- **Role-Based Access Control (RBAC)** — Admin, Security Analyst,
  Employee, and AI Agent roles, enforced server-side on every request
- **Two-layer AI Security Engine**:
  - A deterministic rule-based detector (regex) — instant, always
    available, zero cost
  - Gemma (via Google's Gemini API) — semantic detection for reworded or
    novel attacks the rule engine would miss
  - Automatic fallback to rule-based detection if Gemma is unavailable,
    so security enforcement never silently stops
- **Real-time dashboard** — prompts scanned, blocked count, open alerts,
  and average risk score
- **Threat History** — a searchable record of every prompt/response ever
  scored
- **Alerts queue** — auto-generated on high-risk detections, with status
  tracking (open → acknowledged → resolved)
- **Audit Logs** — immutable trail of logins, AI requests, and admin
  actions
- **User & Role management** — Admin-only screen to create accounts,
  assign roles, and activate/deactivate users

---

## System Architecture

```
┌─────────────────┐        HTTPS/JSON        ┌──────────────────────┐
│   React Frontend │ ───────────────────────► │   FastAPI Backend    │
│ (Vite + Tailwind) │ ◄─────────────────────── │                      │
└─────────────────┘        JWT-authenticated   │  ┌────────────────┐  │
                                                │  │ Auth & RBAC    │  │
                                                │  ├────────────────┤  │
                                                │  │ AI Security    │  │
                                                │  │ Engine         │──┼──► Gemma (Gemini API)
                                                │  │  ├─ Rule engine│  │
                                                │  │  └─ Gemma call │  │
                                                │  ├────────────────┤  │
                                                │  │ Threat History │  │
                                                │  │ Alerts         │  │
                                                │  │ Audit Logs     │  │
                                                │  └────────────────┘  │
                                                │          │           │
                                                │          ▼           │
                                                │   SQLAlchemy ORM     │
                                                │          │           │
                                                │          ▼           │
                                                │  SQLite / PostgreSQL │
                                                └──────────────────────┘
```

**Request flow for an AI Analyze call:**
1. Frontend sends the text to be checked to one of the `/analyze`,
   `/detect-prompt`, or `/detect-sensitive-data` endpoints
2. Backend runs the rule-based detector immediately
3. Backend calls Gemma via `google-genai` for semantic analysis
4. Results are combined into a single risk score + decision (allow/block)
5. The event is written to Threat History; if high-risk, an Alert is
   auto-created
6. Response (including which engine produced it — `gemma` or
   `fallback_rule_engine`) is returned to the frontend

---

## Tech Stack

**Frontend**
- React 19 + Vite — UI and build tooling
- Tailwind CSS — styling
- React Router — page navigation
- Axios — API calls to the backend
- Recharts — dashboard charts
- Lucide-react — icons

**Backend**
- Python + FastAPI — the API server
- Uvicorn — ASGI server that runs FastAPI
- Pydantic — request/response validation
- SQLAlchemy (ORM) — database access
- python-jose — JWT creation/verification
- passlib + bcrypt — password hashing
- python-dotenv — environment config
- **google-genai** — official Google SDK, used to call the Gemma model

**Database**
- SQLite by default (zero-setup, ideal for a demo) — a one-line change in
  `DATABASE_URL` switches to PostgreSQL for production use

**AI Engine**
- **Gemma 4** (via the Gemini API) — semantic detection layer
- A deterministic rule-based engine (regex) — fast, always-available
  first layer, and the automatic fallback if Gemma is unreachable

---

## Installation Steps

### Backend
>>>>>>> e2644c3459e7e24a1640c8e544daccb453567516

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

<<<<<<< HEAD
cp .env.example .env 2>/dev/null || true   # if you don't already have one
=======
cp .env.example .env            # if you don't already have one
>>>>>>> e2644c3459e7e24a1640c8e544daccb453567516
# edit .env: set SECRET_KEY, and optionally GEMMA_API_KEY (see below)

python seed.py                  # creates tables + demo users/roles
uvicorn app.main:app --reload   # http://localhost:8000
```

<<<<<<< HEAD
API docs: http://localhost:8000/docs

### Demo logins (created by `seed.py`)
=======
API docs (Swagger UI): http://localhost:8000/docs

#### Demo logins (created by `seed.py`)
>>>>>>> e2644c3459e7e24a1640c8e544daccb453567516

| Username        | Password        | Role             |
|-----------------|-----------------|------------------|
| admin           | Admin@12345     | Admin            |
| analyst         | Analyst@12345   | Security Analyst |
| employee        | Employee@12345  | Employee         |
| agent_service   | Agent@12345     | AI Agent         |

<<<<<<< HEAD
### Enabling Gemma (Member 1's AI engine)

The AI Security Engine (`/analyze`, `/risk-score`, `/detect-prompt`,
`/detect-sensitive-data`) works out of the box with **no API key** —
it automatically falls back to a rule-based detector so the demo
never breaks. To get real Gemma-powered semantic detection:

1. Get a free key at https://aistudio.google.com/apikey
2. In `backend/.env`, set:
   ```
   GEMMA_API_KEY=your_key_here
   GEMMA_MODEL=gemma-3-27b-it
   ```
3. Restart the backend.

Every AI-engine response includes a `source` field
(`"gemma"` or `"fallback_rule_engine"`) so you always know which
engine produced the result — handy for the demo/judges.

## 2. Run the frontend
=======
#### Enabling Gemma

The AI Security Engine works out of the box with **no API key** — it
automatically falls back to the rule-based detector. To enable real
Gemma-powered detection:

1. Get a free key at https://aistudio.google.com/apikey
2. Confirm which Gemma models your key has access to:
   ```bash
   curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"
   ```
   Look for entries with `gemma` in the name that support `generateContent`.
3. In `backend/.env`:
   ```
   GEMMA_API_KEY=your_key_here
   GEMMA_MODEL=gemma-4-26b-a4b-it
   ```
4. Restart the backend.

Every AI-engine response includes a `source` field (`"gemma"` or
`"fallback_rule_engine"`) so you always know which engine produced it.

> **Note:** Gemma 4 has "thinking" mode on by default, which can consume
> most of its token budget on invisible reasoning before writing an
> answer. `gemma_service.py` sets `thinking_level="MINIMAL"` to avoid
> this.

### Frontend
>>>>>>> e2644c3459e7e24a1640c8e544daccb453567516

```bash
cd frontend
npm install
npm run dev              # http://localhost:5173
```

`frontend/.env` points the UI at `http://localhost:8000` by default
(`VITE_API_BASE_URL`) — change it if your backend runs elsewhere.

<<<<<<< HEAD
## What's inside

- **Login** — JWT auth against `/auth/login`, demo-account quick-fill buttons.
- **Dashboard** — live stats pulled from `/alerts` and `/threat-history`.
- **AI Analyze** — interactive console for all 4 of Member 1's AI-engine
  endpoints, with a live risk gauge and Allow/Block decision badge.
- **Threat History** — every prompt/response the engine has scored.
- **Alerts** — security-team alert queue with status updates
  (open → acknowledged → resolved).
- **Audit Logs** — immutable event trail (logins, AI requests, admin actions).
- **Users & Roles** — Admin-only user management and RBAC assignment.

Navigation and page access adapt to the signed-in user's role, mirroring
the backend's RBAC permission map (`READ_LOGS`, `VIEW_DASHBOARD`,
`MANAGE_USERS`, `EXECUTE_AI_AGENT`, `EXPORT_REPORTS`) — the backend is
still the real enforcement point, so a 403 from the API always wins.
=======
---

## API Documentation

Full interactive docs are auto-generated by FastAPI at `/docs` once the
backend is running. Summary of the main endpoints:

### Authentication — `/auth`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Log in, returns access + refresh tokens |
| POST | `/auth/refresh` | Exchange a refresh token for a new access token |
| POST | `/auth/logout` | Invalidate the current session |

### AI Security Engine
| Method | Endpoint | Description |
|---|---|---|
| POST | `/analyze` | Full analysis — rule engine + Gemma combined |
| POST | `/risk-score` | Returns just a risk score for given text |
| POST | `/detect-prompt` | Checks specifically for prompt injection |
| POST | `/detect-sensitive-data` | Checks specifically for sensitive data leaks |

### Threat History — `/threat-history`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/threat-history` | List all scored prompts/responses (requires `READ_LOGS`) |
| POST | `/threat-history/analyze` | Analyze and log a prompt |
| POST | `/threat-history/analyze-response` | Analyze and log an agent's response |

### Alerts — `/alerts`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/alerts` | List all alerts |
| PUT | `/alerts/{alert_id}` | Update an alert's status |

### Audit Logs — `/auditlogs`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/auditlogs` | List audit log entries (requires `READ_LOGS`) |

### Users & Roles — `/users`, `/roles`, `/permissions`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | List all users (requires `MANAGE_USERS`) |
| POST | `/users` | Create a new user |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |
| GET | `/roles` | List all roles |
| POST | `/roles` | Create a new role |
| GET | `/permissions` | List all permissions |

All protected endpoints require a valid JWT (`Authorization: Bearer
<token>`) and enforce their required permission server-side, regardless
of what the frontend UI shows or hides.

---

## Folder Structure

```
CYBR03-Full-Project/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT creation, password hashing, current-user dependency
│   │   ├── config/        # Settings (reads .env)
│   │   ├── database/      # SQLAlchemy engine/session setup
│   │   ├── middleware/    # Security headers, error handling
│   │   ├── models/        # SQLAlchemy ORM models (User, Role, Alert, etc.)
│   │   ├── routers/       # API endpoints (auth, users, roles, alerts,
│   │   │                    audit, threats, ai_engine)
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── services/      # Business logic (gemma_service.py, rule engine)
│   │   ├── utils/         # Shared helper functions
│   │   └── main.py        # FastAPI app entrypoint, router registration
│   ├── seed.py             # Creates demo users/roles on first run
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── assets/         # Static assets (images, icons)
    │   ├── components/     # Reusable UI components
    │   ├── context/        # React context (auth state, etc.)
    │   ├── lib/             # API client (Axios instance), helpers
    │   └── pages/           # Route-level pages (Dashboard, Analyze, etc.)
    ├── package.json
    └── .env
```

---

## Demo Screenshots

_Add screenshots here before submission — recommended set:_
- Login page
- Dashboard (Security Overview)
- AI Analyze page showing a blocked prompt injection with `source: gemma`
- Threat History table
- Alerts queue
- Users & Roles page

```markdown
![Dashboard](./docs/screenshots/dashboard.png)
![AI Analyze](./docs/screenshots/analyze.png)
```

---

## Future Improvements

- Support for streaming/real-time agent traffic, not just single
  request/response checks
- Configurable detection rules editable from the UI (currently
  hardcoded in the rule engine)
- Export reports (PDF/CSV) for compliance and audit purposes
- Multi-tenant support for securing multiple AI agents/organizations from
  one deployment
- Webhook/Slack integration for real-time alert notifications
- Expand sensitive-data detection beyond regex patterns (e.g. named
  entity recognition for more data types)

---

## Team Members

| Name | Role |
|---|---|
| Pandu C V | Team Leader |
| Pallavi | Team Member |
| Talavar Bhavana | Team Member |


---

## Security Design Notes

- **Two-layer detection**: rule engine + Gemma, with graceful fallback if
  Gemma is unavailable.
- **RBAC enforced server-side** — every protected endpoint checks
  permissions independently of the UI.
- **Passwords hashed** with bcrypt; never stored or logged in plain text.
- **`.env` files gitignored** — secrets never committed to version
  control.
>>>>>>> e2644c3459e7e24a1640c8e544daccb453567516
