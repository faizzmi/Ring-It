"""
app/api/v1/transactions.py
FastAPI routes for the Transaction module.

Routes:
  POST   /transactions                — create single transaction
  GET    /transactions                — list with filters + pagination
  GET    /transactions/{id}           — single transaction detail
  PATCH  /transactions/{id}           — update non-ledger fields only
  DELETE /transactions/{id}           — delete + reverse ledger + recalc balance
  POST   /transactions/import         — bulk import from CSV / XLSX
  GET    /transactions/cloudinary-signature — signed upload token for receipt
"""
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, Query, Request, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.rate_limit import limiter
from app.models.user import User
from app.schemas.transaction import (
    BulkImportResponse,
    CloudinarySignatureResponse,
    CreateTxnRequest,
    TxnListResponse,
    TxnResponse,
    UpdateTxnRequest,
)
from app.services.cloudinary_service import CloudinaryService
from app.services.import_service import ImportService
from app.services.ledger_service import LedgerService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# ── Dependency factories ──────────────────────────────────────────────────────

def get_ledger_service(db: AsyncSession = Depends(get_db)) -> LedgerService:
    return LedgerService(db)

def get_import_service(db: AsyncSession = Depends(get_db)) -> ImportService:
    return ImportService(db)

cloudinary_service = CloudinaryService()


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=TxnResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a single transaction",
)
@limiter.limit("100/minute")
async def create_transaction(
    request: Request,
    response: Response,
    data: CreateTxnRequest,
    service: LedgerService = Depends(get_ledger_service),
    current_user: User = Depends(get_current_user),
) -> TxnResponse:
    txn = await service.create_transaction(data, current_user.id)
    return TxnResponse.model_validate(txn)


@router.get(
    "",
    response_model=TxnListResponse,
    summary="List transactions with filters",
)
@limiter.limit("100/minute")
async def list_transactions(
    request: Request,
    response: Response,
    account_id: UUID | None = Query(default=None),
    txn_type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    division: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    service: LedgerService = Depends(get_ledger_service),
    current_user: User = Depends(get_current_user),
) -> TxnListResponse:
    from app.repositories.transaction_repo import TransactionRepository
    from datetime import datetime
    repo = TransactionRepository(service.db)

    def _parse_date(s: str | None):
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    items, total = await repo.list_by_user(
        user_id=current_user.id,
        account_id=account_id,
        txn_type=txn_type,
        category=category,
        division=division,
        date_from=_parse_date(date_from),
        date_to=_parse_date(date_to),
        limit=limit,
        offset=offset,
    )
    return TxnListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[TxnResponse.model_validate(t) for t in items],
    )


@router.get(
    "/cloudinary-signature",
    response_model=CloudinarySignatureResponse,
    summary="Get signed Cloudinary upload params for receipt",
)
async def get_cloudinary_signature(
    current_user: User = Depends(get_current_user),
) -> CloudinarySignatureResponse:
    return cloudinary_service.get_upload_signature(current_user.id)


@router.post(
    "/import",
    response_model=BulkImportResponse,
    status_code=status.HTTP_200_OK,
    summary="Bulk import transactions from CSV or XLSX",
)
@limiter.limit("10/minute")
async def import_transactions(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    default_account_id: UUID = Form(...),
    service: ImportService = Depends(get_import_service),
    current_user: User = Depends(get_current_user),
) -> BulkImportResponse:
    return await service.import_file(file, current_user.id, default_account_id)


@router.get(
    "/{txn_id}",
    response_model=TxnResponse,
    summary="Get a single transaction by ID",
)
async def get_transaction(
    txn_id: UUID,
    service: LedgerService = Depends(get_ledger_service),
    current_user: User = Depends(get_current_user),
) -> TxnResponse:
    from app.repositories.transaction_repo import TransactionRepository
    from fastapi import HTTPException
    repo = TransactionRepository(service.db)
    txn = await repo.get_by_id(txn_id, current_user.id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return TxnResponse.model_validate(txn)


@router.patch(
    "/{txn_id}",
    response_model=TxnResponse,
    summary="Update non-ledger fields of a transaction",
)
@limiter.limit("100/minute")
async def update_transaction(
    request: Request,
    response: Response,
    txn_id: UUID,
    data: UpdateTxnRequest,
    service: LedgerService = Depends(get_ledger_service),
    current_user: User = Depends(get_current_user),
) -> TxnResponse:
    txn = await service.update_transaction(txn_id, data, current_user.id)
    return TxnResponse.model_validate(txn)


@router.delete(
    "/{txn_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a transaction and recalculate account balance",
)
@limiter.limit("100/minute")
async def delete_transaction(
    request: Request,
    response: Response,
    txn_id: UUID,
    service: LedgerService = Depends(get_ledger_service),
    current_user: User = Depends(get_current_user),
) -> None:
    await service.delete_transaction(txn_id, current_user.id)