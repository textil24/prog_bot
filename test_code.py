# import itertools
#
# s = 'фабричный метод,строитель,одиночка'
#
# words = s.replace(" ", "").split(',')
#
# list_data = []
# for item in itertools.permutations(words):
#     list_data.append(','.join(item))
#
# print(str(list_data).replace("'", '"'))

import asyncio
import random

import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import json

with open("checker_tests/data/questions_and_answers.json", encoding='utf-8') as file:
    src = json.load(file)

list_questions_answers = [src['question_and_answers'][item] for item in src['question_and_answers']]
questions_and_answers = {}
for quest in list_questions_answers:
    questions_and_answers[tuple(quest)[0]] = quest[tuple(quest)[0]]

keys = list(questions_and_answers)

print(questions_and_answers[keys[id]][1])

