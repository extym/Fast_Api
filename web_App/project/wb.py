import time
from datetime import datetime, timedelta
import random
import string
import asyncio

import sqlalchemy
from sqlalchemy import insert, create_engine, select, update, text
from sqlalchemy.orm import Session

from project.models import Marketplaces, Product
from psycopg2.extensions import register_adapter, AsIs
import requests
import json

from project.conn import *

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


def get_wh():
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey}
    link = 'https://suppliers-api.wildberries.ru/api/v2/warehouses'
    answer = requests.get(link, headers=headers)
    text = answer.text
    # print(answer)
    print('get_wh', text)


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
        .where(Marketplaces.shop_name == shop_name) \
        .where(Marketplaces.company_id == company_id)
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
        print('FUCK_UP_get_new_orders_wb {} response {}'
              .format(response.status_code, response.text))
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


def get_product_cards(shop_name=None, company_id=None):
    metod = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
    stmt = select(Marketplaces.key_mp, Marketplaces.shop_id) \
        .where(Marketplaces.shop_name == shop_name) \
        .where(Marketplaces.company_id == company_id)
    with Session(engine) as session:
        wb_apikey = session.execute(stmt).first()
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey[0]}
    limit = 1000
    proxy, count, error_caunt, message = [], 0, 0, 'Error'
    data = {
        "settings": {
            "cursor": {
                "limit": limit
            },
            "filter": {
                "withPhoto": -1
            }
        }
    }
    answer = requests.post(url=metod, headers=headers, json=data)
    if answer.ok:
        response = answer.json()
        cards = response.get('cards')
        cursor = response.get('cursor')
        proxy.extend(cards)
        message = 'Ok'
        while len(cards) >= limit:
            nm_id = cursor.get('nmID')
            update_at = cursor.get('updatedAt')
            data = {
                "settings": {
                    "cursor": {
                        "updatedAt": update_at,
                        "nmID": nm_id,
                        "limit": limit
                    },
                    "filter": {
                        "withPhoto": -1
                    }
                }
            }
            answer = requests.post(url=metod, headers=headers, json=data)
            if answer.ok:
                resp = answer.json()
                cards = resp.get('cards')
                cursor = resp.get('cursor')
                proxy.extend(cards)
                message = 'Ok'
                # print(222, len(cards), nm_id, cursor)
            else:
                count += 1
                print("We get some trouble from WB {}".format(answer.text))
                if count >= 10:
                    break

        else:
            proxy.extend(cards)

    else:
        error_caunt += 1
        print("We get some trouble from WB {}".format(answer.text, error_caunt))

    print('We get from WB {} cards'.format(len(proxy)))
    return proxy, message


def adapt_dict(dict_var):
    return AsIs("'" + json.dumps(dict_var) + "'")


def import_product_from_wb(shop_name=None, company_id=None, uid_edit_user=None):
    register_adapter(dict, adapt_dict)
    data = get_product_cards(shop_name=shop_name, company_id=company_id)[0]
    query = select(Marketplaces.seller_id, Marketplaces.key_mp)\
        .where(Marketplaces.shop_name == shop_name)
    with Session(engine) as session:
        session.begin()
        seller_data = session.execute(query).first()
    count = 0
    time_now = datetime.datetime.now()
    if data:
        for data_prod in data:
            product = {
                'articul_product': str(data_prod.get("vendorCode")),
                'shop_name': shop_name,
                'store_id': seller_data[0],
                'quantity': data_prod.get("stocks"),
                'price_product_base': '0',
                'discount': 0.0,
                'description_product': data_prod.get("description"),
                'photo': data_prod.get("photos"),
                'id_1c': "",
                'date_added': time_now,
                'date_modifed': time_now,
                'selected_mp': 'wb',
                'name_product': data_prod.get("title"),
                'status_mp': 'enabled',
                'images_product': data_prod.get("images"),
                'price_add_k': 0.0,
                'discount_mp_product': 0.0,
                'set_shop_name': data_prod.get("brand"),
                'external_sku': data_prod.get("nmID"),
                'alias_prod_name': data_prod.get("name"),
                'status_in_shop': data_prod.get("status"),
                'uid_edit_user': uid_edit_user,
                'final_price': data_prod.get('price'),
                'description_category_id': data_prod.get("subjectName"),
                'volume_weight': data_prod.get("sizes")[0].get('chrtID'),
                'type_id': data_prod.get("subjectID"),
                'barcode': data_prod.get("sizes")[0].get('skus')
            }

            count_error = 0
            with Session(engine) as session:
                session.begin()
                smth = insert(Product).values(product)
                # print(77777, smth)
                try:
                    session.execute(smth)
                    time.sleep(0.1)
                    count += 1
                    # print(555555555555)
                except sqlalchemy.exc.IntegrityError as error:
                    session.rollback()
                    session.begin()
                    update_prod = update(Product).where(Product.articul_product == product.get('articul_product')) \
                        .where(Product.store_id == product.get('store_id')) \
                        .values(product)
                    session.execute(update_prod)
                    count_error += 1
                    # print(22222222222222, count_error)
                finally:
                    session.commit()

            # os.abort()
            count += 1

        return 'Succes {}'.format(count)
    else:

        return 'Some trouble import {} {}'.format(shop_name, company_id)


# get_product_cards(shop_name='Полиция Вкуса', company_id='AdminTheRock')
# asyncio.run(processing_orders_wb(shop_name='Полиция Вкуса', company_id='AdminTheRock'))
# import_product_from_wb(shop_name='Полиция Вкуса', company_id='AdminTheRock', uid_edit_user=3)
# get_wh()
