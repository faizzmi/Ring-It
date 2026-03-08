"""
app/api/v1/accounts.py
FastAPI route handlers for the /api/v1/accounts resource.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Body, Depends, Query, Request, status
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.core.rate_limit import limiter
from app.models.user import User
from app.repositories.account_repo import AccountRepository
from app.schemas.accounts import (
    AccountListResponse,
    AccountResponse,
    CreateAccountRequest,
    DeleteAccountResponse,
    UpdateAccountRequest,
)
from app.services.account_services import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


def get_account_service() -> AccountService:
    return AccountService(repo=AccountRepository())


@router.get("", response_model=AccountListResponse, summary="List all accounts.")
@limiter.limit("100/minute")
async def list_accounts(
    request: Request,
    response: Response,
    include_inactive: bool = Query(default=False),
    limit: Optional[int] = Query(default=None, ge=1, le=100, description="Max accounts to return. Total and has_more always reflect the full count."),
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AccountListResponse:
    return await service.list_accounts(
        db,
        user_id=current_user.id,
        include_inactive=include_inactive,
        limit=limit,
    )


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED, summary="Create a new account.")
@limiter.limit("30/minute")
async def create_account(
    request: Request,
    response: Response,
    data: CreateAccountRequest = Body(...),
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AccountResponse:
    return await service.create_account(db, user_id=current_user.id, data=data)


@router.get("/{account_id}", response_model=AccountResponse, summary="Get a single account.")
@limiter.limit("100/minute")
async def get_account(
    request: Request,
    response: Response,
    account_id: uuid.UUID,
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AccountResponse:
    return await service.get_account(db, account_id=account_id, user_id=current_user.id)


@router.patch("/{account_id}", response_model=AccountResponse, summary="Partially update an account.")
@limiter.limit("60/minute")
async def update_account(
    request: Request,
    response: Response,
    account_id: uuid.UUID,
    data: UpdateAccountRequest = Body(...),
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AccountResponse:
    return await service.update_account(db, account_id=account_id, user_id=current_user.id, data=data)


@router.delete("/{account_id}", response_model=DeleteAccountResponse, summary="Delete an account.")
@limiter.limit("20/minute")
async def delete_account(
    request: Request,
    response: Response,
    account_id: uuid.UUID,
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DeleteAccountResponse:
    return await service.delete_account(db, account_id=account_id, user_id=current_user.id)