from requests.auth import HTTPBasicAuth

import bot_tg
from cred import admin_ps_login, admin_ps_pass, ps_link
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
    page = 0
    while marketplace_id != result:
        params = {
            'search[customer_id_eq]': customer_id,
            # 'search[marketplace_id_eq]': marketplace_id,
            'per_page': 20,
            'page': page
        }
        url = ps_link + "/orders.json"
        token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
        answer = requests.get(url, auth=token_ps, params=params)
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

    print(7777, result_list)
    try:
        datas = ' '.join([str(i.get('id')) for i in result_list[0].get('order_items')])
    except:
        datas = ''
    print('datas', datas)
    return datas



async def make_data_for_request_v2(data_file, market):
    count = 0
    proxy = ''
    shipment_date = data_file[1]
    for number in data_file[0]:
        item_ids = get_orders_v2(market, marketplace_id=str(number))
        # result = await change_status(item_ids.strip())
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
