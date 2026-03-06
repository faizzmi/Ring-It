"""
app/models/goal.py
Goals table — savings targets with compounding projections.
Powers the 10-year compound wealth visualisation (SDD 1.3).
"""
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import DATE, Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Target amount to reach
    target_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Current saved amount — updated on each contribution transaction
    current_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal("0.00")
    )

    # Expected annual return rate for compounding projection (e.g. 0.06 = 6%)
    expected_return_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), nullable=False, default=Decimal("0.0600")
    )

    # Monthly contribution amount
    monthly_contribution: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal("0.00")
    )

    target_date: Mapped[date | None] = mapped_column(DATE, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MYR")

    # active | completed | paused
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    is_emergency_fund: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

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
    user: Mapped["User"] = relationship(back_populates="goals")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Goal id={self.id} name={self.name} status={self.status}>"