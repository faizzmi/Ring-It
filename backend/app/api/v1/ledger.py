from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import datetime, timezone
import logging

from app.core.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.ledger import LedgerSummaryResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("/summary", response_model=LedgerSummaryResponse)
async def get_ledger_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    this_month = now.month
    this_year = now.year
    last_month = 12 if this_month == 1 else this_month - 1
    last_year = this_year - 1 if this_month == 1 else this_year
    user_id = current_user.id

    # ── Net Worth ──────────────────────────────────────────────────────────────
    net_worth_result = await db.execute(
        select(func.coalesce(func.sum(Account.balance), 0))
        .where(Account.user_id == user_id, Account.is_active == True)
    )
    net_worth = float(net_worth_result.scalar())

    # ── Monthly income / expense helper ───────────────────────────────────────
    async def month_sum(txn_type: str, month: int, year: int) -> float:
        result = await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id == user_id,
                Transaction.txn_type == txn_type,
                extract("month", Transaction.txn_date) == month,
                extract("year", Transaction.txn_date) == year,
            )
        )
        return float(result.scalar())

    income_this   = await month_sum("income",  this_month, this_year)
    expense_this  = await month_sum("expense", this_month, this_year)
    savings_this  = income_this - expense_this

    income_last   = await month_sum("income",  last_month, last_year)
    expense_last  = await month_sum("expense", last_month, last_year)
    savings_last  = income_last - expense_last

    net_worth_delta = savings_this

    # ── Trend helper ──────────────────────────────────────────────────────────
    def pct_change(current: float, previous: float) -> float:
        if previous == 0:
            return 0.0
        return round(((current - previous) / abs(previous)) * 100, 1)

    income_trend  = pct_change(income_this,  income_last)
    expense_trend = pct_change(expense_this, expense_last)
    savings_trend = pct_change(savings_this, savings_last)

    # ── DSR ───────────────────────────────────────────────────────────────────
    # Use func.lower() for case-insensitive match in case DB values are mixed-case
    # ("Commitment", "COMMITMENT", "commitment" all match)
    dsr_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(
            Transaction.user_id == user_id,
            Transaction.txn_type == "expense",
            func.lower(Transaction.division) == "commitment",
            extract("month", Transaction.txn_date) == this_month,
            extract("year", Transaction.txn_date) == this_year,
        )
    )
    monthly_commitments = float(dsr_result.scalar())
    dsr = round((monthly_commitments / income_this * 100), 1) if income_this > 0 else 0.0

    # ── Debug log (remove once confirmed working) ─────────────────────────────
    logger.debug(
        "[DSR DEBUG] user=%s month=%s/%s | income=%.2f expense=%.2f "
        "commitments=%.2f dsr=%.1f%%",
        user_id, this_month, this_year,
        income_this, expense_this, monthly_commitments, dsr,
    )
    # Also print so it shows in uvicorn stdout without log-level config:
    print(
        f"[DSR DEBUG] user={user_id} period={this_month}/{this_year} | "
        f"income={income_this} expense={expense_this} "
        f"commitments={monthly_commitments} dsr={dsr}%"
    )

    # ── DSR health band ───────────────────────────────────────────────────────
    def dsr_health(value: float) -> dict:
        if value < 30:
            return {"status": "healthy", "label": "Healthy",     "message": "You are on the right track, keep it up!"}
        elif value < 52:
            return {"status": "good",    "label": "Good",        "message": "Try to maintain and avoid new commitments."}
        elif value <= 61:
            return {"status": "danger",  "label": "Danger Zone", "message": "Analyse and reflect on your monthly commitments and spendings."}
        else:
            return {"status": "critical","label": "Critical",    "message": "Seek professional help and advice such as AKPK."}

    dsr_indicator = dsr_health(dsr)

    return LedgerSummaryResponse(
        netWorth=round(net_worth, 2),
        netWorthDelta=round(net_worth_delta, 2),
        dsr=dsr,
        dsrStatus=dsr_indicator["status"],
        dsrLabel=dsr_indicator["label"],
        dsrMessage=dsr_indicator["message"],
        income=round(income_this, 2),
        expenses=round(expense_this, 2),
        savings=round(savings_this, 2),
        incomeTrend=income_trend,
        expenseTrend=expense_trend,
        savingsTrend=savings_trend,
    )