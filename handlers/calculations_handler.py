from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

# from bot import telegram_router
from keyboards.calculation_keyboards import (
    crypto_or_currency,
    cash_kb,
    choose_currency_kb,
    crypto_kb,
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
    markup = crypto_or_currency()
    await message.answer(
        text="Choose crypto or cash base asset:",
        reply_markup=markup,
    )
    await state.clear()


@router.message(F.text == CalculationKB.crypto_kb_data)
async def crypto_assets(message: types.Message, state: FSMContext):
    await state.set_state(Calculation.base_currency)
    markup = crypto_kb()
    await message.answer(
        text="Choose crypto base asset for calculation:",
        reply_markup=markup,
    )


@router.message(F.text == CalculationKB.cash_kb_data)
async def cash_assets(message: types.Message, state: FSMContext):
    await state.set_state(Calculation.base_currency)
    markup = cash_kb()
    await message.answer(
        text="Choose cash base asset for calculation:",
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
            f"You chose {markdown.hbold(message.text)} as base currency! Let's continue!",
            parse_mode=ParseMode.HTML,
        )
        await state.clear()
    else:
        await message.answer(
            f"{markdown.hbold(message.text)} is invalid ticker!",
            parse_mode=ParseMode.HTML,
        )


# @telegram_router.message(Command("choose_currency", prefix="!/"))
# async def choose_currency(message: types.Message):
#     markup = choose_currency_kb()
#     await message.answer(
#         text="Choose currency:",
#         reply_markup=markup,
#     )
