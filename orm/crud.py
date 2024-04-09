from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

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

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        async with db as session:
            pass
        # cascade delete calculations and assest


class Calculations:
    @staticmethod
    async def create_calculation(db: AsyncSession, calculation: schemas.Calculation):
        async with db as session:
            db_calculation = models.Calculation(
                base_currency=calculation.base_currency,
                owner_id=calculation.owner_id,
            )
            session.add(db_calculation)
            await session.commit()
            await session.refresh(db_calculation)
            return db_calculation

    @staticmethod
    async def get_calculation_list(db: AsyncSession, owner_id: int):
        async with db as session:
            result = await session.execute(
                select(models.Calculation)
                .filter(models.Calculation.owner_id == owner_id)
                .order_by(desc(models.Calculation.date))
                .limit(5)
            )
            calculations = result.scalars()
            return calculations

    @staticmethod
    async def update_calculation():
        pass

    @staticmethod
    async def delete_calculation():
        pass


class Assets:
    @staticmethod
    async def create_asset(db: AsyncSession, asset: schemas.Asset):
        async with db as session:
            db_asset = models.Asset(
                currency=asset.currency, sum=asset.sum, calc_id=asset.calc_id
            )
            session.add(db_asset)
            await session.commit()
            await session.refresh(db_asset)
            return db_asset

    @staticmethod
    async def update_asset():
        pass

    @staticmethod
    async def get_assets_list(db: AsyncSession, calc_id: int):
        async with db as session:
            result = await session.execute(
                select(models.Asset)
                .filter(models.Asset.calc_id == calc_id)
                .order_by(models.Asset.id)
            )
            assets = result.scalars()
            return assets

    @staticmethod
    async def delete_asset(db: AsyncSession, asset_id: int):
        async with db as session:
            try:
                asset = await session.get(models.Asset, asset_id)
                await db.delete(asset)
                await db.commit()
            except:
                print("Doesn't exist")  # ??????????????????????????
