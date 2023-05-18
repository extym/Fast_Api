# def orders_add():
from datetime import datetime
import json

import pytz
import requests
from gevent import sleep
from cred import token_market_dbs, token_market_fbs,  client_id, token_ym

import urllib3
urllib3.disable_warnings()

# file  = open('data_json.json', 'r')
# data = file.readlines()
#
# print(type(data))
#
# file =  open('data_json.json', 'r')
# data = json.load(file)
# print(type(data))
#
data_to_1c = '''
{
    "order": {
        "shop": "Yandex",
        "businessId": "3675591",
        "id": "1277178",
        "paymentType": "PREPAREID",
        "delivery": false,
        "items": [
            {
                "shopSku": "4fc6a7b0-ad96-11e2-9997-902b34460e77",
                "count": 2,
                "price": 336
            },
            {
                "shopSku": "c9bb4043-d821-11e2-bda3-902b34460e77",
                "count": 2,
                "price": 520
            }
        ]
    }
}
'''

order = {
    "order": {
        "shop": "Yandex",
        "businessId": "3675591",
        "id": "12347878",
        "paymentType": "PREPAREID",
        "delivery": False,
        "items": [
            {
                "shopSku": "d7615bce-f434-11e2-be19-902b34460e77",
                "count": 2,
                "price": 333
            },
            {
                "shopSku": "fe580a50-ee2e-11e8-be4c-4487fcda067f",
                "count": 1,
                "price": 523
            }
        ]
    }
}

# url_address = 'https://92.39.143.137:14723/Trade/hs/post/order/post'   #'http://super-good.ml:8800/json'  #   'http://iiko.ml:8800/json'
# ##  # #'https://iiko.biz:9900/api/0/orders/add?'  # 'https://httpbin.org/post'#'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
# headers = {'Content-type': 'application/json',  # Определение типа данных
#            'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
#            'Content-Encoding': 'utf-8'}
# # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
# answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
# print(datetime.datetime.now(), answer)
# # response = answer.json()
# # print(datetime.datetime.now(), response)

# from cred import token_market, client_id, token_ym
# from proxy_json import proxy_cart

# data = proxy_cart
# <тип_метода> https://api.partner.market.yandex.ru/v<версия_API>/<ресурс>.<формат_ответа>?<параметры>
# metod = ''
# # url_address = 'https://api.partner.market.yandex.ru/v2/' + metod + '.json' #'?<параметры>'  #'https://92.39.143.137:14723/Trade/hs/post/order/post'
# #'http://super-good.ml:8800/json'  #   'http://iiko.ml:8800/json'   ##  # #'https://iiko.biz:9900/api/0/orders/add?'  #'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
# url_address = 'https://api.partner.market.yandex.ru/v2/campaigns/' + compaing_id + '.json'
# headers = {'Content-type': 'application/json',  # Определение типа данных
#            'Authorization': f'OAuth oauth_token=f{token_market}, oauth_client_id=f{client_id}',
#            'Content-Encoding': 'utf-8'}
# # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
# answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
# # answer = requests.get(url_address, headers=headers)
# print(datetime.datetime.now(), answer)
# # response = answer.json()
# # print(datetime.datetime.now(), response)
#
# deliveryService = [{'id': 1, 'name': 'Почта России (РБЛ)'}, {'id': 2, 'name': 'EMS Почта России'}, {'id': 3, 'name': 'СПСР-Экспресс'},
#                    {'id': 6, 'name': 'Гарантпост'}, {'id': 7, 'name': 'Деловые Линии'}, {'id': 8, 'name': 'DHL'}, {'id': 9, 'name': 'ПЭК'},
#                    {'id': 10, 'name': 'Pony Express'}, {'id': 11, 'name': 'Желдорэкспедиция'}, {'id': 12, 'name': 'Байкал-сервис'},
#                    {'id': 13, 'name': 'Экспресс-почта'}, {'id': 14, 'name': 'МТК'}, {'id': 16, 'name': 'Энергия'}, {'id': 17, 'name': 'FedEx'},
#                    {'id': 19, 'name': 'КСЭ'}, {'id': 20, 'name': 'Реил Континент'}, {'id': 21, 'name': 'Доставкин'}, {'id': 22, 'name': 'УралТрансСервис'},
#                    {'id': 24, 'name': 'Starpost'}, {'id': 25, 'name': 'Скороход'}, {'id': 26, 'name': 'ТрансЭкспресс'},
#                    {'id': 27, 'name': 'Русская почтовая служба'}, {'id': 29, 'name': 'TNT'}, {'id': 30, 'name': 'Major Express'}, {'id': 31, 'name': 'РТК-Базис'},
#                    {'id': 32, 'name': 'Эксист'}, {'id': 33, 'name': 'Автолюкс'}, {'id': 34, 'name': 'Гюнсел'}, {'id': 35, 'name': 'Express mail'},
#                    {'id': 36, 'name': 'Ночной экспресс'}, {'id': 37, 'name': 'Новая Почта'}, {'id': 38, 'name': 'Укрпошта'}, {'id': 39, 'name': 'EMS Ukraine - ГПСС'},
#                    {'id': 40, 'name': 'TNT Express Ukraine'}, {'id': 41, 'name': 'Ваш Час'}, {'id': 42, 'name': 'Ин-Тайм'}, {'id': 43, 'name': 'Деливери'},
#                    {'id': 44, 'name': 'UrEx'}, {'id': 45, 'name': 'Міст Експрес'}, {'id': 47, 'name': 'ДАЙМЭКС'}, {'id': 48, 'name': 'Стриж'}, {'id': 49, 'name': 'Аксиомус'},
#                    {'id': 51, 'name': 'СДЭК'}, {'id': 99, 'name': 'Собственная служба'}, {'id': 100, 'name': 'Другая служба'}, {'id': 101, 'name': 'ЖелдорАльянс'},
#                    {'id': 104, 'name': 'TOP Delivery'}, {'id': 105, 'name': 'Maxima Express'}, {'id': 106, 'name': 'Боксберри'}, {'id': 107, 'name': 'PickPoint'},
#                    {'id': 108, 'name': 'B2Cpl'}, {'id': 109, 'name': 'Logibox'}, {'id': 110, 'name': 'О-Курьер'}, {'id': 111, 'name': 'Shop Logistic'},
#                    {'id': 112, 'name': 'RED Express'}, {'id': 113, 'name': 'БизнесПост'}, {'id': 115, 'name': 'Мурманская Транспортная Компания'},
#                    {'id': 116, 'name': 'Озон-Доставка'}, {'id': 117, 'name': 'Почтальон Сервис'}, {'id': 119, 'name': 'IML'}, {'id': 120, 'name': 'Hermes'},
#                    {'id': 121, 'name': 'Marschroute'}, {'id': 122, 'name': '4BIZ'}, {'id': 126, 'name': 'Shiptor'}, {'id': 200, 'name': '5Post'},
#                    {'id': 215, 'name': 'Везу'}, {'id': 238, 'name': 'X5 PVZ'}, {'id': 47722, 'name': 'ГЦСС'}, {'id': 53916, 'name': 'Яндекс Доставка'},
#                    {'id': 1003746, 'name': 'ГлавДоставка'}, {'id': 1003937, 'name': 'DPD'}, {'id': 1004619, 'name': 'ТК GTD'},
#                    {'id': 1005171, 'name': 'Яндекс Такси'}, {'id': 1005372, 'name': 'Стриж. Доставка до ПВЗ'}, {'id': 1005486, 'name': 'Почта России'}]


time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
def write_smth(smth):
    f = open('no_test.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()


def make_cancel(order_id, status, substatus, campaign_id):
    data = {
        "order":
            {
                "status": status,
                "substatus": substatus
            }
    }
    url = 'https://api.partner.market.yandex.ru/v2'
    headers = {'Content-type': 'application/json',
               'Authorization': f'OAuth oauth_token={token_ym}, oauth_client_id={client_id}',
               'Content-Encoding': 'utf-8'}
    url_address = url + campaign_id + '/orders/' + order_id + '.json'
    answer = requests.put(url_address, data=json.dumps(data), headers=headers, verify=False)
    write_smth(answer)
    print('answer', str(time), answer)
    if answer.status_code == 200:
        result = True
    else:
        result = False

    return result

def send_post_to_market(metod, data, campaign_id):
    url = 'https://api.partner.market.yandex.ru/v2'
    headers = {'Content-type': 'application/json',
               'Authorization': f'OAuth oauth_token={token_ym}, oauth_client_id={client_id}',
               'Content-Encoding': 'utf-8'}
    url_address = url + metod
    answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
    write_smth(answer)
    # print('answer', str(time), answer)

def send_get_to_market(metod):
    url = 'https://api.partner.market.yandex.ru/v2'
    headers = {'Content-type': 'application/json',
               'Authorization': f'OAuth oauth_token={token_ym}, oauth_client_id={client_id}',
               'Content-Encoding': 'utf-8'}
    url_address = url + metod + '.json'
    answer = requests.get(url_address, headers=headers)
    print(str(time), answer)
    response = answer.json()
    print(str(time), response)



def send_del_to_market(id):
    url = 'https://api.partner.market.yandex.ru/v2'
    headers = {'Content-type': 'application/json',
               'Authorization': f'OAuth oauth_token={token_ym}, oauth_client_id={client_id}',
               'Content-Encoding': 'utf-8'}
    url_address = url + id
    answer = requests.delete(url_address, headers=headers)
    print(str(time), answer)
    response = answer.json()
    print(str(time), response)


def send_get_ym():
    url = 'https://api.partner.market.yandex.ru/v2'
    headers = {'Content-type': 'application/json',
               'Authorization': f'OAuth oauth_token={token_ym}, oauth_client_id={client_id}',
               'Content-Encoding': 'utf-8'}

    metod = '/delivery/services'
    url_address = url + metod + '.json'
    answer = requests.get(url_address, headers=headers)
    # print(str(time), answer)
    # response = answer.json()
    # print(str(time), response)

# send_get_ym()

# def send_post(data):
#     #sleep(6)
#     url_address = 'https://92.39.143.137:14723/Trade/hs/post/order/post'
#     headers = {'Content-type': 'application/json',
#                'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
#                'Content-Encoding': 'utf-8'}
#
#     answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
#     write_smth(answer)
#     result = answer.status_code
#
#     # datas = json.dumps(data)
#     print('answer1', str(time), answer)
#     # response = answer.json()
#     # print(datetime.datetime.now(), response)
#     return result

def send_test_post(data):
    # sleep(6)
    url_address = 'http://localhost:5000/json'  #'https://92.39.143.137:14723/Trade/hs/post/order/post'
    headers = {'Content-type': 'application/json',
               'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
               'Content-Encoding': 'utf-8'}

    answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)

    write_smth(answer)
    #print('answer', str(time), answer)
    # response = answer.json()
    # print(datetime.datetime.now(), response)


def send_test_post_cart():
    # sleep(6)
    url_address = 'http://46.173.219.89/api/stocs'  #'https://92.39.143.137:14723/Trade/hs/post/order/post'
    headers = {'Content-type': 'application/json',
               'Authorization': 'BA00000126859FCF',
               'Content-Encoding': 'utf-8'}

    answer = requests.post(url_address, headers=headers, verify=False)

    write_smth(answer)
    #print('answer', str(time), answer)
    # response = answer.json()
    # print(datetime.datetime.now(), response)

#send_test_post(order)
#send_test_post_cart()