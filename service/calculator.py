# -*- coding: utf-8 -*-
from keyboards.button_tickers import CASH_TICKERS, CRYPTO_TICKERS
from service.binance_api import set_cache_binance_rates
from service.currencylayer_api import set_cache_cash_rates
from service.redis_pool import pool


async def base_currency_rate(base_currency: str) -> float:
    if base_currency == "USD":
        return 1
    if base_currency in CRYPTO_TICKERS:
        cur_base_rate = await pool.get(base_currency + "USDT")
        cur_base_rate = 1 / float(cur_base_rate)
        return cur_base_rate
    if base_currency in CASH_TICKERS:
        cur_base_rate = await pool.get("USD" + base_currency)
        cur_base_rate = float(cur_base_rate)
        return cur_base_rate


async def get_sum(base_currency: str, asset_sum: list) -> float:
    await set_cache_binance_rates()
    await set_cache_cash_rates()
    total_sum = float(0)
    base_cur_rate = await base_currency_rate(base_currency)
    for asset, amount in asset_sum:
        asset_flag = await check_ticker(asset)
        if asset == base_currency:
            total_sum += float(amount)
        elif asset == "USD":
            cur_asset_rate = 1
            cur_asset_rate_base = float(base_cur_rate) / float(cur_asset_rate)
            total_sum += cur_asset_rate_base * float(amount)
        elif asset_flag == "crypto":
            cur_asset_rate = await pool.get(asset + "USDT")
            cur_asset_rate = 1 / float(cur_asset_rate)
            cur_asset_rate_base = float(base_cur_rate) / float(cur_asset_rate)
            total_sum += float(amount) * cur_asset_rate_base
        elif asset_flag == "cash":
            cur_asset_rate = await pool.get("USD" + asset)
            cur_asset_rate_base = float(base_cur_rate) / float(cur_asset_rate)
            total_sum += cur_asset_rate_base * float(amount)
    return total_sum


async def check_ticker(message_text: str):
    await set_cache_binance_rates()
    if await pool.get(message_text + "USDT"):
        return "crypto"
    await set_cache_cash_rates()
    if await pool.get("USD" + message_text):
        return "cash"
    return None
