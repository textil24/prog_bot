from aiogram import types

from keyboards import keyboards

HELP = """<b>Основные команды бота:</b>

/start - <em>запускает бота;</em>

/test - <em>запускает тест для проверки знаний python;</em>

/question - <em>дает один вопрос для проверки знаний python;</em>

/help - <em>помогает пользователю разобраться в боте;</em>
"""

def help_command(dp):
    @dp.message_handler(commands=['help'])
    async def cmd_start(message: types.Message) -> None:
        await message.answer(HELP, reply_markup=keyboards.get_kb(), parse_mode='html')