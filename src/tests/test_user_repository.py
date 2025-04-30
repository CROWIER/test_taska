import pytest
import pytest_asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import UserModel
from ..repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def user_repository(db_session: AsyncSession):
    print("Creating user repository", db_session)
    return UserRepository(db_session)


@pytest.mark.asyncio
async def test_create_user(user_repository: UserRepository):
    user_data = {
        "name": "Askar",
        "surname": "B",
        "password": "password",
    }
    user_model = UserModel(**user_data)

    created_user = await user_repository.create(user_model)

    assert created_user.id is not None
    assert created_user.name == user_data["name"]
    assert created_user.surname == user_data["surname"]
    assert created_user.password == user_data["password"]
    assert isinstance(created_user.created_at, datetime)
    assert isinstance(created_user.updated_at, datetime)
    assert created_user.created_at == created_user.updated_at

    users = await user_repository.get_all()
    assert len(users) == 1
    assert users[0].name == user_data["name"]
    assert users[0].surname == user_data["surname"]


@pytest.mark.asyncio
async def test_get_by_id(user_repository: UserRepository):
    user_data = {
        "name": "Jane",
        "surname": "Smith",
        "password": "password123",
    }
    user_model = UserModel(**user_data)

    created_user = await user_repository.create(user_model)

    fetched_user = await user_repository.get_by_id(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.name == user_data["name"]
    assert fetched_user.surname == user_data["surname"]
    assert fetched_user.password == user_data["password"]

    non_existent_user = await user_repository.get_by_id(999)
    assert non_existent_user is None


@pytest.mark.asyncio
async def test_update_user(user_repository: UserRepository):
    user_data = {
        "name": "Alice",
        "surname": "Brown",
        "password": "password789"
    }
    user_model = UserModel(**user_data)

    created_user = await user_repository.create(user_model)

    original_created_at = created_user.created_at

    created_user.name = "Askar1"
    created_user.surname = "B1"
    created_user.password = "newpassword101"
    updated_user = await user_repository.update(created_user)

    assert updated_user.name == "Askar1"
    assert updated_user.surname == "B1"
    assert updated_user.password == "newpassword101"
    assert updated_user.created_at == original_created_at
    assert updated_user.updated_at > original_created_at

    fetched_user = await user_repository.get_by_id(created_user.id)
    assert fetched_user.name == "Askar1"
    assert fetched_user.surname == "B1"
    assert fetched_user.password == "newpassword101"
    assert fetched_user.updated_at > original_created_at


@pytest.mark.asyncio
async def test_delete_user(user_repository: UserRepository):
    user_data = {
        "name": "Askar",
        "surname": "B",
        "password": "password202"
    }
    user_model = UserModel(**user_data)

    created_user = await user_repository.create(user_model)

    await user_repository.delete(created_user)

    fetched_user = await user_repository.get_by_id(created_user.id)
    assert fetched_user is None

    users = await user_repository.get_all()
    assert users == []
