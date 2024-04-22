from aiogram import types

from bot import telegram_router


# Создаем обработчик нажатия на кнопку "Info"
@telegram_router.callback_query_handler(lambda query: query.data == "info")
async def send_info_command(callback_query: types.CallbackQuery):
    # Создаем объект сообщения, который будет содержать команду /info
    message = types.Message(
        message_id=callback_query.message.message_id,
        chat=callback_query.message.chat,
        text="/info",  # Команда, которую мы хотим выполнить
        date=callback_query.message.date,
    )

    # Обрабатываем это сообщение, как если бы оно было отправлено пользователем
    await telegram_router.process_message(message)
