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
from read_json import process_json_dict,  read_order_json, read_json_sper, read_json_ids
from our_request import data_psh, data_pshh
from cred import token_market_dbs, tokens_market, token_market_fbs_exp, token_sper
from ozon import read_skus, product_info_price
from sper import post_smth_sb, check_is_accept_sb
from time import sleep
#from cred import token_market_dbs, token_market_fbs
import urllib3
urllib3.disable_warnings()


#time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
#printt(time)  #for development


def write_json(smth_json):
    try:
        with open('/var/www/html/stm/test_json.json', 'w') as file:
            json.dump(smth_json, file)
    except Exception:
        with open('test_json.json', 'w') as file:
            json.dump(smth_json, file)


def write_smth_date():
    try:
        f = open('/var/www/html/stm/test_txt.txt', 'w')
        time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
        f.write(str(time) + '\n')
        f.close()
    except:
        f = open('test_txt.txt', 'w')
        time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
        f.write(str(time) + '\n')
        f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    # f = open('no_test.txt', 'a')
    try:
        f = open('/var/www/html/stm/no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    except:
        f = open('no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()


# write_smth(' start ')


def write_fake(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open('/var/www/html/stm/fake_json.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    except:
        f = open('fake_json.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    # with open('fake_jon.json', 'w') as file:
    #     json.dump(smth, file)


def check_cart(items):
    data_stocks = process_json_dict()
    id_1c = ''
    for item in items:
        offer_id = item['offerId']
        need = item['count']
        if offer_id in data_stocks.keys():
            exist = data_stocks[offer_id][2]
            id_1c = data_stocks[offer_id][0]
            if int(exist) < need:
                #item['count'] = int(exist)
                item['count'] = 0
        else:
            item['count'] = 0

    return items, id_1c


def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# def token_generator(size=10, chars = string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


def create_data_for_1c(data):
    #print('create_data_for_1c', data)
    list_items = data[1]
    items_pr = []
    for item in list_items:
        proxy = {}
        proxy['shopSku'] = item[5]
        proxy['count'] = item[6]
        proxy['price'] = item[7]
        items_pr.append(proxy)

    status = data[0][9]
    statuses = ['PROCESSING', 'ACCEPTED', 'CREATED', "NEW"]
    if status.upper() in statuses:
        status = 'accept'

    data_re = {
        "order": {
            "shop": data[0][7],
            "businessId": data[0][2],
            "id": data[0][1],
            "paymentType": data[0][10],
            "delivery": data[0][13],
            "status": status,
            "date": data[0][8],
            "items": items_pr
        }
    }
    print('create_data_re_for_1c', data_re)
    return data_re




def check_stocks(skus, warehouse_id):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    data_stocks = process_json_dict()
    proxy_list = []
    for sku in skus:
        if sku in data_stocks:
            count = data_stocks[sku][2]  #.get('stock')
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
        rewrite_status(order, shop)
    with open("orders.json", 'w') as file:
        json.dump(data, file)

    # return order_id

async def rewrite_status_order_db(order_id, status, shop):
    data = check_is_exist(query_read_order, (order_id, shop))
    if data:
        await execute_query(update_status_order,
                            (status, "NEW", order_id, shop))
    print('re_write_order', shop, order_id)



def rewrite_status(order, shop):
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


def day_for_stm(string):
    datta = datetime.strptime(string, '%Y-%m-%d')
    dat = datta.weekday()
    dtt = datta.strftime('%d-%m-%Y')
    if 1 <= dat <= 4:
        dtt = (datta - timedelta(1)).strftime('%d-%m-%Y')
    elif dat == 5:
        proxy = datta + timedelta(2)
        dtt = proxy.strftime('%d-%m-%Y')
    elif dat == 6:
        proxy = datta + timedelta(1)
        dtt = proxy.strftime('%d-%m-%Y')

    #print('datta',dat,  dtt)
    return dtt


def check_is_accept_ym(list_items):
    data = process_json_dict()
    result_global = False
    cnt = 0
    #printt('check_is_accept_ym', list_items)
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
    #printt('check_is_accept_ym_222222222', count, len(list_items))
    return result_global, list_items


def order_resp_ym(our_id, global_result):
    # id_create = token_generator()
    if global_result:
        data = {
            "order": {
                "accepted": True,
                "id": our_id,
            }
        }
        # write_order(order, id_create, "Yandex")
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

    return data


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


async def make_cancel_count(order_id, shop, list_items):
    #data  = execute_query(query_read_order, (order_id, shop))
    await execute_query(update_status_order, ('canceled', "NEW", order_id, shop))

    # return created_id



# def make_cancel(order_id, shop):
#     #data  = execute_query(query_read_order, (order_id, shop))
#     execute_query(update_status_order, ('canceled', "NEW", order_id, shop))
#
#     # return created_id


def proxy_time():
    dt = datetime.now().date() + timedelta(days=2)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt

def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
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
    pr, lst = {}, []
    for item in items_list:
        proxy_offer_id = item['offerId']
        pr[proxy_offer_id] = pr.get(proxy_offer_id, 0) + 1
    for itemm in items_list:
        if itemm["offerId"] in pr.keys():
            value = pr.pop(itemm["offerId"])
            itemm["quantity"] = value
            lst.append(itemm)

    #printt('counter_items',lst)
    return lst

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
    day = reverse_time(order["delivery"]["shipments"][0]["shipmentDate"])
    result = None
    if shop == 'Yandex':
        result = (
            order["id"],
            order["our_id"],
            shop,   #order["shop"],
            day_for_stm(day),
            order["status"],
            order["our_status"],
            order["paymentType"],
            order["delivery"]["type"]
        )

    elif shop == 'Ozon':
        time = order["shipment_date"].split('T')[0]

        result = (
            order['id'],
            order["our_id"],
            shop,
            day_for_stm(time), #reverse_time()
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif shop == 'Sber':
        time = order["shipping"]["shippingDate"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            order['our_id'],
            shop,  #order["shop"],
            day_for_stm(time),  #reverse_time(time),
            order["status"],
            order["our_status"],
            "PREPAID",  #order['data'].get("paymentType"),
            order["shipments"][0]['fulfillmentMethod']
        )

    # elif shop == 'Leroy':
    #     result = (
    #         order['order']["id"],
    #         order['order']["our_id"],
    #         order['order']["shop"],
    #         order['order']["date"],
    #         order['order']["status"],
    #         order['order']["paymentType"],
    #         order['order']["delivery"]
    #     )
    #
    # elif shop == 'WB':
    #     result = (
    #         order['order']["businessId"],
    #         order['order']["id"],
    #         order['order']["shop"],
    #         order['order']["date"],
    #         order['order']["status"],
    #         order['order']["paymentType"],
    #         order['order']["delivery"]
    #     )

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
                item["id_1c"],
                item["count"],
                item["price"] + item.get("subsidy")
            )
            result.append(proxy)

    elif shop == 'Ozon':
        result = []
        list_items = order['products']
        # read_skus() -> {sku<str>: (product_id<int>, vendor_code<str>}
        #items_skus = read_skus()
        items_ids = read_json_ids() #ids 1C
        for item in list_items:
            sku = str(item["sku"])
            #vendor_code = items_skus[sku][1]
            vendor_code = item["offer_id"]
            print('product_info_price', sku[0], vendor_code)
            #price = product_info_price(items_skus[sku][0], vendor_code)
            proxy = (
                order["id"],
                order["our_id"],
                shop,
                order["our_status"],
                vendor_code,
                items_ids[vendor_code][0], #1c
                item["quantity"],
                item["price"][:-2]  #price
            )
            result.append(proxy)

    elif shop == 'Sber':
        list_items = order["count_items"]
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
                item["price"]
            )
            result.append(proxy)

    return result


def confirm_data_sb(order): #TODO
    list_items = order["shipments"][0]["items"]
    proxy = []
    for item in list_items:
        it = {}
        it["itemIndex"] = item["itemIndex"]
        it["offerId"] = item["offerId"]
        proxy.append(it)

    result = {
        'data': {
            'token': token_sper,
            'shipments': [{
                'shipmentId': order["shipments"][0]["shipmentId"],
                'orderCode': order['our_id'],
                'items': proxy,
            }]
        }
    }

    return result


app = Flask(__name__)
#for develop ONLY!
#app.debug = True


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
    if ip_addr == '::ffff:46.21.252.7' or ip_addr == '46.21.252.7'\
            or ip_addr == '62.76.102.53':
        request_data = request.get_json()
        write_json(request_data)
        write_smth_date()

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
    if token in tokens_market:
        data_req = request.get_json()
        b2b = data_req['order'].get("paymentMethod")
        if b2b == "B2B_ACCOUNT_PREPAYMENT":
            data_req['order']['delivery']['shipments'][0]['shipmentDate'] = proxy_time()
            data_req['order']['shipmentDate'] = proxy_time()
        confirm_data = data_req["order"].get('fake')
        order = data_req["order"]
        proxy = order['items']
        our_id = token_generator()
        stock = check_is_accept_ym(proxy)  # проверяем наличие for order
        print('fak', stock[1])
        if stock[0]:
            data = order_resp_ym(our_id, stock[0])
            response = app.response_class(
            json.dumps(data),
            status=200,
            content_type='application/json'
            )
            if confirm_data is not True: ## if order not test
                order['our_id'], order['status'], order['our_status']\
                    = our_id, "ACCEPTED", "NEW"
                ref_data = reformat_data_order(order, 'Yandex')
                check_is = check_is_exist(query_read_order, (str(order['id']), 'Yandex'))
                if check_is:
                    response = app.response_class(
                        json.dumps(data),
                        status=200,
                        content_type='application/json'
                    )
                else:
                    await execute_query(query_write_order, ref_data)
                    order['items'] = stock[1]
                    list_items = reformat_data_items(order, 'Yandex')
                    print('list_items', list_items)
                    await executemany_query(query_write_items, list_items)
                    response = app.response_class(
                        json.dumps(data),
                        status=200,
                        content_type='application/json'
                    )
        else:
            data = order_resp_ym(order, False)
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


@app.route('/cart', methods=['POST'])
def cart_ym():
    token = request.headers.get('Authorization')
    if token in tokens_market:
        request_data = request.get_json()
        cart = request_data.get('cart')
        items = cart.get('items')
        check = check_cart(items)
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
    if token in tokens_market:
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
    if token in tokens_market:
        request_data = request.get_json()
        order = request_data.get("order")
        order_id = str(order["id"])
        status = order.get("status")
        if status == "CANCELLED":
            # make_cancel(order_id, "Yandex")
            data = ("canceled", "NEW", order_id, "Yandex")
            await execute_query(update_status_order, data)
        else:
            data = (status, order_id, "Yandex")
            print(data)
            await execute_query(rewrite_status_order, data)
            #rewrite_status(order, "Yandex")

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
    if token in tokens_market:
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
    if token in tokens_market:
        req_cancell = request.get_json()
        order = req_cancell.get('order')
        rewrite_status(order, "Yandex")

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
    print('from_order_new_token', token)
    if token == None or token != None:
        data_req = request.get_json()
        print('data_from_order_new', data_req)
        order = data_req["data"]
        pre_proxy = order["shipments"][0]["items"]
        proxy = counter_items(pre_proxy)
        stock = check_is_accept_sb(proxy)  # проверяем наличие for order
        order["count_items"] = stock[1]

        if stock[0]:
            data = order_resp_sb(stock[0], True)
            order['our_id'], order['status'], order['our_status']\
                = data[1], "NEW", "NEW"
            ref_data = reformat_data_order(order, 'Sber')
            await execute_query(query_write_order, ref_data)
            data_items = reformat_data_items(order, 'Sber')
            await executemany_query(query_write_items, data_items)
            data_confirm = confirm_data_sb(order)
            await post_smth_sb('order/confirm', data_confirm)
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
        ## cancel one vendor_code or mane
        past_proxy = counter_items(proxy)   #TODO
        await make_cancel_count(order_id, "Sber", past_proxy)
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
    #printt(ip_addr, addr)
    if ip_addr == '::ffff:46.21.252.7' or ip_addr == '46.21.252.7':  # or ip_addr == '54.86.50.139':  #POSTMAN
        data = get_one_order()  #query_read_order(get_new_order))
        if data[0] is not None:
            re_data = create_data_for_1c(data)
            print("SEND order", re_data)
            response = json.dumps(re_data)
            await execute_query(rebase_order,
                            ("SEND", data[0][0], data[0][1]))
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
        data = get_one_order()  #query_read_order(get_new_order))
        if data[0] is not None:
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


common_comfirm_response = {"result": True}
common_error = {'error': {
      "code": "ERROR_UNKNOWN",
      "message": "Неизвестный метод",
      "details": None }}


from proxy import proxy_onon
@app.route('/api/on', methods=['GET', 'POST'])
async def onon_push():
    resp = request.get_json()
    print('api_on_resp', resp)
    if resp.get('message_type') == 'TYPE_PING':
        time = resp["time"]
        response = app.response_class(
            json.dumps({ "version": "v.1",
                   "name": "brain-trust.bot",
                   "time": time }),
            status=200
        )

    elif resp.get("message_type") == "TYPE_NEW_POSTING":
        our_id = token_generator()
        id_mp = resp["posting_number"]
        # our_id = id_mp.replace('-', '')[:10]
        sleep(1)
        order = product_info_price(id_mp)
        print('new_order_onon', order)
        order['our_id'], order['id'],  order['status'], order['our_status'] \
            = id_mp, our_id, "NEW", "NEW"  # TODO change place id_mp & our_id
        ref_data = reformat_data_order(order, 'Ozon')
        #print('refdata', ref_data)
        await execute_query(query_write_order, ref_data)
        list_items = reformat_data_items(order, 'Ozon')
        # print('redata_items', list_items)
        # print('list_items_onon', list_items)
        await executemany_query(query_write_items, list_items)

        response = app.response_class(
            json.dumps(common_comfirm_response),
            status=200
        )

    elif resp.get("message_type") == "TYPE_POSTING_CANCELLED":
        order_id = resp["posting_number"]
        data = ("canceled", "NEW", order_id, "Ozon")
        await execute_query(update_status_order_reverse_id, data)
        print('cencelled_order_onon', order_id)
        response = app.response_class(
            json.dumps(common_comfirm_response),
            status=200
        )
        
    elif resp.get("message_type") != None:
        response = app.response_class(
            json.dumps(common_error),
            status=200
        )

    else:
        response = app.response_class(
            json.dumps(common_error),
            status=400
        )

    print('api_on_response', response)
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
    http_server = WSGIServer(('', 9900), app)
    http_server.serve_forever()

