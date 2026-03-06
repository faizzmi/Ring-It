"""
app/services/auth_service.py
Business logic for authentication — with email verification flow.

Registration flow:
  1. Validate email uniqueness
  2. Hash password, create user (is_verified=False)
  3. Generate email verification token (24h)
  4. Send verification email (fire-and-forget — does not block response)
  5. Return tokens immediately so user can browse while unverified
     (enforce is_verified on sensitive endpoints if needed)

Verification flow:
  POST /auth/verify-email?token=<token>
  1. Decode token from DB
  2. Mark user.is_verified = True
  3. Delete / invalidate token
  4. Send welcome email
"""
import secrets
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.encryption import encryptor
from app.core.config import settings
from app.core.email import send_verification_email, send_welcome_email, send_password_reset_email
from app.repositories.user_repository import UserRepository

from app.models.user import User
from app.models.email_verification import EmailVerificationToken
from app.models.password_reset import PasswordResetToken

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    TokenResponse,
    UserResponse,
    MeResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=encryptor.decrypt(user.email_encrypted),
        full_name=encryptor.decrypt(user.full_name_encrypted),
        currency=user.currency,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=getattr(user, "updated_at", None),
    )


def _build_tokens(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def _generate_verification_token() -> str:
    """Cryptographically secure 64-byte URL-safe token."""
    return secrets.token_urlsafe(64)


# ── Service ───────────────────────────────────────────────────────────────────

class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = UserRepository(db)
        self._db = db

    # ── Register ──────────────────────────────────────────────────────────────

    async def register(self, data: RegisterRequest) -> AuthResponse:
        # 1. Check email uniqueness
        if await self._repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        # 2. Hash password & create user
        hashed = hash_password(data.password)
        user = await self._repo.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed,
            currency=data.currency,
        )

        # 3. Create verification token (24h TTL)
        raw_token = _generate_verification_token()
        verification = EmailVerificationToken(
            user_id=user.id,
            token=raw_token,
            expires_at=EmailVerificationToken.make_expires_at(hours=24),
        )
        self._db.add(verification)
        await self._db.flush()

        # 4. Send verification email (fire-and-forget)
        try:
            await send_verification_email(
                to_email=data.email,
                full_name=data.full_name,
                token=raw_token,
            )
        except Exception:
            pass

        # 5. Return tokens immediately
        return AuthResponse(
            user=_build_user_response(user),
            tokens=_build_tokens(user),
        )

    # ── Verify Email ──────────────────────────────────────────────────────────

    async def verify_email(self, token: str) -> dict:
        result = await self._db.execute(
            select(EmailVerificationToken).where(
                EmailVerificationToken.token == token,
                EmailVerificationToken.used == False,  # noqa: E712
            )
        )
        record: EmailVerificationToken | None = result.scalar_one_or_none()

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or already-used verification link.",
            )

        if record.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification link has expired. Please request a new one.",
            )

        user = await self._repo.get_by_id(record.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        user.is_verified = True
        record.used = True
        await self._db.flush()

        try:
            await send_welcome_email(
                to_email=encryptor.decrypt(user.email_encrypted),
                full_name=encryptor.decrypt(user.full_name_encrypted),
            )
        except Exception:
            pass

        return {"verified": True, "message": "Email verified successfully."}

    # ── Resend Verification ───────────────────────────────────────────────────

    async def resend_verification(self, email: str) -> dict:
        user = await self._repo.get_by_email(email)
        if user and not user.is_verified:
            await self._db.execute(
                delete(EmailVerificationToken).where(
                    EmailVerificationToken.user_id == user.id
                )
            )

            raw_token = _generate_verification_token()
            self._db.add(EmailVerificationToken(
                user_id=user.id,
                token=raw_token,
                expires_at=EmailVerificationToken.make_expires_at(hours=24),
            ))
            await self._db.flush()

            try:
                await send_verification_email(
                    to_email=encryptor.decrypt(user.email_encrypted),
                    full_name=encryptor.decrypt(user.full_name_encrypted),
                    token=raw_token,
                )
            except Exception:
                pass

        return {"message": "If that email is registered and unverified, a new link has been sent."}

    # ── Login ─────────────────────────────────────────────────────────────────

    async def login(self, data: LoginRequest) -> AuthResponse:
        user = await self._repo.get_by_email(data.email)

        if user is None or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Contact support.",
            )

        await self._repo.update_last_login(user)

        return AuthResponse(
            user=_build_user_response(user),
            tokens=_build_tokens(user),
        )

    # ── Refresh ───────────────────────────────────────────────────────────────

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)

        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        user_id = payload.get("sub")
        user = await self._repo.get_by_id(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive.",
            )

        return _build_tokens(user)

    # ── Me ────────────────────────────────────────────────────────────────────

    async def get_me(self, user: User) -> MeResponse:
        return MeResponse(
            id=user.id,
            email=encryptor.decrypt(user.email_encrypted),
            full_name=encryptor.decrypt(user.full_name_encrypted),
            currency=user.currency,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )

    # ── Forgot Password ───────────────────────────────────────────────────────

    async def forgot_password(self, data: ForgotPasswordRequest) -> dict:
        user = await self._repo.get_by_email(data.email)

        if user and user.is_active:
            await self._db.execute(
                delete(PasswordResetToken).where(
                    PasswordResetToken.user_id == user.id
                )
            )

            raw_token = _generate_verification_token()
            self._db.add(PasswordResetToken(
                user_id=user.id,
                token=raw_token,
                expires_at=PasswordResetToken.make_expires_at(hours=1),
            ))
            await self._db.flush()

            try:
                await send_password_reset_email(
                    to_email=encryptor.decrypt(user.email_encrypted),
                    full_name=encryptor.decrypt(user.full_name_encrypted),
                    token=raw_token,
                )
            except Exception:
                pass

        return {"message": "If that email is registered, a password reset link has been sent."}

    # ── Reset Password ────────────────────────────────────────────────────────

    async def reset_password(self, data: ResetPasswordRequest) -> dict:
        result = await self._db.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token == data.token,
                PasswordResetToken.used == False,  # noqa: E712
            )
        )
        record: PasswordResetToken | None = result.scalar_one_or_none()

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or already-used reset link.",
            )

        if record.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset link has expired. Please request a new one.",
            )

        user = await self._repo.get_by_id(record.user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset link.",
            )

        user.hashed_password = hash_password(data.new_password)
        record.used = True
        await self._db.flush()

        return {"message": "Password reset successfully. You can now log in."}
    