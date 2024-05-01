# -*- coding: utf-8 -*-
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from handlers.states import Rates
from keyboards.rates_keyboards import (
    crypto_kb,
    crypto_or_currency_kb,
    cash_kb,
    RatesKB,
)
from keyboards.button_tickers import CRYPTO_TICKERS, CASH_TICKERS
from keyboards.common_keyboards import CommonKB
from service.binance_api import set_cache_binance_rates
from service.currencylayer_api import set_cache_cash_rates
from service.redis_pool import pool

from settings import Settings, get_settings

cfg: Settings = get_settings()

router = Router(name=__name__)


@router.message(F.text == CommonKB.exchange_kb_data)
async def choose_crypto_or_cash(message: types.Message, state: FSMContext):
    await state.update_data(rates_or_calculation=message.text)
    markup = crypto_or_currency_kb()
    await message.answer(
        text="Choose crypto or cash asset 👇",
        reply_markup=markup,
    )
    await state.clear()


@router.message(F.text == RatesKB.crypto_kb_data)
async def crypto_assets(message: types.Message, state: FSMContext):
    await state.set_state(Rates.exchange_asset_crypto)
    await state.update_data(exchange_asset_type="crypto")
    markup = crypto_kb()
    await message.answer(
        text="Choose crypto asset to fetch exchange rate 👇",
        reply_markup=markup,
    )
    await set_cache_binance_rates()


@router.message(F.text == RatesKB.cash_kb_data)
async def cash_assets(message: types.Message, state: FSMContext):
    await state.set_state(Rates.exchange_asset_cash)
    await state.update_data(exchange_asset_type="cash")
    markup = cash_kb()
    await message.answer(
        text="Choose cash asset to fetch exchange rate 👇",
        reply_markup=markup,
    )
    await set_cache_cash_rates()


@router.message(Rates.exchange_asset_crypto)
async def handle_crypto_exchange_rate(message: types.Message, state: FSMContext):
    await state.update_data(exchange_rates=message.text)
    if message.text in CRYPTO_TICKERS:
        await message.answer(
            f"You chose {markdown.hbold(message.text)}!",
            parse_mode=ParseMode.HTML,
        )
        requested_pair = message.text + "USDT"
        try:
            response_value = await pool.get(requested_pair)
            response_value = round(float(response_value.decode()), 6)
            if not response_value:
                raise KeyError
            await message.answer(
                f"Current rate for {markdown.hbold(requested_pair)} pair: {markdown.hbold(response_value)}"
            )
        except KeyError:
            await message.answer(
                f"Unfortunately, there is no {markdown.hbold(requested_pair)} pair on the Binance data"
            )
        await state.clear()
    else:
        await message.answer(
            f"'{markdown.hbold(message.text)}' is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
        markup = crypto_kb()
        await message.answer(
            text="Choose crypto asset to get exchange rate again 👇",
            reply_markup=markup,
        )


@router.message(Rates.exchange_asset_cash)
async def handle_cash_exchange_rate(message: types.Message, state: FSMContext):
    await state.update_data(exchange_rates=message.text)
    if message.text in CASH_TICKERS:
        await message.answer(
            f"You chose {markdown.hbold(message.text)}!",
            parse_mode=ParseMode.HTML,
        )
        requested_pair = "USD" + message.text
        print("CASH PAIR: ", requested_pair)
        try:
            response_value = await pool.get(requested_pair)
            response_value = round(float(response_value.decode()), 6)
            if not response_value:
                raise KeyError
            await message.answer(
                f"Current rate for {markdown.hbold(requested_pair)} pair: {markdown.hbold(response_value)}"
            )
        except KeyError:
            await message.answer(
                f"Unfortunately, there is no {markdown.hbold(requested_pair)} pair on the CurrencyLayer data"
            )
        await state.clear()
    else:
        await message.answer(
            f"'{markdown.hbold(message.text)}' is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
        markup = crypto_kb()
        await message.answer(
            text="Choose crypto asset to get exchange rate again 👇",
            reply_markup=markup,
        )
