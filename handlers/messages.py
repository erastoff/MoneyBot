# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from fastapi import Depends
from loguru import logger
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message

from bot import telegram_router
from routes import root


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@telegram_router.message(Command("calc"))
async def cmd_id(message: Message) -> None:
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


@telegram_router.message(F.text.lower() == "fastapi")
async def hello_fastapi(message: types.Message) -> None:
    try:
        response_dict = await root()
        res = response_dict["message"]
        await message.answer(res)
        await message.answer("Additionally...")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")
