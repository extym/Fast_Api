import json
import random
import string
from datetime import datetime, timedelta
from cred import apikey_lm, login_lm, pass_lm, x_api_key, lm_access_token, access_token
from read_json import read_json_lm
import pytz
import requests
from conn import *
from sales import leroy
from proxy import proxy_lm, proxy_lm_1
import asyncio

test_url = 'http://localhost:5500/response'
remote_test_url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'
url_orders = 'https://api.leroymerlin.ru/marketplace/merchants/v1'

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
        #string = datetime.today() + timedelta(1)
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

    #print('datta',dat,  dtt)
    return dtt


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

# send_get_token()

def get_assortment():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/assortment'
    url_address = url + metod
    answer = requests.get(url_address, headers=headers)
    response = answer.json()
    print(answer.text)
    assortment = response['result']
    products = assortment['products']
    print('get_assortment', len(products))
    return products

# get_assortment()


def send_stocks_lm():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/stock'
    url_address = url + metod
    data = check_stocks()
    answer = requests.post(url_address, data=json.dumps(data), headers=headers)

    print('send_stocks_leroy', len(data["data"]["products"]),
          answer, answer.json())


def check_price():
    data_read = read_json_lm()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys():  # or product_id in temp:
            price = data_read.get(product_id)[1]
            proxy = {
                "marketplaceId": marketplaceId,
                "price": price
            }
            #printt(proxy)
            products.append(proxy)

    data = {"data":{"products": products}}
    #print('data----------------', data)
    return data

    
def send_price_lm():
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


def check_stocks():
    data_read = read_json_lm()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys():   # or product_id in temp
            stock = data_read.get(product_id)[2]
            if stock is None:
                stock = 0
            proxy = {
                "marketplaceId": marketplaceId,
                "stock": stock
            }
            products.append(proxy)

    data = {"data":{"products": products}}

    return data

def reformat_data_product(order, list_items,  shop):
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
        #print('reformat_data_product--', result)
    return result


def send_get_new_orders():

    headers = {'Content-type': 'application/json',
               'x-api-key': f'{apikey_lm}',
               'Authorization': f'Bearer {lm_access_token}'
               }
    params = {"status": "created"}
    metod = '/parcels'
    target_url = url_orders + metod
    response = requests.get(target_url, params=params, headers=headers)  # params=params,
    answer = response.text
    print(answer)
    data = response.json()
    print('send_get_new_orders', response.status_code,  len(data), data)
    return data

# send_get_new_orders()

def send_get_orders_lm():
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

    print('send_get_orders_lm',len(data), data)
    return data

# send_stocks_lm()
# send_get_new_orders()

# send_get_orders_lm()

def get_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    #url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'  #TODO for test ONLY
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{x_api_key}',
               'Authorization': f'Bearer {lm_access_token}'
               }

    target_url = url_orders + metod
    response = requests.get(target_url, headers=headers)

    return response

def check_is_exist(id_mp, shop):
    data = check_order(query_read_order, (id_mp, shop))
    # print('check_is_exist', data, id_mp, shop)
    if len(data) > 0:
        result = True
    else:
        result = False

    return result

# check_is_exist('MP2713064-001', 'Leroy')

async def empty_post_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    #url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1/'   #TODO for test ONLY
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{x_api_key}',
               'Authorization': f'Bearer {lm_access_token}'
               }
    target_url = url_orders + metod
    response = requests.post(target_url, headers=headers)
    print(response, response.text, target_url)
    # return response


#
#TODO CAN move to anover file?

def check_count_product(list_items):
    data = read_json_lm()  #return {vendor_code: (id_1c, price, quantity)}
    global_result = []
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

    res_dict = {item["vendorCode"]: data.get(item["vendorCode"])[0] for item in list_items}

    return result, list_items, res_dict


def confirm_orders(data):  #list orders,
    proxy = []
    for order in data:
        confirm = check_count_product(order["products"]) #check to stocks
        id_mp = order["id"]
        if confirm[0]:
            #our_id = token_generator()
            our_id = id_mp.replace('-', '')[:10]
            shop_Name = 'Leroy'
            shipment_Date = day_for_stm(order['pickup']['pickupDate'])  #proxy_time_1()
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
        print(' confirm order', proxy)
    return proxy

async def get_new_orders_lm():
    # data = proxy_lm_1              #for test ONLY
    #data = send_get_orders_lm()       #for test ONLY
    data = send_get_new_orders()  # TODO commented for test ONLY
    result = confirm_orders(data)
    print(len(data), '--- get_new_orders_lm', len(result))
    for order in result:
        if order[1]:
            check = check_is_exist(order[0][0], 'Leroy')
            if check:
                print(order[0][0], 'Leroy', 'is_exist - ', check)
                continue
            else:
                await execute_query(query_write_order, order[0])
                await executemany_query(query_write_items, order[2])
                print('get_new_orders_lm---', order[0])
                # await empty_post_smth('/parcels/' + order[0][0] + ':confirm')  # TODO for PROD use Required

        else:
            #resp = get_smth('/parcels/' + order[0][0] + '/statuses') #for test ONLY
            await empty_post_smth('/parcels/' + order[0][0] + ':cancel') #TODO for PROD use Required
            print('get_new_orders_lm not confirm', order[0][0])


# send_get_token()
# get_assortment()
# # send_stocks_lm()
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