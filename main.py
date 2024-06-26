# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

# import handlers  # noqa, get handlers for Telegram
from service.routes import root_router
from settings import get_settings

cfg = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    from service.bot import start_telegram

    await start_telegram()
    yield
    logger.info("⛔ Stopping application")


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
