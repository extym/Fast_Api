import datetime
import requests
from settings import OZON_HEADERS
import json

# shipments_today = [('130250',), ('118614',), ('139714',), ('118614',), ('139714',), ('189416',), ('139714',), ('139714',), ('118614',), ('139714',), ('139714',), ('130250',)]
# shipments_list_today = [list(cid) for cid in shipments_today]
# proxy = []
# for cd in shipments_today:
#     cd = list(cd)
#     proxy.extend(cd)
#     shipments_list_today = tuple(set(proxy))
# print(shipments_list_today)
#
# print(proxy)


def get_act_today(sklad_id: int, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/create"
    data = {
        'delivery_method_id': sklad_id,
        "departure_date": datetime.datetime.now()
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'], 'Content-Type': headers['Content-Type'], 'Accept' : headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_act', resp.text)
    if not resp.ok:
        print("API error")
        return None
    try:
        res_dict = json.loads(resp.text)
        return res_dict['result']['id']
    except:
        print("API error")
        return None

# get_act_today()

import random
import string

gen = random.choice(string.ascii_letters)