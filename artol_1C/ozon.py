import asyncio
import json

import requests
from cred import api_key_ozon_prod, api_key_ozon_admin, client_id_onon
from read_json import read_json_on, read_json_ids
from time import sleep

common_error = {
   "error": {
      "code": "ERROR_UNKNOWN",
      "message": "ошибка",
      "details": None
   }
}

host = 'https://api-seller.ozon.ru'



# last_id = 'WzQ2MzcyNzEyNyw0NjM3MjcxMjdd'

headers = {
        'Client-Id': client_id_onon,
        'Api-Key': api_key_ozon_admin,
        'Content-Type': 'application/json'
    }


metod_get_list_products = '/v2/product/list'
metod_get_new_orders = ''



def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result


def write_json_skus(smth_json):
    try:
        with open('/var/www/html/artol/onon_skus.json', 'w') as file:
            json.dump(smth_json, file)
    except Exception:
        with open('onon_skus.json', 'w') as file:
            json.dump(smth_json, file)

def get_smth(metod):
    params = {
        'Client-Id': client_id_onon,
        'Api-Key': api_key_ozon_admin,
        'Content-Type': 'application/json'
    }
    link = host + metod
    response = requests.get(link, headers=params)
    print('get_smth_on', metod, response, response.json())
    return response


def post_get_assortment(metod):
    proxy = []
    requesting = True
    link = host + metod
    response = requests.post(link, headers=headers)
    data = response.json()
    result = data['result'].get('items')
    # total = data['result'].get('total')
    last_id = data['result'].get('last_id')
    while requesting:
        proxy.extend(result)
        data_send = {
            "last_id": last_id
        }
        response = requests.post(link, headers=headers, json=data_send)
        data = response.json()
        result = data['result'].get('items')
        last_id = data['result'].get('last_id')
        if len(result) < 1000:
            requesting = False
            proxy.extend(result)
            # break

        print('post_get_assortment_onon_artol', len(proxy))

    return proxy


def post_get_assortment_v2():
    proxy = []
    requesting = True
    link = host + metod_get_list_products
    last_id = ''
    while requesting:
        data_send = {
            "last_id": last_id
        }
        response = requests.post(link, headers=headers, json=data_send)
        data = response.json()
        result = data['result'].get('items')
        last_id = data['result'].get('last_id')
        if len(result) < 1000:
            requesting = False
            proxy.extend(result)
            # break
        else:
            proxy.extend(result)

        print('post_get_assortment_onon_artol_v2', len(proxy))

    return proxy


def post_get_smth(metod):
    link = host + metod
    response = requests.post(link, headers=headers)
    data = response.json()
    result = data['result']
    print('post_get_smth_onon_artol', result)
    return result



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
    print('get_product_info_onon_artol', len(result))
    return result



def create_data_stocks():
    data_read = read_json_ids()
    result = []
    stocks = []
    # proxy_skus = {}
    current_assortment = post_get_assortment(metod_get_list_products)
    for product in current_assortment:
        # try:
        #     sku = get_product_info(product['product_id'], product['offer_id'])
        #     proxy_skus[sku] = (product['product_id'], product['offer_id'])
        # except Exception as error:
        #     print(f"create_data_stocks & get_product_info ".format(error))
        # finally:
        proxy = {}
        if product['offer_id'] in data_read.keys():
            proxy['offer_id'] = product['offer_id']
            proxy['product_id'] = product['product_id']
            proxy['stock'] = data_read[product['offer_id']][2]
            outlets = ['23754458910000']   #data_read[product['offer_id']][3]
            for wh in outlets:
                proxy['warehouse_id'] = wh
                pr = proxy.copy()
                stocks.append(pr)

        # if product['offer_id'] in check_send:
        #     print(product)

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
    else:
        result.append(stocks)

    # write_json_skus(proxy_skus)
    # print('create_data_skus_onon', len(proxy_skus))
    print('create_data_stocks_artol_onon_x100', len(result), result)
    return result



# def read_skus():
#     try:
#         with open('/var/www/html/artol/onon_skus.json', 'r') as file:
#             items_skus = json.load(file)
#     except:
#         with open('onon_skus.json', 'r') as file:
#             items_skus = json.load(file)
#
#     print('items_skus_artol', len(items_skus), type(items_skus))
#     return items_skus


def send_stocks_on():
    pre_data = create_data_stocks()
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row }
        response = requests.post(link,  headers=headers, data=json.dumps(data))
        answer = response.json()
        ans = response.text
        print('answer_send_stock_on_artol', ans)
        result = answer["result"]
        for row in result:
            if len(row["errors"]) > 0:
                print('error from send_stocks_on_artol', row)
            elif row['updated'] == False:
                print('error update from send_stocks_on_artol', row)
        proxy.append(answer)
        sleep(0.4)


def product_info_order(id_mp):  #product_id, offer_id
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'
    data = {
      "posting_number": id_mp,
      "with": {
        "analytics_data": False,
        "barcodes": False,
        "financial_data": False,
        "product_exemplars": False,
        "translit": False }}
    resp = requests.post(url=url, headers=headers, json=data)
    result = resp.json()
    print('product_id_offer_id_artol', result)
    #price = result.get("result")["items"][0]["price"]["marketing_price"][:-2]
    order = result.get("result")
    return order



# send_stocks_on()

#get_product_info(38010832, "LT190601")
# product_info_price("463727127", "LC19-014")
#asyncio.run(post_send_stocks())
# create_data_stocks()

# def convert(string):
#     data = json.dumps(string)
#     print(data)
# # pr = [{'id': 'MP1703473-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703472-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703471-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}]


# post_get_smth(metod_get_list_products)
#post_get_smth('/v1/warehouse/list')   # get list wh
# asyncio.run(create_data_stocks())
# create_data_stocks()
# print(11111, post_get_assortment(metod_get_list_products))
# sleep(5)
# print(22222, post_get_assortment_v2())

create_data_stocks()