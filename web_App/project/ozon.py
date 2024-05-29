import asyncio
import datetime
import json
import logging
import os

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from project.models import *
from project import engine, bot_tg
# from project.creds import *
# from read_json import read_json_on
from time import sleep
# from project import db
from project.conn import maintenans_query

LOG_DIR = os.getcwd() + '/logs'
# logging.basicConfig(level=logging.DEBUG, filename=LOG_DIR + '/oson_log.log',
#                     format="%(asctime)s %(levelname)s %(message)s")
print(os.getcwd())

# получение пользовательского логгера и установка уровня логирования
oson_logger = logging.getLogger("oson")
oson_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
try:
    py_handler = logging.FileHandler("./project/logs/oson.log", mode='a')
except:
    py_handler = logging.FileHandler(LOG_DIR + '/oson.log', mode='a')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
oson_logger.addHandler(py_handler)

common_error = {
    "error": {
        "code": "ERROR_UNKNOWN",
        "message": "ошибка",
        "details": None
    }
}

host = 'https://api-seller.ozon.ru'

last_id = 'custom_last_id'

metod_get_list_products = '/v2/product/list'
get_wh_list = '/v1/warehouse/list'


def write_json_skus(smth_json):
    try:
        with open('/var/www/html/stm/onon_skus.json', 'w') as file:
            json.dump(smth_json, file)
    except Exception:
        with open('onon_skus.json', 'w') as file:
            json.dump(smth_json, file)


def get_smth(metod):
    # params = {
    #     'Client-Id': client_id,
    #     'Api-Key': api_key_oson_admin,
    #     'Content-Type': 'application/json'
    # }
    link = host + metod
    response = requests.get(link)
    print('get_smth_on', metod, response, response.json())
    return response


def post_smth_v2(metod, seller_id=None, key=None):
    headers = {
        'Client-Id': seller_id,
        'Api-Key': key,
        'Content-Type': 'application/json'
    }
    link = host + metod
    response = requests.post(link, headers=headers)
    if response.ok:
        data = response.json()
        oson_logger.info("ALL RIDE From post smth - metod {}, seller_id {}, len_key {}, len data.result {}"
                         .format(metod, seller_id, len(key), len(data.get('result'))))
        print('post_get_smth_onon_v2', data.get('result'))
        return response.status_code, data
    else:
        oson_logger.info("ERROR From post smth - metod {}, seller_id {}, len_key {}, answer {}"
                         .format(metod, seller_id, len(key), response.text))
        # bot_tg.send_get("ERROR From post smth - metod {}, seller_id {}, answer {}"
        #                 .format(metod, seller_id, response.text))
        print('post_get_smth_onon_v2 {}'.format(response.text))
        return response.status_code, response.text


# post_smth_v2(get_wh_list, seller_id="1179095", key="19cb01e0-4098-4587-b0ec-55c5c60b830c")

# def post_get_smth(metod):
#     link = host + metod
#     response = requests.post(link, headers=headers)
#     if response.ok:
#         data = response.json()
#         print('post_get_smth', data)  # (data['result']['items']), type(data['result']['items']))
#         result = data['result']['items']
#         total = data['result']['total']
#         last_id = data['result']['last_id']
#         print('post_get_smth_onon', result[0])
#         return result, total, last_id
#     else:
#         print(response.text)
#         return [], [], 0


# def get_product_info(product_id, offer_id):
#     metod = '/v2/product/info'
#     link = host + metod
#     data = {
#         "offer_id": offer_id,
#         "product_id": int(product_id),
#         "sku": 0
#     }
#     response = requests.post(link, headers=header, json=data)
#     answer = response.json()
#     result = answer['result']["fbs_sku"]
#     sleep(0.4)
#     # print('get_product_info_onon', len(result)) #{'product_id': 38010832, 'offer_id': 'OWLT190601', 'is_fbo_visible': True, 'is_fbs_visible': True, 'archived': False, 'is_discounted': False}
#     return result


# def create_data_stocks():
#     data_read = read_json_on()
#     result = []
#     stocks = []
#     current_assortment = post_get_smth(metod_get_list_products)[0]
#     for product in current_assortment:
#         proxy = {}
#         if product['offer_id'] in data_read.keys():
#             proxy['offer_id'] = product['offer_id']
#             proxy['product_id'] = product['product_id']
#             proxy['stock'] = data_read[product['offer_id']][2]
#             outlets = data_read[product['offer_id']][3]
#             for wh in outlets:
#                 proxy['warehouse_id'] = wh
#                 pr = proxy.copy()
#                 stocks.append(pr)
#
#     while len(stocks) >= 100:
#         result.append(stocks[:100])
#         del stocks[:100]
#         # print('stocks', stocks)
#     else:
#         result.append(stocks)
#
#     print('create_data_stocks_onon_x100', len(result))
#     return result


# def send_stocks_on():
#     pre_data = create_data_stocks()
#     metod = '/v2/products/stocks'
#     link = host + metod
#     proxy = []
#     for row in pre_data:
#         data = {'stocks': row}
#         # print('SEND_DATA', data)
#         response = requests.post(link, headers=headers, json=data)
#         answer = response.json()
#         ans = response.text
#         print('answer send_stocks_on', ans)
#         result = answer.get("result")
#         if result:
#             for row in result:
#                 if len(row[
#                            "errors"]) > 0:
#                     print('ERROR from send_stocks_ozon', row)
#                 elif row['updated'] == False:
#                     print('ERROR update from send_stocks_ozon', row)
#                 elif row['updated'] == True:  # and row['warehouse_id'] != 23012928587000:
#                     print('SUCCES update from send_stocks_on', row)
#             proxy.append(answer)
#         sleep(1)


def create_data_stocks_from_db_v2(seller_id=None, is_stocks_null=False):
    result = []
    stocks = []
    print('{} SELLER_create_data_stocks seller_id {}, is_stocks_null {}'
          .format(datetime.datetime.now(), seller_id, is_stocks_null))

    with Session(engine) as session:
        key = session.scalars(select(Marketplaces.key_mp)
                              .where(Marketplaces.seller_id == seller_id)) \
            .first()
        print('SELLER_2 {}, key {}, type key {}'.format(seller_id, key, type(key)))

    outlets_data = post_smth_v2(get_wh_list, seller_id=seller_id, key=key)
    outlets = [i['warehouse_id'] for i in outlets_data[1].get('result') if outlets_data[0] == 200]

    data = session.query(Product) \
        .where(Product.quantity > 0) \
        .where(Product.store_id == seller_id) \
        .all()

    for product in data:
        if not is_stocks_null:
            quantity = product.quantity
        else:
            quantity = "0"
        proxy = {
            'offer_id': product.articul_product,
            'product_id': product.external_sku,
            'stock': quantity
        }
        for wh in outlets:
            proxy['warehouse_id'] = wh
            pr = proxy.copy()
            stocks.append(pr)

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
    else:
        result.append(stocks)

    oson_logger.info("From create_data_stocks_oson x100 - seller_id {}, is_stocks_null {}, len result {}"
                     .format(seller_id, is_stocks_null, len(result)))
    print('create_data_stocks_oson_x100', len(result))
    return result


def create_data_stocks_from_db_v3(donor_name=None,
                                  recip_id=None, is_stocks_null=False):
    result = []
    stocks = []
    print('{} SELLER_ID_create_data_stocks donor_name {},'
          ' recip_id {},  is_stocks_null {}'
          .format(datetime.datetime.now(), donor_name, recip_id, is_stocks_null))
    with Session(engine) as session:
        key = session.scalars(select(Marketplaces.key_mp)
                                          .where(Marketplaces.seller_id == recip_id)) \
            .first()

        print('{} SELLER_ID_1 key {}, seller_id {}'
              .format(datetime.datetime.now(), key, recip_id))

    outlets_data = post_smth_v2(get_wh_list, seller_id=recip_id, key=key)
    outlets = [i['warehouse_id'] for i in outlets_data[1].get('result') if outlets_data[0] == 200]
    print()
    data = session.query(Product) \
        .where(Product.quantity > 0) \
        .where(Product.shop_name == donor_name) \
        .all()

    for product in data:
        if not is_stocks_null:
            quantity = product.quantity
        else:
            quantity = "0"
        proxy = {
            'offer_id': product.articul_product,
            'product_id': product.external_sku,
            'stock': quantity
        }
        for wh in outlets:
            proxy['warehouse_id'] = wh
            pr = proxy.copy()
            stocks.append(pr)

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
    else:
        result.append(stocks)

    oson_logger.info("From create_data_stocks_oson x100 - seller_id {}, is_stocks_null {}, len result {}"
                     .format(recip_id, is_stocks_null, len(result)))
    print('create_data_stocks_oson_x100', len(result))
    return result


def create_data_price_for_send(seller_id=None, from_db=True):
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
            print('KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKk', koeff, seller_id, type(seller_id))
            for product in data:
                #############################
                # TODO make func custom price oson
                # Make price ended for '9'
                pre_price = int(product.price_product_base) * 2
                price = str(pre_price).split('.')[0][:-1] + "9"
                # print(22222, price, pre_price)
                if not koeff:
                    koeff = 0
                if koeff > 0:
                    final_price = int(price) * (1 + int(koeff) / 100)
                    final_price = str(final_price).split('.')[0]
                else:
                    final_price = price
                old_price = str(int(price) * 4)
                ##############################
                proxy = {
                    "auto_action_enabled": "UNKNOWN",
                    "currency_code": "RUB",
                    "min_price": final_price,
                    "offer_id": product.articul_product,
                    "old_price": old_price,
                    "price": final_price,
                    "price_strategy_enabled": "UNKNOWN",
                    "product_id": product.product_id
                }
                print("Make data price - seller_id {},  data price {}, k={}"
                      .format(seller_id, proxy, koeff))
                prices.append(proxy)

    else:
        # get prices from oson
        print("From_db_false")

    while len(prices) >= 1000:
        result.append(prices[:1000])
        del prices[:1000]
    else:
        result.append(prices)

    oson_logger.info("From create_data_prices_oson_x1000 - seller_id {}, make from_db {}, len result {}"
                     .format(seller_id, from_db, len(result)))
    print('create_data_prices_oson_x1000', len(result))
    return result


def create_data_price_for_send_v2(koef_recipient=None, donor=None,
                                  recipient=None, from_db=True):
    result = []
    prices = []
    if from_db:
        with Session(engine) as session:
            data = session.query(Product) \
                .where(Product.final_price > 0) \
                .where(Product.store_id == donor) \
                .all()
            # koef_recipient = session.execute(select(InternalImport.internal_import_markup_1)
            #                        .where(InternalImport.internal_import_store_1 == donor) \
            #                        .where(InternalImport.internal_import_store_2 == recipient)) \
            #     .first()

            for product in data:
                #############################3
                # Make price ended for '9'
                price = int(product.final_price) * (1 + int(koef_recipient) / 100)
                final_price = str(price).split('.')[0][:-1] + "9"
                old_price = str(int(price) * 4)
                ##############################
                proxy = {
                    "auto_action_enabled": "UNKNOWN",
                    "currency_code": "RUB",
                    "min_price": final_price,
                    "offer_id": product.articul_product,
                    "old_price": old_price,
                    "price": final_price,
                    "price_strategy_enabled": "UNKNOWN",
                    "product_id": product.product_id
                }
                prices.append(proxy)

    else:
        # get prices from oson
        print("From_db_false")

    while len(prices) >= 1000:
        result.append(prices[:1000])
        del prices[:1000]
    else:
        result.append(prices)

    oson_logger.info("From create_data_prices_for_send_v2_oson_x1000 -"
                     " donor {}, k_resip={}, make from_db {}, len result {}"
                     .format(donor, koef_recipient, from_db, len(result)))
    print('create_data_prices_for_send_v2_oson_x1000', len(result))
    return result


def send_stocks_oson_v2(key=None, seller_id=None, is_stocks_null=False):
    pre_data = create_data_stocks_from_db_v2(seller_id=seller_id,
                                             is_stocks_null=is_stocks_null)
    headers = {
        'Client-Id': seller_id,
        'Api-Key': key,
        'Content-Type': 'application/json'
    }
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    count, error = 0, 0
    for row in pre_data:
        data = {'stocks': row}
        response = requests.post(link, headers=headers, json=data)
        if response.ok:
            answer = response.json()
            result = answer.get("result")
            if result:
                for row in result:
                    if len(row["errors"]) > 0:
                        # print('ERROR from send_stocks_ozon', row)
                        error += 1
                    # elif row['updated'] == False:
                    # print('ERROR update from send_stocks_ozon', row)
                    elif row['updated'] == True:
                        count += 1
                    #     print('SUCCES update from send_stocks_on', row)
                proxy.append(answer)

            logging.info('All Ride Send_stocks_oson_v2 - seller_id {}, is_stocks_null {},'
                          ' len key {}, updated {}, errors {}.'
                          .format(seller_id, is_stocks_null, len(key), count, error))
            sleep(0.6)
        else:
            logging.info('Trouble_stocks_oson_v2 - seller_id {}, is_stocks_null {},'
                          ' len key {}, updated {}, errors {}, answer {}'
                          .format(seller_id, is_stocks_null, len(key), count, error, response.text))
            print('answer send_stocks_oson_v2', response.text)
            sleep(0.6)


def send_stocks_oson_v3(key_recipient=None, donor_name=None, recipient=None):
    print('SEND_STOCK_OSON_start_v3 len key {}, recipient {}, donor_name {}'
          .format(key_recipient, recipient, donor_name))
    pre_data = create_data_stocks_from_db_v3(donor_name=donor_name,
                                             recip_id=recipient,
                                             is_stocks_null=False)
    headers = {
        'Client-Id': recipient,
        'Api-Key': key_recipient,
        'Content-Type': 'application/json'
    }
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    count, error = 0, 0
    for row in pre_data:
        data = {'stocks': row}
        # os.abort()
        response = requests.post(link, headers=headers, json=data)
        if response.ok:
            answer = response.json()
            result = answer.get("result")
            if result:
                for row in result:
                    if len(row["errors"]) > 0:
                        # print('ERROR from send_stocks_ozon', row)
                        error += 1
                    # elif row['updated'] == False:
                    #     print('ERROR update from send_stocks_ozon', row)
                    elif row['updated']:
                        count += 1
                    #     print('SUCCES update from send_stocks_on', row)
                proxy.append(answer)
            oson_logger.info('ALL RIDE send_stocks_oson - answer {}, donor {},'
                             ' recipient {}, updated {}, errors update {}'
                             .format(response.text, donor_name, recipient, count, error))
            sleep(0.6)
        else:

            oson_logger.info('Error send_stocks_oson - answer {}, donor {},'
                             ' recipient {}, len key_recip {}'
                             .format(response.text, donor_name, recipient, len(key_recipient)))
            print('answer send_stocks_on_v3', response.text)
            sleep(0.6)


def send_product_price(key_recipient=None, recipient=None):
    metod = 'https://api-seller.ozon.ru/v1/product/import/prices'
    #   "limit": 1000
    headers = {
        'Client-Id': recipient,
        'Api-Key': key_recipient,
        'Content-Type': 'application/json'
    }
    data = create_data_price_for_send(seller_id=recipient, from_db=True)
    count, errors = 0, 0
    for row in data:
        send_data = {"prices": row}
        resp = requests.post(url=metod, headers=headers, json=send_data)
        if resp.ok:
            result = resp.json()
            for line in result.get('result'):
                if not line.get('updated'):
                    errors += 1
                    # print('product_NOT_UPDATED_offer_id {} {}'
                    #       .format(line.get('offer_id'), recipient))
                else:
                    count += 1
            oson_logger.info('product_UPDATED_price_offer_id '
                             'recipient {}, errors {}, count {}'
                             .format(recipient, errors, count))

        else:
            oson_logger.info('Some_trouble_from_export_price_oson -'
                             ' recipient {}, answer {}, len data {}'
                             .format(recipient, resp.text, len(data)))

    return count, errors

# get_product_info(38010832, "OWLT190601")
# with app.app_context():
#     product_info_price("463727127", "OWLC19-014")
# send_stocks_on()
# asyncio.run(post_send_stocks())
# create_data_stocks()

# def convert(string):
#     data = json.dumps(string)
#     print(data)
# # pr = [{'id': 'MP1703473-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703472-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703471-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}]
# pr = {'message_type': 'TYPE_NEW_POSTING', 'seller_id': 90963, 'warehouse_id': 1020000075732000, 'posting_number': '13223249-0059-1', 'in_process_at': '2023-03-18T03:56:36Z', 'products': [{'sku': 789880982, 'quantity': 1}]}
# convert(pr)

# asyncio.run(create_data_stocks())
# create_data_stocks_from_db(seller_id="1278621", is_stocks_null=False)
# create_data_price_for_send(seller_id="1278621", from_db=True)