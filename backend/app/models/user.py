"""
app/models/user.py
Users table — email + full_name stored AES-256-GCM encrypted (PDPA 2010).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # AES-256-GCM encrypted before DB write
    email_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    full_name_encrypted: Mapped[str] = mapped_column(Text, nullable=False)

    # HMAC-SHA256 keyed hash — used only for O(1) email lookups
    # NOT decryptable; keyed with SECRET_KEY to resist offline attacks
    email_hmac: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)

    # bcrypt hashed
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Preferences
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MYR")

    # State
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    accounts: Mapped[list["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    budgets: Mapped[list["Budget"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    goals: Mapped[list["Goal"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    debts: Mapped[list["Debt"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    tax_records: Mapped[list["TaxRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    
    def __repr__(self) -> str:
        return f"<User id={self.id} currency={self.currency}>"
    