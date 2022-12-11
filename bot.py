import asyncio
import operator
import random

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import json

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogRegistry, Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Multiselect, Column
from aiogram_dialog.widgets.managed import ManagedWidgetAdapter
from aiogram_dialog.widgets.text import Const, Format

TOKEN_API = '5886107638:AAHuzhRErcTNw2RCnmHyF79BCXsxcvDo284'

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


with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
    src = json.load(file)

list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
questions_and_answers = {}
for quest in list_questions_answers:
    questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

keys = list(questions_and_answers)
id = 0


class PsgText(StatesGroup):
    text = State()


class PsgQuestion(StatesGroup):
    question = State()


class States(StatesGroup):
    b = State()


@dp.message_handler(commands=["start"])
async def start(message: Message, ):
    global id
    global user_id
    user_id = message.from_user.id
    global text
    text = message.text
    await bot.send_message(user_id, 'Введите время ( в секундах ) для получения вопроса:')
    await PsgText.next()


@dp.message_handler(state=PsgText.text)
async def load_name(message: types.Message, dialog_manager: DialogManager, state: FSMContext) -> None:
    print(message.text)
    # await scheduler('16:29')
    await state.finish()
    await scheduler(message, dialog_manager, int(message.text))


async def scheduler(message: types.Message, dialog_manager: DialogManager, time):
    # aioschedule.every().day.at(time).do(do_get)
    aioschedule.every(time).seconds.do(lambda: question_test(message, dialog_manager))

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(time)
        end_script = text
        if end_script == '/secretend':
            end_script = ''
            break


async def question_test(message: Message, dialog_manager: DialogManager):
    global id
    if id < len(keys)-1:
        if id == 0:
            print("first question send")
            await dialog_manager.start(States.b, mode=StartMode.RESET_STACK)
            await PsgQuestion.next()
        elif photo := questions_and_answers[keys[id]][1]:
            photo_init = open(photo, 'rb')
            await bot.send_photo(user_id, photo_init, caption=keys[id], parse_mode='html')
            await PsgQuestion.next()
        else:
            await bot.send_message(user_id, keys[id], parse_mode='html')
            await PsgQuestion.next()
        id = id + 1


@dp.message_handler(state=PsgQuestion.question)
async def load_name(message: types.Message, state: FSMContext) -> None:
    if message.text.lower().replace(' ', '') in questions_and_answers[keys[id]][0]:
        print(keys)
        print(id)
        if message.text in questions_and_answers[keys[id]][0]:
            await message.answer('<b>Совершенно верно! Продолжай в том же духе...</b>', parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[id]][2])
        else:
            await message.answer(
                f'<b>Это похоже на правильный ответ!</b> В следующий раз пишите: <b>{questions_and_answers[keys[id]][0][-1]}</b>',
                parse_mode='html')
            await bot.send_sticker(user_id, sticker=questions_and_answers[keys[id]][2])
    elif message.text == '/secretend':
        global text
        text = message.text
        await message.answer('<b>Конец вопроса!!!</b>', parse_mode='html')
        await state.finish()
    else:
        global count
        count += 1
        if count in [3, 4]:
            await message.answer(questions_and_answers[keys[id]][3], parse_mode='html')
        elif count in [5]:
            await message.answer('<b>Неправильный ответ! Попробуйте снова...</b>', parse_mode='html')
            count = 0

        else:
            await message.answer('<b>Неправильный ответ! Попробуйте снова...</b>', parse_mode='html')


async def get_data(**kwargs):
    answers = [
        ("Фабричный метод", '1'),
        ("Фасад", '2'),
        ("Строитель", '3'),
        ("Одиночка", '4'),
        ("Декоратор", '5'),
    ]
    return {
        "answers": answers,
        "count": len(answers),
    }


async def selected_buttons(c: CallbackQuery, multiselect_adapter: ManagedWidgetAdapter,
                           dialog_manager: DialogManager, item_id: str):
    print("Filter changed: ", item_id)


column = Column(
    Multiselect(
        Format("✓ {item[0]}"),
        Format("{item[0]}"),
        id="m_fruits",
        item_id_getter=operator.itemgetter(1),
        items="answers",
        on_state_changed=selected_buttons,
    )
)

dialog_questions = Dialog(
    Window(
        Const("Назовите шаблоны проектирования, относящиеся к группе порождающих:"),
        column,
        state=States.b,
        getter=get_data,
    )
)

registry.register(dialog_questions)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
