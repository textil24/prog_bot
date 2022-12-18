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
               ["count", "Сount", 'count()', 'Count()'],
               ["конструктор", "Конструктор"],
               ["декоратор", "Декоратор"],
               ["self", "Self"],
               ["stopiteration", "StopIteration", "stopIteration"],
               ["итератор", "Итератор"],
               ["cинглтон", "Синглтон"]]

    hints = ['надо выбрать три номера',
             "первая буква 'c'",
             "первая буква 'к'",
             "первая буква 'д'",
             "первая буква 's'",
             "первая часть слова: 'stop'",
             "первая буква 'и'",
             "первая буква 'c'"]

    for quest in list_questions_answers:
        questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

    keys = list(questions_and_answers)

    @dp.message_handler(commands=["start"])
    async def start(message: Message):
        global user_id
        user_id = message.from_user.id
        global text
        global m
        m = message
        text = message.text
        await message.reply('Как пользоваться этим ботом: '
                            'необходимо выбрать время, затем уровень.'
                            'Обратите внимание, что поменять в дальнейшем эти значения не получится. '
                            'После того как тебе придет вопрос можно воспользоваться командой /hint для '
                            'получения подсказки по вопросу и командой /theory для развернутой теории по '
                            'теме вопроса. Если ты забудешь прислать верный ответ, '
                            'то бот через 12 часов тебе об этом напомнит.')
        await asyncio.sleep(5)
        await bot.send_message(user_id, 'Введите время (например 17:05) для получения ежедневных уведомлений:')
        await states.PsgText.next()

    @dp.message_handler(state=states.PsgText.text)
    async def get_level(message: types.Message, state: FSMContext) -> None:
        global user_time
        user_time = int(message.text)
        await state.finish()
        await message.reply("Теперь выбери уровень (количество вопросов в день): ", reply_markup=keyboards.level_kb())

    @dp.callback_query_handler(text='btn1')
    async def process_callback_button1(call: types.CallbackQuery):
        await bot.send_message(user_id, FIRST_BUTTON.format(user_time))
        await scheduler(user_time)

    @dp.callback_query_handler(text='btn2')
    async def process_callback_button2(call: types.CallbackQuery):
        await bot.send_message(user_id, "В данной версии доступен только 1 вопрос в день :(")

    @dp.message_handler(commands=["theory"])
    async def send_theory(message: Message):
        photo = open('media/{}.jpg'.format(question_number + 1), 'rb')
        await bot.send_photo(user_id, photo, parse_mode='html')

    @dp.message_handler(commands=["hint"])
    async def send_hint(message: Message):
        await bot.send_message(user_id, hints[question_number])
       # await message.answer(hints[question_number])

    async def scheduler(time):
        # aioschedule.every().day.at(time).do(do_get)
        aioschedule.every(time).seconds.do(send_question_test)
        # aioschedule.every(time+12).seconds.do(check_user_answered)

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(time)
            end_script = text
            if end_script == '/stop':
                end_script = ''
                break

    async def send_question_test():
        global question_number
        question_number += 1
        print("question number {}".format(question_number))
        if question_number < len(keys):
            if photo := questions_and_answers[keys[question_number]][1]:
                photo_init = open(photo, 'rb')
                await bot.send_photo(user_id, photo_init, caption=keys[question_number], parse_mode='html', reply_markup=keyboards.menu_kb())
            else:
                await bot.send_message(user_id, keys[question_number], parse_mode='html', reply_markup=keyboards.menu_kb())
                print("test")
            await states.PsgQuestion.question.set()

    @dp.message_handler(state=states.PsgQuestion.question)
    async def user_answer(message: types.Message, state: FSMContext) -> None:
        print("send answer")
        user_answer = message.text.lower().replace(' ', '')
        global is_user_answered
        if user_answer in answers[question_number]:
            is_user_answered = True
            print("true")
            await message.answer(CORRECT_ANSWER, parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[question_number]][2])
        elif user_answer == '/theory':
            await send_theory(message)
        elif user_answer == '/hint':
            await send_hint(message)
        else:
            await message.answer(WRONG_ANSWER, parse_mode='html')

    async def check_user_answered():
        if not is_user_answered:
            await bot.send_message(user_id, "Напоминаю, что нужно ответить на вопрос." +
                                   "Тебе поможет эта информация: ")
            await send_theory(m)
