from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from bot.config import config
from bot.database.models import Base

# Async engine yaratish
engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Databaseni ishga tushirish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Sessiya olish"""
    async with async_session_maker() as session:
        yield session
