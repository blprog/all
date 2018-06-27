#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import time
import vk_api # https://github.com/python273/vk_api
reload(sys)
sys.setdefaultencoding('utf8')

user_id = 123456789 # ID нужного пользователя. Не путайте с шорткатом!
# ID проще всего узнать, перейдя в фотоальбомы пользователя и взглянув водоёмную строку браузера.
# Там будет нечто вроде album12345678, где цифры — это ID.
my_login = "Example"   # Ваш логин
my_password = "qwerty" # Ваш пароль

def auth_handler():
    key = input("Введите проверочный код двуфакторной авторизации:: ")
    remember_device = True
    return key, remember_device

login, password = my_login, my_password
vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
    exit()
vk = vk_session.get_api()
tools = vk_api.VkTools(vk_session)

groups = tools.get_all('groups.get', 1000, {'user_id': user_id, 'extended': 1})
for group in groups['items']:
    time.sleep(2)
    try:
        wall = []
        response = vk.wall.get(owner_id="-" + str(group['id']), count=100)
        for el in response['items']:
            wall.append(el['id'])
        wall_parted = [wall[d:d + 25] for d in xrange(0, len(wall), 25)]
        for p in wall_parted:
            like = {}
            with vk_api.VkRequestsPool(vk_session) as pool:
                for id in p:
                    like[id] = pool.method('likes.isLiked',
                                           {'user_id': user_id, 'type': 'post', 'owner_id': '-' + str(group['id']),
                                            'item_id': id})
            for key, value in like.items():
                like[key] = value.result
            for result_like in like:
                if like[result_like]['liked'] == 1:
                    print(str(group['name']) + ': ' + 'https://vk.com/wall-' + str(group['id']) + '_' + str(result_like))
    # Знаю, говнокод
    except Exception as e:
        if str(e) == "[29] Rate limit reached":
            print("Исчерпан суточный лимит запросов.")
            exit()
        else:
            if ((str(e) == "[15] Access denied: this wall available only for community members") or (str(e) == "[15] Access denied: group is blocked")):
                pass
            print(e)
        pass
print("Завершено.")