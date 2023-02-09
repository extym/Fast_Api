import json
import requests
from datetime import datetime
from read_json import read_json_sper
from cred import test_token_sper, token_sper


def stocks_update():
    data_from = read_json_sper()
    stocks_sb = []
    for row in data_from:
        proxy = {}
        proxy['offerId'] = row[1]
        proxy['quantity'] = row[3]
        # proxy['price'] = row[2]
        stocks_sb.append(proxy)

    # token_sper = ''
    send_data = {
    "meta": {},
    "data": {
        "token": test_token_sper,
        "stocks": stocks_sb
        }
    }
    print('send', send_data)
    return send_data


def send_stocks():
    data = stocks_update()
    url = 'https://partner.sbermegamarket.ru/api/merchantIntegration/v1/offerService/'
    headers = {'Content-type': 'application/json'
               }

    metod = 'stock/update'
    url_address = url + metod #+ '?login=' + login_lm + '&password=' + pass_lm
    answer = requests.post(url_address, headers=headers, data=json.dumps(data))
    
    print(answer)


send_stocks()