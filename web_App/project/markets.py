import json

import requests
from time import sleep
from creds import *


host = 'https://api-seller.ozon.ru'
O3ON_headers = {
        'Client-Id': client_id_oson_artol,
        'Api-Key': api_key_oson_admin_artol,
        'Content-Type': 'application/json'
    }


def get_smth_from(market, metod, token=None, host=''):
    if market == 'oson':
        host = 'https://api-seller.ozon.ru'
        headers = O3ON_headers

    url = host + metod
    answer = requests.get(url=url, headers=headers)

    print(answer.text)


def post_smth_to(market, metod, data, token):
    headers, link = None, None
    if market == 'oson':
        host = 'https://api-seller.ozon.ru'
        headers = O3ON_headers

    url = host + metod
    answer = requests.post(url=url,json=data, headers=headers)

    data = answer.json()
    print(222222, data)
    return data


def get_product_info_oson(product_id, offer_id):
    metod = '/v2/product/info'
    link = host + metod
    data = {
            "offer_id": offer_id,
            "product_id": int(product_id),
            "sku": 0
        }
    response = requests.post(link, headers=O3ON_headers, json=data)
    answer = response.json()
    result = json.loads(response.text)['result']
    print(*result, sep='\n')
    print(**answer['result'].keys(), sep='\n')
    sleep(0.4)

    # return result



#{'product_id': 312351978, 'offer_id': 'PRAXIS006', 'is_fbo_visible': True, 'is_fbs_visible': True, 'archived': False, 'is_discounted': False},

get_product_info_oson(312351978, 'PRAXIS006')