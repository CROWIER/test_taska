from typing import Annotated

from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_session
from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService


async def provide_db_session() -> AsyncSession:
    async for session in get_session():
        yield session


async def provide_user_repository(session: AsyncSession) -> UserRepository:
    return UserRepository(session)


async def provide_user_service(user_repo: UserRepository) -> UserService:
    return UserService(repository=user_repo)


DbSession = Annotated[AsyncSession, Provide(provide_db_session)]
UserRepo = Annotated[UserRepository, Provide(provide_user_repository)]
UserSvc = Annotated[UserService, Provide(provide_user_service)]

db_session_provider = Provide(provide_db_session)
user_repository_provider = Provide(provide_user_repository)
user_service_provider = Provide(provide_user_service)

common_dependencies = {
    "session": Provide(provide_db_session),
    "user_service": Provide(provide_user_service),
    "user_repo": Provide(provide_user_repository),
}