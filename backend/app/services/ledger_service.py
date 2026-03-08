"""
app/services/ledger_service.py

Core business logic for the transaction module.
Enforces single-sided ledger entries against real user accounts only.
The equity placeholder is not a real DB row — we track only the user-facing
account side of each transaction.

Balance source of truth: SUM of ledger_entries (recalculated after every write).
"""
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.transaction import Transaction
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import CreateTxnRequest, UpdateTxnRequest


class LedgerService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.txn_repo = TransactionRepository(db)
        self.ledger_repo = LedgerRepository(db)

    # ── Helpers ───────────────────────────────────────────────────────────────

    async def _get_account_or_404(self, account_id: UUID, user_id: UUID) -> Account:
        result = await self.db.get(Account, account_id)
        if not result or result.user_id != user_id or not result.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found or inactive.",
            )
        return result

    async def _recalc_and_sync_balance(self, account_id: UUID) -> Decimal:
        new_balance = await self.ledger_repo.get_account_balance(account_id)
        await self.db.execute(
            update(Account)
            .where(Account.id == account_id)
            .values(balance=new_balance)
        )
        return new_balance

    async def _create_account_entry(
        self,
        txn_id: UUID,
        account_id: UUID,
        entry_type: str,
        amount: Decimal,
        notes: Optional[str] = None,
    ) -> None:
        """
        Creates a single ledger entry for a real user account.
        entry_type: 'debit' (money in) or 'credit' (money out).
        """
        last_balance = await self.ledger_repo.get_last_running_balance(account_id)
        if entry_type == "debit":
            running_balance = (last_balance + amount).quantize(Decimal("0.01"))
        else:
            running_balance = (last_balance - amount).quantize(Decimal("0.01"))
        await self.ledger_repo.create_entry(
            txn_id=txn_id,
            account_id=account_id,
            entry_type=entry_type,
            amount=amount,
            running_balance=running_balance,
            notes=notes,
        )

    # ── Create Transaction ────────────────────────────────────────────────────

    async def create_transaction(
        self, data: CreateTxnRequest, user_id: UUID
    ) -> Transaction:
        # 1. Idempotency
        existing = await self.txn_repo.get_by_idempotency_key(data.idempotency_key, user_id)
        if existing:
            return existing

        # 2. Validate source account
        source_account = await self._get_account_or_404(data.account_id, user_id)

        # 3. Transfer validation
        if data.txn_type == "transfer":
            if not data.transfer_to_account_id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="transfer_to_account_id is required for transfer transactions.",
                )
            if data.transfer_to_account_id == data.account_id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Source and destination accounts must be different.",
                )
            await self._get_account_or_404(data.transfer_to_account_id, user_id)

        # 4. Insert transaction row
        txn = await self.txn_repo.create({
            "user_id":                  user_id,
            "account_id":               data.account_id,
            "txn_type":                 data.txn_type,
            "amount":                   data.amount,
            "category":                 data.category,
            "subcategory":              data.subcategory,
            "division":                 data.division,
            "txn_date":                 data.txn_date,
            "description":              data.description,
            "store":                    data.store,
            "notes":                    data.notes,
            "is_tax_deductible":        data.is_tax_deductible,
            "cloudinary_url":           data.cloudinary_url,
            "idempotency_key":          data.idempotency_key,
            "transfer_to_account_id":   data.transfer_to_account_id,
        })

        # 5. Single-sided ledger entry against real account only
        if data.txn_type == "income":
            await self._create_account_entry(
                txn_id=txn.id,
                account_id=data.account_id,
                entry_type="debit",
                amount=data.amount,
                notes=f"Income: {data.description or ''}",
            )
            await self._recalc_and_sync_balance(data.account_id)

        elif data.txn_type == "expense":
            await self._create_account_entry(
                txn_id=txn.id,
                account_id=data.account_id,
                entry_type="credit",
                amount=data.amount,
                notes=f"Expense: {data.description or ''}",
            )
            await self._recalc_and_sync_balance(data.account_id)

        elif data.txn_type == "transfer":
            # Credit source (money out)
            await self._create_account_entry(
                txn_id=txn.id,
                account_id=data.account_id,
                entry_type="credit",
                amount=data.amount,
                notes=f"Transfer out from {source_account.name}",
            )
            # Debit destination (money in)
            await self._create_account_entry(
                txn_id=txn.id,
                account_id=data.transfer_to_account_id,
                entry_type="debit",
                amount=data.amount,
                notes=f"Transfer in from {source_account.name}",
            )
            await self._recalc_and_sync_balance(data.account_id)
            await self._recalc_and_sync_balance(data.transfer_to_account_id)

        # 6. Commit
        await self.db.commit()
        await self.db.refresh(txn, ["account"])
        txn.account_balance_after = await self._recalc_and_sync_balance(data.account_id)
        return txn

    # ── Update Transaction ────────────────────────────────────────────────────

    async def update_transaction(
        self, txn_id: UUID, data: UpdateTxnRequest, user_id: UUID
    ) -> Transaction:
        update_data = data.model_dump(exclude_none=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No fields provided for update.",
            )
        txn = await self.txn_repo.update(txn_id, user_id, update_data)
        if not txn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found.",
            )
        await self.db.commit()
        await self.db.refresh(txn, ["account"])
        return txn

    # ── Delete Transaction ────────────────────────────────────────────────────

    async def delete_transaction(self, txn_id: UUID, user_id: UUID) -> None:
        txn = await self.txn_repo.get_by_id(txn_id, user_id)
        if not txn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found.",
            )
        affected_accounts = [txn.account_id]
        if txn.transfer_to_account_id:
            affected_accounts.append(txn.transfer_to_account_id)
        deleted = await self.txn_repo.delete(txn_id, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found.",
            )
        for acc_id in affected_accounts:
            await self._recalc_and_sync_balance(acc_id)
        await self.db.commit()