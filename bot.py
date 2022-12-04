from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from checker_tests import handlers
from checker_question import handler
from keyboards import keyboards
from preview_bot import start, help

TOKEN_API = '5886107638:AAF7Oej_W7wIyRm28CI7x9SvdVbLI50IziQ'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

keyboards.get_kb()

start.start_command(dp)
help.help_command(dp)

handler.handler(dp)
handlers.handlers(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)