"""
app/schemas/auth.py
Pydantic v2 request/response schemas for the auth endpoints.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Request schemas ───────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=128)
    password: str = Field(..., min_length=8, max_length=128)
    currency: str = Field(default="MYR", min_length=3, max_length=3)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        errors = []
        if not any(c.isupper() for c in v):
            errors.append("at least one uppercase letter")
        if not any(c.islower() for c in v):
            errors.append("at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            errors.append("at least one digit")
        if errors:
            raise ValueError("Password must contain " + ", ".join(errors))
        return v
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str


# ── Response schemas ──────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token TTL in seconds")


class MeResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    currency: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    """General-purpose user representation returned from user-facing endpoints."""
    id: UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime| None = None
    currency: str

    model_config = {"from_attributes": True}

class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    