import asyncio
import os

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import json

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram_dialog import DialogManager, StartMode, DialogRegistry, Dialog, Window

TOKEN_API = '1670961232:AAGt74keHH_CeyGOi9lxe1FEMNi9-8JBcis'

user_id = ''
text = ''
count = 0

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

# keyboards.get_kb()

# start.start_command(dp)
# help.help_command(dp)

# handler.handler(dp)
# handlers.handlers(dp)

BEFORE_STOP_BOT = "Бот остановлен"
question_number = 0

with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
    src = json.load(file)

list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
questions_and_answers = {}
for quest in list_questions_answers:
    questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

keys = list(questions_and_answers)


class PsgText(StatesGroup):
    text = State()


class PsgQuestion(StatesGroup):
    question = State()


class SelectState(StatesGroup):
    b = State()


@dp.message_handler(commands=["start"])
async def start(message: Message):
    global user_id
    user_id = message.from_user.id
    global text
    text = message.text
    await bot.send_message(user_id, 'Введите время ( в секундах ) для получения вопроса:')
    await PsgText.next()


@dp.message_handler(state=PsgText.text)
async def load_name(message: types.Message, state: FSMContext) -> None:
    print(message.text)
    # await scheduler('16:29')
    await state.finish()
    await scheduler(int(message.text))


@dp.message_handler(commands=["theory"])
async def send_theory(message: types.Message):
    photo = open('media/{}'.format(question_number), 'rb')
    await bot.send_photo(user_id, photo, caption=keys[question_number], parse_mode='html')


async def scheduler(time):
   #aioschedule.every().day.at(time).do(do_get)
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
    print("question number {}".format(question_number))
    print(keys)
    if question_number < len(keys) - 1:
        if photo := questions_and_answers[keys[question_number]][1]:
            photo_init = open(photo, 'rb')
            await bot.send_photo(user_id, photo_init, caption=keys[question_number], parse_mode='html')
            await PsgQuestion.next()
        else:
            await bot.send_message(user_id, keys[question_number], parse_mode='html')
            await PsgQuestion.next()
        question_number += 1


@dp.message_handler(state=PsgQuestion.question)
async def load_name(message: types.Message, state: FSMContext) -> None:
    if message.text.lower().replace(' ', '') in questions_and_answers[keys[question_number]][0]:
        await message.answer('<b>Совершенно верно! Продолжай в том же духе...</b>', parse_mode='html')
        await bot.send_sticker(user_id, sticker=questions_and_answers[keys[question_number]][2])
    else:
        await message.answer('<b>Неправильный ответ! Попробуйте снова...</b>', parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

