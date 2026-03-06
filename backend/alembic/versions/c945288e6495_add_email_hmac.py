"""add_email_hmac

Revision ID: c945288e6495
Revises: 868fd0016221
Create Date: 2026-03-06 18:06:20.774648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c945288e6495'
down_revision: Union[str, None] = '868fd0016221'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass