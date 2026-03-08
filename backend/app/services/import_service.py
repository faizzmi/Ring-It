"""
app/services/import_service.py

Handles bulk transaction import from CSV and XLSX files.

Your sheet column mapping:
  Date             → txn_date
  Category         → subcategory  (e.g. "Treat", "Grab", "Gold", "Salary")
  Description      → description
  Payment Method   → payment_method_hint  (E-Wallet / Debit / Online / Cash)
  Account          → payment_method  (matched to account name/institution)
  Amount (RM)      → amount
  Type             → txn_type  (Income / Expenses → income / expense)
  Store            → store
  Division         → category  (Commitment/Want/Savings/Income — top-level)
  Notes            → notes
"""
import io
import uuid
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

import pandas as pd
from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.schemas.transaction import BulkImportResponse, CreateTxnRequest, ImportRowError
from app.services.ledger_service import LedgerService

# ── Valid values ───────────────────────────────────────────────────────────────

VALID_CATEGORIES = {"commitment", "want", "savings", "income"}
VALID_DIVISIONS  = {"commitment", "savings", "want", "income"}

DEFAULT_CATEGORY = "commitment"
DEFAULT_DIVISION = "commitment"
DEFAULT_TXN_TYPE = "expense"

CATEGORY_ALIASES: dict[str, str] = {
    "commitment": "commitment",
    "comitmment": "commitment",
    "comitment":  "commitment",
    "want":       "want",
    "savings":    "savings",
    "saving":     "savings",
    "income":     "income",
}

TXN_TYPE_ALIASES: dict[str, str] = {
    "income":   "income",
    "expense":  "expense",
    "expenses": "expense",
    "transfer": "transfer",
}

COLUMN_ALIASES: dict[str, str] = {
    "date":           "txn_date",
    "txn_date":       "txn_date",
    "amount":         "amount",
    "amount (rm)":    "amount",
    "amount(rm)":     "amount",
    "description":    "description",
    "desc":           "description",
    "category":       "subcategory",
    "subcategory":    "subcategory",
    "division":       "category",
    "type":           "txn_type",
    "txn_type":       "txn_type",
    "store":          "store",
    "notes":          "notes",
    "payment_method": "payment_method",
    "account":        "payment_method",
    "payment method": "payment_method",
}


class ImportService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.ledger_service = LedgerService(db)

    async def _read_file(self, file: UploadFile) -> pd.DataFrame:
        content = await file.read()
        filename = (file.filename or "").lower()
        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(io.BytesIO(content), dayfirst=True)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not parse CSV: {e}")
        elif filename.endswith((".xlsx", ".xls")):
            try:
                # parse_dates=False keeps dates as pandas Timestamps which _parse_date handles
                df = pd.read_excel(io.BytesIO(content), parse_dates=False)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not parse Excel file: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only .csv, .xlsx, and .xls files are supported.")

        df.columns = [COLUMN_ALIASES.get(c.strip().lower(), c.strip().lower()) for c in df.columns]
        return df

    def _parse_date(self, raw: Any) -> Optional[date]:
        if raw is None:
            return None
        try:
            if pd.isna(raw):
                return None
        except (TypeError, ValueError):
            pass
        # pandas already parses XLSX dates as Timestamp or datetime
        if isinstance(raw, pd.Timestamp):
            return raw.date()
        if isinstance(raw, datetime):
            return raw.date()
        if isinstance(raw, date):
            return raw
        # Excel serial number (float/int) — days since 1899-12-30
        if isinstance(raw, (int, float)):
            try:
                return (pd.Timestamp("1899-12-30") + pd.Timedelta(days=int(raw))).date()
            except Exception:
                return None
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                return datetime.strptime(str(raw).strip(), fmt).date()
            except ValueError:
                continue
        return None

    def _parse_amount(self, raw: Any) -> Optional[Decimal]:
        if raw is None:
            return None
        try:
            if pd.isna(raw):
                return None
        except (TypeError, ValueError):
            pass
        try:
            val = Decimal(str(raw).replace(",", "").replace("RM", "").strip())
            return val.quantize(Decimal("0.01")) if val > 0 else None
        except InvalidOperation:
            return None

    def _clean_str(self, raw: Any, max_len: int = 255) -> Optional[str]:
        if raw is None:
            return None
        try:
            if pd.isna(raw):
                return None
        except (TypeError, ValueError):
            pass
        val = str(raw).strip()
        return val[:max_len] if val else None

    async def import_file(self, file: UploadFile, user_id: uuid.UUID, default_account_id: uuid.UUID) -> BulkImportResponse:
        df = await self._read_file(file)
        errors: list[ImportRowError] = []
        imported = skipped = 0

        # Cache user accounts once to avoid one query per row
        result = await self.db.execute(
            select(Account).where(Account.user_id == user_id, Account.is_active == True)  # noqa: E712
        )
        accounts = result.scalars().all()

        for idx, row in df.iterrows():
            row_num = int(idx) + 2

            # ── Required: date ────────────────────────────────────────────
            txn_date = self._parse_date(row.get("txn_date"))
            if not txn_date:
                skipped += 1
                continue

            # ── Required: amount ──────────────────────────────────────────
            amount = self._parse_amount(row.get("amount"))
            if not amount:
                skipped += 1
                continue

            # ── txn_type ──────────────────────────────────────────────────
            raw_type = self._clean_str(row.get("txn_type"), 20)
            txn_type = TXN_TYPE_ALIASES.get(raw_type.lower() if raw_type else "", DEFAULT_TXN_TYPE)

            # ── category (from Division column) ───────────────────────────
            raw_cat = self._clean_str(row.get("category"), 50)
            if raw_cat:
                category = CATEGORY_ALIASES.get(raw_cat.lower(), DEFAULT_CATEGORY)
            else:
                category = "income" if txn_type == "income" else DEFAULT_CATEGORY

            # ── subcategory (from Category column) ────────────────────────
            subcategory = self._clean_str(row.get("subcategory"), 100)

            # ── division mirrors category ─────────────────────────────────
            division = category if category in VALID_DIVISIONS else DEFAULT_DIVISION

            # ── account resolution (cached) ───────────────────────────────
            payment_method = self._clean_str(row.get("payment_method"), 100)
            account_id = default_account_id
            if payment_method:
                val = payment_method.lower()
                for acc in accounts:
                    if acc.name.lower() == val or (acc.institution and acc.institution.lower() == val):
                        account_id = acc.id
                        break

            # ── build + create ────────────────────────────────────────────
            try:
                req = CreateTxnRequest.model_construct(
                    account_id=account_id,
                    amount=amount,
                    txn_type=txn_type,
                    category=category,
                    subcategory=subcategory,
                    division=division,
                    txn_date=txn_date,
                    description=self._clean_str(row.get("description")),
                    store=self._clean_str(row.get("store"), 100),
                    notes=self._clean_str(row.get("notes")),
                    is_tax_deductible=False,
                    idempotency_key=str(uuid.uuid4()),
                    transfer_to_account_id=None,
                    cloudinary_url=None,
                )
                await self.ledger_service.create_transaction(req, user_id)
                imported += 1
            except Exception as e:
                # Rollback the failed row so the DB session stays usable for the next row
                await self.db.rollback()
                reason = e.detail if isinstance(e, HTTPException) else str(e)
                errors.append(ImportRowError(row=row_num, reason=reason))

        return BulkImportResponse(
            imported=imported,
            skipped=skipped,
            errors=errors,
            message=f"Import complete: {imported} imported, {skipped} skipped, {len(errors)} errors.",
        )