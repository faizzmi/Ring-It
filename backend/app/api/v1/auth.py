"""
app/api/v1/auth.py
Auth endpoints — register, login, refresh, me, logout, verify-email, resend-verification,
                 forgot-password, reset-password.
"""
from fastapi import APIRouter, Depends, Request, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.rate_limit import limiter
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MeResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth_services import AuthService

router = APIRouter(tags=["Authentication"])


# ── POST /api/v1/auth/register ────────────────────────────────────────────────
@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new vault account",
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    response: Response,
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)
    return await service.register(data)


# ── POST /api/v1/auth/verify-email ───────────────────────────────────────────
@router.post(
    "/verify-email",
    summary="Verify email address with token",
)
@limiter.limit("10/minute")
async def verify_email(
    request: Request,
    response: Response,
    token: str = Query(..., description="One-time verification token from email"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    service = AuthService(db)
    return await service.verify_email(token)


# ── POST /api/v1/auth/resend-verification ────────────────────────────────────
@router.post(
    "/resend-verification",
    summary="Resend verification email",
)
@limiter.limit("3/minute")
async def resend_verification(
    request: Request,
    response: Response,
    email: str = Query(..., description="Email address to resend verification to"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    service = AuthService(db)
    return await service.resend_verification(email)


# ── POST /api/v1/auth/login ───────────────────────────────────────────────────
@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login to your vault",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    service = AuthService(db)
    return await service.login(data)


# ── POST /api/v1/auth/refresh ─────────────────────────────────────────────────
@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
@limiter.limit("20/minute")
async def refresh_token(
    request: Request,
    response: Response,
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    service = AuthService(db)
    return await service.refresh(data.refresh_token)


# ── GET /api/v1/auth/me ───────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=MeResponse,
    summary="Get current authenticated user",
)
@limiter.limit("60/minute")
async def get_me(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MeResponse:
    service = AuthService(db)
    return await service.get_me(current_user)


# ── POST /api/v1/auth/logout ──────────────────────────────────────────────────
@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout (client-side token discard)",
)
async def logout(
    current_user: User = Depends(get_current_user),
) -> None:
    return None


# ── POST /api/v1/auth/forgot-password ────────────────────────────────────────
@router.post(
    "/forgot-password",
    summary="Request a password reset email",
)
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    response: Response,
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Sends a password reset link to the email if it exists.
    Always returns 200 — never reveals whether email is registered.
    Token is single-use and expires in 1 hour.
    """
    service = AuthService(db)
    return await service.forgot_password(data)


# ── POST /api/v1/auth/reset-password ─────────────────────────────────────────
@router.post(
    "/reset-password",
    summary="Reset password using token from email",
)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    response: Response,
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Validates reset token and sets new password.
    - Token is single-use (invalidated after use).
    - Expires in 1 hour.
    """
    service = AuthService(db)
    return await service.reset_password(data)
