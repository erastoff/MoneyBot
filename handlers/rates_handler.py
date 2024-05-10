# -*- coding: utf-8 -*-
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from handlers.states import Rates
from keyboards.common_keyboards import CommonKB
from keyboards.rates_keyboards import RatesKB, cash_kb, crypto_kb, crypto_or_currency_kb
from service.binance_api import set_cache_binance_rates
from service.calculator import check_ticker
from service.currencylayer_api import set_cache_cash_rates
from service.redis_pool import pool
from settings import Settings, get_settings

cfg: Settings = get_settings()

router = Router(name=__name__)


@router.message(F.text == CommonKB.exchange_kb_data)
async def choose_crypto_or_cash(message: types.Message, state: FSMContext):
    await state.update_data(rates_or_calculation=message.text)
    await state.set_state(Rates.crypto_or_cash)
    markup = crypto_or_currency_kb()
    await message.answer(
        text="👇 Choose crypto or cash asset.",
        reply_markup=markup,
    )
    # await state.clear()


@router.message(F.text == RatesKB.crypto_kb_data)
async def crypto_assets(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Rates.exchange_asset)
    await state.update_data(exchange_asset_type="crypto")
    markup = crypto_kb()
    await message.answer(
        text="👇 Choose or enter crypto asset to fetch exchange rate.",
        reply_markup=markup,
    )
    await set_cache_binance_rates()


@router.message(F.text == RatesKB.cash_kb_data)
async def cash_assets(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Rates.exchange_asset)
    await state.update_data(exchange_asset_type="cash")
    markup = cash_kb()
    await message.answer(
        text="👇 Choose or enter cash asset to fetch exchange rate.",
        reply_markup=markup,
    )
    await set_cache_cash_rates()


@router.message(Rates.crypto_or_cash)
async def random_crypto_or_cash_text_handler(message: types.Message, state: FSMContext):
    markup = crypto_or_currency_kb()
    await message.answer(
        text="🙏 Choose or enter crypto asset to fetch exchange rate, please.",
        reply_markup=markup,
    )


@router.message(Rates.exchange_asset)
async def handle_exchange_rate(message: types.Message, state: FSMContext):
    choice = message.text.upper()
    await state.update_data(exchange_rates=choice)
    ticker_flag = await check_ticker(choice)
    if ticker_flag or choice == "USD":
        await message.answer(
            f"💲 You chose {markdown.hbold(choice)}!",
            parse_mode=ParseMode.HTML,
        )
        if ticker_flag == "cash":
            requested_pair = "USD" + choice
        elif ticker_flag == "crypto":
            requested_pair = choice + "USDT"
        else:
            requested_pair = "USDRUB"
        try:
            response_value = await pool.get(requested_pair)
            response_value = round(float(response_value.decode()), 6)
            if not response_value:
                raise KeyError
            await message.answer(
                f"💱 Current rate for {markdown.hbold(requested_pair)} pair:\n{markdown.hbold(response_value)}"
            )
        except KeyError:
            await message.answer(
                f"🙈 Unfortunately, there is no {markdown.hbold(requested_pair)} pair on the Binance data."
            )
        await state.clear()
        await message.answer(
            f"↩️ Use command {markdown.text('/money')} to return to start menu."
        )
    else:
        await message.answer(
            f"🙈 '{markdown.hbold(message.text)}' is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
        data = await state.get_data()
        markup = crypto_kb() if data["exchange_asset_type"] == "crypto" else cash_kb()
        await message.answer(
            text=f"👇 Choose or enter {data['exchange_asset_type']} asset to get exchange rate again.",
            reply_markup=markup,
        )
