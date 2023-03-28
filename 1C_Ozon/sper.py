import json
import requests
from datetime import datetime
from read_json import read_json_sper
from cred import test_token_sper, token_sper

url = 'https://partner.sbermegamarket.ru/api/merchantIntegration/v1/offerService/'

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
        "token": token_sper,
        "stocks": stocks_sb
        }
    }
    print('create_send_stocks_sb', len(stocks_sb))

    return send_data


def send_stocks_sb():
    data = stocks_update()
    headers = {'Content-type': 'application/json'
               }
    metod = 'stock/update'
    url_address = url + metod #+ '?login=' + login_lm + '&password=' + pass_lm
    answer = requests.post(url_address, headers=headers, data=json.dumps(data))
    
    print('send_stocks_sb', answer, answer.text)


def check_is_accept_sb(list_items):
    data = read_json_sper()  #return list
    result_global = False
    cnt = 0
    for item in list_items:
        item['id_1c'] = None
        shop_sku = item['offerId']
        for row in data:
            if row[1] == shop_sku:
                count = row[3]
                if count >= item['quantity']:
                    cnt += 1
                item['id_1c'] = row[0]

    if cnt == len(list_items):
        result_global = True
    print('check_is_accept_sb', result_global, list_items)
    return result_global, list_items


#send_stocks_sb()
test_url = 'http://localhost:5500/response'
async def post_smth_sb(metod, data):
    headers = {'Content-type': 'application/json'}
    # target_url = test_url  #TODO for TEST ONLY
    target_url = url + metod  #TODO for PRODUCTION
    response = requests.post(target_url, headers=headers, data=json.dumps(data))
    print(''
          'post_smth_sb', response, response.text, target_url, metod)
