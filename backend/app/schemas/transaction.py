"""
app/schemas/transaction.py
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ── Enums ─────────────────────────────────────────────────────────────────────

TxnType = Literal["income", "expense", "transfer"]
TxnCategory = Literal["commitment", "want", "savings", "income"]
TxnDivision = Literal["commitment", "savings", "want", "income"]

# ── Request Schemas ───────────────────────────────────────────────────────────

class CreateTxnRequest(BaseModel):
    model_config = ConfigDict(strict=False)

    account_id: UUID
    amount: Decimal = Field(gt=0, decimal_places=2)
    txn_type: TxnType
    category: TxnCategory = "commitment"
    subcategory: Optional[str] = None
    division: TxnDivision = "commitment"
    txn_date: date
    description: Optional[str] = Field(default=None, max_length=255)
    store: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None
    is_tax_deductible: bool = False
    idempotency_key: str = Field(min_length=1, max_length=100)
    transfer_to_account_id: Optional[UUID] = None
    cloudinary_url: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Transaction amount must be positive.")
        return v.quantize(Decimal("0.01"))

    @field_validator("transfer_to_account_id")
    @classmethod
    def transfer_requires_destination(cls, v: Optional[UUID], info) -> Optional[UUID]:
        return v

class UpdateTxnRequest(BaseModel):
    model_config = ConfigDict(strict=False)

    description: Optional[str] = Field(default=None, max_length=255)
    store: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None
    is_tax_deductible: Optional[bool] = None
    cloudinary_url: Optional[str] = None
    category: Optional[TxnCategory] = None
    subcategory: Optional[str] = None
    division: Optional[TxnDivision] = None

class TxnFilterParams(BaseModel):
    model_config = ConfigDict(strict=False)

    account_id: Optional[UUID] = None
    txn_type: Optional[TxnType] = None
    category: Optional[TxnCategory] = None
    subcategory: Optional[str] = None
    division: Optional[TxnDivision] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    limit: int = Field(default=50, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)

# ── Response Schemas ──────────────────────────────────────────────────────────

class AccountSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    institution: Optional[str]
    account_type: str

class TxnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    account_id: UUID
    account: AccountSummary
    txn_type: TxnType
    amount: Decimal
    category: str
    subcategory: Optional[str]
    division: Optional[str]
    txn_date: date
    description: Optional[str]
    store: Optional[str]
    notes: Optional[str]
    is_tax_deductible: bool
    cloudinary_url: Optional[str]
    transfer_to_account_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    account_balance_after: Optional[Decimal] = None

class TxnListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TxnResponse]

class CloudinarySignatureResponse(BaseModel):
    signature: str
    timestamp: int
    folder: str
    api_key: str
    cloud_name: str

class ImportRowError(BaseModel):
    row: int
    reason: str

class BulkImportResponse(BaseModel):
    imported: int
    skipped: int
    errors: list[ImportRowError]
    message: str