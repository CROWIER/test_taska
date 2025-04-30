from typing import List

from litestar import get, post, patch, delete, Router

from src.api.dependencies import UserSvc
from src.schemas.user import UserCreate, UserUpdate, UserResponse


@get("/", description="Получить всех пользователей", response_model=List[UserResponse])
async def get_all_users(user_service: UserSvc) -> List[UserResponse]:
    return await user_service.get_all_users()


@get("/{user_id:int}", description="Получить пользователя по ID", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserSvc) -> UserResponse:
    return await user_service.get_user_by_id(user_id)


@post("/", description="Создать нового пользователя", response_model=UserResponse)
async def create_user(data: UserCreate, user_service: UserSvc) -> UserResponse:
    return await user_service.create_user(data)


@patch("/{user_id:int}", description="Обновить пользователя", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, user_service: UserSvc) -> UserResponse:
    return await user_service.update_user(user_id, data)


@delete("/{user_id:int}", status_code=204, description="Удалить пользователя")
async def delete_user(user_id: int, user_service: UserSvc) -> None:
    await user_service.delete_user(user_id)


user_router = Router(
    path="/users",
    route_handlers=[get_all_users, get_user, create_user, update_user, delete_user],
    tags=["users"],
)
