"""
app/schemas/accounts.py
Pydantic v2 request / response schemas for the Accounts resource.

All monetary amounts are represented as Decimal strings to prevent
IEEE-754 float rounding errors on financial values (Design Decision DD-02).
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── Shared literals ──────────────────────────────────────────────────────────
AccountType = Literal["bank", "ewallet", "cash"]
CurrencyCode = Literal["MYR", "USD", "EUR", "SGD", "GBP"]


# ── Card theme mapping (derived, not stored in DB) ───────────────────────────
THEME_MAP: dict[str, str] = {
    "bank":    "ox",
    "ewallet": "tng",
    "cash":    "slate",
}


# ════════════════════════════════════════════════════════════════════════════
# REQUEST SCHEMAS
# ════════════════════════════════════════════════════════════════════════════

class CreateAccountRequest(BaseModel):
    """POST /api/v1/accounts — create a new account."""
    model_config = ConfigDict()

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable account label, e.g. 'Maybank Savings'.",
    )
    account_type: AccountType = Field(
        default="bank",
        description="Account category: bank | ewallet | cash.",
    )
    currency: CurrencyCode = Field(
        default="MYR",
        description="ISO 4217 currency code. Defaults to MYR.",
    )
    institution: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Financial institution name, e.g. 'Maybank'.",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional free-text notes visible only to the owner.",
    )
    opening_balance: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        description="Initial balance seeded into the ledger on account creation.",
    )

    @field_validator("opening_balance")
    @classmethod
    def quantize_balance(cls, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.01"))

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class UpdateAccountRequest(BaseModel):
    """PATCH /api/v1/accounts/{account_id} — partial update."""
    model_config = ConfigDict(strict=True)

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    account_type: Optional[AccountType] = None
    currency: Optional[CurrencyCode] = None
    institution: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


# ════════════════════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS
# ════════════════════════════════════════════════════════════════════════════

class AccountResponse(BaseModel):
    """Single account — returned by create, get, and update endpoints."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    account_type: AccountType
    currency: str
    balance: Decimal
    institution: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # ── Derived presentation fields (computed in service layer) ──────────────
    theme: str = Field(
        default="ox",
        description="CSS theme token used by the frontend card component.",
    )
    last4: str = Field(
        default="0000",
        description="Last 4 chars of the UUID — used as card number stub.",
    )

    @classmethod
    def from_orm_with_meta(cls, account: object) -> "AccountResponse":
        """
        Factory that populates derived fields (theme, last4) from the ORM
        object before returning the schema.  Call this instead of
        model_validate() everywhere in the service layer.
        """
        obj = cls.model_validate(account)
        obj.theme = THEME_MAP.get(obj.account_type, "ox")
        obj.last4 = str(obj.id).replace("-", "")[-4:].upper()
        return obj


class AccountListResponse(BaseModel):
    """GET /api/v1/accounts — paginated list of accounts."""
    model_config = ConfigDict(from_attributes=True)

    items: list[AccountResponse]
    total: int
    active_count: int
    total_balance: Decimal = Field(
        description="Sum of balances for all active accounts (same currency).",
    )


class DeleteAccountResponse(BaseModel):
    """DELETE /api/v1/accounts/{account_id}"""
    deleted: bool
    account_id: uuid.UUID
    message: str

class AccountListResponse(BaseModel):
    items:         list[AccountResponse]
    total:         int
    active_count:  int
    total_balance: Decimal
    has_more:      bool = False