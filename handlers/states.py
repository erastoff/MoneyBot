# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup


class Calculation(StatesGroup):
    add_or_calculate = State()
    base_currency = State()
    currency_amount = State()
    currency_for_calculation = State()
    exchange_rates = State()
    rates_or_calculation = State()
