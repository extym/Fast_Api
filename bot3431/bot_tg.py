from cred import token_bot
import requests
from time import sleep


BOT_URL = 'https://api.telegram.org/bot'
TEXT = "Hi for all"
chat_id = '-4187039238'

def send_get(text):
    response = requests.get(url=BOT_URL + token_bot + '/sendMessage?' + 'chat_id=' + chat_id + '&' + 'text=' + text)

    if not response.ok:
        print(333, response.text)
    sleep(2)

# send_get(TEXT)


# print(answer)