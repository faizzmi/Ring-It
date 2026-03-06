"""
app/models/account.py
Accounts table — bank, ewallet, cash.
Each user can have multiple accounts.
Balance is derived from ledger_entries (Double-Entry), not stored directly.
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # bank | ewallet | cash
    account_type: Mapped[str] = mapped_column(String(20), nullable=False, default="bank")

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MYR")

    # Display balance — updated by LedgerService after each transaction
    # Source of truth is always SUM of ledger_entries
    balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal("0.00")
    )

    institution: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="accounts")  # noqa: F821
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account", foreign_keys="[Transaction.account_id]", cascade="all, delete-orphan")  # noqa: F821
    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(back_populates="account", cascade="all, delete-orphan")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Account id={self.id} name={self.name} type={self.account_type}>"