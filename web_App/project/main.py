import json
import os
import random
import string
from time import sleep

import pandas as pd
#pip install openpyxl

from flask import Blueprint, render_template, app, redirect
from flask import request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from project.conn import execute_query, executemany_query
from project.conn_maintenance import query_write_order, query_write_items, update_status_order_reverse_id
from project import LOCAL_MODE
from project.ozon import product_info_price, common_error

main = Blueprint('main', __name__)


common_comfirm_response = {"result": True}
common_error = {'error': {
      "code": "ERROR_UNKNOWN",
      "message": "Неизвестный метод",
      "details": None }}


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

    return proxy  #dict


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
        for item in list_items:
            sku = str(item["sku"])
            # vendor_code = items_skus[sku][1]
            vendor_code = item["offer_id"]
            print('product_info_price', sku[0], vendor_code)
            # price = product_info_price(items_skus[sku][0], vendor_code)
            proxy = (
                order["id"],
                order["our_id"],
                shop,
                order["our_status"],
                vendor_code,
                # items_ids[vendor_code][0],  # 1c
                item["quantity"],
                item["price"][:-2]  # price
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


@main.route('/')
def index_main():
    return render_template('start_page.html')


@main.route('/profile')
@login_required
def profile():
    name = current_user.name
    uid = current_user.id
    role = current_user.roles
    return render_template('hospital.html', name=name, uid=uid, role=role)  # index.html


@main.route('/api/on', methods=['GET', 'POST'])
async def onon_push():
    resp = request.get_json()
    print('api_on_resp', resp)
    if resp.get('message_type') == 'TYPE_PING':
        time = resp["time"]
        response = app.response_class(
            json.dumps({"version": "v.1",
                        "name": "brain-trust.bot",
                        "time": time}),
            status=200
        )

    elif resp.get("message_type") == "TYPE_NEW_POSTING":
        our_id = token_generator()
        id_mp = resp["posting_number"]
        # our_id = id_mp.replace('-', '')[:10]
        sleep(1)
        order = product_info_price(id_mp)
        print('new_order_onon', order)
        order['our_id'], order['id'], order['status'], order['our_status'] \
            = id_mp, our_id, "NEW", "NEW"  # TODO change place id_mp & our_id
        ref_data = reformat_data_order(order, 'Ozon')
        # print('refdata', ref_data)
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
