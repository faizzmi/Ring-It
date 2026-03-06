"""
app/models/ledger_entry.py
ledger_entries table — the heart of the Double-Entry Bookkeeping system.

Every Transaction creates EXACTLY 2 LedgerEntry rows:
  - 1 DEBIT entry
  - 1 CREDIT entry

This ensures: Assets = Liabilities + Equity at all times.
SUM of all ledger_entries for an account = correct balance.
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Parent transaction — every entry belongs to a transaction
    txn_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # Account this entry affects
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # debit | credit
    entry_type: Mapped[str] = mapped_column(String(6), nullable=False)

    # Always positive — direction is determined by entry_type
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Running balance of the account AFTER this entry is applied
    # Indexed for fast balance lookups
    running_balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal("0.00"), index=True
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Immutable — never updated after creation
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    transaction: Mapped["Transaction"] = relationship(back_populates="ledger_entries")  # noqa: F821
    account: Mapped["Account"] = relationship(back_populates="ledger_entries")  # noqa: F821

    def __repr__(self) -> str:
        return f"<LedgerEntry id={self.id} type={self.entry_type} amount={self.amount}>"