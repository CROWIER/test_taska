import bcrypt
from typing import List

from litestar.exceptions import NotFoundException

from ..models.user import UserModel
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.repository.get_all()
        return [UserResponse.from_orm(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")
        return UserResponse.from_orm(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        hashed_password = self.hash_password(user_data.password)
        user = UserModel(
            name=user_data.name,
            surname=user_data.surname,
            password=hashed_password
        )

        created_user = await self.repository.create(user)
        return UserResponse.from_orm(created_user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")

        update_data = {
            field: value for field, value in user_data.model_dump().items()
            if value is not None
        }

        if 'password' in update_data:
            update_data['password'] = self.hash_password(update_data['password'])

        for field, value in update_data.items():
            setattr(user, field, value)

        updated_user = await self.repository.update(user)
        return UserResponse.from_orm(updated_user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")

        await self.repository.delete(user)
