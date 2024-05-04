import csv
import json
import random
import string
from datetime import datetime, timedelta
from cred import apikey_lm, login_lm, pass_lm, x_api_key, LOCAL_MODE, lm_access_token
from read_json import read_json_lm, read_json_lm_v2
import pytz
import requests
from conn import *
import os
# from sales import leroy
from proxy import proxy_lm, proxy_lm_1
import asyncio

test_url = 'http://localhost:5500/response'
remote_test_url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'
url_orders = 'https://api.leroymerlin.ru/marketplace/merchants/v1'
print(11111111111111111111111111111111111111111111111111111111111111111, os.getcwd())

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH = os.getcwd()
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH = '/home/userbe/stm/'

time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()


def token_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt


def day_for_stm(string):
    # if string == '0000-00-00':
    # string = datetime.today() + timedelta(1)
    # else:
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


def write_leroy_token(response):
    with open(PATH + 'leroy_creds.json', 'w') as file:
        json.dump(response, file)


def write_jwt_leroy(response):
    with open(PATH + 'orders_token_leroy.json', 'w') as file:
        json.dump(response, file)


def read_jwt_leroy():
    with open(PATH + 'orders_token_leroy.json', 'r') as file:
        data = json.load(file)
        lm_access_token = data.get('access_token')

        return lm_access_token


def read_leroy_token():
    with open(PATH + 'leroy_creds.json', 'r') as file:
        data = json.load(file)
        access_token = data.get('access_token')

        return access_token


def send_get_token():
    url = 'https://api.leroymerlin.ru/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Accept': 'application/json'
               }

    metod = 'marketplace/user/authbypassword'
    url_address = url + metod + '?login=' + login_lm + '&password=' + pass_lm
    answer = requests.get(url_address, headers=headers)
    response = answer.json()
    print(str(time), response)
    write_leroy_token(response)


def get_assortment():
    access_token = read_leroy_token()
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/assortment'
    url_address = url + metod
    answer = requests.get(url_address, headers=headers)
    # print('products/assortment', answer.text)
    response = answer.json()
    assortment = response.get('result')
    products = assortment.get('products')

    print('get_assortment_len', len(products))

    return products


# get_assortment()


def check_stocks():
    # data_read = read_json_lm()
    data_read = read_json_lm_v2()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys():  # or product_id in temp
            stock = data_read.get(product_id)[2]
        else:
            stock = 0

        products.append({"marketplaceId": marketplaceId,
                         "stock": stock})

    data = {"data": {"products": products}}

    return data


# check_stocks()

def send_stocks_lm():
    access_token = read_leroy_token()
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/stock'
    url_address = url + metod
    data = check_stocks()
    answer = requests.post(url_address, data=json.dumps(data), headers=headers)

    print('send_stocks_leroy', len(data["data"]["products"]), answer.text)


# send_stocks_lm()


def read_sales():
    with open(UPLOAD_FOLDER + 'sales.json', 'r') as file:
        return json.load(file)


def check_price():
    data_read = read_json_lm()
    leroy = read_sales()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys():  # or product_id in temp:
            price = data_read.get(product_id)[1]
            if product_id in leroy.keys():  # make discount
                price = price * (1 - leroy[product_id] / 100)
            proxy = {
                "marketplaceId": marketplaceId,
                "price": price
            }
            # printt(proxy)
            products.append(proxy)

    data = {"data": {"products": products}}
    # print('data----------------', data)
    return data


# check_price()

def send_price_lm():
    access_token = read_leroy_token()
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/price'
    url_address = url + metod
    data = check_price()
    answer = requests.post(url_address, data=json.dumps(data), headers=headers)
    re = answer.json()
    print('send_price_leroy', len(data), answer, re)


def reformat_data_product(order, list_items, shop):
    result = []
    if shop == 'Leroy':

        # list_items = order["products"]
        for item in list_items:
            proxy = (
                order[0],
                order[1],
                shop,
                order[5],
                item["vendorCode"],
                item["id_1c"],
                item["qty"],
                item["price"]
            )
            result.append(proxy)

    # elif shop == 'WB':
    #     result = (
    #         order['order']["businessId"],
    #         order['order']["id"],
    #         order['order']["shop"],
    #         order['order']["date"],
    #         order['order']["status"],
    #         order['order']["paymentType"],
    #         order['order']["delivery"]
    #     )
    # print('reformat_data_product--', result)
    return result


def send_get_new_orders():
    lm_access_token = read_jwt_leroy()
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{apikey_lm}',
               'Authorization': f'Bearer {lm_access_token}'
               }

    params = {"status": "created"}
    metod = '/parcels'
    target_url = url_orders + metod
    response = requests.get(target_url, params=params, headers=headers)  # params=params,
    # answer = response.text
    # print(answer)
    data = response.json()
    print('send_get_new_orders', response.status_code, len(data), data)
    return data


# send_get_new_orders()

def send_get_orders_lm():
    lm_access_token = read_jwt_leroy()
    # url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{apikey_lm}',
               'Authorization': f'Bearer {lm_access_token}'
               }
    params = {"status": "created"}
    metod = '/parcels'
    target_url = url_orders + metod
    response = requests.get(target_url, headers=headers)
    data = response.json()

    print('send_get_orders_lm', len(data), data)
    return data


def get_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    # url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'  #TODO for test ONLY
    lm_access_token = read_jwt_leroy()
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{x_api_key}',
               'Authorization': f'Bearer {lm_access_token}'
               }

    target_url = url_orders + metod
    response = requests.get(target_url, headers=headers)

    return response


def check_is_exist(id_mp, shop):
    print('check_exist', id_mp, shop)
    data = check_order(query_read_order, (id_mp, shop))
    print('check_exist2222222222222', data)
    if len(data) > 0:
        result = True
    else:
        result = False
    print('check_exist_result', result)
    return result


# check_is_exist('MP3816268-001', 'Leroy')

async def empty_post_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    # url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1/'   #TODO for test ONLY
    lm_access_token = read_jwt_leroy()
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{x_api_key}',
               'Authorization': f'Bearer {lm_access_token}'
               }
    target_url = url_orders + metod
    response = requests.post(target_url, headers=headers)
    print(response, response.text, target_url)
    # return response


async def cancel_post_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    # url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1/'   #TODO for test ONLY

    headers = {'Content-type': 'application/json',
               'x-api-key': f'{x_api_key}',
               'Authorization': f'Bearer {lm_access_token}'
               }
    params = {
        "stage": "CancelAtConfirmation",
        "reason": "Problems processing order"
    }
    target_url = url_orders + metod
    response = requests.post(target_url, headers=headers, params=params)
    print(response, response.text, target_url)
    # return response


#
# TODO CAN move to anover file?

def check_count_product(list_items):
    data = read_json_lm()  # return {vendor_code: (id_1c, price, quantity)}
    global_result, res_dict = [], {}
    result = False
    for item in list_items:
        vendor_code = item["vendorCode"]
        qty = item["qty"]
        quantity = data.get(vendor_code, (0, 0, 0))[2]
        if quantity >= qty:
            item_result = True
            item['id_1c'] = data.get(vendor_code)[0]
        else:
            item_result = False
        global_result.append(item_result)

    if False not in global_result:
        result = True

        print('!!!!!!!!!!!!', result, list_items, 'global_result', global_result)
    try:
        res_dict = {item["vendorCode"]: data.get(item["vendorCode"])[0] for item in list_items}
    except:
        pass

    return result, list_items, res_dict


def confirm_orders(data):  # list orders,
    proxy = []
    for order in data:
        confirm = check_count_product(order["products"])  # check to stocks
        id_mp = order["id"]
        if confirm[0]:
            # our_id = token_generator()
            our_id = id_mp.replace('-', '')[:10]
            shop_Name = 'Leroy'
            shipment_Date = day_for_stm(order['pickup']['pickupDate'])  # proxy_time_1()
            # status = order.get("status", "accept")
            our_status = 'NEW'
            payment_Type = "PREPAID"
            delivery = order.get("deliveryServiceName")
            order_summ = order.get("parcelPrice")
            order_data = (id_mp, our_id, shop_Name, shipment_Date,
                          "accept", our_status, payment_Type, delivery)
            list_items = reformat_data_product(order_data, confirm[1], 'Leroy')
            order = (order_data, True, list_items)

        else:
            order = (id_mp, False, [])

        proxy.append(order)
        print(' confirm_order', proxy)
    return proxy


async def get_new_orders_lm():
    # data = proxy_lm_1              #for test ONLY
    # data = send_get_orders_lm()       #for test ONLY
    data = send_get_new_orders()  # TODO commented for test ONLY
    result = confirm_orders(data)
    print(len(data), 'prepare_get_new_orders_lm', len(result))
    for order in result:
        if order[1]:
            check = check_is_exist(order[0][0], 'Leroy')
            if check:
                print(order[0], 'Leroy', 'is_exist - ', check)
                continue
            else:
                await execute_query(query_write_order, order[0])
                await executemany_query(query_write_items, order[2])
                print('get_new_orders_lm_write', order[0])
                # await empty_post_smth('/parcels/' + order[0][0] + ':confirm')  # TODO for PROD use Required
        else:
            # resp = get_smth('/parcels/' + order[0][0] + '/statuses') #for test ONLY
            # TODO for PROD use Required ## VALID order[0]
            await cancel_post_smth('/parcels/' + order[0][0] + ':cancel')
            print('get_new_orders_lm_not_confirm', order[0])


def get_jwt_token_orders():
    url = 'https://api.leroymerlin.ru/marketplace/oauth/token'
    metod = '/oauth/token'
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'x-api-key': f'{apikey_lm}'
               }
    data = {'grant_type': 'password',
            'password': 'iCjUTdRg',
            'username': 'bt@brain-trust.ru',
            'client_id': 'merchants_orchestrator',
            'client_secret': 'zbpHEJ4rwVrzz9rka3KwvgyUtd8GyfDY'
            }
    data = requests.post(url, data=data, headers=headers)
    response = data.json()
    write_jwt_leroy(response)
    # print(response)


# get_jwt_token_orders()


def convert_sales():
    leroy = {}
    with open('sales_lm.csv', 'r') as file:
        data = csv.reader(file, delimiter=';')
        for row in data:
            leroy[str(row[0])] = int(row[1])

        f = open('sales.py', 'w')
        f.write(f'leroy = {leroy}')
        f.close()

        # print(leroy)


# convert_sales()

# send_get_orders_lm()
# send_get_token()
# get_assortment()
# send_stocks_lm()
# send_price_lm()
# check_stocks()
# asyncio.run(get_new_orders_lm())
# send_get_orders_lm()
# resp = get_smth('/parcels/' + 'MP2758412-001' + '/statuses')
# print(resp.text)
# send_get_token()

def ten():
    time = datetime.now()
    print('10--', time)


def five():
    time = datetime.now()
    print('55--', time)


def tt():
    time = datetime.now()
    print('111--', time)


# confirm_orders([{'id': 'MP3865511-001', 'pickup': {'deliveryServiceId': 123640, 'deliveryServiceName':
# 'Самопривоз', 'warehouseId': '7866', 'timeInterval': '07:00:00.000Z/11:00:00.000Z', 'pickupDate': '2023-08-22'},
# 'products': [{'lmId': '91114119', 'vendorCode': 'OWLM200801', 'price': 8742, 'qty': 1, 'comissionRate': 0}],
# 'deliveryCost': 0, 'parcelPrice': 8742, 'creationDate': '2023-08-20', 'promisedDeliveryDate': '2023-08-23',
# 'calculatedWeight': 7.3, 'calculatedLength': 1112, 'calculatedHeight': 52, 'calculatedWidth': 800},
# {'id': 'MP3864774-001', 'pickup': {'deliveryServiceId': 123640, 'deliveryServiceName': 'Самопривоз', 'warehouseId':
# '7866', 'timeInterval': '07:00:00.000Z/11:00:00.000Z', 'pickupDate': '2023-08-22'}, 'products': [{'lmId':
# '91105230', 'vendorCode': 'OWLIB191102', 'price': 34084.5, 'qty': 1, 'comissionRate': 0}], 'deliveryCost': 0,
# 'parcelPrice': 34084.5, 'creationDate': '2023-08-20', 'promisedDeliveryDate': '2023-08-24', 'calculatedWeight':
# 120, 'calculatedLength': 1924, 'calculatedHeight': 624, 'calculatedWidth': 832}])


def make_log():
    # PATH = '/var/www/html/stm/'
    today = str(datetime.today()).replace(' ', '_')[:-7]
    try:
        os.system(f'cp /var/www/html/stm/test_json.json /var/www/html/stm/test_json_{today}.json')
        print("ALL_RIDE_make_log_json")
    except:
        print("FACK_UP_make_log_json")


# make_log()


import pandas as pd


def read_xls(files):
    file = pd.read_excel(files)
    df = pd.DataFrame(file).values
    proxy = {}
    for row in df:
        proxy[row[1]] = row[0]

    print(proxy)

# read_xls('1111.xlsx')
