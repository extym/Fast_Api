import asyncio
import json
import os

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from project.models import *
from project import engine
from project.creds import *
# from read_json import read_json_on
from time import sleep
from project import db

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
        print('post_get_smth_onon_v2', data.keys())
        return response.status_code, data
    else:
        print(response.text)
        return response.status_code, response.text


def post_get_smth(metod):
    link = host + metod
    response = requests.post(link, headers=headers)
    if response.ok:
        data = response.json()
        print('post_get_smth', data)  # (data['result']['items']), type(data['result']['items']))
        result = data['result']['items']
        total = data['result']['total']
        last_id = data['result']['last_id']
        print('post_get_smth_onon', result[0])
        return result, total, last_id
    else:
        print(response.text)
        return [], [], 0


def get_product_info(product_id, offer_id):
    metod = '/v2/product/info'
    link = host + metod
    data = {
        "offer_id": offer_id,
        "product_id": int(product_id),
        "sku": 0
    }
    response = requests.post(link, headers=header, json=data)
    answer = response.json()
    result = answer['result']["fbs_sku"]
    sleep(0.4)
    # print('get_product_info_onon', len(result)) #{'product_id': 38010832, 'offer_id': 'OWLT190601', 'is_fbo_visible': True, 'is_fbs_visible': True, 'archived': False, 'is_discounted': False}
    return result


def create_data_stocks():
    data_read = read_json_on()
    result = []
    stocks = []
    current_assortment = post_get_smth(metod_get_list_products)[0]
    for product in current_assortment:
        proxy = {}
        if product['offer_id'] in data_read.keys():
            proxy['offer_id'] = product['offer_id']
            proxy['product_id'] = product['product_id']
            proxy['stock'] = data_read[product['offer_id']][2]
            outlets = data_read[product['offer_id']][3]
            for wh in outlets:
                # if wh != 23012928587000:  # TODO for TEST only
                proxy['warehouse_id'] = wh
                pr = proxy.copy()
                stocks.append(pr)

                # if wh == 23012928587000:  # TODO for TEST only
                #     print('stocks', stocks)
    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
        # print('stocks', stocks)
    else:
        result.append(stocks)

    print('create_data_stocks_onon_x100', len(result))
    return result


def send_stocks_on():
    pre_data = create_data_stocks()
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row}
        # print('SEND_DATA', data)
        response = requests.post(link, headers=headers, json=data)
        answer = response.json()
        ans = response.text
        print('answer send_stocks_on', ans)
        result = answer.get("result")
        if result:
            for row in result:
                if len(row[
                           "errors"]) > 0:  # and row['warehouse_id'] != 23012928587000: #TODO temporary 'warehouse_id': 23012928587000
                    print('ERROR from send_stocks_ozon', row)
                elif row['updated'] == False:
                    print('ERROR update from send_stocks_ozon', row)
                elif row['updated'] == True:  # and row['warehouse_id'] != 23012928587000:
                    print('SUCCES update from send_stocks_on', row)
            proxy.append(answer)
        sleep(1)


def create_data_stocks_from_db(seller_id=None, is_stocks_null=False):
    result = []
    stocks = []
    if not is_stocks_null:
        with Session(engine) as session:
            data = session.query(Product) \
                .where(Product.quantity > 0) \
                .where(Product.store_id == seller_id) \
                .all()
            key = session.execute(select(Marketplaces.key_mp)
                                  .where(Marketplaces.seller_id == seller_id))\
                .first()
            outlets_data = post_smth_v2(get_wh_list, seller_id=seller_id, key=key[0])
            outlets = [i['warehouse_id'] for i in outlets_data[1].get('result') if outlets_data[0] == 200]
            for product in data:
                proxy = {
                    'offer_id': product.articul_product,
                    'product_id': product.external_sku,
                    'stock': product.quantity
                }
                for wh in outlets:
                    proxy['warehouse_id'] = wh
                    pr = proxy.copy()
                    stocks.append(pr)
    else:
        with Session(engine) as session:
            key = session.execute(select(Marketplaces.key_mp)
                                  .where(Marketplaces.seller_id == seller_id))\
                .first()
        outlets_data = post_smth_v2(get_wh_list, seller_id=seller_id, key=key[0])
        outlets = [i['warehouse_id'] for i in outlets_data[1].get('result') if outlets_data[0] == 200]
        data = post_smth_v2(metod_get_list_products, seller_id=seller_id, key=key[0])
        # print(77777, data[1].get('result'), data)
        if data[0] == 200:
            for product in data[1].get('result'):
                proxy = {
                    'offer_id': product['offer_id'],
                    'product_id': product['product_id'],
                    'stock': 0
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

    print('create_data_stocks_onon_x100', len(result))
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
            # key = session.execute(select(Marketplaces.key_mp)
            #                       .where(Marketplaces.seller_id == seller_id))\
            #     .first()

            for product in data:
                proxy.clear()
                proxy = {
                    "auto_action_enabled": "UNKNOWN",
                    "currency_code": "RUB",
                    "min_price": product.price,
                    "offer_id": product.articul_product,
                    "old_price": product.old_price,
                    "price": product.final_price,
                    "price_strategy_enabled": "UNKNOWN",
                    "product_id": product.external_sku
                }

    else:
        #get prices from oson
        print("From_db_false")

    while len(prices) >= 1000:
        result.append(prices[:1000])
        del prices[:1000]
    else:
        result.append(prices)

    print('create_data_prices_oson_x1000', len(result))
    return result


def create_data_price_for_send_v2(key_recipient=None, donor=None,
                                          recipient=None, from_db=True):
    result = []
    prices = []
    if from_db:
        with Session(engine) as session:
            data = session.query(Product) \
                .where(Product.final_price > 0) \
                .where(Product.store_id == donor) \
                .all()
            koef = session.execute(select(InternalImport.internal_import_markup_1)
                                  .where(InternalImport.internal_import_store_1 == donor) \
                                  .where(InternalImport.internal_import_store_2 == recipient)) \
                    .first()

            for product in data:
                proxy.clear()
                proxy = {
                    "auto_action_enabled": "UNKNOWN",
                    "currency_code": "RUB",
                    "min_price": product.price,
                    "offer_id": product.articul_product,
                    "old_price": product.old_price,
                    "price": product.final_price,
                    "price_strategy_enabled": "UNKNOWN",
                    "product_id": product.external_sku
                }

    else:
        #get prices from oson
        print("From_db_false")

    while len(prices) >= 1000:
        result.append(prices[:1000])
        del prices[:1000]
    else:
        result.append(prices)

    print('create_data_prices_oson_x1000', len(result))
    return result


def send_stocks_oson_v2(key=None, seller_id=None, is_stocks_null=False):
    pre_data = create_data_stocks_from_db(seller_id=seller_id,
                                          is_stocks_null=is_stocks_null)
    headers = {
        'Client-Id': seller_id,
        'Api-Key': key,
        'Content-Type': 'application/json'
    }
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row}
        response = requests.post(link, headers=headers, json=data)
        if answer.ok:
            answer = response.json()
            result = answer.get("result")
            if result:
                for row in result:
                    if len(row["errors"]) > 0:
                        print('ERROR from send_stocks_ozon', row)
                    elif row['updated'] == False:
                        print('ERROR update from send_stocks_ozon', row)
                    # elif row['updated'] == True:
                    #     print('SUCCES update from send_stocks_on', row)
                proxy.append(answer)
            sleep(0.7)
        else:
            ans = response.text
            print('answer send_stocks_on', ans)
            sleep(0.7)


def send_stocks_oson_v3(key_recipient=None, donor=None, recipient=None):
    pre_data = create_data_stocks_from_db(seller_id=donor,
                                          is_stocks_null=False)
    headers = {
        'Client-Id': recipient,
        'Api-Key': key_recipient,
        'Content-Type': 'application/json'
    }
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row}
        # os.abort()
        response = requests.post(link, headers=headers, json=data)
        if answer.ok:
            answer = response.json()
            result = answer.get("result")
            if result:
                for row in result:
                    if len(row["errors"]) > 0:
                        print('ERROR from send_stocks_ozon', row)
                    # elif row['updated'] == False:
                    #     print('ERROR update from send_stocks_ozon', row)
                    # elif row['updated'] == True:
                    #     print('SUCCES update from send_stocks_on', row)
                proxy.append(answer)
            sleep(0.7)
        else:
            ans = response.text
            print('answer send_stocks_on', ans)
            sleep(0.7)


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
            for line in result:
                if not line.get('updated'):
                    errors +=1
                    print('product_NOT_UPDATED_offer_id {} {}'
                          .format(line.get('offer_id'), recipient))
                else:
                    count += 1

        else:
            print('Some_trouble_from_export_price_oson {} {}'
                  .format(recipient, resp.text))

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
# create_data_stocks_from_db(seller_id="1278621", is_stocks_null=True)