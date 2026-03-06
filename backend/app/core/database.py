"""
app/core/database.py
Async SQLAlchemy engine + session factory.
Uses asyncpg driver for PostgreSQL.
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ── Engine ────────────────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,        # SQL logging in dev
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,         # reconnect on stale connections
)

# ── Session factory ───────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # keep objects usable after commit
    autocommit=False,
    autoflush=False,
)


# ── Base for all ORM models ───────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Dependency — yields a session, always closes it ──────────────────────────
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            