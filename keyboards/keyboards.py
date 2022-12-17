from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def menu_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="/hint"),
            types.KeyboardButton(text="/theory")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb, one_time_keyboard=True)
    return keyboard


def end_test_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/stop'))

    return kb


def level_kb() -> InlineKeyboardMarkup:
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_3 = InlineKeyboardButton('Easy (1 вопрос)', callback_data='btn1')
    inline_btn_4 = InlineKeyboardButton('Hard (3 вопроса)', callback_data='btn2')
    inline_kb_full.row(inline_btn_3, inline_btn_4)
    return inline_kb_full