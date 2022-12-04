from aiogram import types
from aiogram.dispatcher import FSMContext

import json

from keyboards import keyboards
from . import states


def handlers(dp):
    with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
        src = json.load(file)

    list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
    questions_and_answers = {}
    for quest in list_questions_answers:
        questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

    keys = list(questions_and_answers)

    # Начало тестирования
    @dp.message_handler(commands=['test'])
    async def cmd_create(message: types.Message) -> None:
        await message.answer('Начинается <b>Первый тест</b>...\n\nЕсли хотите закончить тест нажмите на кнопку - <b>/end</b>', parse_mode='html')
        await message.answer('<b>Вопрос №1</b>\n\n' + keys[0], reply_markup=keyboards.end_test_kb(), parse_mode='html')
        await states.ProfileStatesGroup().question1.set()

    @dp.message_handler(state=states.ProfileStatesGroup().question1)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question1'] = message.text

        if message.text in questions_and_answers[keys[0]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Вопрос №2</b>\n\n' + keys[1], parse_mode='html')
            # await states.ProfileStatesGroup().next()
        elif message.text == '/end':
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
            await state.finish()
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')

    @dp.message_handler(state=states.ProfileStatesGroup().question2)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question2'] = message.text

        if message.text in questions_and_answers[keys[1]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Вопрос №3</b>\n\n' + keys[2], parse_mode='html')
            await states.ProfileStatesGroup().next()
        elif message.text == '/end':
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')

    @dp.message_handler(state=states.ProfileStatesGroup().question3)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question3'] = message.text

        if message.text in questions_and_answers[keys[2]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Вопрос №4</b>\n\n' + keys[3], parse_mode='html')
            await states.ProfileStatesGroup().next()
        elif message.text == '/end':
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')

    @dp.message_handler(state=states.ProfileStatesGroup().question4)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question4'] = message.text

        if message.text in questions_and_answers[keys[3]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Вопрос №5</b>\n\n' + keys[4], parse_mode='html')
            await states.ProfileStatesGroup().next()
        elif message.text == '/end':
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')

    @dp.message_handler(state=states.ProfileStatesGroup().question5)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question5'] = message.text

        if message.text in questions_and_answers[keys[4]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Вопрос №6</b>\n\n' + keys[5], parse_mode='html')
            await states.ProfileStatesGroup().next()
        elif message.text == '/end':
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')

    # # Концовка тестирования
    @dp.message_handler(state=states.ProfileStatesGroup().question6)
    async def load_desc(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question6'] = message.text
            print(data)

        if message.text in questions_and_answers[keys[5]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Конец теста!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
            await state.finish()
