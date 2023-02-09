import json
from datetime import datetime
from cred import apikey_lm, login_lm, pass_lm, test_apikey_lm, test_access_token, access_token
from read_json import read_json_lm
import pytz
import requests


time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()



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

    print(str(time), 'result', len(products))  #, products)

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

    print(answer)
    
    
def test_check_price():
    data_read = read_json_lm()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys() or product_id in temp:
            price = data_read.get(product_id)[1]
            proxy = {
                "marketplaceId": marketplaceId,
                "price": price
            }
            print(proxy)
            products.append(proxy)
            continue

        continue

    data = {"data":{"products": products}}
    print('data----------------', data)
    return data
    

temp = ['ИМOWLT190303', 'OW29.50.12', 'OWLB191038']


def check_stocks():
    data_read = read_json_lm()
    products = []
    market_data = get_assortment()
    for prod in market_data:
        product_id = prod['productId']
        marketplaceId = prod['marketplaceId']
        if product_id in data_read.keys():   # or product_id in temp
            stock = data_read.get(product_id)[2]
            proxy = {
                "marketplaceId": marketplaceId,
                "stock": stock
            }

            products.append(proxy)
            continue

        continue



    data = {"data":{"products": products}}

    return data





# send_get_token()
# get_assortment()
# send_stocks()
# check_stocks()
