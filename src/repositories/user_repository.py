from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[UserModel]:
        result = await self.session.execute(select(UserModel))
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalars().first()

    async def create(self, user_model: UserModel) -> UserModel:
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model

    async def update(self, user_model: UserModel) -> UserModel:
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model

    async def delete(self, user_model: UserModel) -> None:
        await self.session.delete(user_model)
        await self.session.commit()
