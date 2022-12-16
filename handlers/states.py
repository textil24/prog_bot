from aiogram.dispatcher.filters.state import State, StatesGroup


class PsgText(StatesGroup):
    text = State()


class PsgQuestion(StatesGroup):
    question = State()


class LevelState(StatesGroup):
    level = State()


