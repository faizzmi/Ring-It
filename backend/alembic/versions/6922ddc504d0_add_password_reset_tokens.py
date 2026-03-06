"""add_password_reset_tokens

Revision ID: 6922ddc504d0
Revises: c945288e6495
Create Date: 2026-03-06 19:11:20.046052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6922ddc504d0'
down_revision: Union[str, None] = 'c945288e6495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass