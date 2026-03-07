"""
app/repositories/account_repo.py
Data-access layer for the accounts table.

All SQLAlchemy session interactions live here — the service layer
never touches the session directly (Repository Pattern, SDD §2.2.1).
"""
import uuid
from decimal import Decimal

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account


class AccountRepository:
    """CRUD + query operations for the accounts table."""

    # ── Create ───────────────────────────────────────────────────────────────

    async def create(
        self,
        db: AsyncSession,
        *,
        user_id: uuid.UUID,
        name: str,
        account_type: str,
        currency: str,
        institution: str | None,
        notes: str | None,
        opening_balance: Decimal,
    ) -> Account:
        """
        Insert a new account row.
        The opening_balance is written directly to the balance column here;
        LedgerService is responsible for also creating the corresponding
        opening ledger_entry rows so the DEB invariant is maintained.
        """
        account = Account(
            user_id=user_id,
            name=name,
            account_type=account_type,
            currency=currency,
            institution=institution,
            notes=notes,
            balance=opening_balance,
            is_active=True,
        )
        db.add(account)
        await db.flush()   # Populate account.id without committing
        await db.refresh(account)
        return account

    # ── Read ─────────────────────────────────────────────────────────────────

    async def get_by_id(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Account | None:
        """Fetch a single account — enforces user_id isolation (RLS mirror)."""
        stmt = (
            select(Account)
            .where(Account.id == account_id, Account.user_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        *,
        include_inactive: bool = False,
    ) -> list[Account]:
        """Return all accounts for a user, ordered by creation date."""
        stmt = (
            select(Account)
            .where(Account.user_id == user_id)
            .order_by(Account.created_at.asc())
        )
        if not include_inactive:
            stmt = stmt.where(Account.is_active == True)  # noqa: E712
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def count_active(self, db: AsyncSession, user_id: uuid.UUID) -> int:
        """Count of active accounts for the user."""
        stmt = (
            select(func.count(Account.id))
            .where(Account.user_id == user_id, Account.is_active == True)  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one() or 0

    async def total_balance(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> Decimal:
        """Sum of balances across all active accounts (mixed-currency caveat: summed raw)."""
        stmt = (
            select(func.coalesce(func.sum(Account.balance), Decimal("0.00")))
            .where(Account.user_id == user_id, Account.is_active == True)  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one() or Decimal("0.00")

    # ── Update ───────────────────────────────────────────────────────────────

    async def update(
        self,
        db: AsyncSession,
        account: Account,
        *,
        name: str | None = None,
        account_type: str | None = None,
        currency: str | None = None,
        institution: str | None = None,
        notes: str | None = None,
        is_active: bool | None = None,
    ) -> Account:
        """
        Apply partial update to an already-fetched Account ORM object.
        Only non-None kwargs are applied.
        """
        if name is not None:
            account.name = name
        if account_type is not None:
            account.account_type = account_type
        if currency is not None:
            account.currency = currency
        if institution is not None:
            account.institution = institution
        if notes is not None:
            account.notes = notes
        if is_active is not None:
            account.is_active = is_active

        await db.flush()
        await db.refresh(account)
        return account

    async def update_balance(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
        new_balance: Decimal,
    ) -> None:
        """
        Bulk-update balance column directly — used by LedgerService after
        posting ledger entries.  Bypasses ORM to avoid stale-object issues
        in concurrent async contexts.
        """
        stmt = (
            update(Account)
            .where(Account.id == account_id)
            .values(balance=new_balance)
        )
        await db.execute(stmt)

    # ── Delete (soft) ─────────────────────────────────────────────────────────

    async def soft_delete(
        self,
        db: AsyncSession,
        account: Account,
    ) -> Account:
        """
        Mark account as inactive.  Hard delete is deliberately NOT exposed —
        an account with ledger_entries must never be destroyed (audit trail).
        """
        account.is_active = False
        await db.flush()
        await db.refresh(account)
        return account

    async def has_transactions(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
    ) -> bool:
        """
        Return True if the account has any associated transactions.
        Used by the service layer to decide between soft-delete and
        hard-delete (only empty accounts allow hard-delete).
        """
        from app.models.transaction import Transaction  # local import to avoid circular

        stmt = (
            select(func.count(Transaction.id))
            .where(Transaction.account_id == account_id)
            .limit(1)
        )
        result = await db.execute(stmt)
        return (result.scalar_one() or 0) > 0