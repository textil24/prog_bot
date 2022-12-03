import asyncio
import logging
from aiogram import Bot, Dispatcher, types

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="5494716985:AAGT8sfi28BG21qTDJD4rvu9ki5uCjiRSzY")
# Диспетчер
dp = Dispatcher(bot)

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello world!")


# Запуск процесса поллинга новых апдейтов

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())