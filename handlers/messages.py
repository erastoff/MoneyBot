# -*- coding: utf-8 -*-
__author__ = "erastoff (yury.erastov@gmail.com)"

from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.utils import markdown
from aiogram.utils.markdown import hbold
from loguru import logger

from bot import telegram_router, bot
from handlers.states import Calculation
from orm import crud, schemas
from orm.database import get_session
from routes import root


from keyboards.common_keyboards import (
    ButtonText,
    get_on_help_kb,
    get_actions_kb,
    get_on_start_kb,
)


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@telegram_router.message(Command("calc"))
async def calc_assets(message: Message) -> None:
    await message.answer(
        f"We are ready to create assets calculation for user {message.from_user.id}"
    )


@telegram_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        new_user = schemas.User(
            id=message.from_user.id, name=message.from_user.full_name
        )
        db_user = await crud.Users.get_user(session, user_id=new_user.id)
        if db_user is None:
            await crud.Users.create_user(session, new_user)
    # await state.set_state(Calculation.rates_or_calculation)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    await message.answer(
        """In the MoneyBot you can get current exchange rate and evaluate your multicurrency assets. Push the appropriate button below. 👇"""
    )
    markup = get_on_start_kb()
    await message.answer(text="Choose action:", reply_markup=markup)


@telegram_router.message(F.text.lower() == "echo")
async def echo(message: types.Message) -> None:
    try:
        # await message.send_copy(chat_id=message.chat.id)
        await message.answer("Echo👻")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@telegram_router.message(F.text.lower() == "ping")
async def ping(message: types.Message) -> None:
    try:
        await message.answer("PONG🏓")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


# @telegram_router.message(F.text.lower() == "fastapi")
@telegram_router.message(Command("fastapi"))
async def hello_fastapi(message: types.Message) -> None:
    try:
        response_dict = await root()
        res = response_dict["message"]
        await message.answer(res)

        # TEST GET USER
        # async with get_session() as session:
        #     db_user = await crud.Users.get_user(session, user_id=message.from_user.id)
        # print(db_user.name)

        # TEST CREATE USER
        # async with get_session() as session:
        #     new_user = schemas.User(id=30000000, name="Create Test 2")
        #     db_user = await crud.Users.get_user(session, user_id=new_user.id)
        #     if db_user is None:
        #         db_user = await crud.Users.create_user(session, new_user)
        # await message.answer(
        #     f"Additionally, I get your username from DB: {db_user.name}"
        # )

        # TEST CREATE CALCULATION
        # async with get_session() as session:
        #     new_calc = schemas.Calculation(
        #         base_currency="AED", owner_id=message.from_user.id
        #     )
        #     db_calc = await crud.Calculations.create_calculation(session, new_calc)
        #     await message.answer(
        #         f"Additionally, I create new calculation in DB: {db_calc.id}, {db_calc.base_currency} from user {db_calc.owner_id}"
        #     )

        # # TEST CREATE ASSET
        # async with get_session() as session:
        #     new_asset = schemas.Asset(
        #         currency="CYN", sum=999.99997876543221, calc_id=db_calc.id
        #     )
        #     db_asset = await crud.Assets.create_asset(session, new_asset)
        #     await message.answer(
        #         f"Additionally, I create new asset in DB: {db_asset.id}, {db_asset.currency} from calc_id {db_asset.calc_id}"
        #     )

        # TEST GET CALCULATION LIST
        # async with get_session() as session:
        #     db_calc = await crud.Calculations.get_calculation_list(
        #         session, owner_id=message.from_user.id
        #     )
        # for item in db_calc:
        #     await message.answer(f"Calculation id{item.id}: {item.base_currency}")

        # TEST GET ASSETS LIST
        # async with get_session() as session:
        #     db_asset = await crud.Assets.get_assets_list(session, calc_id=1)
        # for item in db_asset:
        #     await message.answer(f"Asset id{item.id}: {item.currency}")

        # TEST DELETE ASSETS
        # async with get_session() as session:
        #     await crud.Assets.delete_asset(session, asset_id=8)
        # await message.answer(f"Asset deleted id8")

    except Exception as e:
        print(e)
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try! But something went wrong...")


@telegram_router.message(Command("info", prefix="!/"))
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


@telegram_router.message(F.text == ButtonText.WHATS_NEXT)
@telegram_router.message(Command("help", prefix="!/"))
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


@telegram_router.message(Command("more", prefix="!/"))
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
