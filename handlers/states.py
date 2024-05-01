# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup


class Calculation(StatesGroup):
    add_or_calculate = State()
    base_currency = State()
    currency_amount = State()
    currency_for_calculation = State()
    rates_or_calculation = State()


class Rates(StatesGroup):
    exchange_asset = State()
    rates_or_calculation = State()
