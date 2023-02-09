import json
import random
import string

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from read_json import processing_json,  read_order_json
from cred import token_market_dbs, token_market_fbs


import urllib3
urllib3.disable_warnings()


def write_json(smth_json):
    with open('/var/www/html/artol/test_json.json', 'w') as file:
        json.dump(smth_json, file)


def write_smth_date():
    f = open('/var/www/html/artol/test_txt.txt', 'w')
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f.write(str(time) + '\n')
    f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    # f = open('/home/userbe/artol/no_test.txt', 'a')
    f = open('no_test.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()

write_smth(' start ')

def write_fake(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('fake_json.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()


def check_cart(items, businessId):
    data_stocks = processing_json()
    #print('check_cart', len(data_stocks))
    id_1c = ''
    for item in items:
        offer_id = item['offerId']
        need_count = item['count']
        if offer_id in data_stocks.keys():
            stock = data_stocks[offer_id].get('stock')
            id_1c = data_stocks[offer_id].get('id_ic')

            if int(stock) < need_count:
                item['count'] = int(stock)

        else:
            item['count'] = 0

    return items, id_1c


# def token_generator(size=10, chars = string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


def token_generator(size=10, chars = string.digits): #string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_data_for_1c(order, created_id, status):
    delivery = order['delivery']['type']
    #business_id = order['businessId']
    payment_type = order['paymentType']
    date_from = order['delivery']['dates']['fromDate']
    list_items = order['items']
    #print('check_is_2222222222222222accept', list_items)
    items_pr = []
    for item in list_items:
        proxy = {}
        proxy['shopSku'] = item['id_1c']
        proxy['count'] = item['count']
        proxy['price'] = item['price']
        items_pr.append(proxy)
    data_re = {
        "order": {
            "shop": "Yandex",
            #"businessId": business_id,
            "id": created_id,
            "paymentType": payment_type,
            "delivery": delivery,
            "status": status,
            "date": date_from,
            "items": items_pr
        }
    }
    #print('data_re', data_re)
    return data_re


def make_cancel(order_id):
    data  = read_order_json()
    if str(order_id) in data.keys():
        our_order = data[str(order_id)]
        created_id = our_order.get("created_id")
        print(our_order)

        return our_order


def check_stocks(skus, warehouse_id):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    data_stocks = processing_json()
    proxy_list = []
    for sku in skus:
        if sku in data_stocks:
            count = data_stocks[sku].get('stock')
            if count is None:
                count = 0
            data = {
                "sku": sku,
                "warehouseId": warehouse_id,
                "items":
                [
                    {
                        "type": "FIT",
                        "count": count,
                        "updatedAt": str(time)
                    }
                ]
            }
            proxy_list.append(data)
    
    return {"skus": proxy_list}  #, proxy_list


def write_order(order, created_id):
    data = read_order_json()
    print('write_order', type(order))
    order_id = order.get("id")
    order['created_id'] = created_id
    if order_id not in data.keys():
        data[order_id] = order
        with open("/var/www/html/artol/orders.json", 'w') as file:
            json.dump(data, file)
    else:
        rewrite_order_status(order)


def rewrite_order_status(order):
    data = read_order_json()
    print('re_write_order', type(order))
    order_id = order.get("id")
    status = order.get("status")
    substatus = order.get("substatus")
    if order_id in data.keys():
        current_order = data[order_id]
        current_order["prev_status"] = current_order["status"]
        current_order["status"] = status
        current_order["substatus"] = substatus
        data[order_id] = current_order

    with open("/var/www/html/artol/orders.json", 'w') as file:
    # with open("orders.json", 'w') as file:
        json.dump(data, file)


def data_summary():
    with open("/var/www/html/artol/orders.json", 'r') as file:
        data_orders = json.load(file)

    return data_orders


def check_is_accept(list_items):
    print(type(list_items))
    data = processing_json()
    result_global = False
    cnt = 0

    for item in list_items:
        shop_sku = item['shopSku']
        if shop_sku in data.keys():
            item_data = data.get(shop_sku)
            count = item_data['stock']
            if count >= item['count']:
                result = True
                cnt += 1
            else:
                result = False
            item['id_1c'] = item_data.get('id_1c')
            item['result'] = result

    if cnt == len(list_items):
        result_global = True
    print('check_is_accept', cnt, len(list_items))
    return result_global, list_items



def order_resp(order, global_result):
    if global_result:
        id_create = token_generator()
        data = {
            "order": {
                "accepted": True,
                "id": id_create,
            }
        }
        write_order(order, id_create)
        # result = True
    else:
        data = {
            "order":
                {
                    "accepted": False,
                    "reason": "OUT_OF_DATE"
                }
        }
        id_create = None

    return data, id_create


def proxy_time():
    dt = datetime.now().date() + timedelta(days=2)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt


def create_re_cart(items):
    service_name = "Яндекс Доставка"
    delivery_id = token_generator()
    proxy_list = []
    for item in items:
        proxy_item = {}
        proxy_item['sellerInn'] = "6234113064"
        proxy_item['delivery'] = True
        proxy_item['feedId'] = item['feedId']
        proxy_item['offerId'] = item['offerId']
        proxy_item['count'] = item['count']
        proxy_list.append(proxy_item)

    data = {
       "cart":
       {
        "deliveryOptions":
        [
            {
            "id": delivery_id,
            "serviceName": service_name,
            "type": "DELIVERY",
            "dates":
               {
              "fromDate": proxy_time(),
               }
            }
        ],
        "items": proxy_list,
        "paymentMethods":
        [
               "YANDEX",
               "CARD_ON_DELIVERY",
               "CASH_ON_DELIVERY",
               "TINKOFF_CREDIT",
               "TINKOFF_INSTALLMENTS",
               "SBP"
           ]
        }
    }

    return data


async def send_post(data):
    url_address = 'https://92.39.143.137:14723/Trade/hs/post/order/post'
    headers = {'Content-type': 'application/json',
               'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ==',
               'Content-Encoding': 'utf-8'}
    answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
    write_smth(answer)
    result = answer.status_code
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    print('answer1', str(time), answer)
    #return result


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


# allow both GET and POST requests
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        campaign_id = request.form.get('campaign_id')
        status = 'CANCELLED'
        substatus = 'SHOP_FAILED'
        smth = make_cancel(order_id)
        return f'''<h2>The cenceled order {order_id} is: {smth[0]}</h2>
        <form method="GET">
        <button type="submit">BACK</button>
        </form>'''
    # elif request.method == 'GET':
    return '''
        <form id="cancel" method="POST"></form>
            <div><label>OrderID: <input type="text" name="order_id"></label>
        
        <select name="cancel" size="2" multiple form="cancel">
            <option value="40215474">ARTOL_DBS</option>
            <option value="10771112">FBS_ARTOL</option>
        </select>
        <input type="submit" value="CANCEL"></div>
        
        '''


#
@app.route('/json', methods=['GET', 'POST'])
def json_example():
    head = request.headers.get('X-Forwarded-For')
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return ::ffff:92.39.143.137
    # head = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)  ## return ::ffff:92.39.143.137
    print('X-Forwarded-For', type(ip_addr), ip_addr)
    print('REMOTE_ADDR', type(head), head)
    if str(ip_addr) == '::ffff:92.39.143.137':
        request_data = request.get_json()
        # if 'test' in request_data:
        write_json(request_data)
        write_smth_date()

        print(request_data)
        response = app.response_class(
            status=200
        )

    else:

        response = app.response_class(
            status=403
        )

    return response


@app.route('/order/accept', methods=['POST'])
async def order_accept():
    # req = request.get_json()
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        data_req = request.get_json()
        confirm_data = data_req["order"].get('fake')
        order = data_req["order"]
        proxy = order['items']
        stock = check_is_accept(proxy)  # проверяем наличие for order
        data = order_resp(order, False)
        response = app.response_class(json.dumps(data[0]), status=200, content_type='application/json')
        if stock[0]:
            order['items'] = stock[1]   ###?????
            print('id_ic', order.get('id_ic'))
            data = order_resp(order, stock[0])
            send_data = create_data_for_1c(order, data[1], "accept")
            print('send_data', send_data)
            if confirm_data is not True: ## if order not test
                se_id = str(send_data['order']['id'])  #for test
                write_smth(' order_id_accept ' + se_id)  #for test
                await send_post(send_data)

                write_order(order, data[1])  # TODO #is need create for 2 model? FBS & DBS
                response = app.response_class(
                    json.dumps(data[0]),
                    status=200,
                    content_type='application/json'
                )

                # se_id = str(send_data['order']['id'])  #for test
                # write_smth(' order_id_accept ' + se_id)  #for test
                # result = send_post(send_data)
                # if result == 200:
                #     write_order(order, data[1])  # TODO #is need create for 2 model? FBS & DBS
                #     response = app.response_class(
                #         json.dumps(data[0]),
                #         status=200,
                #         content_type='application/json'
                #     )

            else:
                write_fake(data_req)
                response = app.response_class(
                json.dumps(data[0]),
                status=200,
                content_type='application/json'
            )

    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/order/status', methods=['POST'])
def status():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        order = request_data.get("order")
        status = order.get("status")
        if status == "CANCELLED":
            try:
                id = order["id"]
                #print('created_', id)
                our_order = make_cancel(id)
                print('/order/status', status,  our_order)
                created_id  = our_order["created_id"]
                data = create_data_for_1c(our_order, created_id, "canceled")
                result = send_post(data)
                print('CANCELLED', result)
            except :
                rewrite_order_status(order)
                response = app.response_class(
                    status=200
                )

        else:
            rewrite_order_status(order)

        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/cart', methods=['POST'])
def cart():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        cart = request_data.get('cart')
        businessId = cart.get('businessId')
        #delivery = cart.get('delivery')
        items = cart.get('items')
        check = check_cart(items, businessId)
        data = create_re_cart(check[0])
        print(check)
        response = app.response_class(
            json.dumps(data),
            status=200,
            content_type='application/json'
        )

    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        data = data_summary()  #TODO
        response = app.response_class(
            json.dumps(data),
            status=200,
            content_type='application/json'
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/stocks', methods=['POST'])
def stocks():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        req = request.get_json()
        warehouseId = req.get('warehouseId')
        skus = req.get('skus')
        result = check_stocks(skus, warehouseId)
        response = app.response_class(
            json.dumps(result),
            status=200,
            content_type='application/json'
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/order/cancellation/notify', methods=['POST'])
def order_cancell():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        req_cancell = request.get_json()
        order = req_cancell.get('order')
        rewrite_order_status(order)

        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=403
        )

    return response

@app.route('/test', methods=['GET'])
def test():
    return "OK"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
