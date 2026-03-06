"""
app/models/debt.py
Debts table — tracked by the Debt Netting Engine.
Supports DSR calculation, snowball and avalanche payoff strategies.
DSR formula per BNM guidelines (SDD Section 4.2).
"""
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import DATE, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Debt(Base):
    __tablename__ = "debts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # personal_loan | credit_card | car_loan | housing_loan | BNPL | study_loan | other
    debt_type: Mapped[str] = mapped_column(String(30), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Original principal
    principal_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Current outstanding balance
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Fixed monthly payment commitment
    monthly_payment: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Annual interest rate (e.g. 0.1800 = 18%)
    interest_rate: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)

    # Consecutive months with on-time payments — for behavioural streak display
    payment_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    start_date: Mapped[date | None] = mapped_column(DATE, nullable=True)
    end_date: Mapped[date | None] = mapped_column(DATE, nullable=True)

    institution: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # active | settled | defaulted
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MYR")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="debts")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Debt id={self.id} type={self.debt_type} balance={self.outstanding_balance}>"