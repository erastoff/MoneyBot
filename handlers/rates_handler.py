# -*- coding: utf-8 -*-
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from handlers.states import Calculation
from keyboards.calculation_keyboards import crypto_kb, TICKERS
from keyboards.common_keyboards import CommonKB
from service.binance_api import fetch_binance_rates, set_cache_binance_rates
from service.redis_pool import pool

router = Router(name=__name__)


@router.message(F.text == CommonKB.exchange_kb_data)
async def choose_crypto_or_cash(message: types.Message, state: FSMContext):
    await state.update_data(rates_or_calculation=message.text)
    await state.set_state(Calculation.exchange_rates)
    markup = crypto_kb()
    await message.answer(
        text="Choose crypto asset pair USDT 👇",
        reply_markup=markup,
    )


@router.message(Calculation.exchange_rates)
async def handle_calculation_base_currency(message: types.Message, state: FSMContext):
    await state.update_data(exchange_rates=message.text)
    if message.text in TICKERS:
        await message.answer(
            f"You chose {markdown.hbold(message.text)}!",
            parse_mode=ParseMode.HTML,
        )
        requested_pair = message.text + "USDT"
        await set_cache_binance_rates()
        try:
            response_value = await pool.get(requested_pair)
            if not response_value:
                raise KeyError
            await message.answer(
                f"Current rate for {markdown.hbold(requested_pair)} pair:\
 {markdown.hbold(response_value.decode())}"
            )
        except KeyError:
            await message.answer(
                f"Unfortunately, there is no {markdown.hbold(requested_pair)}\
 pair on the Binance data"
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
