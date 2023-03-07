from gevent import monkey
monkey.patch_all()

from conn import *
import random
import string
import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from read_json import process_json_dict,  read_order_json, read_json_sper
from our_request import data_psh, data_pshh

token_market_dbs = 'BA00000126859FCF'
token_market_fbs = ''
#from cred import token_market_dbs, token_market_fbs

import urllib3
urllib3.disable_warnings()


#time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
#print(time)  #for development


def write_json(smth_json):
    # with open('test_json.json', 'w') as file:
    with open('/var/www/html/stm/test_json.json', 'w') as file:
        json.dump(smth_json, file)


def write_smth_date():
    # f = open('test_txt.txt', 'r+')
    f = open('/var/www/html/stm/test_txt.txt', 'w')
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f.write(str(time) + '\n')
    f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    # f = open('no_test.txt', 'a')
    f = open('/var/www/html/stm/no_test.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()


# write_smth(' start ')


def write_fake(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open('fake_json.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
    f.close()
    # with open('fake_jon.json', 'w') as file:
    #     json.dump(smth, file)


def check_cart(items, business_id):
    data_stocks = process_json_dict()
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


def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# def token_generator(size=10, chars = string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


def create_data_for_1c(data):
    list_items = data[12]
    items_pr = []
    # for item in list_items:
    #     proxy = {}
    #     proxy['shopSku'] = item['id_1c']
    #     proxy['count'] = item['count']
    #     proxy['price'] = item['price']
    #     items_pr.append(proxy)
    data_re = {
        "order": {
            "shop": data[6],
            "businessId": data[2],
            "id": data[1],
            "paymentType": data[10],
            "delivery": data[13],
            "status": data[8],
            "date": data[7],
            "items": items_pr
        }
    }
    print('data_re', data_re)
    return data_re




def check_stocks(skus, warehouse_id):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    data_stocks = process_json_dict()
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


def write_order(order, created_id, shop):
    data = read_order_json()
    print('write_order', type(order))
    order_id = order.get("id")
    order['created_id'] = created_id
    if order_id not in data.keys():
        data[order_id] = order
    else:
        rewrite_order_status(order, shop)
    with open("orders.json", 'w') as file:
        json.dump(data, file)

    # return order_id



def rewrite_order_status(order, shop):
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

    with open("orders.json", 'w') as file:
        json.dump(data, file)

    # return order_id


def data_summary():
    with open("orders.json", 'r') as file:
        data_orders = json.load(file)

    return data_orders


def check_is_accept_ym(list_items):
    data = process_json_dict()
    result_global = False
    cnt = 0
    print('check_is_accept_ym', list_items)
    for item in list_items:
        shop_sku = item['shopSku']
        if shop_sku in data.keys():
            item_data = data.get(shop_sku)
            count = item_data[2]
            if count >= item['count']:
                result = True
                cnt += 1
            else:
                result = False
            item['id_1c'] = item_data[0]
            item['result'] = result

    if cnt == len(list_items):
        result_global = True
    #print('check_is_accept_ym_222222222', count, len(list_items))
    return result_global, list_items


def check_is_accept_sb(list_items):
    data = read_json_sper()  #return list
    result_global = False
    cnt = 0
    for item in list_items:
        item['id_1c'] = None
        shop_sku = item['offerId']
        for row in data:
            if row[1] == shop_sku:
                count = row[3]
                if count >= item['quantity']:
                    cnt += 1
                item['id_1c'] = row[0]

    if cnt == len(list_items):
        result_global = True
    print(result_global, list_items)
    return result_global, list_items


def order_resp_ym(order, global_result):
    id_create = token_generator()
    if global_result:
        data = {
            "order": {
                "accepted": True,
                "id": id_create,
            }
        }
        write_order(order, id_create, "Yandex")
        # result = True
    else:
        data = {
            "order":
                {
                    "accepted": False,
                    "reason": "OUT_OF_DATE"
                }
        }
        # result = False

    return data, id_create


def order_resp_sb(global_result, is_new):
    id_create = None
    if global_result:
        data = {
                "data": {},
                "meta": {},
                "success": 1
            }
        if is_new:
            id_create = token_generator()

    else:
        data = {
                "data": {},
                "meta": {},
                "success": 0
            }

    return data, id_create


def make_cancel(order_id, shop):
    #data  = execute_query(query_read_order, (order_id, shop))
    execute_query(update_status_order, ('canceled', "NEW", order_id, shop))

    # return created_id


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
              "fromDate": proxy_time(),   #data['cart']["deliveryOptions"][0]["dates"]["fromDate"]
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

#
##for sper
def counter_items(items_list):
    count = 1
    if len(items_list) > 1:
        proxy = items_list[0]['offerId']
        for i in range(1, len(items_list)):
            if items_list[i]['offerId'] == proxy:
                count += 1
                items_list[i - 1]['quantity'] = count
                del items_list[i]

            else:
                proxy = items_list[i]['offerId']
    print(items_list)
    return items_list

#
# async def send_post(data):
#     url_address = ''
#     headers = {'Content-type': 'application/json',
#                'Authorization': 'Basic 0JzQsNGA0LrQtdGC0L/Qu9C10LnRgdGLOjExMQ=11=',
#                'Content-Encoding': 'utf-8'}
#     answer = requests.post(url_address, data=json.dumps(data), headers=headers, verify=False)
#     write_smth(answer)
#     result = answer.status_code
#     time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
#     print('answer1', str(time), answer)
#     #return result


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result

#"Yandex", "Ozon", "Sber", "Leroy", "WB"

def reformat_data_order(order, shop):
    result = None
    if shop == 'Yandex':
        result = (
            order["id"],
            order["our_id"],
            shop,   #order["shop"],
            order["delivery"]["shipments"][0]["shipmentDate"],
            order["status"],
            order["our_status"],
            order["paymentType"],
            order["delivery"]["type"]
        )

    elif shop == 'Ozon':
        result = (
            order['order']["id"],
            order['order']["our_id"],
            order['order']["shop"],
            order['order']["date"],
            order['order']["status"],
            order['order']["paymentType"],
            order['order']["delivery"]
        )

    elif shop == 'Sber':
        time = order["shipments"][0]["shipmentDate"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            order['our_id'],
            shop,  #order["shop"],
            reverse_time(time),
            order["status"],
            order["our_status"],
            "PREPAID",  #order['data'].get("paymentType"),
            order["shipments"][0]['fulfillmentMethod']
        )

    elif shop == 'Leroy':
        result = (
            order['order']["id"],
            order['order']["our_id"],
            order['order']["shop"],
            order['order']["date"],
            order['order']["status"],
            order['order']["paymentType"],
            order['order']["delivery"]
        )

    elif shop == 'WB':
        result = (
            order['order']["businessId"],
            order['order']["id"],
            order['order']["shop"],
            order['order']["date"],
            order['order']["status"],
            order['order']["paymentType"],
            order['order']["delivery"]
        )

    return result


def reformat_data_items(order, shop):
    result = []
    if shop == 'Yandex':
        list_items = order['items']
        for item in list_items:
            proxy = (
                order["id"],
                order["our_id"],
                shop,
                order["our_status"],
                item["offerId"],
                item["id_ic"],
                item["count"],
                item["price"]
            )
            result.append(proxy)

    elif shop == 'Ozon':
        result = (
            order['order']["id"],
            order['order']["our_id"],
            order['order']["shop"],
            order['order']["date"],
            order['order']["status"],
            order['order']["paymentType"],
            order['order']["delivery"]
        )

    elif shop == 'Sber':
        list_items = order["items"]
        result = []
        for item in list_items:
            proxy = (
                order["shipments"][0]["shipmentId"],
                order["our_id"],
                shop,
                order["our_status"],
                item["offerId"],
                item["id_1c"],
                item["quantity"],
                item["finalPrice"]
            )
            result.append(proxy)

    return result



app = Flask(__name__)
#for develop ONLY!
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


@app.route('/json', methods=['GET', 'POST'])
def get_json():
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return ::ffff:46.21.252.7
    #'X-Forwarded-For': '46.21.252.7'
    addr = request.headers.get('X-Forwarded-For')
    if str(ip_addr) == '::ffff:46.21.252.7' or addr == '46.21.252.7':
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
async def order_accept_ym():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        data_req = request.get_json()
        confirm_data = data_req["order"].get('fake')
        order = data_req["order"]
        proxy = order['items']
        stock = check_is_accept_ym(proxy)  # проверяем наличие for order
        if stock[0]:
            data = order_resp_ym(order, stock[0])
            response = app.response_class(
            json.dumps(data[0]),
            status=200,
            content_type='application/json'
            )
            if confirm_data is not True: ## if order not test
                order['our_id'], order['status'], order['our_status']\
                    = data[1], "ACCEPTED", "NEW"
                ref_data = reformat_data_order(order, 'Yandex')
                await execute_query(query_write_order, ref_data)
                list_items = reformat_data_items(order, 'Yandex')
                await execute_query(query_write_items, list_items)
                response = app.response_class(
                    json.dumps(data[0]),
                    status=200,
                    content_type='application/json'
                )
        else:
            data = order_resp_ym(order, False)
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
def cart_ym():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        cart = request_data.get('cart')
        # if cart is not None:
        businessId = cart.get('businessId')
        #delivery = cart.get('delivery')
        items = cart.get('items')
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
def orders_ym():
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


@app.route('/order/status', methods=['POST'])
async def status_ym():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        request_data = request.get_json()
        order = request_data.get("order")
        order_id = order["id"]
        status = order.get("status")
        if status == "CANCELLED":
            # make_cancel(order_id, "Yandex")
            data = ("canceled", "NEW", order_id, "Yandex")
            await execute_query(update_status_order, data)
        else:
            rewrite_order_status(order, "Yandex")

        response = app.response_class(
            status=200
        )

    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/stocks', methods=['POST'])
def stocks_ym():
    headers = dict(request.headers)
    request_data = request.get_json()
    #write_smth(request_data)
    write_smth('stocks')
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
def order_cancell_ym():
    token = request.headers.get('Authorization')
    if token == token_market_dbs or token == token_market_fbs:
        req_cancell = request.get_json()
        order = req_cancell.get('order')
        rewrite_order_status(order, "Yandex")

        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


##for sper
@app.route('/order/new', methods=['POST'])
async def new_order_sb():
    token = request.headers.get('Basic auth')
    if token == None:
        data_req = request.get_json()
        order = data_req["data"]
        pre_proxy = order["shipments"][0]["items"]
        proxy = counter_items(pre_proxy)
        stock = check_is_accept_sb(proxy)  # проверяем наличие for order
        order["items"] = stock[1]

        if stock[0]:
            data = order_resp_sb(stock[0], True)
            order['our_id'], order['status'], order['our_status']\
                = data[1], "NEW", "NEW"
            ref_data = reformat_data_order(order, 'Sber')
            await execute_query(query_write_order, ref_data)
            data_items = reformat_data_items(order, 'Sber')
            print(data_items)
            await executemany_query(query_write_items, data_items)

            response = app.response_class(
                json.dumps(data[0]),
                status=200,
                content_type='application/json'
            )

        else:
            data = order_resp_sb(False, True)
            print('response_order_new', data[0])
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

##for sper
@app.route('/order/cancel', methods=['POST'])
async def order_cancel():
    token = request.headers.get('Basic auth')
    if token == None:
        data_req = request.get_json()
        order = data_req["data"]
        order_id = order["shipments"][0]['shipmentId']
        proxy = order["shipments"][0]["items"]
        past_proxy = counter_items(proxy)
        # make_cancel(order_id, "Sber")
        data = ( "canceled", "NEW", order_id, "Sber" )
        await execute_query(update_status_order, data)
        re_data = order_resp_sb(True, False)
        response = app.response_class(
            json.dumps(re_data),
            status=200,
            content_type='application/json'
        )
    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/check/orders', methods=['GET', 'POST'])
async def check_orders():
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return ::ffff:46.21.252.7
    addr = request.headers.get('X-Forwarded-For')  # 'X-Forwarded-For': '46.21.252.7'
    #print(ip_addr, addr)
    if str(ip_addr) == '::ffff:46.21.252.7' or addr == '46.21.252.7':
        data = get_single_rows()  #query_read_order(get_new_order))
        if data is not None:
            re_data = create_data_for_1c(data)
            response = json.dumps(re_data)
            await execute_query(rebase_order,
                            ("SEND", data[0], data[1]))
            write_smth(" SEND " + re_data["order"]["shop"]
                            + " " + re_data["order"]["id"])
        else:
            empty_data = {
                "order": {
                    "status": "stop"
                }
            }
            response = json.dumps(empty_data)
            write_smth(" empty_data")

    elif addr == '62.76.102.53' or ip_addr == '62.76.102.53' or ip_addr == '::1':
        data = get_single_rows()  #query_read_order(get_new_order))
        if data is not None:
            re_data = create_data_for_1c(data)
            response = json.dumps(re_data)
            write_smth(" test " + re_data["order"]["id"])
        else:
            empty_data = {
                "order": {
                    "status": "stop"
                }
            }
            response = json.dumps(empty_data)

    else:
        response = app.response_class(
            status=402
        )

    return response


@app.route('/test', methods=['GET', 'POST'])
def test():
    response = 'OK'
    # response = app.response_class(
    #     json.dumps('OK'),
    #     status=200,
    #     content_type='application/json'
    # )
    return response


# allow both GET and POST requests
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
#
#         '''


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8800), app)
    http_server.serve_forever()
