from typing import Optional

from sqlalchemy import select

from nlp.entities import User
from .base import BaseAlchemyRepository


class UserRepository(BaseAlchemyRepository):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.session.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.session.scalar(select(User).where(User.email == email))
