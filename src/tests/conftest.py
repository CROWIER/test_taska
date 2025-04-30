import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pytest_postgresql import factories
from src.models.user import Base

postgresql_proc = factories.postgresql_proc()

postgresql = factories.postgresql("postgresql_proc")


@pytest_asyncio.fixture
async def db_session(postgresql):
    print(f"Type of postgresql: {type(postgresql)}")
    print(f"postgresql.info: {vars(postgresql.info)}")
    connection_string = (
        f"postgresql+asyncpg://{postgresql.info.user}:@localhost:"
        f"{postgresql.info.port}/{postgresql.info.dbname}"
    )
    print(f"Connection string: {connection_string}")

    engine = create_async_engine(connection_string, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()