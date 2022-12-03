from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = '5494716985:AAGT8sfi28BG21qTDJD4rvu9ki5uCjiRSzY'

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler()
async def cmd_start(message: types.Message):
    await message.answer("Hello world!")


if __name__ == "__main__":
    executor.start_polling(dp)