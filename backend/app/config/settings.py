"""
settings.py
------------
Centralized application configuration.
All sensitive values are read from environment variables (.env file)
so nothing secret is hardcoded into source control.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from a .env file into the environment


class Settings:
    # --- Database ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_agent_security.db")

    # --- JWT Auth ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_IN_PRODUCTION")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # --- Session / Security Policy ---
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", 30))
    MAX_FAILED_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_FAILED_LOGIN_ATTEMPTS", 5))
    FAILED_LOGIN_LOCK_MINUTES: int = int(os.getenv("FAILED_LOGIN_LOCK_MINUTES", 15))

    # --- Threat Detection Thresholds ---
    HIGH_RISK_SCORE_THRESHOLD: int = int(os.getenv("HIGH_RISK_SCORE_THRESHOLD", 70))

    # --- AI Security Engine (Member 1 - Gemma) ---
    # Get a free key at https://aistudio.google.com/apikey
    GEMMA_API_KEY: str = os.getenv("GEMMA_API_KEY", "")
    GEMMA_MODEL: str = os.getenv("GEMMA_MODEL", "gemma-3-27b-it")
    GEMMA_API_URL: str = os.getenv(
        "GEMMA_API_URL",
        "https://generativelanguage.googleapis.com/v1beta/models",
    )
    # If no GEMMA_API_KEY is configured, the AI engine automatically
    # falls back to the rule-based detector so the demo still works.

    # --- App Meta ---
    APP_NAME: str = "AI Agent Security Platform - Backend"
    APP_VERSION: str = "1.0.0"


settings = Settings()
