import json
import os
import random
import string
from time import sleep

import requests

from project import db
import pandas as pd
# pip install openpyxl
from project.models import *
from flask import Blueprint, render_template, app, redirect, make_response, Response
from flask import request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from project.conn import *  # execute_query, executemany_query
# from project.conn_maintenance import query_write_order,
# query_write_items, update_status_order_reverse_id
from project import LOCAL_MODE
from project.ozon import common_error

main = Blueprint('main', __name__)

common_comfirm_response = {"result": True}
common_error = {'error': {
    "code": "ERROR_UNKNOWN",
    "message": "Неизвестный метод",
    "details": None}}


def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result


our_path = os.getcwd()

ALLOWED = {'csv', 'xls', 'xlsx'}
if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH = our_path


def read_xls(files):
    file = pd.read_excel(files)
    df = pd.DataFrame(file).values
    proxy = {}
    for row in df:
        proxy[row[0]] = int(row[2])
    print(type(proxy))

    return proxy  # dict


def check_allowed_filename(filename):
    result = '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED
    curr_name = filename.rsplit('.', 1)[1]
    # print(result)
    return result, curr_name


def reformat_data_order(order, shop):
    result = None
    if shop == 'Yandex':
        pass
        # try:
        #     day = reverse_time(order["delivery"]["shipments"][0]["shipmentDate"])
        # except:
        #     day = reverse_time(order['delivery']['dates']['fromDate'])
        # result = (
        #     order["id"],
        #     order["our_id"],
        #     shop,   #order["shop"],
        #     day_for_stm(day),
        #     order["status"],
        #     order["our_status"],
        #     order["paymentType"],
        #     order["delivery"]["type"]
        # )

    elif shop == 'Ozon':
        time = order["shipment_date"].split('T')[0]

        result = (
            order['id'],
            order["our_id"],
            shop,
            reverse_time(time),
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif shop == 'Sber':
        time = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            order['our_id'],
            shop,  # order["shop"],
            reverse_time(time),
            order["status"],
            order["our_status"],
            "PREPAID",  # order['data'].get("paymentType"),
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


def try_get_id_1c(offer_id):
    # items_skus = read_skus()
    # items_ids = read_json_ids()  # we wait dict[vendor_code] = (id_1c, price, quantity)
    # id_1c = items_ids[vendor_code][0]  # 1c
    pass
    return None


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
        # items_skus = read_skus()
        # items_ids = read_json_ids()  # we wait dict[vendor_code] = (id_1c, price, quantity)
        # id_1c = items_ids[vendor_code][0]  # 1c

        for item in list_items:
            sku = str(item["sku"])
            # vendor_code = items_skus[sku][1]
            vendor_code = item["offer_id"]
            # print('product_info_price', sku[0], vendor_code)
            # price = product_info_price(items_skus[sku][0], vendor_code)
            id_1c = try_get_id_1c(item["offer_id"])
            proxy = (
                order["posting_number"],
                order["our_id"],
                shop,
                order["our_status"],
                vendor_code,
                id_1c,
                item["quantity"],
                item["price"][:-2],
                item['offer_id'],
                item['sku']
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


def reformat_data_items_v2(order, shop_name, mp):
    result = []
    if mp == 'Yandex':
        list_items = order['items']
        for item in list_items:
            proxy = (
                order["id"],
                order["our_id"],
                mp,
                order["our_status"],
                item["offerId"],
                item["id_1c"],
                item["count"],
                item["price"] + item.get("subsidy")
            )
            result.append(proxy)

    elif mp == 'Ozon':
        result = []
        list_items = order['products']

        for item in list_items:
            sku = str(item["sku"])
            # vendor_code = items_skus[sku][1]
            vendor_code = item["offer_id"]
            print('product_info_price', sku[0], vendor_code)
            # price = product_info_price(items_skus[sku][0], vendor_code)
            id_1c = try_get_id_1c(item["offer_id"])
            proxy = (
                order["id"],
                order["our_id"],
                mp,
                shop_name,
                order['status'],
                order["our_status"],
                vendor_code,
                id_1c,
                item["quantity"],
                item["price"][:-2],
                item['offer_id'],
                item['sku']
            )
            result.append(proxy)

    elif mp == 'Sber':
        list_items = order["count_items"]
        result = []
        for item in list_items:
            proxy = (
                order["shipments"][0]["shipmentId"],
                order["our_id"],
                mp,
                order["our_status"],
                item["offerId"],
                item["id_1c"],
                item["quantity"],
                item["price"]
            )
            result.append(proxy)

    return result


def product_info_price(id_mp, seller_id):
    api_key = Marketplaces.query.filter_by(seller_id=seller_id).first().key_mp
    headers = {
        'Client-Id': seller_id,
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'
    data = {
        "posting_number": id_mp,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "product_exemplars": False,
            "translit": False}}
    resp = requests.post(url=url, headers=headers, json=data)
    # {'code': 5,
    # 'message': 'Unknown posting number "55200317-0207-4"',
    # 'details': []}
    result = resp.json()
    print('product_id_offer_id', result)
    order = result.get("result")
    if order:
        return order
    elif result.get('code') == 5:
        # write_notice_order
        return None
    else:
        return None


@main.route('/')
def index_main():
    return render_template('ui-login.html')  # 'start_page.html')


@main.route('/profile')
@login_required
def profile():
    name = current_user.name
    uid = current_user.id
    role = current_user.roles
    return render_template('hospital.html', name=name, uid=uid, role=role)  # index.html


@main.route('/api/on', methods=['POST'])
async def onon_push():
    ip_addr = request.environ.get('X-Real-IP')
    print('X-Real-IP', ip_addr)
    addr = request.headers.get('X-Forwarded-For')
    print('X-Forwarded-For', addr)
    resp = request.get_json()
    # head = dict(request.headers)
    # print('resp_header', head)
    if resp is not None:
        if resp.get('message_type') == 'TYPE_PING':
            time = resp["time"]
            response = Response(
                json.dumps({"version": "v.1",
                            "name": "brain-trust.bot",
                            "time": time}),
                status=200
            )

        elif resp.get("message_type") == "TYPE_NEW_POSTING":
            our_id = token_generator()
            id_mp = resp["posting_number"]
            seller_id = str(resp.get('seller_id'))
            sleep(1.5)
            order = product_info_price(id_mp, seller_id)
            if order:
                print('new_order_onon', order['posting_number'])
                order['our_id'], order['id'], order['status'], order['our_status'] \
                    = our_id, id_mp, "NEW", "NEW"  # TODO change place id_mp & our_id
                shop_name = Marketplaces.query.\
                    filter_by(seller_id=seller_id).first().shop_name
                ref_data = reformat_data_order(order, 'Ozon')
                # list_items = reformat_data_items(order, 'Ozon')
                list_items = reformat_data_items_v2(order, shop_name, 'Ozon')
                await write_order(query1=query_write_order, data1=ref_data,
                                  query2=query_write_items_v2, data2=list_items)
                # await execute_query(query_write_order, ref_data)
                # await executemany_query(query_write_items, list_items)

            response = Response(
                json.dumps(common_comfirm_response),
                status=200
            )

        elif resp.get("message_type") == "TYPE_POSTING_CANCELLED":
            order_id = resp["posting_number"]
            order_status = resp.get('status')
            print('INFO CANCELED ORDER - status {} from {}'
                  .format(order_status, resp))
            data = ("canceled", "canceled", order_id, "Ozon")
            # await execute_query(update_status_order_reverse_id, data)
            await execute_query_v3(query=update_status_order,
                                   query2=update_status_order_items,
                                   data=data)
            print('cencelled_order_onon', order_id)
            response = Response(
                json.dumps(common_comfirm_response),
                status=200
            )

        elif resp.get("message_type") != None:
            response = Response(
                json.dumps(common_error),
                status=200
            )

        else:
            response = Response(
                json.dumps(common_error),
                status=400
            )
    else:
        response = Response(
            status=403
        )

    print('api_on_response', response)
    return response


@main.route('/file', methods=['get', 'post'])
def download():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Невозможно прочитать файл')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)

        check = check_allowed_filename(file.filename)
        if file and check[0]:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        if check[1] == 'xlsx':
            data = read_xls(file)
            with open(UPLOAD_FOLDER + 'sales.json', 'w') as ff:
                json.dump(data, ff)

                flash('Файл excel загружен')
                return redirect(request.url)

    return render_template('index.html')


@main.route('/test', methods=['GET', 'POST'])
def test():
    return 'OK'
