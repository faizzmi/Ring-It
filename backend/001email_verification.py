"""add email_verification_tokens

Revision ID: 001_email_verification
Revises: <your previous revision id>
Create Date: 2026-01-01 00:00:00

Run:  alembic upgrade head
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_email_verification'
down_revision = None   # ← replace with your previous revision id
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'email_verification_tokens',
        sa.Column('id',         postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id',    postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token',      sa.String(128), nullable=False, unique=True),
        sa.Column('used',       sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index('ix_email_verification_tokens_user_id', 'email_verification_tokens', ['user_id'])
    op.create_index('ix_email_verification_tokens_token',   'email_verification_tokens', ['token'])


def downgrade() -> None:
    op.drop_table('email_verification_tokens')