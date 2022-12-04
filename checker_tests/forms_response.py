# Рекурсивная перестановка
from itertools import permutations
list_answers = ['фабричный метод', 'строитель', 'одиночка']
lst = [','.join(p) for p in permutations(list_answers)]
str(lst).replace("'", '"')