"""
app/repositories/transaction_repository.py
DB access layer for Transaction model.
No business logic here — pure DB operations only.
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.transaction import Transaction


class TransactionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Create ────────────────────────────────────────────────────────────────

    async def create(self, data: dict) -> Transaction:
        """Insert a new transaction row. Does NOT create ledger entries."""
        txn = Transaction(**data)
        self.db.add(txn)
        await self.db.flush()   # get the generated ID without committing
        await self.db.refresh(txn, ["account"])
        return txn

    # ── Read ──────────────────────────────────────────────────────────────────

    async def get_by_id(
        self, txn_id: UUID, user_id: UUID
    ) -> Optional[Transaction]:
        """Fetch a single transaction — scoped to the requesting user."""
        result = await self.db.execute(
            select(Transaction)
            .options(selectinload(Transaction.account))
            .where(Transaction.id == txn_id, Transaction.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_idempotency_key(
        self, key: str, user_id: UUID
    ) -> Optional[Transaction]:
        result = await self.db.execute(
            select(Transaction).where(
                Transaction.idempotency_key == key,
                Transaction.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        account_id: Optional[UUID] = None,
        txn_type: Optional[str] = None,
        category: Optional[str] = None,
        division: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 5,
        offset: int = 0,
    ) -> tuple[list[Transaction], int]:
        """Returns (items, total_count) for pagination."""
        base_query = (
            select(Transaction)
            .options(selectinload(Transaction.account))
            .where(Transaction.user_id == user_id)
        )

        # Apply filters
        if account_id:
            base_query = base_query.where(Transaction.account_id == account_id)
        if txn_type:
            base_query = base_query.where(Transaction.txn_type == txn_type)
        if category:
            base_query = base_query.where(Transaction.category == category)
        if division:
            base_query = base_query.where(Transaction.division == division)
        if date_from:
            base_query = base_query.where(Transaction.txn_date >= date_from)
        if date_to:
            base_query = base_query.where(Transaction.txn_date <= date_to)

        # Total count for pagination
        count_result = await self.db.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()

        # Paginated result
        result = await self.db.execute(
            base_query.order_by(Transaction.txn_date.desc(), Transaction.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = list(result.scalars().all())

        return items, total

    # ── Update ────────────────────────────────────────────────────────────────

    async def update(
        self, txn_id: UUID, user_id: UUID, data: dict
    ) -> Optional[Transaction]:
        """Patch non-ledger fields only."""
        await self.db.execute(
            update(Transaction)
            .where(Transaction.id == txn_id, Transaction.user_id == user_id)
            .values(**data)
        )
        return await self.get_by_id(txn_id, user_id)

    # ── Delete ────────────────────────────────────────────────────────────────

    async def delete(self, txn_id: UUID, user_id: UUID) -> bool:
        """
        Hard delete — ledger entries cascade via DB FK.
        Balance recalc is handled by LedgerService after this call.
        Returns True if a row was deleted.
        """
        txn = await self.get_by_id(txn_id, user_id)
        if not txn:
            return False
        await self.db.delete(txn)
        await self.db.flush()
        return True