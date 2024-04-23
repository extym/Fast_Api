# def orders_add():
import datetime
import json

import requests
# data = '''
# {
#     "order": {
#         "shop": "Yandex",
#         "businessId": "3675591",
#         "id": "12771",
#         "paymentType": "PREPAREID",
#         "delivery": false,
#         "items": [
#             {
#                 "shopSku": "4fc6a7b0-ad96-11e2-9997-902b34460e77",
#                 "count": 2,
#                 "price": 336
#             },
#             {
#                 "shopSku": "c9bb4043-d821-11e2-bda3-902b34460e77",
#                 "count": 2,
#                 "price": 520
#             }
#         ]
#     }
# }
# '''
# file  = open('data_json.json', 'r')
# data = file.readlines()
#
# print(type(data))
#
# file =  open('data_json.json', 'r')
# data = json.load(file)
# print(type(data))

data_psh = {
    "order": {
        "shop": "Yandex",
        "businessId": "3675591",
        "id": "127712771",
        "paymentType": "PREPAREID",
        "delivery": False,
        "status": "stop",
        "date": "12-02-2023",
        "items": []
    }
}

data_pshh = {
    "order": {
        "shop": "Ozon",
        "businessId": "3675591",
        "id": "127712771",
        "paymentType": "PREPAREID",
        "delivery": True,
        "status": "accept",
        "date": "21-02-2023",
        "items": [
            {
                "shopSku": "26fb989e-fdbe-11ec-a655-00155d58510a",
                "count": 2,
                "price": 1336
            }
        ]
    }
}



data_pshh_2 = {
    "order": {
        "shop": "Ozon",
        "businessId": "3675591",
        "id": "127712771",
        "paymentType": "PREPAREID",
        "delivery": True,
        "status": "accept",
        "date": "21-02-2023",
        "items": [
            {
                "shopSku": "26fb989e-fdbe-11ec-a655-00155d58510a",
                "count": -2,
                "price": 999999001336
            }
        ]
    }
}

# url_address = 'https://92.39.143.137:14723/Trade/hs/post/order/post'   #'http://super-good.ml:8800/json'  #   'http://iiko.ml:8800/json'   ##  # #'https://iiko.biz:9900/api/0/orders/add?'  # 'https://httpbin.org/post'#'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
# headers = {'Content-type': 'application/json',  # Определение типа данных
#            'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
#            'Content-Encoding': 'utf-8'}
# # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
# answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
# print(datetime.datetime.now(), answer)
# # response = answer.json()
# # print(datetime.datetime.now(), response)