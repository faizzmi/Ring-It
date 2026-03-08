"""
app/repositories/ledger_repository.py
DB access layer for LedgerEntry model.
Handles double-entry creation and balance recalculation.
"""
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ledger_entry import LedgerEntry


class LedgerRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Write ─────────────────────────────────────────────────────────────────

    async def create_entry(
        self,
        txn_id: UUID,
        account_id: UUID,
        entry_type: str,   # "debit" | "credit"
        amount: Decimal,
        running_balance: Decimal,
        notes: str | None = None,
    ) -> LedgerEntry:
        entry = LedgerEntry(
            txn_id=txn_id,
            account_id=account_id,
            entry_type=entry_type,
            amount=amount,
            running_balance=running_balance,
            notes=notes,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    # ── Balance ───────────────────────────────────────────────────────────────

    async def get_account_balance(self, account_id: UUID) -> Decimal:
        """
        Source of truth balance:
        SUM(debit entries) - SUM(credit entries) for this account.

        For asset accounts (bank/ewallet/cash):
          - DEBIT = money in  → increases balance
          - CREDIT = money out → decreases balance
        """
        debit_result = await self.db.execute(
            select(func.coalesce(func.sum(LedgerEntry.amount), Decimal("0.00")))
            .where(
                LedgerEntry.account_id == account_id,
                LedgerEntry.entry_type == "debit",
            )
        )
        credit_result = await self.db.execute(
            select(func.coalesce(func.sum(LedgerEntry.amount), Decimal("0.00")))
            .where(
                LedgerEntry.account_id == account_id,
                LedgerEntry.entry_type == "credit",
            )
        )
        total_debit = debit_result.scalar_one()
        total_credit = credit_result.scalar_one()
        return (total_debit - total_credit).quantize(Decimal("0.01"))

    async def get_last_running_balance(self, account_id: UUID) -> Decimal:
        """
        Gets the most recent running_balance for an account.
        Used as the base for the next ledger entry's running_balance.
        """
        result = await self.db.execute(
            select(LedgerEntry.running_balance)
            .where(LedgerEntry.account_id == account_id)
            .order_by(LedgerEntry.created_at.desc())
            .limit(1)
        )
        val = result.scalar_one_or_none()
        return val if val is not None else Decimal("0.00")