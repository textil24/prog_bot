from aiogram import types
from aiogram.dispatcher import FSMContext

import json
import random

from keyboards import keyboards
from . import state


def handler(dp):
    with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
        src = json.load(file)

    list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
    questions_and_answers = {}
    for quest in list_questions_answers:
        questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

    keys = list(questions_and_answers)

    # Начало тестирования
    @dp.message_handler(commands=['question'])
    async def cmd_create(message: types.Message) -> None:
        global id
        id = random.randint(0, len(keys) - 1)
        await message.answer('<b>Внимание вопрос...</b>\n\nЕсли хотите закончить вопрос нажмите на кнопку - <b>/end</b>', parse_mode='html')
        await message.answer('<b>Вопрос</b>\n\n' + keys[id], reply_markup=keyboards.end_test_kb(), parse_mode='html')
        await state.ProfileStatesGroup().question.set()

    @dp.message_handler(state=state.ProfileStatesGroup().question)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question'] = message.text

        if message.text in questions_and_answers[keys[id]]:
            await message.reply('<b>Правильный ответ!!!</b>', parse_mode='html')
            await message.answer('<b>Конец вопроса!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
            await state.finish()
        elif message.text == '/end':
            await message.answer('<b>Конец вопроса!!!</b>', reply_markup=keyboards.get_kb(), parse_mode='html')
            await state.finish()
        else:
            await message.answer('<b>Неправильный ответ!</b>', parse_mode='html')
