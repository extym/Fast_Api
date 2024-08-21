import datetime
import json
import os
import sys
import pandas as pd
from connect import *
from cred import bearer_token
import parts_soft as ps
import requests


# 93445631

def get_current_orders(campaign_id: int):
    link = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    result = []
    # date_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=3), "%d-%m-%Y")
    date_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), "%d-%m-%Y")
    requesting = True
    page = 1
    while requesting:
        params = {
            "fromDate": date_time,
            "page": page
        }
        headers = {
            "Authorization": "Bearer " + bearer_token
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
            print('Error_get_data {}'.format(answer.text))

    # result.extend(data['orders'])

    print(222222, len(result))
    return result


def get_current_orders_ym_v2(campaign_id: int, time_delta: int=1):
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
            "Authorization": "Bearer " + bearer_token
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




from io import StringIO
#  pip install lxml

# articul = "ZIC162658"

#
# get_vendor_code_from_xls(articul)