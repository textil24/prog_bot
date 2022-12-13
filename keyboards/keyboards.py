from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/test'))
    kb.add(KeyboardButton('/question'))
    kb.add(KeyboardButton('/help'))

    return kb


def end_test_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/stop'))

    return kb


def level_kb() -> InlineKeyboardMarkup:
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_3 = InlineKeyboardButton('Easy (1 вопрос)', callback_data='btn3')
    inline_btn_4 = InlineKeyboardButton('Hard (3 вопроса)', callback_data='btn4')
    inline_kb_full.row(inline_btn_3, inline_btn_4)
    return inline_kb_full