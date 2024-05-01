# -*- coding: utf-8 -*-
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards.button_tickers import TICKERS
from keyboards.calculation_keyboards import (
    CalculationKB,
    add_or_calculate_kb,
    choose_currency_kb,
)
from keyboards.common_keyboards import CommonKB
from orm import crud, schemas
from orm.database import get_session
from service.calculator import get_sum, check_ticker

from .states import Calculation

router = Router(name=__name__)


@router.message(F.text == CommonKB.calculation_kb_data)
async def choose_crypto_or_cash(message: types.Message, state: FSMContext):
    await state.set_state(Calculation.base_currency)
    await state.update_data(rates_or_calculation=message.text)
    markup = choose_currency_kb()
    await message.answer(
        text="Choose crypto or cash base asset 👇",
        reply_markup=markup,
    )


@router.message(Calculation.base_currency)
async def handle_calculation_base_currency(message: types.Message, state: FSMContext):
    choice = message.text.upper()
    await state.update_data(base_currency=choice)
    if choice in TICKERS:

        async with get_session() as session:
            new_calc = schemas.Calculation(
                base_currency=choice, owner_id=message.from_user.id
            )
            await crud.Calculations.create_calculation(session, new_calc)

        await message.answer(
            f"You chose {markdown.hbold(choice)} as base currency. Let's continue!",
            parse_mode=ParseMode.HTML,
        )
        await state.clear()
        await state.set_state(Calculation.currency_for_calculation)
        markup = choose_currency_kb()
        await message.answer(
            text="Choose currency for calculation 👇",
            reply_markup=markup,
        )
    else:
        await message.answer(
            f"'{markdown.hbold(message.text)}' is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
        markup = choose_currency_kb()
        await message.answer(
            text="Choose base asset for calculation again 👇",
            reply_markup=markup,
        )


@router.message(Calculation.currency_for_calculation)
async def choose_currency_for_calculation_first(
    message: types.Message, state: FSMContext
):
    choice = message.text.upper()
    await state.update_data(currency_for_calculation=choice)
    ticker_flag = await check_ticker(choice)
    if choice in TICKERS or ticker_flag:
        await message.answer(
            f"You chose {markdown.hbold(choice)} to add into calculation."
        )
        await message.answer("Input amount 👇")
        await state.set_state(Calculation.currency_amount)
    else:
        await message.answer(
            f"'{markdown.hbold(message.text)}' is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
        markup = choose_currency_kb()
        await message.answer(
            text="Choose currency for calculation again 👇",
            reply_markup=markup,
        )


@router.message(Calculation.currency_amount)
async def currency_amount(message: types.Message, state: FSMContext):
    await state.update_data(currency_amount=message.text)
    data = await state.get_data()
    amount = message.text
    amount = amount.replace(",", ".")
    amount.replace(".", "", 1)

    if amount.replace(".", "", 1).isnumeric() and float(amount) < 10**9:
        amount = float(amount)

        async with get_session() as session:
            db_calc = await crud.Calculations.get_last_user_calculation(
                session, owner_id=message.from_user.id
            )
            new_asset = schemas.Asset(
                currency=data.get("currency_for_calculation"),
                sum=amount,
                calc_id=db_calc.id,
            )
            await crud.Assets.create_asset(session, new_asset)  # db_asset =

        await message.answer(
            f"You entered {markdown.hbold(amount)} {markdown.hbold(data.get('currency_for_calculation'))}\
 to add into calculation."
        )
        await state.clear()

        await state.set_state(Calculation.add_or_calculate)
        markup = add_or_calculate_kb()
        await message.answer(
            text="Choose next step 👇",
            reply_markup=markup,
        )
    else:
        await message.answer(
            f"Invalid value. You can input {markdown.hbold('float value less than 10^9')}. Input again 👇"
        )
        await state.set_state(Calculation.currency_amount)


@router.message(F.text == CalculationKB.add_button)
async def add_currency_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Calculation.currency_for_calculation)
    markup = choose_currency_kb()
    await message.answer(
        text="Choose currency for calculation 👇",
        reply_markup=markup,
    )


@router.message(F.text == CalculationKB.calculate_button)
async def calculate_handler(message: types.Message, state: FSMContext):
    await state.clear()
    async with get_session() as session:
        db_calc = await crud.Calculations.get_last_user_calculation(
            session, owner_id=message.from_user.id
        )
        assets_list = await crud.Assets.get_assets_list(session, calc_id=db_calc.id)
        asset_sum = []
        for item in assets_list:
            asset_sum.append((item.currency, item.sum))
        print(asset_sum)
        total = await get_sum(db_calc.base_currency, asset_sum)
        db_calc.total = total
        session.add(db_calc)
        await session.commit()
        await session.refresh(db_calc)
    await message.answer(
        f"Your total budget in base currency is:\n{markdown.hbold(round(total, 6))}\
 {markdown.hbold(db_calc.base_currency)}!"
    )
    await state.clear()
