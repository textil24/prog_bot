from aiogram import types

from keyboards import keyboards

START = """Ответы на тест:
1) count()
2) фабричный метод,строитель,одиночка
3) конструктор
4) декоратор
5) self
6) StopIteration

<b>Welcome to Test!</b> Click to start the test - /test
"""


# def start_command(dp):
#     @dp.message_handler(commands=['start'])
#     async def cmd_start(message: types.Message) -> None:
#         await message.answer(START, reply_markup=keyboards.get_kb(), parse_mode='html')
