from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN_API = '5494716985:AAGT8sfi28BG21qTDJD4rvu9ki5uCjiRSzY'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

questions_and_answers = {
    'Send your name?': 'root',
    'Send your age?': '20',
    'Send your desc?': 'I love pizza',
}


class ProfileStatesGroup(StatesGroup):
    quest = {}
    for item in questions_and_answers:
        quest[item] = (questions_and_answers[item], State())


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))

    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Welcome! So as to create profile - type /create',
                         reply_markup=get_kb())


keys = list(questions_and_answers)


@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await message.reply(keys[0])
    await ProfileStatesGroup.quest[keys[0]][1].set()


@dp.message_handler(state=ProfileStatesGroup.quest[keys[0]][1])
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['quest1'] = message.text

    if message.text == ProfileStatesGroup.quest[keys[0]][0]:
        await message.reply(keys[1])
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.quest[keys[1]][1])
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    print(ProfileStatesGroup.quest[keys[1]][0])
    if message.text == ProfileStatesGroup.quest[keys[1]][0]:
        await message.reply(keys[2])
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.quest[keys[2]][1])
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        print(data)

    await message.reply('Конец теста')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
