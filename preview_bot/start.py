import operator

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.utils import executor
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.manager import registry
from aiogram_dialog.widgets.kbd import Column, Multiselect
from aiogram_dialog.widgets.text import Const, Format

from keyboards import keyboards

START = """Ответы на тест:
1) count()
2) фабричный метод,строитель,одиночка
3) конструктор
4) декоратор
5) self
6) StopIteration

<b>Welcome to Test!</b> Click to start the test - /test
"""


class SelectState(StatesGroup):
    b = State()


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
                           dialog_manager: DialogManager):
    print("Filter changed: ")


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
        state=PsgQuestion.b,
        getter=get_data,
    )
)

registry.register(dialog_questions)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# def start_command(dp):
#     @dp.message_handler(commands=['start'])
#     async def cmd_start(message: types.Message) -> None:
#         await message.answer(START, reply_markup=keyboards.get_kb(), parse_mode='html')
