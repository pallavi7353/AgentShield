# AI Agent Security Platform — CYBR-03

Full-stack project: FastAPI security/database backend + Member 1's
Gemma-powered AI Security Engine + a React frontend console.

```
CYBR03-Full-Project/
├── backend/     FastAPI app (auth, RBAC, audit, alerts, threat history, AI engine)
└── frontend/    React + Vite + Tailwind security console
```

## 1. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env 2>/dev/null || true   # if you don't already have one
# edit .env: set SECRET_KEY, and optionally GEMMA_API_KEY (see below)

python seed.py                  # creates tables + demo users/roles
uvicorn app.main:app --reload   # http://localhost:8000
```

API docs: http://localhost:8000/docs

### Demo logins (created by `seed.py`)

| Username        | Password        | Role             |
|-----------------|-----------------|------------------|
| admin           | Admin@12345     | Admin            |
| analyst         | Analyst@12345   | Security Analyst |
| employee        | Employee@12345  | Employee         |
| agent_service   | Agent@12345     | AI Agent         |

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

```bash
cd frontend
npm install
npm run dev              # http://localhost:5173
```

`frontend/.env` points the UI at `http://localhost:8000` by default
(`VITE_API_BASE_URL`) — change it if your backend runs elsewhere.

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
