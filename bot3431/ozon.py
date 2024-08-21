import asyncio
import csv
import json
import os
import time

import pandas
import requests
from cred import oson_key_admin_3431, oson_client_id_3431
# from read_json import read_json_on
from time import sleep

common_error = {
    "error": {
        "code": "ERROR_UNKNOWN",
        "message": "ошибка",
        "details": None
    }
}

host = 'https://api-seller.ozon.ru'


last_id = 'WzQ2MzcyNzEyNyw0NjM3MjcxMjdd'

headers = {
    'Client-Id': oson_client_id_3431,
    'Api-Key': oson_key_admin_3431,
    'Content-Type': 'application/json'
}
wh_id = {'JP Express': 1020000245246000, 
         'Comfort JP Express': 1020000804327000, 
         'пр.Культуры': 1020001551250000}
metod_get_list_products = '/v2/product/list'
metod_get_warehouses = '/v1/warehouse/list'
metod_get_new_orders = ''

outlets = [1020000804327000, 1020001551250000]

def write_json_skus(smth_json):
    try:
        with open('/var/www/html/stm/onon_skus.json', 'w') as file:
            json.dump(smth_json, file)
    except Exception:
        with open('onon_skus.json', 'w') as file:
            json.dump(smth_json, file)


def get_smth(metod):
    params = {
        'Client-Id': oson_client_id,
        'Api-Key': oson_key_admin,
        'Content-Type': 'application/json'
    }
    link = host + metod
    response = requests.get(link, headers=params)
    print('get_smth_on', metod, response, response.text)
    return response


def post_get_smth(metod):
    link = host + metod
    response = requests.post(link, headers=headers)
    data = response.json()
    # print('post_get_smth',len(data['result']), *data['result'], sep='\n')
    if metod == metod_get_list_products:
        result = data['result']['items']
        total = data['result']['total']
        last_id = data['result']['last_id']
        print('post_get_smth_onon', total, last_id, result[0])
        return result, total, last_id
    elif metod == metod_get_warehouses:
        proxy = {row['name']: row['warehouse_id'] for row in data['result']}
        print(proxy)
        return proxy
    else:
        print(11111, response.text)
        return data


# post_get_smth(metod_get_warehouses)


# wh = ['OZ.RFBSнашсклДЛ', 'OZ.RFBSНашсклСДЭК', 'OZ.НашадостМиМО',
#       'OZ.ОктКГnew', 'OZ.ОснКурьер', 'OZ.ДостКГ']


def get_product_info(product_id, offer_id):
    metod = '/v2/product/info'
    link = host + metod
    data = {
        "offer_id": offer_id,
        "product_id": int(product_id),
        "sku": 0
    }
    response = requests.post(link, headers=headers, json=data)
    answer = response.json()
    result = answer['result']["fbs_sku"]
    sleep(0.4)
    # print('get_product_info_onon', len(result)) #{'product_id': 38010832, 'offer_id': 'OWLT190601', 'is_fbo_visible': True, 'is_fbs_visible': True, 'archived': False, 'is_discounted': False}
    return result


def create_data_stocks():
    data_read = read_json_on()
    result = []
    stocks = []
    # proxy_skus = {}
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


head = ['Категория Ozon', 'offer id', 'Название', 'Цена', 'Бренд', 'Код', 'Наличие']

def read_csv_from(file):
    dt = None
    faxy = {}
    try:
        with open(file, 'r') as f:
            data = csv.DictReader(f)
            for row in data:
                print(row.keys())
            # print(222, data)
            # print(len(data))
    except:
        dt = pandas.read_excel(file)
        data = dt.to_dict()

        for row in dt.values:
            proxy = tuple(row)
            faxy.update({proxy[1]: proxy})

        for k, v  in data.items():
            # print(11111111,k, type(k))

            os.abort()


    return faxy, data


def get_current_assortment():
    result = []
    link = host + metod_get_list_products
    headers = {
        "Client-Id": oson_client_id_3431,
        "Api-Key": oson_key_admin_3431
    }
    last_id = ""
    requesting = True
    while requesting:
        data = {
            "filter": {
                "visibility": "ALL"
            },
            "last_id": last_id,
            "limit": 1000
        }
        try:
            answer = requests.post(url=link, headers=headers, json=data)
            if answer.ok:
                assortment = answer.json()
                proxy = assortment.get('result').get('items')
                last_id = assortment.get('result').get('last_id')
                if len(proxy) > 999:
                    result.extend(proxy)
                    print(8888888888, len(result))
                else:
                    requesting = False
                    result.extend(proxy)
            else:
                print('We are sleep and got {}'.format(answer.text))
                time.sleep(1)
                continue
        except:
            time.sleep(1)
            continue
    print(7777777777, len(result), result[-50:])
    return result



def read_xlsx_from(file, key_kolumn:int = 1):
    faxy = {}
    dt = pandas.read_excel(file)
    data = dt.to_dict()

    for row in dt.values:
        proxy = tuple(row)
        faxy.update({proxy[key_kolumn]: proxy})
    print(3434345, type(data))
    return faxy


def create_data_stocks_v2(file):
    data_read = read_xlsx_from(file)
    result = []
    stocks = []
    count = 0
    # current_assortment = post_get_smth(metod_get_list_products)[0]
    current_assortment = get_current_assortment()
    for product in current_assortment:
        proxy = {}
        if product['offer_id'] in data_read.keys():
            proxy['offer_id'] = product['offer_id']
            proxy['product_id'] = product['product_id']
            proxy['stock'] = data_read[product['offer_id']][6]
            proxy['warehouse_id'] = 1020000804327000
            pr = proxy.copy()
            rr = proxy.copy().update({'warehouse_id': 1020001551250000})
            stocks.append(pr)
            stocks.append(rr)
        else:
            count += 1

    print(444444, count)

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
        print('stocks', len(stocks))
    else:
        result.append(stocks)

    print('create_data_stocks_onon_x100', len(result), result[-50:])
    return result


def create_data_stocks_v3(file):
    data_read = read_xlsx_from(file, key_kolumn=0)
    # print('DATA READ {}'.format(data_read.keys()))
    result = []
    stocks = []
    count = 0
    current_wh = {'Культуры 63': 1020001947468000}
    current_assortment = get_current_assortment()
    for product in current_assortment:
        proxy = {}
        proxy_offer_id = product['offer_id'].strip("'")
        if proxy_offer_id in data_read.keys():
            proxy['offer_id'] = proxy_offer_id
            proxy['product_id'] = product['product_id']
            proxy['stock'] = data_read[proxy_offer_id][6]
            proxy['warehouse_id'] = 1020001947468000
            pr = proxy.copy()
            # rr = proxy.copy().update({'warehouse_id': 1020001947468000})
            stocks.append(pr)
            # stocks.append(rr)
        elif product['offer_id'] in data_read.keys():
            proxy['offer_id'] = product['offer_id']
            proxy['product_id'] = product['product_id']
            proxy['stock'] = data_read[product['offer_id']][6]
            proxy['warehouse_id'] = 1020001947468000
            pr = proxy.copy()
            # rr = proxy.copy().update({'warehouse_id': 1020001947468000})
            stocks.append(pr)
            # stocks.append(rr)
        else:
            count += 1

    print("Found {} & Not found {} in {} "
          .format(len(stocks), count, len(data_read.keys())))

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
        print('stocks', len(stocks))
    else:
        result.append(stocks)

    print('create_data_stocks_onon_x100', len(result), result[-5:])
    return result


def send_stocks_on(show_success: bool = False,
                   show_errors: bool = True):
    pre_data = create_data_stocks()
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row}
        # dt = json.dumps(data)
        response = requests.post(link, headers=headers, json=data)
        answer = response.json()
        ans = response.text
        print('answer send_stocks_on', ans)
        result = answer.get("result")
        if result:
            for row in result:
                if row['updated'] == False and show_errors:
                    print('ERROR update from send_stocks_ozon', row)
                elif row['updated'] == True and show_success:  # and row['warehouse_id'] != 23012928587000:
                    print('SUCCESS update from send_stocks_on', row)
            proxy.append(answer)
        sleep(1)


# send_stocks_on()


def send_stocks_on_oson(file, type_data: int = 2):
    if type_data == 3:
        pre_data = create_data_stocks_v3(file)
    else:
        pre_data = create_data_stocks_v2(file)
    metod = '/v2/products/stocks'
    link = host + metod
    count_success, count_error = 0, 0
    proxy = []
    for row in pre_data:
        data = {'stocks': row}
        response = requests.post(link, headers=headers, json=data)
        answer = response.json()
        ans = response.text
        print('answer send_stocks_on', ans)
        result = answer.get("result")
        if result:
            for row in result:
                if len(row["errors"]) > 0:  # and row['warehouse_id'] != 23012928587000: #TODO temporary 'warehouse_id': 23012928587000
                    print('ERROR from send_stocks_ozon', row)
                elif row['updated'] == False:
                    print('ERROR update from send_stocks_ozon', row)
                elif row['updated'] == True:  # and row['warehouse_id'] != 23012928587000:
                    print('SUCCES update from send_stocks_on', row)
            proxy.append(answer)
        sleep(1)


def product_info_price(id_mp):  # product_id, offer_id
    # url = 'https://api-seller.ozon.ru/v4/product/info/prices'
    # data = {"filter": {
    #             "offer_id": [offer_id],
    #             "product_id": [str(product_id)],
    #             "visibility": "ALL"
    #         },
    #         "last_id": "",
    #         "limit": 100}
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'
    data = {
        "posting_number": id_mp,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "product_exemplars": False,
            "translit": False}}
    resp = requests.post(url=url, headers=headers, json=data)
    result = resp.json()
    print('product_id_offer_id', result)
    # price = result.get("result")["items"][0]["price"]["marketing_price"][:-2]
    order = result.get("result")
    return order

# get_product_info(38010832, "OWLT190601")
# product_info_price("463727127", "OWLC19-014")
# send_stocks_on()
# asyncio.run(post_send_stocks())
# create_data_stocks()
# post_get_smth('/v1/warehouse/list')

# send_stocks_on_oson('https://3431.ru/system/unload_prices/17/ozon1.xlsx')
# send_stocks_on_oson('https://3431.ru/system/unload_prices/30/novyyozon.xlsx', type_data=3)
# create_data_stocks_v3('https://3431.ru/system/unload_prices/30/novyyozon.xlsx')
# get_current_assortment()
