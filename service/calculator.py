# -*- coding: utf-8 -*-
from keyboards.calculation_keyboards import CRYPTO_TICKERS, CASH_TICKERS
from service.redis_pool import pool
from service.binance_api import set_cache_binance_rates
from service.currencylayer_api import set_cache_cash_rates


async def base_currency_rate(base_currency: str) -> float:
    if base_currency == "USD":
        return 1
    if base_currency in CRYPTO_TICKERS:
        cur_base_rate = await pool.get(base_currency + "USDT")
        cur_base_rate = float(cur_base_rate)
        return cur_base_rate
    if base_currency in CASH_TICKERS:
        cur_base_rate = await pool.get("USD" + base_currency)
        cur_base_rate = float(cur_base_rate)
        return 1 / cur_base_rate


async def get_sum(base_currency: str, asset_sum: dict) -> float:
    await set_cache_binance_rates()
    await set_cache_cash_rates()
    total_sum = float(0)
    base_cur_rate = await base_currency_rate(base_currency)
    for asset, amount in asset_sum.items():
        if asset == base_currency:
            total_sum += float(amount)
        elif asset == "USD":
            cur_asset_rate = 1

            cur_asset_rate_base = float(cur_asset_rate) / float(base_cur_rate)
            total_sum += cur_asset_rate_base * float(amount)
        elif asset in CRYPTO_TICKERS:
            # await set_cache_binance_rates()
            cur_asset_rate = await pool.get(asset + "USDT")
            # base_cur_rate = await base_currency_rate(base_currency)
            cur_asset_rate_base = float(cur_asset_rate) / float(base_cur_rate)
            total_sum += cur_asset_rate_base * float(amount)
        elif asset in CASH_TICKERS:
            # await set_cache_cash_rates()
            cur_asset_rate = await pool.get("USD" + asset)
            # base_cur_rate = await base_currency_rate(base_currency)
            cur_asset_rate_base = float(cur_asset_rate) / float(base_cur_rate)
            total_sum += cur_asset_rate_base * float(amount)
    return total_sum
