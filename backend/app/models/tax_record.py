"""
app/models/tax_record.py
Tax records table — LHDN receipt vault.
7-year encrypted retention per Malaysian tax law.
Links to Cloudinary receipt storage.
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TaxRecord(Base):
    __tablename__ = "tax_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # Optional link to originating transaction
    transaction_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="SET NULL"),
        nullable=True, index=True
    )

    tax_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # LHDN relief category (e.g. "medical", "education", "lifestyle", "EPF")
    relief_category: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Claimable amount
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MYR")

    # Cloudinary receipt URL (encrypted)
    cloudinary_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Whether this has been submitted in a tax filing
    is_claimed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # 7-year retention — auto-calculated from tax_year
    retain_until_year: Mapped[int] = mapped_column(Integer, nullable=False)

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
    user: Mapped["User"] = relationship(back_populates="tax_records")  # noqa: F821

    def __repr__(self) -> str:
        return f"<TaxRecord id={self.id} year={self.tax_year} category={self.relief_category}>"