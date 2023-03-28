import asyncio
import json

import requests
from cred import api_key_ozon_prod, api_key_ozon_admin
from read_json import read_json_on
from time import sleep

common_error = {
   "error": {
      "code": "ERROR_UNKNOWN",
      "message": "ошибка",
      "details": None
   }
}

host = 'https://api-seller.ozon.ru'
client_id = '90963'


last_id = 'WzQ2MzcyNzEyNyw0NjM3MjcxMjdd'

headers = {
        'Client-Id': client_id,
        'Api-Key': api_key_ozon_admin,
        'Content-Type': 'application/json'
    }


metod_get_list_products = '/v2/product/list'
metod_get_new_orders = ''



def write_json_skus(smth_json):
    try:
        with open('/var/www/html/stm/onon_skus.json', 'w') as file:
            json.dump(smth_json, file)
    except Exception:
        with open('onon_skus.json', 'w') as file:
            json.dump(smth_json, file)

def get_smth(metod):
    params = {
        'Client-Id': client_id,
        'Api-Key': api_key_ozon_admin,
        'Content-Type': 'application/json'
    }
    link = host + metod
    response = requests.get(link, headers=params)
    print('get_smth_on', metod, response, response.json())
    return response

def post_get_smth(metod):
    link = host + metod
    response = requests.post(link, headers=headers)
    data = response.json()
    #print('post_get_smth',len(data['result']['items']), type(data['result']['items']))
    result = data['result']['items']
    total = data['result']['total']
    last_id = data['result']['last_id']
    print('post_get_smth_onon', result[0])
    return result, total, last_id

#post_get_smth(metod_get_list_products)


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
    data_read = read_json_on()  #{'OWLM200602': ('b9719989-e055-11ea-82ad-00155d58510a', 11500, 15)}
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
                proxy['warehouse_id'] = wh
                pr = proxy.copy()
                stocks.append(pr)

    while len(stocks) >= 100:
        result.append(stocks[:100])
        del stocks[:100]
        # print(len(stocks))
    else:
        result.append(stocks)

    print('create_data_stocks_onon_x100', len(result))
    return result

# asyncio.run(create_data_stocks())
# create_data_stocks()

def read_skus():
    try:
        with open('/var/www/html/stm/onon_skus.json', 'r') as file:
            items_skus = json.load(file)
    except:
        with open('onon_skus.json', 'r') as file:
            items_skus = json.load(file)

    print('items_skus', len(items_skus), type(items_skus))
    return items_skus
#
# read_skus()

def send_stocks_on():
    pre_data = create_data_stocks()
    metod = '/v2/products/stocks'
    link = host + metod
    proxy = []
    for row in pre_data:
        data = {'stocks': row }
        response = requests.post(link,  headers=headers, data=json.dumps(data))
        answer = response.json()
        #ans = response.text
        # print(ans)
        result = answer["result"]
        for row in result:
            if len(row["errors"]) > 0 and row['warehouse_id'] != 23012928587000: #TODO temporary 'warehouse_id': 23012928587000
                print('error from send_stocks_on', row)
            # elif row['updated'] == False:
            #     print('error update from send_stocks_on', row)
            # elif row['offer_id'] == 'OWLINSTTI.OWLT190101':
            #     print('SUCCES update from send_stocks_on', row)
        proxy.append(answer)
        sleep(0.4)

# send_stocks_on()

def product_info_price(id_mp):  #product_id, offer_id
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
        "translit": False }}
    resp = requests.post(url=url, headers=headers, json=data)
    result = resp.json()
    print('product_id_offer_id', result)
    #price = result.get("result")["items"][0]["price"]["marketing_price"][:-2]
    order = result.get("result")
    return order



#get_product_info(38010832, "OWLT190601")
# product_info_price("463727127", "OWLC19-014")
# send_stocks_on()
#asyncio.run(post_send_stocks())
# create_data_stocks()

# def convert(string):
#     data = json.dumps(string)
#     print(data)
# # pr = [{'id': 'MP1703473-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703472-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}, {'id': 'MP1703471-001', 'pickup': {'deliveryServiceId': 123600, 'deliveryServiceName': 'Леруа Мерлен сервис доставки', 'warehouseId': '1200', 'timeInterval': 'Invalid Interval', 'pickupDate': '2022-12-14'}, 'products': [{'lmId': '90115665', 'vendorCode': 'BT2834B', 'price': 5860, 'qty': 3, 'comissionRate': 0}, {'lmId': '90121362', 'vendorCode': 'HPUV65ELC', 'price': 5860, 'qty': 3, 'comissionRate': 0}], 'deliveryCost': 0, 'parcelPrice': 5860, 'creationDate': '2022-12-14', 'promisedDeliveryDate': '2022-12-22', 'calculatedWeight': 4.8, 'calculatedLength': 707, 'calculatedHeight': 156, 'calculatedWidth': 686}]
# pr = {'message_type': 'TYPE_NEW_POSTING', 'seller_id': 90963, 'warehouse_id': 1020000075732000, 'posting_number': '13223249-0059-1', 'in_process_at': '2023-03-18T03:56:36Z', 'products': [{'sku': 789880982, 'quantity': 1}]}
# convert(pr)


