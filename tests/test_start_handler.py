from aiogram import types
from aiogram.dispatcher import FSMContext

from data.consts import START_MESSAGE
from handlers import handlers


async def test_start_command(dp, event_loop):
    # Создаем сообщение от пользователя с командой /start
    message = types.Message(
        message_id=1,
        from_user=types.User(id=1, is_bot=False, first_name="Tanya", last_name="Tarinskaya"),
        chat=types.Chat(id=1, type=types.ChatType.PRIVATE),
        date=None,
        text="/start",
    )

    # Обрабатываем команду /start
    await handlers.start_handler(message, FSMContext())

    # Проверяем, что бот отправил сообщение пользователю
    messages = await dp.bot.get_new_messages(chat_id=1)
    assert len(messages) == 1
    assert messages[0].text == START_MESSAGE

    # Проверяем, что контекст FSM сохранен
    data = await dp.bot.get_data(chat_id=1)
    assert data == {"state": None}
