from aiogram.fsm.state import StatesGroup, State


class Calculation(StatesGroup):
    add_or_calculate = State()
    base_currency = State()
    currency_amount = State()
    currency_for_calculation = State()
    rates_or_calculation = State()
