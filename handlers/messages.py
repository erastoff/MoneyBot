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

        # TEST GET USER
        # async with get_session() as session:
        #     db_user = await crud.Users.get_user(session, user_id=message.from_user.id)
        # print(db_user.name)

        # TEST CREATE USER
        async with get_session() as session:
            new_user = schemas.User(id=30000000, name="Create Test 2")
            db_user = await crud.Users.get_user(session, user_id=new_user.id)
            if db_user is None:
                db_user = await crud.Users.create_user(session, new_user)

        await message.answer(res)
        await message.answer(
            f"Additionally, I get your username from DB: {db_user.name}"
        )
    except Exception as e:
        print(e)
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")
