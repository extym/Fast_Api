from gevent import monkey

monkey.patch_all()

import json
import random
import string

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from read_json import processing_json, read_order_json, read_json_on
from cred import token_market_dbs, token_market_fbs, url_address, headers
from ozon import product_info_order
# from proxy import proxy_onon

import urllib3

urllib3.disable_warnings()


def write_json(smth_json):
    try:
        with open('/var/www/html/artol/test_json.json', 'w') as file:
            json.dump(smth_json, file)
    except:
        with open('test_json.json', 'w') as file:
            json.dump(smth_json, file)


def write_smth_date():
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open('/var/www/html/artol/test_txt.txt', 'w')
        f.write(str(time) + '\n')
        f.close()
    except:
        f = open('test_txt.txt', 'w')
        f.write(str(time) + '\n')
        f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open('/home/userbe/artol/no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    except:
        f = open('no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()


write_smth(' start ')


def write_fake(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('fake_json.json', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()


def check_cart(items, businessId):
    data_stocks = processing_json()
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


def write_order(order, created_id):
    data = read_order_json()
    order_id = order.get("id")
    order['created_id'] = created_id
    if order_id not in data.keys():  # check order is exist
        data[order_id] = order
        try:
            with open("/var/www/html/artol/orders.json", 'w') as file:
                json.dump(data, file)
        except:
            with open("orders.json", 'w') as file:
                json.dump(data, file)


# def token_generator(size=10, chars = string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


def token_generator(size=10, chars=string.digits):  # string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


## check the order number for the one date and shop
def check_order_number(order_id, shipment_date, shop):
    is_day_in_orders = False
    order_num = order_id
    data = read_order_json()
    for value in data.values():
        try:
            if value['delivery']['shipments'][0]['shipmentDate'] == shipment_date and shop == "Yandex":
                order_num = value['created_id']
                is_day_in_orders = True
                break

            string_time = value.get('shipment_date', '00T00').split('T')[0]
            if reverse_time(string_time) == shipment_date and shop == "Ozon":
                order_num = value['created_id']
                is_day_in_orders = True
                break
        except:
            continue
    print('check_order_number', is_day_in_orders, order_num, shipment_date, shop)
    return is_day_in_orders, order_num, shipment_date


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result


def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt


def create_data_for_1c(order, status, shop):
    data_re = {}
    if shop == "Yandex":
        try:
            shipment_date = order['delivery']['shipments'][0].get('shipmentDate')
        except:
            shipment_date = order.get('shipmentDate')
        if shipment_date is None:
            shipment_date = proxy_time()
        response_id = order['our_id']
        order_number = check_order_number(response_id, shipment_date, shop)
        list_items = order['items']
        items_pr = []
        for item in list_items:
            proxy = {}
            proxy['shopSku'] = item['id_1c']
            proxy['count'] = item['count']
            proxy['price'] = item['price']
            items_pr.append(proxy)
        data_re = {
            "order": {
                "shop": shop,  # "Yandex",
                "businessId": order['businessId'],
                # "id": response_id,
                "id": order_number[1],
                "paymentType": order['paymentType'],
                "delivery": order['delivery']['type'],
                "status": status,
                "date": order_number[2],
                "items": items_pr
            }
        }

    elif shop == "Ozon":
        # shipment_date = order['in_process_at'].split('T')[0]
        shipment_date = proxy_time_1()  # ?????????
        response_id = order['our_id']
        order_number = check_order_number(response_id, shipment_date, shop)
        list_items = order['products']
        items_pr = []
        for item in list_items:
            proxy = {}
            proxy['shopSku'] = item['id_1c']
            proxy['count'] = item['quantity']
            proxy['price'] = item['price'][:-2]
            items_pr.append(proxy)
        data_re = {
            "order": {
                "shop": shop,
                "businessId": order['order_number'],
                # "id": response_id,
                "id": order_number[1],
                "paymentType": 'PREPAID',
                "delivery": order['delivery_method']['id'],
                "status": status,
                "date": shipment_date,  # order_number[2],
                "items": items_pr
            }
        }
        # print('data_re', data_re)

    return data_re


def make_cancel(order_id):
    data = read_order_json()
    if str(order_id) in data.keys():
        our_order = data[str(order_id)]
        # created_id = our_order.get("created_id")
        print(our_order)

        return our_order


def check_stocks(skus, warehouse_id):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    data_stocks = processing_json()
    proxy_list = []
    for sku in skus:
        if sku in data_stocks:
            count = data_stocks[sku].get('stock', "0")
            if count == None:
                count = "0"
            data = {
                "sku": sku,
                "warehouseId": warehouse_id,
                "items":
                    [
                        {
                            "type": "FIT",
                            "count": str(count),
                            "updatedAt": str(time)
                        }
                    ]
            }
            proxy_list.append(data)

    return {"skus": proxy_list}  # , proxy_list


def rewrite_order_status(order):
    data = read_order_json()
    order_id = order.get("id")
    status = order.get("status")
    substatus = order.get("substatus")
    if str(order_id) in data.keys() and status != "DELIVERED":
        order["prev_status"] = order["status"]
        order["status"] = status
        order["substatus"] = substatus

    elif status == "DELIVERED":
        try:
            del data[str(order_id)]

        except Exception as error:
            print('ERROR', error)
    else:
        print('WRONG ORDER', order_id)

    with open("/var/www/html/artol/orders.json", 'w') as file:
        # with open("orders.json", 'w') as file:
        json.dump(data, file)


def data_summary():
    with open("/var/www/html/artol/orders.json", 'r') as file:
        data_orders = json.load(file)

    return data_orders


def check_is_accept_ym(list_items):
    data = processing_json()
    result_global = False
    cnt = 0
    for item in list_items:
        shop_sku = item['offerId']
        if shop_sku in data.keys():
            item_data = data.get(shop_sku)
            count = item_data['stock']
            if count >= item['count']:
                # result = True
                cnt += 1
            # else:
            #     result = False
            item['id_1c'] = item_data.get('id_1c')
            # item['result'] = result

    if cnt == len(list_items):
        result_global = True

    return result_global, list_items


def check_is_accept_onon(list_items):
    data = read_json_on()
    result_global, cnt = False, 0
    for item in list_items:
        vendor_code = item['offer_id']
        if vendor_code in data.keys():
            item_data = data.get(vendor_code)
            count = item_data[2]
            print(count, item['quantity'])
            if int(count) >= item['quantity']:
                cnt += 1
            item['id_1c'] = item_data[0]

    if cnt == len(list_items):
        result_global = True
    print(cnt, len(list_items))
    return result_global, list_items


def order_resp_ym(order, global_result):
    if global_result:
        response_id = token_generator()
        data = {
            "order": {
                "accepted": True,
                "id": response_id,
            }
        }
        write_order(order, response_id)

    else:
        data = {
            "order":
                {
                    "accepted": False,
                    "reason": "OUT_OF_DATE"
                }
        }
        response_id = None

    return data, response_id


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
        proxy_item = {'sellerInn': "6234113064",
                      'delivery': True,
                      'feedId': item['feedId'],
                      'offerId': item['offerId'],
                      'count': item['count']}
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
    answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
    write_smth(answer)
    write_smth(data)
    # result = answer.text
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    print('answer1', str(time), answer, data)
    # return result


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


common_comfirm_response = {"result": True}
common_error = {'error': {
    "code": "ERROR_UNKNOWN",
    "message": "Неизвестный метод",
    "details": None}}
common_product_error = {'error': {
    "code": "ERROR_UNKNOWN",
    "message": "Product not found",
    "details": None}}


@app.route('/api/on', methods=['GET', 'POST'])
async def onon_push():
    resp = request.get_json()
    # print('api_on_resp', resp)
    if resp.get('message_type') == 'TYPE_PING':
        time = resp["time"]
        response = app.response_class(
            json.dumps({"version": "v.1",
                        "name": "brain-trust.bot",
                        "time": time}),
            status=200
        )

    elif resp.get("message_type") == "TYPE_NEW_POSTING":
        id_mp = resp["posting_number"]
        our_id = id_mp.replace('-', '')[:10]
        order = product_info_order(id_mp)
        # order = proxy_onon["result"]   #FOR TEST ONLY
        stock = check_is_accept_onon(order['products'])
        print('stock', stock[0], order['products'])
        if stock[0]:
            order['our_id'], order['id'], order['status'], order['our_status'], order['shop'] \
                = our_id, id_mp, "NEW", "NEW", "Ozon"
            order['products'] = stock[1]
            send_data = create_data_for_1c(order, "accept", "Ozon")
            print('send_data', send_data)
            se_id = str(send_data['order']['id'])
            write_smth(' order_id_accept ' + se_id)
            await send_post(send_data)
            write_order(order, our_id)
            response = app.response_class(
                json.dumps(common_comfirm_response),
                status=200
            )

        else:
            response = app.response_class(
                json.dumps(common_product_error),
                status=200
            )

    elif resp.get("message_type") == "TYPE_POSTING_CANCELLED":
        order_id = resp["posting_number"]
        our_order = make_cancel(order_id)
        if our_order is not None:
            created_id = our_order.get("created_id")
            data = create_data_for_1c(our_order, "canceled", "Ozon")
            print('send_cancel_data', data, created_id, our_order)
            await send_post(data)
            response = app.response_class(
                json.dumps(common_comfirm_response),
                status=200
            )
        else:
            body = {order_id: 'ORDER NOT FOUND'}
            response = app.response_class(
                json.dumps(body),
                status=400,
                content_type='application/json'
            )

        # response = app.response_class(
        #     json.dumps(common_comfirm_response),
        #     status=200
        # )

    else:
        response = app.response_class(
            json.dumps(common_error),
            status=400
        )

    print('api_on_response', response)
    return response


#
@app.route('/json', methods=['GET', 'POST'])
def json_example():
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return ::ffff:92.39.143.137
    if str(ip_addr) == '::ffff:92.39.143.137':
        request_data = request.get_json()
        write_json(request_data)
        write_smth_date()

        # print(request_data)
        response = app.response_class(
            status=200
        )

    else:

        response = app.response_class(
            status=403
        )

    return response


##СЕЙЧАС ПЕРЕСОЗДАЕТ И ПЕРЕЗАПИСЫВАЕТ НОМЕРА ЗАКАЗОВ
@app.route('/order/accept', methods=['POST'])
async def order_accept():
    # req = request.get_json()
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        data_req = request.get_json()
        b2b = data_req['order'].get("paymentMethod")
        if b2b == "B2B_ACCOUNT_PREPAYMENT":
            data_req['order']['delivery']['shipments'][0]['shipmentDate'] = proxy_time()
            data_req['order']['shipmentDate'] = proxy_time()
        confirm_data = data_req["order"].get('fake')
        current_order = data_req["order"]
        proxy = current_order['items']
        stock = check_is_accept_ym(proxy)  # проверяем наличие for order

        data = order_resp_ym(None, False)
        response = app.response_class(
            json.dumps(data[0]),
            status=200,
            content_type='application/json')

        if stock[0]:
            current_order['items'], current_order['shop'] = stock[1], "Yandex"
            data = order_resp_ym(current_order, stock[0])
            current_order['our_id'] = data[1]
            send_data = create_data_for_1c(current_order, "accept", "Yandex")
            print('send_data', send_data)
            if confirm_data is not True:  ## if order not test
                se_id = str(send_data['order']['id'])
                write_smth(' order_id_accept ' + se_id)
                await send_post(send_data)

                response = app.response_class(
                    json.dumps(data[0]),
                    status=200,
                    content_type='application/json'
                )

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
async def status():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        order = request_data.get("order")
        id = order["id"]
        status = order.get("status")
        response = app.response_class(status=200)
        if status == "CANCELLED":
            our_order = make_cancel(id)
            if our_order is not None:
                created_id = our_order.get("created_id")
                data = create_data_for_1c(our_order, created_id, "canceled")
                await send_post(data)
            # else:
            #     body = {id: 'ORDER NOT FOUND'}
            #     response = app.response_class(
            #         json.dumps(body),
            #         status=400,
            #         content_type='application/json'
            #     )

        else:
            rewrite_order_status(order)
            # if res == False:
            #
            #     body = {id: 'ORDER NOT FOUND'}
            #     response = app.response_class(
            #         json.dumps(body),
            #         status=400,
            #         content_type='application/json'
            #     )

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
        # delivery = cart.get('delivery')
        items = cart.get('items')
        check = check_cart(items, businessId)
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
        data = data_summary()
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
        # id = order['id']
        # re = rewrite_order_status(order)
        # if re == False:
        #     body = {id: 'ORDER NOT FOUND'}
        #     response = app.response_class(
        #         json.dumps(body),
        #         status=400,
        #         content_type='application/json'
        #     )
        # else:
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

# @app.route('/form', methods=['GET', 'POST'])
# def form():
#     if request.method == 'POST':
#         order_id = request.form.get('order_id')
#         campaign_id = request.form.get('campaign_id')
#         status = 'CANCELLED'
#         substatus = 'SHOP_FAILED'
#         smth = make_cancel(order_id)
#         return f'''<h2>The cenceled order {order_id} is: {smth[0]}</h2>
#         <form method="GET">
#         <button type="submit">BACK</button>
#         </form>'''
#     # elif request.method == 'GET':
#     return '''
#         <form id="cancel" method="POST"></form>
#             <div><label>OrderID: <input type="text" name="order_id"></label>
#
#         <select name="cancel" size="2" multiple form="cancel">
#             <option value="40215474">ARTOL_DBS</option>
#             <option value="10771112">FBS_ARTOL</option>
#         </select>
#         <input type="submit" value="CANCEL"></div>

# '''
