"""
app/services/account_service.py
Business logic layer for account management.

Routes are thin — all domain rules live here (Service Pattern, SDD §2.2.2).
The service is injected into route handlers via FastAPI Depends().
"""
import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repo import AccountRepository
from app.schemas.accounts import (
    AccountListResponse,
    AccountResponse,
    CreateAccountRequest,
    DeleteAccountResponse,
    UpdateAccountRequest,
)


class AccountService:
    """
    Orchestrates account CRUD and balance integrity.

    Dependencies
    ------------
    repo : AccountRepository
        Injected at construction — makes the service unit-testable
        by swapping in a mock repository.
    """

    def __init__(self, repo: AccountRepository) -> None:
        self.repo = repo

    # ── Create ───────────────────────────────────────────────────────────────

    async def create_account(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        data: CreateAccountRequest,
    ) -> AccountResponse:
        """
        Create a new account for the authenticated user.

        Business rules
        --------------
        • A user may not have more than 20 active accounts (soft cap).
        • Opening balance ≥ 0 is enforced by the Pydantic schema.
        • Balance is seeded directly; a companion ledger_entry (CREDIT to
          an equity/opening-balance account) should be created by the caller
          if the full DEB audit trail is required.  For MVP this is deferred.
        """
        active_count = await self.repo.count_active(db, user_id)
        if active_count >= 20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Account limit reached. A user may have at most 20 active accounts.",
            )

        account = await self.repo.create(
            db,
            user_id=user_id,
            name=data.name,
            account_type=data.account_type,
            currency=data.currency,
            institution=data.institution,
            notes=data.notes,
            opening_balance=data.opening_balance,
        )
        await db.commit()
        return AccountResponse.from_orm_with_meta(account)

    # ── Read ─────────────────────────────────────────────────────────────────

    async def list_accounts(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        include_inactive: bool = False,
    ) -> AccountListResponse:
        """Return all accounts for the authenticated user with aggregate totals."""
        accounts = await self.repo.get_all_by_user(
            db, user_id, include_inactive=include_inactive
        )
        active_count = sum(1 for a in accounts if a.is_active)
        total_balance = sum(
            (a.balance for a in accounts if a.is_active),
            Decimal("0.00"),
        )
        return AccountListResponse(
            items=[AccountResponse.from_orm_with_meta(a) for a in accounts],
            total=len(accounts),
            active_count=active_count,
            total_balance=total_balance,
        )

    async def get_account(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> AccountResponse:
        """
        Fetch a single account by ID.
        Raises 404 if not found or belongs to a different user.
        """
        account = await self.repo.get_by_id(db, account_id, user_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found.",
            )
        return AccountResponse.from_orm_with_meta(account)

    # ── Update ───────────────────────────────────────────────────────────────

    async def update_account(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
        data: UpdateAccountRequest,
    ) -> AccountResponse:
        """
        Partial update — only fields present in the request payload are applied.

        Business rules
        --------------
        • Inactive accounts can be re-activated via is_active=True.
        • Currency changes are allowed only on accounts with zero balance
          to avoid silent multi-currency balance corruption.
        """
        account = await self.repo.get_by_id(db, account_id, user_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found.",
            )

        # Guard: block currency change if there's an existing balance
        if data.currency and data.currency != account.currency:
            if account.balance != Decimal("0.00"):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        "Cannot change currency on an account with a non-zero balance. "
                        "Zero the balance first or create a new account."
                    ),
                )

        updated = await self.repo.update(
            db,
            account,
            name=data.name,
            account_type=data.account_type,
            currency=data.currency,
            institution=data.institution,
            notes=data.notes,
            is_active=data.is_active,
        )
        await db.commit()
        return AccountResponse.from_orm_with_meta(updated)

    # ── Delete ───────────────────────────────────────────────────────────────

    async def delete_account(
        self,
        db: AsyncSession,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> DeleteAccountResponse:
        """
        Delete strategy:
        • Account has transactions  →  soft-delete (is_active = False).
          The audit trail must be preserved per BNM RMIT requirements.
        • Account has no transactions  →  hard-delete (row removed from DB).

        Raises 404 if not found or belongs to a different user.
        """
        account = await self.repo.get_by_id(db, account_id, user_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found.",
            )

        has_txns = await self.repo.has_transactions(db, account_id)

        if has_txns:
            # Soft-delete — preserve ledger history
            await self.repo.soft_delete(db, account)
            await db.commit()
            return DeleteAccountResponse(
                deleted=True,
                account_id=account_id,
                message=(
                    "Account deactivated. Transaction history is retained "
                    "for audit purposes."
                ),
            )
        else:
            # Hard-delete — no ledger entries exist; safe to purge
            await db.delete(account)
            await db.commit()
            return DeleteAccountResponse(
                deleted=True,
                account_id=account_id,
                message="Account permanently deleted.",
            )