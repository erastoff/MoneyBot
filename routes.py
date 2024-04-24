# -*- coding: utf-8 -*-
from typing import Annotated

from aiogram import types
from fastapi import APIRouter, Depends, Header
from loguru import logger
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from bot import bot, dp
from orm import crud
from orm.database import get_session
from settings import get_settings

cfg = get_settings()

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = await crud.Users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@root_router.post(cfg.webhook_path)
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> None | dict:
    """Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != cfg.telegram_my_token:
        logger.error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)
