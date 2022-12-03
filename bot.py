from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN_API = '5886107638:AAEs26-_sJU6rZwg2k2GUKbDrd_ZRi_GZfM'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

questions_and_answers = {
    'Что такое Python?': 'язык программирования',
    'C помощью какой функции (метода) в модуле itertools возможно последовательно перебирать элементы iterable-объекта бесконечно? Напишите название функции без скобок с учетом регистра?': 'count()',
    'Назовите шаблоны проектирования, относящиеся к группе порождающих:': 'фабричный метод, фасад, строитель, одиночка, декоратор',
}


class ProfileStatesGroup(StatesGroup):

    question1 = State()
    question2 = State()
    question3 = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/test'))

    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('<b>Welcome to Test!</b> Click to start the test - /test',
                         reply_markup=get_kb(), parse_mode='html')

keys = list(questions_and_answers)


@dp.message_handler(commands=['test'])
async def cmd_create(message: types.Message) -> None:
    await message.reply(keys[0])
    await ProfileStatesGroup.question1.set()


@dp.message_handler(state=ProfileStatesGroup.question1)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question1'] = message.text

    if message.text == questions_and_answers[keys[0]]:
        await message.reply(keys[1])
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question2)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question2'] = message.text

    if message.text == questions_and_answers[keys[1]]:
        await message.reply(keys[2])
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question3)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question3'] = message.text
        print(data)

    if message.text == questions_and_answers[keys[2]]:
        await message.reply('<b>Конец теста!!!</b>', parse_mode='html')
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
