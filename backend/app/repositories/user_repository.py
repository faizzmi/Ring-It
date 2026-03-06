# app/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.encryption import encryptor, hmac_email  # ← add hmac_email import
import uuid


class UserRepository:

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(
            select(User).where(User.email_hmac == hmac_email(email))  # O(1) index lookup
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def create(self, **kwargs) -> User:
        if 'email' in kwargs:
            plain_email = kwargs.pop('email')
            kwargs['email_encrypted'] = encryptor.encrypt(plain_email)
            kwargs['email_hmac'] = hmac_email(plain_email)  # ← store HMAC alongside
        if 'full_name' in kwargs:
            kwargs['full_name_encrypted'] = encryptor.encrypt(kwargs.pop('full_name'))
        user = User(**kwargs)
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update_last_login(self, user: User) -> None:
        from datetime import datetime, timezone
        user.last_login_at = datetime.now(timezone.utc)
        await self._db.commit()