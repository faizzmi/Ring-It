"""
app/main.py
FastAPI application factory.
Registers middleware, routers, and lifespan events.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.rate_limit import limiter
from app.models import *  # noqa: F401, F403 — ensures models are registered with Base


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    # On startup: nothing needed (Alembic handles migrations)
    yield
    # On shutdown: dispose engine connection pool
    await engine.dispose()


# ── App factory ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="Ring-It Personal Finance Vault — IEEE 1016-2009 SDD v1.0",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,   # hide Swagger in production
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Rate limiting ─────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ── CORS (BNM RMIT — whitelist only, no wildcard) ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Idempotency-Key"],
)


# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all — never expose internal details in production."""
    if settings.DEBUG:
        raise exc
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred. Please try again."},
    )


# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check() -> dict:
    """Simple liveness probe — used by Railway/Vercel deployment."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}