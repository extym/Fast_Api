from project.creds import token_bot, chat_id
import requests
from time import sleep


BOT_URL = 'https://api.telegram.org/bot'
TEXT = "Hi for all"


def send_get(text):
    response = requests.get(url=BOT_URL + token_bot + '/sendMessage?' + 'chat_id=' + chat_id + '&' + 'text=' + text)

    if not response.ok:
        print(333, response.text)
    sleep(2)

# send_get(TEXT)
# how to get chat id
# answer = requests.get(url=f'https://api.telegram.org/bot{token_bot}/getUpdates')
# print(answer)