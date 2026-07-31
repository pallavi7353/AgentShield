"""
main.py
--------
FastAPI application entrypoint.

- Creates all tables on startup (fine for hackathon/demo use;
  swap for Alembic migrations in a real production deployment).
- Registers CORS so the frontend (Member 1) can call this API
  from a different origin during development.
- Registers the security middleware and every router.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import Base, engine
from app.config.settings import settings
from app.middleware.security_middleware import SecurityHeadersMiddleware

from app.routers import auth, users, roles, permissions, audit, alerts, threats, ai_engine

# Import models so their tables are registered on Base.metadata before create_all
from app import models  # noqa: F401

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Security & Database backend for the AI Agent Security Platform "
        "(IEEE Neo Nexus 36.1 - CYBR-03). Provides JWT auth, RBAC, "
        "audit logging, alerting, and prompt-injection / data-leakage "
        "detection for autonomous AI agents."
    ),
)

# --- CORS: open for hackathon dev; restrict allow_origins in production ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

# --- Routers ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(audit.router)
app.include_router(alerts.router)
app.include_router(threats.router)
app.include_router(ai_engine.router)  # Member 1: /analyze, /risk-score, /detect-prompt, /detect-sensitive-data


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
