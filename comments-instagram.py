import instagram # https://github.com/OlegYurchik/InstagramLib
from time import sleep

account_name = "example" # Целевой аккаунт
all_owners_comments = 0 # 1 - отобразить все комментарии владельца аккаунта; 0 - не использовать эту функцию
search_only_in_owners_comments = 0 # 1 - искать только в комментариях владельца аккаунта; 0 - искать во всех комментариях
# Массив искомых слов
find_words = ['слово1', 'слово2']

def getComments (post):
    check = False
    countAttemp = 0
    while check == False:
        countAttemp += 1
        try:
            sleep(2)
            comments = agent.getComments(post, count=10000)
            check = True
        except Exception as e:
            if countAttemp > 5:
                comments = 0
                check = True
            else:
                sleep(900)
    return comments

agent=instagram.Agent()
account=instagram.Account(str(account_name))
agent.update(account)
p = 0
c = 0
media=agent.getMedia(account, count=10000)
for post in media[0]:
    p += 1
    comments = getComments(post)
    if comments == 0:
        pass
    else:
        for n in comments[0]:
            c += 1
            i = 0
            if all_owners_comments == 1:
                if str(n.owner) == str(account_name):
                    print(str(n.owner) + " (https://www.instagram.com/p/" + str(n.media) + "/): " + str(n.text))
            else:
                if (search_only_in_owners_comments == 0) or (str(n.owner) == str(account_name)):
                    for word in find_words:
                        if word.lower() in n.text.lower():
                            i += 1
                if i > 0:
                    print(str(n.owner) + " (https://www.instagram.com/p/" + str(n.media) + "/): " + str(n.text))
print("Постов: " + str(p) + "; комментариев: " + str(c))
