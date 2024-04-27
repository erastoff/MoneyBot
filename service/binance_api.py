# -*- coding: utf-8 -*-
import asyncio

from binance import Client

from settings import get_settings

from service.redis_pool import pool

cfg = get_settings()


async def fetch_binance_rates():
    client = Client(cfg.binance_api_key, cfg.binance_secret_key)
    tickers_raw = client.get_all_tickers()
    tickers = {}
    for item in tickers_raw:
        tickers[item["symbol"]] = item["price"]
    # print(tickers)
    return tickers


async def set_cache_binance_rates():
    check_btcusdt = await pool.get("BTCUSDT")
    if not check_btcusdt:
        print("CHECK BTCUSDT NOT PASSED")
        tickers = await fetch_binance_rates()
        for key, value in tickers.items():
            await pool.set(key, value, 60 * 60)


async def main():
    await set_cache_binance_rates()


if __name__ == "__main__":
    asyncio.run(main())
