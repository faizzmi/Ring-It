"""
app/models/__init__.py
Import all models here in dependency order.
Alembic env.py and main.py import this to ensure
Base.metadata is fully populated before migrations run.
"""
from app.models.base import Base          # noqa: F401  — must be first
from app.models.user import User          # noqa: F401
from app.models.account import Account   # noqa: F401
from app.models.transaction import Transaction        # noqa: F401
from app.models.ledger_entry import LedgerEntry       # noqa: F401
from app.models.budget import Budget                  # noqa: F401
from app.models.goal import Goal                      # noqa: F401
from app.models.debt import Debt                      # noqa: F401
from app.models.tax_record import TaxRecord           # noqa: F401
from app.models.policy_config import PolicyConfig     # noqa: F401
from app.models.email_verification import EmailVerificationToken

__all__ = [
    "Base",
    "User",
    "Account",
    "Transaction",
    "LedgerEntry",
    "Budget",
    "Goal",
    "Debt",
    "TaxRecord",
    "PolicyConfig",
    "EmailVerificationToken"
]