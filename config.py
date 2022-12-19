import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

token_api = os.getenv("TOKEN_API")

storage = MemoryStorage()

bot = Bot(token_api, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)



