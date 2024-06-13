import logging
import time
from datetime import datetime, timedelta
import random
import string
import asyncio

import sqlalchemy
from sqlalchemy import insert, create_engine, select, update, text
from sqlalchemy.orm import Session

from project.models import Marketplaces, Product, Sales, SalesToday
from psycopg2.extensions import register_adapter, AsIs
import requests
import json
from project import engine
from project.bot_tg import send_get
from project.conn import *

# data = read_json_wb()
# https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}
link = 'https://suppliers-api.wildberries.ru'
l = 'https://suppliers-api.wildberries.ru/api/v3/supplies'


# wh = [{"name": "Обычный склад СТМ", "id": 664706, "name_1C": "WB.НашсклСТМ"},
#       {"name": "Сверхгабаритный товар", "id": 730558, "name_1C": "WB.СверхГБсклNEW"}]  # ,


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


def day_for_stm(time_string):
    datta = datetime.strptime(time_string, '%Y-%m-%d')
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


def get_wh(key=None):
    headers = {'Content-type': 'application/json',
               'Authorization': key}
    link = 'https://suppliers-api.wildberries.ru/api/v2/warehouses'
    answer = requests.get(link, headers=headers)
    if answer.ok:
        print('get_wh', answer.json())
        return answer.status_code, answer.json()
    else:
        print('errot_get_wh', answer.text)
        return answer.status_code, answer.text


def get_curent_stocks(key=None, warehouse_id=None):
    headers = {'Content-type': 'application/json',
               'Authorization': key}
    link = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse_id}'
    answer = requests.get(link, headers=headers)
    if answer.ok:
        print('get_wh', answer.json())
        return answer.status_code, answer.json()
    else:
        print('errot_get_wh', answer.text)
        return answer.status_code, answer.text


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


def make_send_data_stocks_v2(key=None, seller_id=None, is_stocks_null=False):
    warehouse = {}
    outlets_data = get_wh(key=key)
    outlets = [i['id'] for i in outlets_data[1] if outlets_data[0] == 200]
    if not is_stocks_null:
        with Session(engine) as session:
            data = session.query(Product) \
                .where(Product.quantity > 0) \
                .where(Product.store_id == seller_id) \
                .all()
            # TODO fix it - products maybe in to different warehouses
            # все товары на все склады
            for w_house in outlets:
                stocks = []
                for row in data:
                    proxy = {
                        'sku': row.external_sku,
                        'amount': row.quantity
                    }
                    stocks.append(proxy)

            warehouse[w_house] = {'stocks': stocks}
    else:
        for w_house in outlets:
            stocks = []
            data = get_curent_stocks(key=key, warehouse_id=w_house)
            if data[0] == 200:
                for row in data[1].get('stocks'):
                    proxy = {
                        'sku': row.get('sku'),
                        'amount': 0
                    }
                    stocks.append(proxy)

            warehouse[w_house] = {'stocks': stocks}

            print('warehouse-', w_house, len(warehouse[w_house]['stocks']))

    print(warehouse.keys())
    return warehouse


def make_send_data_stocks_v3(key_wh_recip=None, seller_id=None):
    warehouse = {}
    outlets_data = get_wh(key=key_wh_recip)
    outlets = [i['id'] for i in outlets_data[1] if outlets_data[0] == 200]

    with Session(engine) as session:
        data = session.query(Product) \
            .where(Product.quantity > 0) \
            .where(Product.store_id == seller_id) \
            .all()
        # TODO fix it - products maybe in to different warehouses
        # все товары на все склады
        for w_house in outlets:
            stocks = []
            for row in data:
                proxy = {
                    'sku': row.external_sku,
                    'amount': row.quantity
                }
                stocks.append(proxy)

        warehouse[w_house] = {'stocks': stocks}

    print(warehouse.keys())
    return warehouse


def create_data_price_for_send_wb(seller_id=None, from_db=True):
    result = []
    prices = []
    if from_db:
        with Session(engine) as session:
            data = session.query(Product) \
                .where(Product.quantity > 0) \
                .where(Product.store_id == seller_id) \
                .all()
            koeff = session.scalars(select(Marketplaces.store_markup)
                                    .where(Marketplaces.seller_id == seller_id)) \
                .first()
            # print(koeff)
            for product in data:
                #############################
                # TODO make func custom price WB
                # Make price ended for '9'
                discount = int(product.discount)
                pre_price = int(product.price_product_base) * 2
                price = str(pre_price).split('.')[0][:-1] + "9"
                if discount > 0:
                    next_price = int(price) + int(price) * (discount + 5) / 100
                else:
                    next_price = int(price) + int(price) * 5 / 100
                final_price = next_price * 100 / int(koeff)
                ##############################
                proxy = {
                    "nmID": product.external_sku,
                    "price": final_price,
                    "discount": product.discount
                }
                prices.append(proxy)

    else:
        # get prices from oson
        print("price_From_db_false")

    while len(prices) >= 1000:
        result.append(prices[:1000])
        del prices[:1000]
    else:
        result.append(prices)

    print('create_data_prices_oson_x1000', len(result))
    return result


def send_price_to_wb(seller_id=None, sourse=None):
    api_key = ''
    with Session(engine) as session:
        session.begin()
        data_keys = session.scalars(select(Marketplaces)
                                    .where(Marketplaces.seller_id == seller_id) \
                                    .where(Marketplaces.name_mp == "wb")) \
            .all()
    for datas in data_keys:
        if 'Цены и скидки' in datas.tags:
            api_key = datas.key_mp
        else:
            print('!!!!!!!!!!_api_key_ERROR seller_id {}, key tags {}'
                  .format(seller_id, datas.tags))
            return "Error in cred keys"

    if sourse is None:
        os.abort()
    else:
        data = create_data_price_for_send_wb(seller_id=seller_id)
        for row in data:
            metod = f'https://discounts-prices-api.wb.ru/api/v2/upload/task'
            headers = {'Content-type': 'application/json',
                       'Authorization': api_key}
            send_data = {
                'data': row
            }
            answer = requests.put(metod, data=json.dumps(send_data), headers=headers)
            if answer.ok:
                print('All_ride_send to WB - wh {} stocks {}'
                      .format(seller_id, len(data)))
                send_get("Отправлено цены селлеру {}: удачно  из {} доступных."
                         .format(seller_id, len(data)))

            else:
                print('All_ride_send to WB - wh {} stocks {} - result {}'
                      .format(seller_id, len(data), answer.text))
                send_get("НЕ отправлено цены селлеру {}: удачно  из {} доступных - result {}."
                         .format(seller_id, len(data), answer.text))


def make_import_export_wb_price(donor=None, recipient=None,
                                  k=1):
    if donor is not None and recipient is not None:
        data = []
        with Session(engine) as session:
            session.begin()
            recipient_data = session.execute(select(Marketplaces.seller_id,
                                                    Marketplaces.key_mp)
                                             .where(Marketplaces.shop_name == recipient)) \
                .first()
            product_data = session.query(Product).filter_by(shop_name=donor).all()

        if product_data:
            for row in product_data:
                # print(22222, row )
                #############################
                # TODO is need it is for wb separately ?
                # Make price ended for '9'
                price = int(row.final_price) * (1 + int(k) / 100)
                price = str(price).split('.')[0][:-1] + "9"
                old_price = str(int(price) * 4)
                ##############################3
                item = {
                    'final_price': price,
                    'old_price': old_price,
                    "date_modifed": datetime.now()
                }

                with Session(engine) as session:
                    session.begin()
                    session.execute(update(Product)
                                    .where(Product.articul_product == row.articul_product)
                                    .where(Product.shop_name == recipient).values(item))
                    session.commit()


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


def send_stocks_wb_v2(seller_id=None, is_stocks_null=None, sourse=None):
    api_key = ''
    with Session(engine) as session:
        session.begin()
        data_keys = session.scalars(select(Marketplaces)
                                    .where(Marketplaces.seller_id == seller_id) \
                                    .where(Marketplaces.name_mp == "wb")) \
            .all()
    for datas in data_keys:
        if 'Маркетплейс' in datas.tags:
            api_key = datas.key_mp
        else:
            print('!!!!!!!!!!_api_key_ERROR seller_id {}, key tags {}'
                  .format(seller_id, datas.tags))
            return "Error in cred keys"

    if sourse is None:
        os.abort()
    else:
        data = make_send_data_stocks_v2(key=api_key, seller_id=seller_id,
                                        is_stocks_null=is_stocks_null)
        for wh_id, value in data.items():
            metod = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{wh_id}'
            headers = {'Content-type': 'application/json',
                       'Authorization': api_key}
            print('SEND_WB', wh_id, len(value['stocks']))
            answer = requests.put(metod, data=json.dumps(value), headers=headers)
            if answer.ok:
                print('All_ride_send to WB - wh {} stocks {}'
                      .format(wh_id, len(wh_id)))
            else:
                print('All_ride_send to WB - wh {} stocks {} - result {}'
                      .format(wh_id, len(wh_id), answer.text))

# send_stocks_wb_v2(seller_id='admin100500')

def send_stocks_wb_v3(donor=None, recipient=None):
    key_wh_recip, key_recipient = '', ''
    with Session(engine) as session:
        session.begin()
        data_keys = session.execute(select(Marketplaces)
                                    .where(Marketplaces.shop_name == recipient) \
                                    .where(Marketplaces.name_mp == "wb")) \
            .all()
    for datas in data_keys:
        if 'Маркетплейс' in datas.tags:
            key_wh_recip = datas.mp_key
            key_recipient = datas.mp_key

    if key_wh_recip != ''  and key_recipient != '':
        data = make_send_data_stocks_v3(key_wh_recip=key_wh_recip, seller_id=donor)
        for wh_id, value in data.items():
            metod = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{wh_id}'
            headers = {'Content-type': 'application/json',
                       'Authorization': key_recipient}
            print('SEND_WB', wh_id, len(value['stocks']))
            answer = requests.put(metod, data=json.dumps(value), headers=headers)
            if answer.ok:
                print('All_ride_send to WB - wh {} stocks {}'
                      .format(wh_id, len(wh_id)))
            else:
                print('All_ride_send to WB - wh {} stocks {} - result {}'
                      .format(wh_id, len(wh_id), answer.text))
    else:
        logging.error("Some error with keys from send_stocks_wb_v3 - donor {}, res {}"
                      .format(donor, recipient))


def check_is_exist(id_mp, shop):
    data = check_order(query_read_order, (id_mp, shop))
    print(data, id_mp, shop)
    if len(data) > 0:
        result = True
    else:
        result = False

    return result


def check_is_exist_v2(id_mp, shop):
    result = False
    with Session(engine) as session:
        session.begin()
        data = session.execute(select(SalesToday.id)
                               .where(SalesToday.mp_order_id == id_mp)
                               .where(SalesToday.shop_name == shop)
                               ).first()
    if len(data) > 0:
        result = True

    return result


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

    elif response.status_code == 403:
        print('ERROR_get_new_orders_wb {} response {}'
              .format(response.status_code, response.text))
        send_get('Ошибка получения заказов с WB {} response {}.'
                 'Проверьте корректность сохраненного ключа API.'
                 .format(response.status_code, response.text))
        return response.status_code, response.text

    else:
        print('ERROR_get_new_orders_wb {} response {}'
              .format(response.status_code, response.text))
        send_get('Ошибка получения заказов с WB {} response {}.'
                 .format(response.status_code, response.text))
        return response.status_code, response.text


def get_new_orders_wb_v2(key=None):
    headers = {'Content-type': 'application/json',
               'Authorization': key}

    metod = '/api/v3/orders/new'
    url = link + metod
    response = requests.get(url, headers=headers)
    data = {}
    if response.ok:
        data = response.json()
        print('ALL_RIDE_get_new_orders_wb', response, len(data), data)
        return response.status_code, data

    elif response.status_code == 403:
        print('ERROR_get_new_orders_wb {} response {}'
              .format(response.status_code, response.text))
        send_get('Ошибка получения заказов с WB {} response {}.'
                 'Проверьте корректность сохраненного ключа API.'
                 .format(response.status_code, response.text))
        return response.status_code, response.text

    else:
        print('ERROR_get_new_orders_wb {} response {}'
              .format(response.status_code, response.text))
        send_get('Ошибка получения заказов с WB {} response {}.'
                 .format(response.status_code, response.text))
        return response.status_code, response.text


async def get_id_1c(vendor_code):
    data = read_json_ids()
    if vendor_code in data.keys():
        id_1c = data[vendor_code][0]

        return id_1c


def get_id_1c_v2(vendor_code, shop_name):
    id_1c = None
    with Session(engine) as session:
        Session.begin()
        data = session.execute(select(Product.id_1c)
                               .where(Product.articul_product == vendor_code)
                               .where(Product.shop_name == shop_name)
                               ).first()

    if len(data) > 0:
        id_1c = data[0]

    return id_1c


async def processing_orders_wb(shop_name=None, company_id=None):
    # orders = proxy_wb_orders["orders"]
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
                shipment_Date = proxy_time_1()  # order["createdAt"]
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


def processing_orders_wb_v2(shop_name=None, key=None):
    # orders = proxy_wb_orders["orders"]    # FOR TEST ONLY
    data = get_new_orders_wb_v2(key=key)
    if data[0] == 200:
        orders = data[1].get("orders")
        for order in orders:
            id_mp = str(order["id"])
            our_id = token_generator()
            check = check_is_exist(id_mp, shop_name)
            if check:
                continue
            else:
                shipment_Date = proxy_time_1()  # order["createdAt"]
                status = "CREATED"
                our_status = "NEW"
                payment_Type = "PREPAID"
                delivery = order.get("deliveryType", 'Not_Know')
                # list_items = order["skus"]
                summ_order = order["price"] / 100
                vendor_code = order["article"]
                quantity = order.get("quantity", 1)
                id_1c = get_id_1c_v2(vendor_code)
                article = order["article"]
                article_mp = order["skus"][0]
                result = (id_mp, our_id, shop_name, "wb", shipment_Date,
                          status, our_status, payment_Type, delivery)
                execute_query_v3(query_write_order, result)
                items_data = (id_mp, our_id, "wb", shop_name, "NEW", vendor_code,
                              id_1c, quantity, summ_order, article, article_mp)
                print('items_data_WB', items_data)
                executemany_query_v3(query_write_items_v2, [items_data])
        print(f"Write {len(orders)} orders WB")
        return "Write {} orders WB".format(len(orders))

    else:
        print("Error ger orders WB by {} to {}".format(data[0], data[1]))
        return "Error ger orders WB by {} to {}".format(data[0], data[1])


def run_processing_orders_wb():
    default_company_id = "AdminTheRock"  # TODO FIX magic name company
    with Session(engine) as session:
        session.begin()
        default_shop_name = session \
            .execute(select(Marketplaces.shop_name)
                     .where(Marketplaces.company_id == default_company_id)
                     .where(Marketplaces.name_mp == 'wb')
                     ).first()
        # TODO check is possible made TWO & more stores in WB
    if default_shop_name is not None:
        print(444444, default_shop_name, default_company_id)
        asyncio.run(processing_orders_wb(shop_name=default_shop_name[0],
                                         company_id=default_company_id))
    else:
        print("Some trouble get shop_name for WB {} {}"
              .format(default_company_id, default_shop_name))


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


def make_cart_id(shop_name=None, data=None):
    metod = 'https://suppliers-api.wildberries.ru/content/v2/cards/upload'
    query = select(Marketplaces.seller_id, Marketplaces.key_mp) \
        .where(Marketplaces.shop_name == shop_name)
    with Session(engine) as session:
        session.begin()
        seller_data = session.execute(query).first()


def adapt_dict(dict_var):
    return AsIs("'" + json.dumps(dict_var) + "'")


def import_product_from_wb(shop_name=None, company_id=None,
                           uid_edit_user=None, change_base_price=False):
    register_adapter(dict, adapt_dict)
    data = get_product_cards(shop_name=shop_name, company_id=company_id)[0]
    query = select(Marketplaces.seller_id, Marketplaces.key_mp) \
        .where(Marketplaces.shop_name == shop_name)
    with Session(engine) as session:
        session.begin()
        seller_data = session.execute(query).first()
    count = 0
    time_now = datetime.datetime.now()
    if data and not change_base_price:
        for data_prod in data:
            product = {
                'articul_product': str(data_prod.get("vendorCode")),
                'shop_name': shop_name,
                'store_id': seller_data[0],
                'quantity': data_prod.get("stocks"),
                'discount': 0.0,
                'description_product': data_prod.get("description"),
                'photo': data_prod.get("photos"),
                'id_1c': "",
                'date_added': time_now,
                'date_modifed': time_now,
                'selected_mp': 'wb',
                'name_product': data_prod.get("title"),
                'status_mp': 'enabled',
                'images_product': data_prod.get("photos")[0].get('square'),
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
                'barcode': data_prod.get("sizes")[0].get('skus'),
                'cart_id': data_prod.get("imtID"),
                'brand': data_prod.get("brand"),
                'brand_id': ""
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
                    update_prod = update(Product) \
                        .where(Product.articul_product == product.get('articul_product')) \
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

    elif data and change_base_price:
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
                'images_product': data_prod.get("photos")[0].get('square'),
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
                'barcode': data_prod.get("sizes")[0].get('skus'),
                'cart_id': data_prod.get("imtID"),
                'brand': data_prod.get("brand"),
                'brand_id': ""
            }

            count_error = 0
            with Session(engine) as session:
                session.begin()
                smth = insert(Product).values(product)
                try:
                    session.execute(smth)
                    time.sleep(0.1)
                    count += 1
                except sqlalchemy.exc.IntegrityError as error:
                    session.rollback()
                    session.begin()
                    update_prod = update(Product) \
                        .where(Product.articul_product == product.get('articul_product')) \
                        .where(Product.store_id == product.get('store_id')) \
                        .values(product)
                    session.execute(update_prod)
                    count_error += 1
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

# run_processing_orders_wb()
