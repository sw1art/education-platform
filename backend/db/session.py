from typing import Generator
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, 
    async_sessionmaker, 
    create_async_engine, 
    AsyncSession
    )
from sqlalchemy.orm import (
    sessionmaker, 
    Mapped, 
    mapped_column, 
    DeclarativeBase
    )

from settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


# create async engine for interaction with database
engine = create_async_engine(
    settings.REAL_DATABASE_URL, 
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()