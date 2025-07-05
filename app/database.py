from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Example PostgreSQL URL
POSTGRES_USER = "munyroth"
POSTGRES_PASSWORD = "734658"
POSTGRES_DB = "konektagri"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

postgres_url = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

async_engine = create_async_engine(
    postgres_url,
    echo=True  # echo=True to log SQL queries
)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
