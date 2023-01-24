# def orders_add():
import datetime
import json

import requests
# data = '''{
#     "language" : "Русский",
#     "framework" : "Кириллица",
#     "website" : "Рандом",
#     "version_info" : {
#         "python" : "3.9.0",
#         "flask" : "1.1.2"
#     },
#     "examples" : ["query", "form", "json"],
#     "boolean_test" : true
# }'''
# file  = open('data_json.json', 'r')
# data = file.readlines()
#
# print(type(data))
#
# file =  open('data_json.json', 'r')
# data = json.load(file)
# print(type(data))

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

# url_address = 'https://92.39.143.137:14723/Trade/hs/post/order/post'   #'http://super-good.ml:8800/json'  #   'http://iiko.ml:8800/json'   ##  # #'https://iiko.biz:9900/api/0/orders/add?'  # 'https://httpbin.org/post'#'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
# headers = {'Content-type': 'application/json',  # Определение типа данных
#            'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
#            'Content-Encoding': 'utf-8'}
# # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
# answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
# print(datetime.datetime.now(), answer)
# # response = answer.json()
# # print(datetime.datetime.now(), response)