from datetime import datetime
import pytest
from unittest.mock import MagicMock
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.models.user import UserModel
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from litestar.exceptions import NotFoundException


@pytest.fixture
def mock_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_repository):
    return UserService(repository=mock_repository)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_repository):
    user_data = UserCreate(name="Askar", surname="B", password="password123")

    mock_repository.create.return_value = UserModel(
        id=1,
        name=user_data.name,
        surname=user_data.surname,
        password="hashed_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    created_user = await user_service.create_user(user_data)

    mock_repository.create.assert_called_once()

    assert created_user.name == "Askar"
    assert created_user.surname == "B"
    assert created_user.created_at is not None
    assert created_user.updated_at is not None


@pytest.mark.asyncio
async def test_get_user_by_id(user_service, mock_repository):
    mock_user = UserModel(
        id=1, name="Askar",
        surname="B",
        password="hashed_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_repository.get_by_id.return_value = mock_user

    user = await user_service.get_user_by_id(user_id=1)

    mock_repository.get_by_id.assert_called_once_with(1)

    assert user.name == "Askar"
    assert user.surname == "B"
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await user_service.get_user_by_id(user_id=999)


@pytest.mark.asyncio
async def test_update_user(user_service, mock_repository):
    user_data = UserUpdate(name="Ask", surname="B2", password="newpassword123")
    mock_user = UserModel(
        id=1, name="Askar",
        surname="B",
        password="hashed_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_repository.get_by_id.return_value = mock_user
    mock_repository.update.return_value = mock_user

    updated_user = await user_service.update_user(user_id=1, user_data=user_data)

    mock_repository.update.assert_called_once()

    assert updated_user.name == "Ask"
    assert updated_user.surname == "B2"
    assert updated_user.created_at is not None


@pytest.mark.asyncio
async def test_delete_user(user_service, mock_repository):
    mock_user = UserModel(id=1, name="Askar", surname="B", password="hashed_password")
    mock_repository.get_by_id.return_value = mock_user

    await user_service.delete_user(user_id=1)

    mock_repository.delete.assert_called_once()
