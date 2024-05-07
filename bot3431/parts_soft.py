import logging
import os

from requests.auth import HTTPBasicAuth

import bot_tg
from cred import admin_ps_login, admin_ps_pass, ps_link, ps_YM_II_api_key
from base64 import b64encode
import requests
from requests import Session


# from bot_tg import send_get


def basic_auth():
    token = b64encode(f"{admin_ps_login}:{admin_ps_pass}".encode('utf-8')).decode("ascii")
    return token


def get_client():
    session = Session()
    session.auth = (admin_ps_login, admin_ps_pass)

    return session.auth


def get_smth(metod):
    url = ps_link + metod
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.get(url, auth=token_ps)

    print(333, answer.text)


async def change_status(ids: str):
    url = ps_link + '/order_items/change_status'
    data = {
        "order_item_ids": ids,
        "status_id": 8
    }
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.post(url=url, auth=token_ps, data=data)
    print('answer_changed_status', answer.text)
    if answer.ok:
        return True
    else:
        return False


def get_orders_v2(customer_id, marketplace_id):
    result, result_list = '', []
    page, error = 0, 0
    while marketplace_id != result:
        params = {
            'search[customer_id_eq]': customer_id,
            'search[marketplace_id_eq]': marketplace_id,
            'per_page': 20,
            'page': page
        }
        url = ps_link + "/orders.json"
        token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
        answer = requests.get(url, auth=token_ps, params=params)
        if answer.ok:
            data = answer.json()
            result_list = [i for i in data.get('orders')
                           if i.get('marketplace_id') == marketplace_id]

            if result_list:
                result = marketplace_id
            else:
                page += 1
                print('page ', page)
            if page >= 5:
                bot_tg.send_get('So many pages {} for {} in {}'.format(page, marketplace_id, customer_id))
                break
        else:
            error += 1
            logging.info('Some trouble with access parts-soft - status {} text {}'
                         .format(answer.status_code, answer.text))
            bot_tg.send_get('Some trouble with access parts-soft - status {} text {}'
                            .format(answer.status_code, answer.text))
            if page >= 5:
                break

    # print(7777, result_list)
    try:
        datas = ' '.join([str(i.get('id')) for i in result_list[0].get('order_items')])
    except:
        datas = ''
    # print('datas', datas)
    return datas


async def make_data_for_request_v2(data_file, market):
    count = 0
    proxy = ''
    shipment_date = data_file[1]
    # print(33333333, data_file)
    for number in data_file[0]:
        item_ids = get_orders_v2(market, marketplace_id=str(number))
        proxy += item_ids.strip() + ' '
        count += 1

    result = await change_status(proxy.strip())
    if result:
        bot_tg.send_get("All_ride_Rewrite {} statuses for all {} from market {} at {}"
                        .format(count, len(data_file[0]), market, shipment_date))
    else:
        bot_tg.send_get("Fuck_up_Rewrite {} statuses for all {} from market {} at {}"
                        .format(count, len(data_file[0]), market, shipment_date))

    print('All_order_items', proxy)


# get_orders_v2(710, marketplace_id='9009797416999')

# get_smth('/regions.json')
# get_smth("/orders.json")
# get_smth("/order_status_types.json")

#  {"id":8,"name":"Выдано","code":"vydano"}

# post_smth()


## FOR VERSION 1 API - CLIENT ONLY!
basket = '/api/v1/baskets/'
add_basket = "/api/v1/baskets"

def get_current_client_smth(metod):
    url = "https://3431.ru" + metod
    # token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    params = {
        "api_key": ps_YM_II_api_key
    }
    answer = requests.get(url, params=params)

    print(answer.text)


def send_current_basket_to_order():
    url = "https://3431.ru/api/v1/baskets/order"
    headers = {
        "api_key": ps_YM_II_api_key}
    data = {
        "api_key": ps_YM_II_api_key
    }
    answer = requests.post(url, headers=headers, data=data)

    print("FINAL_result {}".format(answer.text))



def make_basket(qnt=None, external_id=None, propousal=None):
    url = "https://3431.ru/api/v1/baskets"
    headers = {
        "api_key": ps_YM_II_api_key}
    data = {
        "api_key": ps_YM_II_api_key,
        "oem": propousal.get('oem'),
        "make_name": propousal.get('make_name'),
        "detail_name": propousal.get('detail_name'),
        "qnt": str(qnt),
        "comment": str(external_id),
        "min_delivery_day": str(propousal.get('min_delivery_day')),
        "max_delivery_day": str(propousal.get('max_delivery_day')),
        "api_hash": propousal.get('hash_key')
        }
    answer = requests.post(url, headers=headers, data=data)
    print("!!!!!!!!!!!!!!!!", answer.text)

    return answer.status_code


def choice_function(items, full_items, qnt):
    listing = sorted(items.values())[:5]
    print(333, listing)
    result = []
    for item in full_items:
        if item["cost"] in listing and item['qnt'] >= qnt:
            result.append(item)

    return result


def create_resp_is_exist(oem=None, brand=None, qnt=0, external_id=None):
    # for item, quantity in sku.items:
    params = {
        "api_key": ps_YM_II_api_key,
        "oem": oem,
        "make_name": brand,
        "without_cross": True
    }
    metod = "/backend/price_items/api/v1/search/get_offers_by_oem_and_make_name"
    url = "https://3431.ru" + metod
    answer = requests.get(url, params=params)
    need_data = answer.json()["data"]
    if len(need_data) > 0:
        propousal = {i['hash_key']: i['cost'] for i in need_data if
                     (i["oem"] == oem and i['make_name'] == brand)}
        list_propousal = choice_function(propousal, need_data, qnt)

        print(*list_propousal[0].items(), sep='\n')
        # print(len(propousal))

        result_make_basket = make_basket(propousal=list_propousal[0],
                                         qnt=qnt, external_id=external_id)






# send_current_basket_to_order()

# create_resp_is_exist(brand="STELLOX", oem="42140459SX", qnt=2, external_id=451642783)
# get_current_client_smth(basket)
