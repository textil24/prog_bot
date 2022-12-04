from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN_API = '5886107638:AAFiClorhFiskGmTswuFXGBQ9OCxl7CLYW8'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

questions_and_answers = {
    'C помощью какой функции (метода) в модуле itertools возможно последовательно перебирать элементы iterable-объекта бесконечно? Напишите название функции без скобок с учетом регистра?' : 'count()',
    'Назовите шаблоны проектирования, относящиеся к группе порождающих:' : 'фабричный метод, строитель, одиночка',
    '...класса - это функция, имплементированная внутри класса и имеющая следующий синтаксис:\n\n<b>def __init__(self):</b>\n<b>Pass</b>' : 'конструктор',
    'Как называется одним словом конструкция, примененная к функции foo, описанной ниже:\n\n<b>@trace</b>\n<b>def foo(x):</b>\n<b>return 42</b>' : 'декоратор',
    'Для создания связанного метода класса при его объявлении первым аргументом должен быть аргумент с названием …' : 'self',
    'Какой тип исключения должен подниматься в ситуации, когда итератор исчерпан (следующего по порядку элемента итератора нет)?' : 'StopIteration'
}


class ProfileStatesGroup(StatesGroup):

    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/test'))

    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Ответы на тест:\n1)count()\n2)фабричный метод, строитель, одиночка\n3)конструктор\n4)декоратор\n5)self\n6)StopIteration\n\n<b>Welcome to Test!</b> Click to start the test - /test',
                         reply_markup=get_kb(), parse_mode='html')

keys = list(questions_and_answers)


@dp.message_handler(commands=['test'])
async def cmd_create(message: types.Message) -> None:
    await message.reply(keys[0], parse_mode='html')
    await ProfileStatesGroup.question1.set()


@dp.message_handler(state=ProfileStatesGroup.question1)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question1'] = message.text

    if message.text == questions_and_answers[keys[0]]:
        await message.reply(keys[1], parse_mode='html')
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question2)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question2'] = message.text

    if message.text == questions_and_answers[keys[1]]:
        await message.reply(keys[2], parse_mode='html')
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question3)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question3'] = message.text

    if message.text == questions_and_answers[keys[2]]:
        await message.reply(keys[3], parse_mode='html')
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question4)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question4'] = message.text

    if message.text == questions_and_answers[keys[3]]:
        await message.reply(keys[4], parse_mode='html')
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question5)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question5'] = message.text

    if message.text == questions_and_answers[keys[4]]:
        await message.reply(keys[5], parse_mode='html')
        await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.question6)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question6'] = message.text
        print(data)

    if message.text == questions_and_answers[keys[5]]:
        await message.reply('<b>Конец теста!!!</b>', parse_mode='html')
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)