import datetime
import json
import os
import sys
# from connect import *
from cred import oauth_token_yandex, ids_markets
import requests


# 93445631

def get_current_orders(campaign_id: int):
    link = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    result = []
    date_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), "%d-%m-%Y")
    requesting = True
    page = 1
    while requesting:
        params = {
            "fromDate": date_time,
            "page": page
        }
        headers = {
            "Authorization": "Bearer " + oauth_token_yandex
        }
        answer = requests.get(link, params=params, headers=headers)
        if answer.ok:
            data = answer.json()
            print(len(data['orders']), type(data))
            print('!!!!!! - page', page, data['pager'])
            result.extend(data['orders'])
            if data['pager']['pagesCount'] > page:
                page += 1
            else:
                requesting = False
        else:
            print('Error_get_data {}'.format(answer.text))

    # result.extend(data['orders'])

    print(222222, len(result))
    return result


# print(get_current_orders(117527284))


def get_current_orders_ym_v2(campaign_id: int, time_delta: int = 1):
    link = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    result = []
    date_time = datetime.datetime.strftime(datetime.datetime.now()
                                           - datetime.timedelta(days=time_delta),
                                           "%d-%m-%Y")
    requesting = True
    page = 1
    while requesting:
        params = {
            "fromDate": date_time,
            "page": page
        }
        headers = {
            "Authorization": "Bearer " + oauth_token_yandex
        }
        answer = requests.get(link, params=params, headers=headers)
        if answer.ok:
            data = answer.json()
            print(len(data['orders']), type(data))
            print('!!!!!!!!!!!! - page', page, data['pager'])
            result.extend(data['orders'])
            if data['pager']['pagesCount'] > page:
                page += 1
            else:
                requesting = False
        else:
            print('Error_get_data_v2 {}'.format(answer.text))

    # result.extend(data['orders'])

    print(222222, len(result))
    return result


def check_orders_exist():
    for id in ids_markets:
        orders = get_current_orders(id)



from io import StringIO
#  pip install lxml

# articul = "ZIC162658"

#
# get_vendor_code_from_xls(articul)
