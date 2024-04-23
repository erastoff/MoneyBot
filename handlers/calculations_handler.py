from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards.calculation_keyboards import (
    crypto_or_currency_kb,
    cash_kb,
    choose_currency_kb,
    crypto_kb,
    add_or_calculate_kb,
)
from keyboards.common_keyboards import CommonKB
from keyboards.calculation_keyboards import CalculationKB, TICKERS
from orm import schemas, crud
from orm.database import get_session

from .states import Calculation

router = Router(name=__name__)


@router.message(F.text == CommonKB.calculation_kb_data)
async def choose_crypto_or_cash(message: types.Message, state: FSMContext):
    await state.update_data(rates_or_calculation=message.text)
    markup = crypto_or_currency_kb()
    await message.answer(
        text="Choose crypto or cash base asset 👇",
        reply_markup=markup,
    )
    await state.clear()


@router.message(F.text == CalculationKB.crypto_kb_data)
async def crypto_assets(message: types.Message, state: FSMContext):
    await state.set_state(Calculation.base_currency)
    markup = crypto_kb()
    await message.answer(
        text="Choose crypto base asset for calculation 👇",
        reply_markup=markup,
    )


@router.message(F.text == CalculationKB.cash_kb_data)
async def cash_assets(message: types.Message, state: FSMContext):
    await state.set_state(Calculation.base_currency)
    markup = cash_kb()
    await message.answer(
        text="Choose cash base asset for calculation 👇",
        reply_markup=markup,
    )


@router.message(Calculation.base_currency)
async def handle_calculation_base_currency(message: types.Message, state: FSMContext):
    await state.update_data(base_currency=message.text)
    # await state.set_state(Calculation.base_currency)
    if message.text in TICKERS:
        # Calculation DB instance creation
        async with get_session() as session:
            new_calc = schemas.Calculation(
                base_currency=message.text, owner_id=message.from_user.id
            )
            await crud.Calculations.create_calculation(session, new_calc)
        await message.answer(
            f"You chose {markdown.hbold(message.text)} as base currency. Let's continue!",
            parse_mode=ParseMode.HTML,
        )
        await state.clear()
    else:
        await message.answer(
            f"{markdown.hbold(message.text)} is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )
    await state.set_state(Calculation.currency_for_calculation)
    markup = choose_currency_kb()
    await message.answer(
        text="Choose currency for calculation 👇",
        reply_markup=markup,
    )


@router.message(Calculation.currency_for_calculation)
async def choose_currency_for_calculation_first(
    message: types.Message, state: FSMContext
):
    await state.update_data(currency_for_calculation=message.text)
    await message.answer(
        f"You choose {markdown.hbold(message.text)} to add into calculation."
    )
    await message.answer("Input amount 👇")
    await state.set_state(Calculation.currency_amount)

    # markup = choose_currency_kb()
    # await message.answer(
    #     text="What's next:",
    #     reply_markup=markup,
    # )


@router.message(Calculation.currency_amount)
async def currency_amount(message: types.Message, state: FSMContext):
    await state.update_data(currency_amount=message.text)
    data = await state.get_data()
    amount = message.text

    if amount.replace(".", "", 1).isnumeric():

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
            db_asset = await crud.Assets.create_asset(session, new_asset)

        await message.answer(
            f"You choose {markdown.hbold(message.text)} to add into calculation."
        )
        await state.clear()
    else:
        await message.answer("Invalid value. Input again 👇")

    await state.set_state(Calculation.add_or_calculate)
    # await message.answer("Choose next step 👇")
    markup = add_or_calculate_kb()
    await message.answer(
        text="Choose next step 👇",
        reply_markup=markup,
    )


@router.message(F.text == CalculationKB.add_button)
async def add_currency_handler(message: types.Message, state: FSMContext):
    # await state.update_data(add_currency=message.text)
    await state.clear()
    await state.set_state(Calculation.currency_for_calculation)
    markup = choose_currency_kb()
    await message.answer(
        text="Choose currency for calculation 👇",
        reply_markup=markup,
    )


@router.message(F.text == CalculationKB.calculate_button)
async def calculate_handler(message: types.Message, state: FSMContext):
    # await state.update_data(add_currency=message.text)
    await state.clear()

    async with get_session() as session:
        db_calc = await crud.Calculations.get_last_user_calculation(
            session, owner_id=message.from_user.id
        )
        assets_list = await crud.Assets.get_assets_list(session, calc_id=db_calc.id)
        total = float(0)
        for item in assets_list:
            total += float(item.sum)
        db_calc.total = total  ## TO DO: SET TOTAL IN DB
    await message.answer(
        f"You total {markdown.hbold(total)} {markdown.hbold(db_calc.base_currency)}!"
    )

    # await message.answer(
    #     text="Choose currency for calculation 👇",
    #     reply_markup=markup,
    # )
