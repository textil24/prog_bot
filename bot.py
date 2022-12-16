from aiogram import executor
from config import dp
from handlers import handlers


handlers.handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
