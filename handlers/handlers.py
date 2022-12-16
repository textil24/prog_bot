import asyncio

import aioschedule
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data.values import *
from . import states
from config import *
from keyboards import keyboards
import json


def handlers(dp):
    with open("data/questions_and_answers.json", encoding='utf-8') as file:
        src = json.load(file)

    list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
    questions_and_answers = {}
    answers = [["134", "143", "341", "431", "314", "413"],
               ["count", "Сount"],
               ["конструктор", "Конструктор"],
               ["декоратор", "Декоратор"],
               ["self", "Self"],
               ["stopiteration", "StopIteration", "stopIteration"],
               ["итератор", "Итератор"],
               ["cинглтон", "Синглтон"]]
    for quest in list_questions_answers:
        questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

    keys = list(questions_and_answers)

    @dp.message_handler(commands=["start"])
    async def start(message: Message):
        global user_id
        user_id = message.from_user.id
        global text
        text = message.text
        await bot.send_message(user_id, 'Введите время (в секундах) для получения вопроса:')
        await states.PsgText.next()

    #
    # @dp.message_handler(state=LevelState.level)
    # async def select_level(message: types.Message, state: FSMContext) -> None:
    #     await message.reply("Выбери уровень: ", reply_markup=keyboards.get_kb())

    @dp.message_handler(state=states.PsgText.text)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        global user_time
        user_time = message.text
        # await scheduler('16:29')
        await state.finish()
        await message.reply("Теперь выбери уровень (количество вопросов в день): ", reply_markup=keyboards.level_kb())

    @dp.callback_query_handler(text='btn1')
    async def process_callback_button1(call: types.CallbackQuery):
        # await call.message.answer("first")
        await bot.send_message(user_id, FIRST_BUTTON.format(user_time))
        await scheduler(int(user_time))

    @dp.message_handler(commands=["theory"])
    async def send_theory(message: types.Message):
        photo = open('media/{}.jpg'.format(question_number + 1), 'rb')
        await bot.send_photo(user_id, photo, parse_mode='html')

    async def scheduler(time):
        # aioschedule.every().day.at(time).do(do_get)
        aioschedule.every(time).seconds.do(send_question_test)

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(time)
            end_script = text
            if end_script == '/secretend':
                end_script = ''
                break

    async def send_question_test():
        global question_number
        question_number += 1
        print("question number {}".format(question_number))
        if question_number < len(keys) - 1:
            if photo := questions_and_answers[keys[question_number]][1]:
                photo_init = open(photo, 'rb')
                await bot.send_photo(user_id, photo_init, caption=keys[question_number], parse_mode='html')
                await states.PsgQuestion.next()
            else:
                await bot.send_message(user_id, keys[question_number], parse_mode='html')
                await states.PsgQuestion.next()

    @dp.message_handler(state=states.PsgQuestion.question)
    async def load_name(message: types.Message, state: FSMContext) -> None:
        user_answer = message.text.lower().replace(' ', '')
        if user_answer in answers[question_number]:
            await message.answer(CORRECT_ANSWER, parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[question_number]][2])
        elif user_answer == '/theory':
            await send_theory(message)
        else:
            await message.answer(WRONG_ANSWER, parse_mode='html')
