"""
app/core/config.py
Pydantic v2 Settings — loads from .env automatically.
Variable names match the existing .env file exactly.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",          # ← silently ignores any unrecognised .env keys
    )

     # ── Email / SMTP ──────────────────────────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""          # yourapp@gmail.com
    SMTP_PASSWORD: str = ""      # Gmail App Password (not your real password)
    EMAIL_FROM_NAME: str = "Ring-It Vault"
    FRONTEND_URL: str = "http://localhost:5173"  # change for production


    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = "Ring-It Vault API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Accepts either ENVIRONMENT or APP_ENV in .env
    ENVIRONMENT: str = "development"

    @property
    def APP_ENV(self) -> str:
        return self.ENVIRONMENT

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str  # required — must be in .env

    # ── JWT ───────────────────────────────────────────────────────────────────
    # Your .env uses SECRET_KEY_B64 — we map it here
    SECRET_KEY_B64: str = ""        # used as the JWT signing secret
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440   # 24h
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # RS256 keys (optional — present in your .env, ignored for HS256)
    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""

    @property
    def SECRET_KEY(self) -> str:
        """
        Returns the JWT signing secret.
        Uses SECRET_KEY_B64 from .env (your existing key).
        """
        if not self.SECRET_KEY_B64:
            raise ValueError("SECRET_KEY_B64 must be set in .env")
        return self.SECRET_KEY_B64

    # ── Encryption (AES-256-GCM) ──────────────────────────────────────────────
    # Your .env uses SECRET_KEY_B64 for both JWT + encryption, or set separately
    ENCRYPTION_KEY_B64: str = ""    # if blank, falls back to SECRET_KEY_B64

    @property
    def ENCRYPTION_KEY(self) -> str:
        return self.ENCRYPTION_KEY_B64 or self.SECRET_KEY_B64

    # ── CORS ──────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # ── Cloudinary ────────────────────────────────────────────────────────────
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # ── Supabase ──────────────────────────────────────────────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""          # your .env uses SUPABASE_KEY

    @property
    def SUPABASE_SERVICE_KEY(self) -> str:
        return self.SUPABASE_KEY


settings = Settings()