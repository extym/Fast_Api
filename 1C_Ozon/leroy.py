from datetime import datetime
from cred import apikey_lm, login_lm, pass_lm
import pytz
import requests

time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()

access_token = '13748c6a-87e9-46d5-be89-ec10bef8bd18'

def send_get_token():
    url = 'https://api.leroymerlin.ru/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Accept': 'application/json'
               }

    metod = 'marketplace/user/authbypassword'
    url_address = url + metod + '?login=' + login_lm + '&password=' + pass_lm
    answer = requests.get(url_address, headers=headers)
    # print(str(time), type(answer))
    response = answer.json()
    print(str(time), answer)
    response = answer.json()
    print(str(time), response)


def send_get_assortment():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/assortment'
    url_address = url + metod
    answer = requests.get(url_address, headers=headers)
    # print(str(time), type(answer))
    response = answer.json()
    assortment = response['result']
    products = assortment['products']

    print(str(time), 'result', len(products), products)








#send_get_token()
send_get_assortment()