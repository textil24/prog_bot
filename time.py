import asyncio
import random

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import json

from aiogram.utils.markdown import hide_link

TOKEN_API = '5886107638:AAHuzhRErcTNw2RCnmHyF79BCXsxcvDo284'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

user_id = ''

with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
    src = json.load(file)

list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
questions_and_answers = {}
for quest in list_questions_answers:
    questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

keys = list(questions_and_answers)


class ProfileStatesGroup(StatesGroup):

    text = State()


class ProfileStatesGroup1(StatesGroup):

    question = State()


@dp.message_handler(commands=['start'])
async def choose_your_dinner(message: types.Message):
    global user_id
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Введите время ( в секундах ) для получения вопроса:')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.text)
async def load_name(message: types.Message, state: FSMContext) -> None:
    # await scheduler('16:29')
    await scheduler(int(message.text))


async def question_test():
    global id
    id = random.randint(0, len(keys) - 1)

    if photo := questions_and_answers[keys[id]][1]:
        print('Я работаю')
        photo_init = open(photo, 'rb')
        await bot.send_photo(user_id, photo_init, caption=keys[id], parse_mode='html')
        # await bot.send_message(user_id,
        #     text=f'Тра-та-та{hide_link(photo)}',
        #     parse_mode='HTML'
        # )
        await ProfileStatesGroup1.next()
    else:
        await bot.send_message(user_id, keys[id], parse_mode='html')
        await ProfileStatesGroup1.next()


@dp.message_handler(state=ProfileStatesGroup1.question)
async def load_name(message: types.Message, state: FSMContext) -> None:

    if message.text.lower().replace(' ', '') in questions_and_answers[keys[id]][0]:
        if message.text in questions_and_answers[keys[id]][0]:
            await message.answer('<b>Совершенно верно! Продолжай в том же духе...</b>', parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[id]][2])
            await state.finish()
        else:
            await message.answer(f'<b>Это похоже на правильный ответ!</b> В следующий раз пишите: <b>{questions_and_answers[keys[id]][0][-1]}</b>', parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[id]][2])
            await state.finish()
    elif message.text == '/end':
        await message.answer('<b>Конец вопроса!!!</b>', parse_mode='html')
        await state.finish()
    else:
        await message.answer('<b>Неправильный ответ! Попробуйте снова...</b>', parse_mode='html')


async def scheduler(time):
    # aioschedule.every().day.at(time).do(do_get)
    aioschedule.every(time).seconds.do(question_test)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


