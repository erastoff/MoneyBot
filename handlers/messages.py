# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from fastapi import Depends
from loguru import logger
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import telegram_router
from orm import crud
from orm.database import get_session
from routes import root, read_user


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

        async with get_session() as session:
            db_user = await crud.Users.get_user(session, user_id=message.from_user.id)
        print(db_user.name)
        res = response_dict["message"]
        await message.answer(res)
        await message.answer(
            f"Additionally, I get your username from DB: {db_user.name}"
        )
    except Exception as e:
        print(e)
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")
