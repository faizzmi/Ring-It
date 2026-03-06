"""
app/models/policy_config.py
Policy config table — stores annual LHDN tax relief limits, EPF rates,
Zakat nisab values, etc. Managed by APScheduler annual migration (SDD Section 8).
Admin updates values manually; Jan 1 cron activates the new year config.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PolicyConfig(Base):
    __tablename__ = "policy_configs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Policy year this config applies to (e.g. 2026)
    policy_year: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)

    # Policy type: lhdn_relief | epf_rates | zakat_nisab | bnm_rates
    policy_type: Mapped[str] = mapped_column(String(30), nullable=False, default="lhdn_relief")

    # JSONB blob — flexible config structure per year
    # Example: {"lifestyle_limit": 2500, "medical_limit": 10000, "epf_rate": 0.11}
    config_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Only one config per year is active at a time
    # APScheduler flips is_active=False on old, True on new each Jan 1
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    # Human-readable notes for admin
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Immutable audit trail — who activated this config and when
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    activated_by: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<PolicyConfig year={self.policy_year} active={self.is_active}>"