"""
app/models/transaction.py
Transactions table — every financial event.
Each transaction creates 2 ledger_entries (Double-Entry Bookkeeping).
"""
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    DATE, Boolean, DateTime, ForeignKey,
    Numeric, String, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # income | expense | transfer
    txn_type: Mapped[str] = mapped_column(String(20), nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # need | want | savings | investment
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="need")

    txn_date: Mapped[date] = mapped_column(DATE, nullable=False, index=True)

    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Behavioral finance — mandatory for "want" purchases > RM 50 (SDD 1.3)
    justification: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Cloudinary receipt URL — encrypted before storage
    cloudinary_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # LHDN tax deductible flag
    is_tax_deductible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Idempotency key — prevents duplicate transactions from network retries
    idempotency_key: Mapped[str | None] = mapped_column(
        String(100), nullable=True, unique=True, index=True
    )

    # Transfer destination account (only set when txn_type = 'transfer')
    transfer_to_account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True
    )

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
    user: Mapped["User"] = relationship(back_populates="transactions")  # noqa: F821
    account: Mapped["Account"] = relationship(back_populates="transactions", foreign_keys=[account_id])  # noqa: F821
    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} type={self.txn_type} amount={self.amount}>"