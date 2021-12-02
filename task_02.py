# 2. Изучить список открытых API. Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.

import vk

with open('token.txt') as t:
    token = t.read()

access_token = token
V = '5.131'
session = vk.Session(access_token=access_token)
api = vk.API(session, v=V)

g = api.groups.get(user_id=7089698, extended=1, count=100)['items']

for name in g:
    print(name['name'])

# result
# MEN'S GROUP
# Мужской Журнал
# Типичный Нижний Новгород
# Men's Lux
# Киномания - Лучшие фильмы
# Убойный юмор
# Apple
# 5 интересных фактов
# Тонкий юмор