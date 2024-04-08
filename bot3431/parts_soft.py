from requests.auth import HTTPBasicAuth
from cred import admin_ps_login, admin_ps_pass, ps_link
from base64 import b64encode
import requests
from requests import Session




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

    print(answer.text)


def change_status(ids: str):
    url = ps_link + '/order_items/change_status'
    data = {
        "order_item_ids": ids,
        "status_id": 8
    }
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.post(url=url, auth=token_ps, data=data)
    print(answer.text)


def get_orders(customer_id):
    params = {
        'search[customer_id_et]': customer_id,
        # 'per_page': 50,
        'search[status_id_et]': 8,
    }
    url = ps_link + "/orders.json"
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.get(url, auth=token_ps, params=params)
    data = answer.json()


    print(*data.get('orders')[0].get('order_items')[0].keys(), sep='\n')
    print(data.get('orders')[0])
    print(*data.get('orders')[0].keys(), sep='\n')
    print({i['marketplace_id']:
                (
                    i['order_id'],
                    i['customer_id'],
                    len(i['order_items']),
                    i['order_items']
                ) for i in data['orders']}, sep='\n')





get_orders(710)

# get_smth('/regions.json')
# get_smth("/orders.json")
# get_smth("/order_status_types.json")

#  {"id":8,"name":"Выдано","code":"vydano"}

# post_smth()

