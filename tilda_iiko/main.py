# import main Flask class and request object
import datetime
import time
import logging
import uuid
import json
from flask import Flask, request
from cred import user_id, user_secret
#from trap import access_token
import requests
from cred import organization
from gevent.pywsgi import WSGIServer
from schedule import every, repeat, run_pending


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
        #isSelfService = request_data
        if delivery == "САМОВЫВОЗ":
            street = None
            home = None
            apartment = None
            isselfservice = True
        else:
            isselfservice = False
            street = request_data['street']
            if 'home' in request_data:
                home = request_data['home']
                if len(home) > 10:
                    if 'корпус' in home:
                        home = home.replace('корпус', 'к.')
                    else:
                        home = home.strip()
            else:
                home = 'УТОЧНИТЬ'
            if 'apartment' in request_data:
                apartment = request_data['apartment']
            else:
                apartment = 'УТОЧНИТЬ'
        paymentsystem = request_data['paymentsystem']
        payment = request_data['payment']
        products = request_data['payment']['products']
        summ = request_data['payment']['subtotal']
        if 'comment' in request_data:
            comment = request_data['comment']
        else:
            comment = None

    f = open('log.txt', 'a')
    f.write(str(datetime.datetime.now()) +' request_from_tilda = ' + str(request_data) + '\n')
    # f.write('\n')
    f.close()

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
                "isSelfService": isselfservice,
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

    print("create_data", datetime.datetime.now(), create_data())


    def get_token():
        with open('trap.py') as file:
            access_token = str(file.readline())
        return access_token

    access_token = get_token()

    # def orders_add():
    url_address = 'https://iiko.biz:9900/api/0/orders/add?'  # 'https://httpbin.org/post'#'https://f73fc613-638a-487f-8a19-e528b998c4b6.mock.pstmn.io'
    headers = {'Content-type': 'application/json',  # Определение типа данных
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    # metods = '/orders/add?' #'post' #+ 'access_token=' + token.replace('"', '')
    answer = requests.post(url_address + 'access_token=' + access_token.replace('"', ''), data=json.dumps(create_data()),
                           headers=headers)

    response = answer.json()
    print(datetime.datetime.now(), response)
    f = open('log.txt', 'a')
    f.write(str(datetime.datetime.now()) + ' - reQuest = ' + str(create_data()))
    f.write('\n')
    f.write(str(datetime.datetime.now()) + ' - response = ' + str(response))
    f.write('\n')
    f.write(str(datetime.datetime.now()) + ' - answer = ' + str(answer) + '\n')
    f.write('\n')
    f.close()
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