# -*- coding: utf-8 -*-
import asyncio
import aiohttp

from settings import get_settings
from service.redis_pool import pool

cfg = get_settings()


async def fetch_exchange_rates():
    access_key = cfg.currencylayer_api_key
    params = {
        "access_key": access_key,
        "source": "USD",
        "format": "1",
    }
    url = cfg.currencylayer_api_url

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data
            else:
                print("Error encountered fetching the rates:", response.status)
                return None


async def set_cache_cash_rates():
    check_usdrub = await pool.get("USDRUB")
    if not check_usdrub:
        print("CHECK USDRUB NOT PASSED")
        tickers = await fetch_exchange_rates()
        for key, value in tickers["quotes"].items():
            await pool.set(key, value, 24 * 60 * 60)


async def main():
    await set_cache_cash_rates()
    exchange_rate1 = await pool.get("USDRUB")
    exchange_rate2 = await pool.get("USDAED")
    print("USDRUB", float(exchange_rate1), "USDAED", float(exchange_rate2))


if __name__ == "__main__":
    asyncio.run(main())
