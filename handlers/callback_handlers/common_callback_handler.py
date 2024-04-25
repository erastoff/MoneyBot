# router = Router(name=__name__)


# @telegram_router.callback_query(F.data == CallBacks.exchange_cb_data)
# async def exchange_cb_handle(callback_query: CallbackQuery):
#     # if callback_query.data == CallBacks.exchange_cb_data:
#     print(CallBacks.exchange_cb_data)
#     await callback_query.answer()
#     await callback_query.answer(text="/fastapi")
#     # elif callback_query.data == CallBacks.calculation_cb_data:
#     #     await callback_query.message.answer("/choose_currency")
#
#
# @telegram_router.callback_query(F.data == CallBacks.calculation_cb_data)
# async def calculation_cb_handle(callback_query: CallbackQuery):
#     print(CallBacks.calculation_cb_data)
#     await callback_query.answer()
#     await callback_query.answer(text="/choose_currency")


# @telegram_router.callback_query()
# async def handle_callback_query(callback_query: CallbackQuery):
#     callback_data = callback_query.data
#     print("HERE!!!!! ", callback_data)
#     if callback_data == CallBacks.calculation_cb_data:
#         await callback_query.answer(text="/fastapi")
#     elif callback_data == CallBacks.exchange_cb_data:
#         await callback_query.answer(text="/choose_currency")
