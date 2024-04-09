# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from loguru import logger

from bot import telegram_router
from orm import crud, schemas
from orm.database import get_session
from routes import root


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@telegram_router.message(Command("calc"))
async def calc_assets(message: Message) -> None:
    await message.answer(
        f"We are ready to create assets calculation for user {message.from_user.id}"
    )


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    async with get_session() as session:
        new_user = schemas.User(
            id=message.from_user.id, name=message.from_user.full_name
        )
        db_user = await crud.Users.get_user(session, user_id=new_user.id)
        if db_user is None:
            await crud.Users.create_user(session, new_user)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@telegram_router.message(F.text.lower() == "echo")
async def echo(message: types.Message) -> None:
    try:
        # await message.send_copy(chat_id=message.chat.id)
        await message.answer("Echo👻")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@telegram_router.message(F.text.lower() == "ping")
async def ping(message: types.Message) -> None:
    try:
        await message.answer("PONG🏓")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


# @telegram_router.message(F.text.lower() == "fastapi")
@telegram_router.message(Command("fastapi"))
async def hello_fastapi(message: types.Message) -> None:
    try:
        response_dict = await root()
        res = response_dict["message"]
        await message.answer(res)

        # TEST GET USER
        # async with get_session() as session:
        #     db_user = await crud.Users.get_user(session, user_id=message.from_user.id)
        # print(db_user.name)

        # TEST CREATE USER
        # async with get_session() as session:
        #     new_user = schemas.User(id=30000000, name="Create Test 2")
        #     db_user = await crud.Users.get_user(session, user_id=new_user.id)
        #     if db_user is None:
        #         db_user = await crud.Users.create_user(session, new_user)
        # await message.answer(
        #     f"Additionally, I get your username from DB: {db_user.name}"
        # )

        # TEST CREATE CALCULATION
        # async with get_session() as session:
        #     new_calc = schemas.Calculation(
        #         base_currency="AED", owner_id=message.from_user.id
        #     )
        #     db_calc = await crud.Calculations.create_calculation(session, new_calc)
        #     await message.answer(
        #         f"Additionally, I create new calculation in DB: {db_calc.id}, {db_calc.base_currency} from user {db_calc.owner_id}"
        #     )

        # # TEST CREATE ASSET
        # async with get_session() as session:
        #     new_asset = schemas.Asset(
        #         currency="CYN", sum=999.99997876543221, calc_id=db_calc.id
        #     )
        #     db_asset = await crud.Assets.create_asset(session, new_asset)
        #     await message.answer(
        #         f"Additionally, I create new asset in DB: {db_asset.id}, {db_asset.currency} from calc_id {db_asset.calc_id}"
        #     )

        # TEST GET CALCULATION LIST
        # async with get_session() as session:
        #     db_calc = await crud.Calculations.get_calculation_list(
        #         session, owner_id=message.from_user.id
        #     )
        # for item in db_calc:
        #     await message.answer(f"Calculation id{item.id}: {item.base_currency}")

        # TEST GET ASSETS LIST
        # async with get_session() as session:
        #     db_asset = await crud.Assets.get_assets_list(session, calc_id=1)
        # for item in db_asset:
        #     await message.answer(f"Asset id{item.id}: {item.currency}")

        # TEST DELETE ASSETS
        # async with get_session() as session:
        #     await crud.Assets.delete_asset(session, asset_id=8)
        # await message.answer(f"Asset deleted id8")

    except Exception as e:
        print(e)
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")
