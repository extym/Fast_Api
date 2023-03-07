import json
import random
import string
from datetime import datetime
from cred import apikey_lm, login_lm, pass_lm, test_apikey_lm, test_access_token, access_token, test_x_api_key, test_orders_jwt_lm
from read_json import read_json_lm
import pytz
import requests
from conn import *
import asyncio

time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()

def token_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def send_get_token():
    url = 'https://api.leroymerlin.ru/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Accept': 'application/json'
               }

    metod = 'marketplace/user/authbypassword'
    url_address = url + metod + '?login=' + login_lm + '&password=' + pass_lm
    answer = requests.get(url_address, headers=headers)
    # print(str(time), type(answer))
    print(str(time), answer)
    response = answer.json()
    print(str(time), response)


def get_assortment():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/assortment'
    url_address = url + metod
    answer = requests.get(url_address, headers=headers)
    # print(str(time), type(answer))
    response = answer.json()
    assortment = response['result']
    products = assortment['products']

    # for row in products:
    #     if row['productId'] in temp:
    #         print(str(time), 'result', len(products), row)

    #print(str(time), 'result', len(products), products)  #, products)

    return products


def send_stocks():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{apikey_lm}',
               'Authorization': f'Bearer {access_token}'
               }

    metod = 'products/stock'
    url_address = url + metod
    data = check_stocks()
    print(data)
    answer = requests.post(url_address, data=json.dumps(data), headers=headers)

    print(answer)


def test_check_price():
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
            #print(proxy)
            products.append(proxy)

    data = {"data":{"products": products}}
    #print('data----------------', data)
    return data

    
def test_send_price():
    url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    headers = {'Content-type': 'application/json',
               'apikey': f'{test_apikey_lm}',
               'Authorization': f'Bearer {test_access_token}'
               }

    metod = 'products/price'
    url_address = url + metod
    data = test_check_price()
    print(data)
    answer = requests.post(url_address, data=json.dumps(data), headers=headers)
    re = answer.json()
    print(answer, re)



    
# test_check_price()
 # temp = ['ИМOWLT190303', 'OW29.50.12', 'OWLB191038']


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

def reformat_data_product(order, shop):
    if shop == 'Leroy':
        result = []
        list_items = order["products"]
        for item in list_items:
            proxy = (
                order["id"],
                order['our_id'],
                shop,
                order["our_status"],
                item["offerId"],
                item["id_ic"],
                item["quantity"],
                item["finalPrice"]
            )
            result.append(proxy)

    elif shop == 'WB':
        result = (
            order['order']["businessId"],
            order['order']["id"],
            order['order']["shop"],
            order['order']["date"],
            order['order']["status"],
            order['order']["paymentType"],
            order['order']["delivery"]
        )

    return result


def send_get_new_orders():
    url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{test_x_api_key}',
               'Authorization': f'Bearer {test_orders_jwt_lm}'
               }
    params = {"status": "created"}
    metod = '/parcels'
    target_url = url + metod
    response = requests.get(target_url, params=params, headers=headers)
    data = response.json()

    print(len(data), data)
    return data


def send_get_orders():
    url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{test_x_api_key}',
               'Authorization': f'Bearer {test_orders_jwt_lm}'
               }
    params = {"status": "created"}
    metod = 'parcels'
    target_url = url + metod
    response = requests.get(target_url, headers=headers)
    data = response.json()

    print(len(data), data)
    return data

# send_stocks()
#send_get_new_orders()


def get_smth(metod):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1'  #TODO for test ONLY
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{test_x_api_key}',
               'Authorization': f'Bearer {test_orders_jwt_lm}'
               }

    target_url = url + metod
    response = requests.get(target_url, headers=headers)

    return response

async def post_smth(metod, data):
    # url = 'https://api.leroymerlin.ru/marketplace/api/v1/'
    url = 'https://api-test.leroymerlin.ru/marketplace/merchants/v1/'   #TODO for test ONLY
    headers = {'Content-type': 'application/json',
               'x-api-key': f'{test_x_api_key}',
               'Authorization': f'Bearer {test_orders_jwt_lm}'
               }
    target_url = url + metod
    response = requests.post(target_url, headers=headers, data=json.dumps(data))
    print(response, response.json(), target_url)
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
        else:
            item_result = False
        global_result.append(item_result)

    if False not in global_result:
        result = True

    return result



def confirm_orders(data):  #list orders,
    proxy = []
    for order in data:
        confirm = check_count_product(order["products"]) #check to stocks
        id_mp = order["id"]
        if confirm:
            our_id = token_generator()
            shop_Name = 'Leroy'
            shipment_Date = order["creationDate"]  ##add one day?
            status = order.get("status", "CREATED")
            our_status = 'NEW'
            payment_Type = "PREPAID"
            delivery = order.get("deliveryServiceName")
            order_summ = order.get("parcelPrice")
            order = ((id_mp, our_id, shop_Name, shipment_Date,
                     status, our_status, payment_Type, delivery), True)
        else:
            order = (id_mp, (None), False)
        proxy.append(order)

    return proxy

async def get_new_orders_lm():
    #data = send_get_new_orders()  # commented for test ONLY

    data = send_get_orders()       #for test ONLY
    result = confirm_orders(data)
    for order in result:
        if order[1]:
            await post_smth('/parcels/' + order[0][0] + ':confirm', None)  #TODO make async def post_smth
            await execute_query(query_write_order, order[0])
        else:
            resp = get_smth('/parcels/' + order[0][0] + '/statuses') #for test ONLY
            # await post_smth('/parcels/' + order[0] + ':cancel', None)
            print('get_status', resp, resp.json())
    print(len(data), '--- check', len(result), result)


# send_get_token()
# get_assortment()
send_stocks()
test_send_price()
# check_stocks()
# asyncio.run(get_new_orders_lm())
