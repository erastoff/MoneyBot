from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import models, schemas


class Users:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        async with db as session:
            result = await session.execute(
                select(models.User).filter(models.User.id == user_id)
            )
            user = result.scalars().first()
            return user

    @staticmethod
    async def create_user(db: AsyncSession, user: schemas.User):
        async with db as session:
            db_user = models.User(id=user.id, name=user.name)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user
