from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

CRYPTO_TICKERS = [
    "BTC",
    "ETH",
    "TWT",
    "SOL",
    "TON",
    "APT",
]
CASH_TICKERS = [
    "USD",
    "EUR",
    "RUB",
    "TRY",
    "CNY",
    "KZT",
]
TICKERS = CRYPTO_TICKERS + CASH_TICKERS


class CalculationKB:
    crypto_kb_data = "Crypto"
    cash_kb_data = "Cash"


def crypto_or_currency() -> ReplyKeyboardMarkup:
    crypto_button = KeyboardButton(text=CalculationKB.crypto_kb_data)
    cash_button = KeyboardButton(text=CalculationKB.cash_kb_data)
    buttons_rows = [[crypto_button], [cash_button]]
    markup = ReplyKeyboardMarkup(
        keyboard=buttons_rows, resize_keyboard=True, one_time_keyboard=True
    )
    return markup


def crypto_kb() -> ReplyKeyboardMarkup:
    tickers = CRYPTO_TICKERS
    buttons_row = [KeyboardButton(text=num) for num in tickers]
    buttons_rows = []
    for i, button in enumerate(buttons_row):
        if not i % 2:
            buttons_rows.append([])
        buttons_rows[-1].append(button)
    markup = ReplyKeyboardMarkup(
        keyboard=buttons_rows, resize_keyboard=True, one_time_keyboard=True
    )
    return markup


def cash_kb() -> ReplyKeyboardMarkup:
    tickers = CASH_TICKERS
    buttons_row = [KeyboardButton(text=num) for num in tickers]
    buttons_rows = []
    for i, button in enumerate(buttons_row):
        if not i % 2:
            buttons_rows.append([])
        buttons_rows[-1].append(button)
    markup = ReplyKeyboardMarkup(
        keyboard=buttons_rows, resize_keyboard=True, one_time_keyboard=True
    )
    return markup


def choose_currency_kb() -> ReplyKeyboardMarkup:
    tickers = TICKERS
    buttons_row = [KeyboardButton(text=num) for num in tickers]
    buttons_rows = []
    for i, button in enumerate(buttons_row):
        if not i % 3:
            buttons_rows.append([])
        buttons_rows[-1].append(button)
    markup = ReplyKeyboardMarkup(
        keyboard=buttons_rows, resize_keyboard=True, one_time_keyboard=True
    )
    return markup
