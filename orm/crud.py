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
    def create_user(db: Session, user: schemas.User):
        db_user = models.User(id=user.id, username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
