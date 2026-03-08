"""
app/models/transaction.py
"""
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import ClassVar, Optional

from sqlalchemy import DATE, Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    txn_type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    # commitment | savings | want | income
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="commitment")
    # subcategory: Rent, Food, Grab, Gold, etc.
    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # commitment | savings | want | income — kept for legacy/filter compat
    division: Mapped[str | None] = mapped_column(String(50), nullable=True, default="commitment")
    txn_date: Mapped[date] = mapped_column(DATE, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    store: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_tax_deductible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cloudinary_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, index=True)
    transfer_to_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="transactions")  # noqa: F821
    account: Mapped["Account"] = relationship(back_populates="transactions", foreign_keys=[account_id])  # noqa: F821
    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")  # noqa: F821

    account_balance_after: ClassVar[Optional[Decimal]] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_balance_after: Optional[Decimal] = None

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} type={self.txn_type} amount={self.amount}>"