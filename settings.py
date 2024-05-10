# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import final

from decouple import config
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".prod.env", ".dev.env"),  # first search .dev.env, then .prod.env
        env_file_encoding="utf-8",
    )

    debug: bool = config("DEBUG")
    redis_url: str = f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT')}/0"
    bot_token: str = config("HTTP_API")
    base_webhook_url: str = "https://erastov-store.ru:8443"
    webhook_path: str = "/path/"
    telegram_my_token: str = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Additional security token for webhook
    )
    db_name: str = config("DATABASE_NAME")
    db_user: str = config("DATABASE_USER")
    db_password: str = config("DATABASE_PASSWORD")
    db_host: str = config("DATABASE_HOST")
    db_port: int = config("DATABASE_PORT")
    db_uri: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    currencylayer_api_key: str = config("CURRENCYLAYER_API_KEY")
    currencylayer_api_url: str = config("CURRENCYLAYER_API_URL")

    binance_api_key: str = config("BINANCE_API_KEY")
    binance_secret_key: str = config("BINANCE_SECRET_KEY")


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
