# import main Flask class and request object
import datetime
import time
import logging
import uuid
import json
from flask import Flask, request
from cred import user_id, user_secret
from trap import token
import requests
from cred import organization
from gevent.pywsgi import WSGIServer
from schedule import every, repeat, run_pending


# class Biz:
#     def __init__(self, login, password):
#         self.login = login
#         self.password = password
#         self.address = 'https://iiko.biz/api/0'
#
#     def get_token(self):
#         try:
#             r = requests.get(
#                 self.address + '/auth/access_token?user_id=' + self.login + '&user_secret=' + self.password)
#             r.text[1:-1]
#             return r.text
#         except requests.exceptions.ConnectTimeout:
#             print("Не удалось получить токен " + "\n" + self.login)

# i = Biz(user_id, user_secret)
# token = i.get_token()
# print('Token2: ', token)
#
# @repeat(every(9).seconds) #every(10).seconds) #for development
# def job():
#     i = Biz(user_id, user_secret)
#     global token
#     token = i.get_token()
#     print(datetime.datetime.now(), 'Token3: ', token)




def getid():
    id = uuid.uuid4()  # .__hash__()  # setID
    # id = hash(str(dict_data))
    return id


# create   the Flask app
app = Flask(__name__)


@app.route('/api/0', methods=['POST'])
def json_example():
    request_data = request.get_json()
    if 'test' in request_data:
        return "test"
    else:
        customerName = request_data['customerName']
        customerPhone = request_data['phone']
        delivery = request_data['delivery']
        if delivery == "САМОВЫВОЗ":
            street = None
            home = None
            apartment = None
        else:
            street = request_data['street']
            home = request_data['home']
            apartment = request_data['apartment']
        paymentsystem = request_data['paymentsystem']
        payment = request_data['payment']
        products = request_data['payment']['products']
        summ = request_data['payment']['subtotal']
        if 'comment' in request_data:
            comment = request_data['comment']
        else:
            comment = None

    def create_items(products):
        items = []
        try:
            for prod in products:
                items.append({'id': prod['externalid'], 'name': prod['name'], \
                              'sum': prod['amount'], 'code': prod['sku'],
                              'amount': prod['quantity']})  # 'code': prod['sku'],
        except  KeyError:
            # logging.LogRecord.message
            items.append({'id': prod['externalid'], 'name': prod['name'], \
                          'sum': prod['amount'], 'amount': prod['quantity']})
        return items

    def create_data():
        data = {
            "organization": organization,
            "customer": {
                "id": None,
                "name": customerName,
                "phone": customerPhone
            },
            "order": {
                "id": None,  # getid(),
                "date": None,  # "2022-05-17 14:39:50",
                "phone": customerPhone,
                "isSelfService": "false",
                "items": create_items(products),
                "address": {
                    "city": "Санкт-Петербург",
                    "street": street,
                    "home": home,
                    "housing": None,
                    "apartment": apartment,
                    "comment": comment
                },
                "paymentItems": [
                    {
                        "sum": summ,  # !!!!
                        "paymentType": {
                            "id": "859a83b8-c1db-4411-bbf3-24b16f04eb83",
                            "code": "SAIT",
                            "name": "Оплата Сайт",
                            "comment": "САЙТ",
                            "combinable": True,
                            "externalRevision": 3462277,
                            "applicableMarketingCampaigns": None,
                            "deleted": False
                        },
                        "isProcessedExternally": True
                    }
                ]
            }
        }
        return data

    print("555", type(create_data()), create_data())

    # def orders_add():
    url_address = 'https://iiko.biz:9900/api/0/orders/add?'  # 'https://httpbin.org/post'#'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
    headers = {'Content-type': 'application/json',  # Определение типа данных
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
    answer = requests.post(url_address + 'access_token=' + token.replace('"', ''), data=json.dumps(create_data()),
                           headers=headers)

    response = answer.json()
    print(answer, datetime.datetime.now(), response)
    #print(token)

    return 'JSON Object'


if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()



# while True:
#     run_pending()
#     time.sleep(1)