# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final
from decouple import config


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".prod.env", ".dev.env"),  # first search .dev.env, then .prod.env
        env_file_encoding="utf-8",
    )

    debug: bool = config("DEBUG")
    redis_url: str = f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT')}/0"
    bot_token: str = config("HTTP_API")
    base_webhook_url: str = "https://0598cb9f3c267b.lhr.life"
    webhook_path: str = "/"
    telegram_my_token: str = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Additional security token for webhook
    )


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
