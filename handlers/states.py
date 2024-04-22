from aiogram.fsm.state import StatesGroup, State


class Calculation(StatesGroup):
    rates_or_calculation = State()
    base_currency = State()
