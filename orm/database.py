from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import get_settings

cfg = get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{cfg.db_user}:{cfg.db_password}@{cfg.db_host}:{cfg.db_port}/{cfg.db_name}"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=cfg.debug,
    future=True,  # pool_size=max(5, settings.POSTGRES_POOL_SIZE),
)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


def async_session_generator():
    return sessionmaker(async_engine, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
