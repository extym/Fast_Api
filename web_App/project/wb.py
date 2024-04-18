from datetime import datetime, timedelta
import random
import string
import asyncio

from sqlalchemy import insert, create_engine, select, update, text
from sqlalchemy.orm import Session

from project.models import Marketplaces
from read_json import read_json_wb, read_json_ids
import requests
import json

from conn import *

# data = read_json_wb()
# https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}
link = 'https://suppliers-api.wildberries.ru'
l = 'https://suppliers-api.wildberries.ru/api/v3/supplies'

engine = create_engine("postgresql+psycopg2://user_name:user_pass@localhost/stm_app")

wh = [{"name": "Обычный склад СТМ", "id": 664706, "name_1C": "WB.НашсклСТМ"},
      {"name": "Сверхгабаритный товар", "id": 730558, "name_1C": "WB.СверхГБсклNEW"}]  # ,


# {"name_1C": "WB.СверхГБсклСТМ", "name":"Сверхгабаритный СТМ склад","id":664704}] # {"name":"Сверхгабаритный товар","id":730558, "name_1C": "WB.СверхГБсклNEW"}


def token_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)
    print(pt)
    return pt


def day_for_stm(string):
    datta = datetime.strptime(string, '%Y-%m-%d')
    dat = datta.weekday()
    dtt = datta.strftime('%d-%m-%Y')
    if 1 <= dat <= 4:
        dtt = (datta - timedelta(1)).strftime('%d-%m-%Y')
    elif dat == 5:
        proxy = datta + timedelta(2)
        dtt = proxy.strftime('%d-%m-%Y')
    elif dat == 6:
        proxy = datta + timedelta(1)
        dtt = proxy.strftime('%d-%m-%Y')

    # print('datta',dat,  dtt)
    return dtt


def make_send_data():
    data = read_json_wb()
    print('make_send_data_wb', len(data), data)
    warehouse = {}
    for string in wh:
        stocks = []
        w_house = string['id']
        warehouse[w_house] = {'stocks': stocks}
        for row in data:
            barcode = row[2]
            sku = compare_id.get(row[1], barcode)  # barcode WB
            if sku is not None and string['name_1C'] in row[4].keys():
                proxy = {
                    'sku': sku,
                    'amount': row[3]
                }
                stocks.append(proxy)
            elif sku is None:
                print('ERROR_sku_WB', sku, row[1])

        warehouse[w_house] = {'stocks': stocks}

    print('warehouse[730558]', len(warehouse[730558]['stocks']))  # ,warehouse[730558])
    print('warehouse[664706]', len(warehouse[664706]['stocks']))  # , warehouse[664706])
    # print(warehouse.keys())
    return warehouse


# make_send_data()

def send_stocks_wb():
    data = make_send_data()
    for key, value in data.items():
        metod = '/api/v3/stocks/'
        target = link + metod + str(key)
        headers = {'Content-type': 'application/json',
                   'Authorization': wb_apikey}
        print('SEND_WB', key, len(value['stocks']))
        answer = requests.put(target, data=json.dumps(value), headers=headers)
        re_data = answer.text

        # print('send_stocks_wb', key, re_data, len(value['stocks']), value)


# send_stocks_wb()


# def check_is_exist(id_mp, shop):
#     data = check_order(query_read_order, (id_mp, shop))
#     print(data, id_mp, shop)
#     if len(data) > 0:
#         result = True
#     else:
#         result = False
#
#     return result


def get_new_supply_wb(next):
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey}
    params = {
        "next": next,  # 0
        "limit": 500
    }
    metod = '/api/v3/supplies'
    url = link + metod
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    next_page = data['next']  # 32899717
    print('get_new_supply_wb', response, data)
    return response, data, next_page


# get_new_supply_wb()
# https://suppliers-api.wildberries.ru/api/v3/supplies/{supply}/orders


def get_orders_from_supply_wb(supply_id):
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey}

    metod = '/api/v3/supplies/' + str(supply_id) + '/orders'
    url = link + metod
    response = requests.get(url, headers=headers)
    data = response.json()

    print('get_orders_from_supply_wb', response, len(data), data)
    return response, data



def get_new_orders_wb(shop_name=None, company_id=None):
    stmt = select(Marketplaces.key_mp, Marketplaces.shop_id) \
        .where(Marketplaces.shop_name == shop_name).where(Marketplaces.company_id == company_id)
    with Session(engine) as session:
        wb_apikey = session.execute(stmt).first()
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey[0]}

    metod = '/api/v3/orders/new'
    url = link + metod
    response = requests.get(url, headers=headers)
    data = {}
    if response.ok:
        data = response.json()
        print('ALL_RIDE_get_new_orders_wb', response, len(data), data)
        return response.status_code, data
    else:
        print('FUCK_UP_get_new_orders_wb ', response.status_code, 'response', response.text)
        return response.status_code, response.text


async def get_id_1c(vendor_code):
    data = read_json_ids()
    if vendor_code in data.keys():
        id_1c = data[vendor_code][0]

        return id_1c


async def processing_orders_wb(shop_name=None, company_id=None):
    # orders = proxy_wb_orders["orders"]    # FOR TEST ONLY TODO
    data = get_new_orders_wb(shop_name=shop_name, company_id=company_id)
    if data[0] == 200:
        orders = data[1].get("orders")
        for order in orders:
            id_mp = str(order["id"])
            our_id = token_generator()
            check = check_is_exist(id_mp, shop_name)
            if check:
                continue
            else:
                shipment_Date = proxy_time_1()  # order["createdAt"] #TODO plus 1 day?
                status = "CREATED"
                our_status = "NEW"
                payment_Type = "PREPAID"
                delivery = order.get("deliveryType", 'Not_Know')
                # list_items = order["skus"]
                summ_order = order["price"] / 100
                vendor_code = order["article"]
                quantity = order.get("quantity", 1)
                id_1c = await get_id_1c(vendor_code)
                result = (id_mp, our_id, shop_name, shipment_Date,
                          status, our_status, payment_Type, delivery)
                await execute_query(query_write_order, result)
                items_data = (id_mp, our_id, shop_name, "NEW", vendor_code,
                              id_1c, quantity, summ_order)
                print('items_data_WB', items_data)
                await executemany_query(query_write_items, [items_data])
        print(f"Write {len(orders)} orders WB")
        return "Write {} orders WB".format(len(orders))

    else:
        print("Error ger orders WB by {} to {}".format(data[0], data[1]))
        return "Error ger orders WB by {} to {}".format(data[0], data[1])



asyncio.run(processing_orders_wb(shop_name='Полиция Вкуса', company_id='AdminTheRock'))

def get_wh():
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey}
    link = 'https://suppliers-api.wildberries.ru/api/v2/warehouses'
    answer = requests.get(link, headers=headers)
    text = answer.text
    # print(answer)
    print('get_wh', text)

# get_wh()
