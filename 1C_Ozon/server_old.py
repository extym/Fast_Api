import json
import random
import string

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from read_json import processing_json
token_market_dbs = ''
token_market_fbs = ''
#from cred import token_market_dbs, token_market_fbs, compaing_id_dbs, compaing_id_fbs
#from request import send_post, make_cancel


# time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()

# print(time)  #for development


def write_json(smth_json):
    with open('test.json', 'w') as file:
        json.dump(smth_json, file)


def write_smth_date():
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('test_txt.txt', 'w')
    f.write(str(time) + '\n')
    f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('no_test.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()


write_smth(' start ')


def write_fake(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('fake_json.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()
    # with open('fake_jon.json', 'w') as file:
    #     json.dump(smth, file)


def check_cart(items, businessId):
    data_stocks = processing_json()
    # print('check_cart', len(data_stocks))
    id_1c = ''
    for item in items:
        offer_id = item['offerId']
        count = item['count']
        if offer_id in data_stocks.keys():
            stock = data_stocks[offer_id].get('stock')
            id_1c = data_stocks[offer_id].get('id_ic')

            if int(stock) < count:
                item['count'] = int(stock)

        else:
            item['count'] = 0

    return items, id_1c


def token_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_data_for_1c(order, list_items, created_id):
    delivery = order['delivery']['type']
    business_id = order['businessId']
    payment_type = order['paymentType']
    # items = order['items']
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
            "businessId": business_id,
            "id": created_id,
            "paymentType": payment_type,
            "delivery": delivery,
            "items": items_pr
        }
    }
    print('data_re', data_re)
    return data_re


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

    return {"skus": proxy_list}  # , proxy_list


def write_order(order):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    print('write_order', type(order))
    f = open('orders.txt', 'a')
    f.write(str(time) + str(order) + '\n')
    f.close()
    # order_id = order.get("order_id")
    with open("orders.json", 'w') as file:
        json.dump(order, file)

    # return order_id


def data_summary():
    with open("orders.json", 'r') as file:
        data_orders = json.load(file)

    return data_orders


def check_is_accept(list_items):
    data = processing_json()
    result_global = False
    cnt = 0
    print('check_is_2222222222222222accept', list_items)
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
    print('check_is_accept', count, len(list_items))
    return result_global, list_items


def order_resp(order, global_result):
    order_id = order.get("id")
    id_create = token_generator()
    result = ''
    if global_result:
        data = {
            "order": {
                "accepted": True,
                "id": id_create,
            }
        }
        # write_order(order)
        result = id_create
    else:
        data = {
            "order":
                {
                    "accepted": False,
                    "id": order_id,
                    "reason": "OUT_OF_DATE"
                }
        }
        # result = False

    return data, result, id_create


# def make_cancel(order_id):
#
#     return True, order_id

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
        proxy_item['sellerInn'] = ""
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


# def send_resp():
#     r = requests.post('', data=data)


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
        #smth = make_cancel(order_id, status, substatus, campaign_id)
        return f'''<h2>The cenceled order {order_id} is: </h2>
        <form method="GET">
        <button type="submit">BACK</button>
        </form>'''
    # elif request.method == 'GET':
    return '''
        <form id="cancel" method="POST"></form>
            <div><label>OrderID: <input type="text" name="order_id"></label>

        <select name="cancel" size="2" multiple form="cancel">
            <option value="40215474">DBS</option>
            <option value="10771112">FBS</option>
        </select>
        <input type="submit" value="CANCEL"></div>

        '''


#
@app.route('/json', methods=['GET', 'POST'])
def json_example():
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return ::ffff:62.76.102.53
    head = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)  ## return ::ffff:62.76.102.53
    print('X-Forwarded-For', type(ip_addr), ip_addr)
    print('REMOTE_ADDR', type(head), head)
    if str(ip_addr) == '::ffff:62.76.102.53':
        request_data = request.get_json()
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
        stock = check_is_accept(proxy)
        data = order_resp(order, stock[0])
        if stock[0]:
            send_data = create_data_for_1c(order, proxy, data[1])
            print('send_data', send_data)
            write_order(send_data)  # TODO #is need create for 2 model? FBS & DBS
            if confirm_data is not True:
                se_id = str(send_data['order']['id'])
                write_smth(' order_id_accept ' + se_id)
                #await send_post(send_data)
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


@app.route('/cart', methods=['POST'])
def cart():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        cart = request_data.get('cart')
        if cart is not None:
            businessId = cart.get('businessId')
            delivery = cart.get('delivery')
            items = cart.get('items')
            # cart = {"cart":{}}
            check = check_cart(items, businessId)
            # TODO
            data = create_re_cart(check[0])

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
        data = data_summary()  # TODO
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


@app.route('/order/status', methods=['POST'])
def status():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        order_status = request_data['order']['status']
        write_smth(order_status)
        # TODO
        # if order_status == 'DELIVERED':
        #     write_order(request_data)
        # else:
        #     pass

        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/stocks', methods=['POST'])
def stocks():
    headers = dict(request.headers)
    request_data = request.get_json()
    write_smth(request_data)
    write_smth(headers)
    ## for debag
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
        write_smth(req_cancell)

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
    http_server = WSGIServer(('', 8800), app)
    http_server.serve_forever()
