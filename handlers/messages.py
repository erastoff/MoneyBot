# -*- coding: utf-8 -*-
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils import markdown
from aiogram.utils.markdown import hbold
from loguru import logger

from handlers.states import Calculation
from keyboards.common_keyboards import (
    ButtonText,
    get_actions_kb,
    get_on_help_kb,
    get_on_start_kb,
)
from orm import crud, schemas
from orm.database import get_session
from service.redis_pool import pool

router = Router(name=__name__)


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"🆔 Your ID: {message.from_user.id}")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        new_user = schemas.User(
            id=message.from_user.id, name=message.from_user.full_name
        )
        db_user = await crud.Users.get_user(session, user_id=new_user.id)
        if db_user is None:
            await crud.Users.create_user(session, new_user)
    await state.set_state(Calculation.rates_or_calculation)
    await message.answer(f"🖖🏼 Hello, {hbold(message.from_user.full_name)}!")
    await message.answer(
        """✅ In the MoneyBot you can get current exchange rate\
 and evaluate your multicurrency assets."""
    )
    markup = get_on_start_kb()
    await message.answer(
        text="👇 Push the appropriate button below.", reply_markup=markup
    )


@router.message(Command("money"))
async def calc_assets(message: Message, state: FSMContext) -> None:
    await state.set_state(Calculation.rates_or_calculation)
    markup = get_on_start_kb()
    await message.answer(
        text="👇 Push the appropriate button below to get rates or create new calculation.",
        reply_markup=markup,
    )


@router.message(F.text.lower() == "echo")
async def echo(message: types.Message) -> None:
    try:
        await message.answer("Echo👻")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@router.message(F.text.lower() == "ping")
async def ping(message: types.Message) -> None:
    try:
        await message.answer("PONG🏓")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@router.message(Command("fastapi"))
async def hello_fastapi(message: types.Message) -> None:
    try:
        await message.answer("There was fastapi test. But not now...")
        await message.answer("Now we try to set up key - value into redis storage ...")

        await pool.set("key", "fastapi_command_redis", 60)

        await message.answer("Result ...")
        value = await pool.get("key")
        await message.answer(f"{markdown.hbold(value.decode())}")

    except Exception as e:
        print(e)
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")


@router.message(Command("info", prefix="!/"))
async def handle_info_command(message: types.Message):
    tg_channel_btn = InlineKeyboardButton(
        text="🔉Channel", url="https://t.me/erast_off"
    )
    git_btn = InlineKeyboardButton(text="🔉GitHub", url="https://github.com/erastoff")
    vk_btn = InlineKeyboardButton(text="🔉VK", url="https://vk.com")
    row1 = [tg_channel_btn]
    row2 = [git_btn, vk_btn]
    rows = [row1, row2]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(text="Links to resources:", reply_markup=markup)


@router.message(F.text == ButtonText.WHATS_NEXT)
@router.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an {echo} bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any",
                ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_on_help_kb(),
    )


@router.message(Command("more", prefix="!/"))
async def handle_more(message: types.Message):
    markup = get_actions_kb()
    await message.answer(
        text="Choose action:",
        reply_markup=markup,
    )


# @telegram_router.callback_query(F.data == CallBacks.exchange_cb_data)
# async def exchange_cb_handle(callback_query: CallbackQuery):
#     # if callback_query.data == CallBacks.exchange_cb_data:
#     print(CallBacks.exchange_cb_data)
#     await callback_query.answer()
#     # await callback_query.answer(text="/fastapi")
#     await bot.send_message(callback_query.from_user.id, "/fastapi")
#     # elif callback_query.data == CallBacks.calculation_cb_data:
#     #     await callback_query.message.answer("/choose_currency")
#
#
# @telegram_router.callback_query(F.data == CallBacks.calculation_cb_data)
# async def calculation_cb_handle(callback_query: CallbackQuery):
#     print(CallBacks.calculation_cb_data)
#     await callback_query.answer()
#     # await callback_query.answer(text="/choose_currency")
#     await bot.send_message(callback_query.from_user.id, "/choose_currency")
