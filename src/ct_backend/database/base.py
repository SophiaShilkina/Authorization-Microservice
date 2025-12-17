from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import config

engine = create_async_engine(config.postgres.dsn, pool_size=20, max_overflow=10)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
