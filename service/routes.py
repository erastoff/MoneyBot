# -*- coding: utf-8 -*-s
from typing import Annotated

from aiogram import types
from fastapi import APIRouter, Depends, Header
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from keyboards.button_tickers import TICKERS
from .binance_api import set_cache_binance_rates
from .bot import bot, dp
from orm import crud
from orm.database import get_session
from settings import get_settings
from .redis_pool import pool

cfg = get_settings()

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


class Rate(BaseModel):
    pair: str
    price: float


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = await crud.Users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@root_router.get("/rates/{pair}")
async def get_pair_rates(pair: str):
    if pair in TICKERS:
        raise HTTPException(status_code=404, detail=f"{pair} not found!")
    await set_cache_binance_rates()
    response_value = await pool.get(pair)
    if not response_value:
        raise HTTPException(status_code=404, detail=f"{pair} not found!")
    tmp = Rate(pair=pair, price=response_value)
    return tmp


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
