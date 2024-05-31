import sys

from psycopg2 import IntegrityError

from cred import *
# from cred_update import creds
from gevent import monkey

monkey.patch_all()
import random
import string
import json
from werkzeug.utils import secure_filename
from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from gevent.pywsgi import WSGIServer
import datetime
import requests
from maintenance import shorter_data
from excel_read import read_xlsx, read_xlsx_v2
import csv
from avito import *
from amo import *
import urllib3
import logging
from bot_tg import send_get
from parts_soft import make_data_for_request_v2
import connect as conn
import uuid
from psycopg2.errors import UniqueViolation
from psycopg2.extensions import register_adapter, AsIs
import json

def adapt_dict(dict_var):
    return AsIs("'" + json.dumps(dict_var) + "'")

register_adapter(dict, adapt_dict)
urllib3.disable_warnings()

# url = 'https://zakazjpexpressru.amocrm.ru'
ALLOWED = {'csv', 'xls', 'xlsx'}

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH_DIR = './'
    LOG_DIR = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH_DIR = '/home/userbe/phone/'
    LOG_DIR = 'home/userbe/phone/logs/'

logging.basicConfig(filename=os.path.join(LOG_DIR + 'webhook.log'), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

refresh = creds.get('refresh')


def check_allowed_filename(filename):
    result = '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED
    curr_name = filename.rsplit('.', 1)[1]

    return result, curr_name


def make_data(resp_data):
    data = [
        {
            "name": resp_data.get('form_fields[32121][name]'),
            'pipeline_id': 5420530,
            'custom_fields_values': [
                {
                    "field_id": 1277277,  # sity - now make on field address
                    "values": [
                        {
                            "value": resp_data.get('form_fields[32119][values][0]')
                        }
                    ]
                },
                {
                    "field_id": 1253783,  # auto mark
                    "values": [
                        {
                            "value": resp_data.get('form_fields[32124][values][0]')
                        }
                    ]
                },
                {
                    "field_id": 294471,  # advertising source TODO
                    "values": [
                        {
                            "value": resp_data.get('form_fields[32120][values][0]')
                        }
                    ]
                },
                {
                    "field_id": 294471,  # call result TODO
                    "values": [
                        {
                            "value": resp_data.get('form_fields[32122][values][0]')
                        }
                    ]
                },
                {
                    "field_id": 1277265,  # comment
                    "values": [
                        {
                            "value": resp_data.get('form_fields[32124][values][0]')
                        }
                    ]
                },
                {
                    "field_id": 952417,  # phone number
                    "values": [
                        {
                            "value": resp_data.get('caller_num')
                        }
                    ]
                },
                {
                    "field_id": 294471,  # caller name TODO
                    "values": [
                        {
                            "value": resp_data.get('caller_name')
                        }
                    ]
                }
            ]
        }
    ]

    return data


def make_compex_data(resp_data):
    data = [  # (sity, name, phone, source, mark, first_name, call_result, comment, target)
        {
            "name": resp_data[8],
            "_embedded": {
                "contacts": [
                    {
                        "first_name": resp_data[5],
                        'custom_fields_values': [
                            {
                                "field_id": 1277277,  # sity - now make on field address
                                "values": [
                                    {
                                        "value": resp_data[0]
                                    }
                                ]
                            },
                            {
                                "field_id": 952417,  # phone number
                                "values": [
                                    {
                                        "value": resp_data[2]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            'pipeline_id': 5420530,
            'custom_fields_values': [
                {
                    "field_id": 1253779,  # auto mark
                    "values": [
                        {
                            "value": resp_data[4]
                        }
                    ]
                },
                {
                    "field_id": 1315595,  # advertising source TODO
                    "values": [
                        {
                            "value": resp_data[3]
                        }
                    ]
                },
                {
                    "field_id": 1315601,  # call result TODO
                    "values": [
                        {
                            "value": resp_data[6]
                        }
                    ]
                },
                {
                    "field_id": 1277265,  # comment
                    "values": [
                        {
                            "value": resp_data[7]
                        }
                    ]
                }
            ]
        }
    ]

    return data


def read_avito_messages():
    pass


def read_write_file(file, curr_name):
    pass


def write_result(result):
    with open(PATH_DIR + 'result.txt', 'a') as file:
        file.write(str(datetime.datetime.now()) + str(result))
        file.write('\n')


def write_incoming(proxy_tuple):
    with open(PATH_DIR + 'incoming.txt', 'a') as file:
        file.write(str(datetime.datetime.now()) + str(proxy_tuple))
        file.write('\n')


def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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

    return lst




def check_is_exist_message_answer(msg_id, chat_id):
    '''
    data = {"chat_id": ["price", "link", "msg_id", avito_id: int, name(?), first_answer: bool]}
    '''
    data = read_links()
    compare = False
    first_answer = False
    if data.get(chat_id):
        try:
            if data.get(chat_id)[2] == msg_id:
                compare = True
        except IndexError as err:
            print("FUCK UP_msg_id {}".format(err), data.get(chat_id), chat_id)

        try:
            first_answer = data.get(chat_id)[5]
        except IndexError as err:
            print("FUCK UP_first_answer {}".format(err), data.get(chat_id), chat_id)

    return compare, first_answer


async def check_is_exist_message_answer_v2(msg_id, chat_id):
    '''
    data = {"chat_id": ["price", "link", "msg_id", avito_id: int, name(?), first_answer: bool]}
    '''
    # data = read_links()
    data = await read_links_v4(chat_id)
    compare = False
    first_answer = False
    rewrite_lead = False
    # if data.get(chat_id):
    if data:
        try:
            # if data.get(chat_id)[2] == msg_id:
            if data[2] == msg_id:
                compare = True
        except IndexError as err:
            print("FUCK UP_msg_id {}"
                  .format(err), data.get(chat_id), chat_id)

        try:
            # first_answer = data.get(chat_id)[5]
            first_answer = data[5]
        except IndexError as err:
            print("FUCK UP_first_answer {}"
                  .format(err), data.get(chat_id), chat_id)

        try:
            # rewrite_lead = data.get(chat_id)[6]
            rewrite_lead = data[6]
        except IndexError as err:
            print("FUCK UP_rewrite_lead {}"
                  .format(err), data.get(chat_id), chat_id, rewrite_lead)

    return compare, first_answer, rewrite_lead


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result

# print(asyncio.run(check_is_exist_message_answer_v2('ad6c351403976b0f6175b81965221000', 'u2i-PalCq8X5aU0iwwKcwfUAqQ' )))

def reformat_data_order(order, shop):
    result = None
    if shop == 'Yandex':
        try:
            day = reverse_time(order["delivery"]["shipments"][0]["shipmentDate"])
        except:
            day = reverse_time(order['delivery']['dates']['fromDate'])
        result = (
            order["id"],
            order["our_id"],
            shop,   #order["shop"],
            day,
            order["status"],
            order["our_status"],
            order["paymentType"],
            order["delivery"]["type"]
        )

    elif shop == 'Ozon':
        day = order["shipment_date"].split('T')[0]
        result = (
            order['id'],
            order["our_id"],
            shop,
            day,
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif shop == 'Sber':
        day = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            order['our_id'],
            shop,
            day,
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
        items_ids = read_json_ids() #ids 1C
        for item in list_items:
            sku = str(item["sku"])
            vendor_code = item["offer_id"]
            id_1c = items_ids[vendor_code][0]
            #price = product_info_price(items_skus[sku][0], vendor_code)
            proxy = (
                order["id"],
                order["our_id"],
                shop,
                order["our_status"],
                vendor_code,
                id_1c, #1c
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


def reformat_data_order_v2(order, mp, client_id_ps,
                           model=None, customers=True):
    result_items, result_customer = [], ()
    result = None
    if mp == 'Yandex':
        try:
            day = reverse_time(order["delivery"]["shipments"][0]["shipmentDate"])
        except:
            day = reverse_time(order['delivery']['dates']['fromDate'])
        result = (
            order["id"],
            order["our_id"],
            mp,   #order["shop"],
            day,
            order["status"],
            order["our_status"],
            order["paymentType"],
            order["delivery"]["type"]
        )

    elif mp == 'Ozon':
        day = order["shipment_date"].split('T')[0]
        result = (
            order['id'],
            order["our_id"],
            mp,
            day,
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif mp == 'Sber':
        list_items = order["count_items"]
        summ_order = 0
        for item in list_items:
            proxy = (
                order["shipments"][0]["shipmentId"],
                mp,
                item["offerId"],
                '', # item["id_1c"],
                item["quantity"],
                str(item["price"])
            )
            result_items.append(proxy)
            summ_order += item["price"]

        if model == 'dbs':
            day = order["shipments"][0]["handover"]["deliveryInterval"]["dateFrom"].split('T')[0]
            order_create_day = order["shipments"][0]['shipmentDate'].split('T')[0]
            delivery = order["shipments"][0]["handover"]['serviceScheme']
        else:
            day = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
            order_create_day = order['shipmentDate'].split('T')[0]
            delivery = order["shipments"][0]['fulfillmentMethod']
        result = (
            order["shipments"][0]["shipmentId"],
            mp,
            day,
            order_create_day,
            order["status"],
            "new",  # order["substatus"],
            order["our_status"],
            "PREPAID",  #order['data'].get("paymentType"),
            delivery,
            str(summ_order),
            client_id_ps
        )

        if customers and model == 'dbs':
            result_customer = (
                order["shipments"][0]["shipmentId"],
                mp,
                order_create_day,
                str(summ_order),
                order["shipments"][0]["customer"]['phone'],
                order["shipments"][0]["customer"]['email'],
                order["shipments"][0]["customer"]["address"]["fias"]['regionId'],
                order["shipments"][0]["customer"]["address"]["fias"]['destinationId'],
                order["shipments"][0]["customer"]["address"]["geo"]['lat'],
                order["shipments"][0]["customer"]["address"]["geo"]['lon'],
                order["shipments"][0]["customer"]["address"]['regionKladrId'],
                order["shipments"][0]["customer"]["address"]['regionWithType'],
                order["shipments"][0]["customer"]["address"]['cityWithType']
            )

    return result, result_items, result_customer


app = Flask(__name__,
            template_folder='templates/')
app.secret_key = import_key


# for develop ONLY!
# app.debug = True


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


@app.route('/token', methods=['get', 'post'])
def get_token():
    data = request.json
    print('data_token', data)


@app.route('/token-token', methods=['get', 'post'])
def get_token_token():
    data = request.json
    print('data_token_token', data)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'OK phone'


@app.route('/external_orders/<uuid>/new', methods=['GET', 'POST'])
async def new_order_sber(uuid):
    # print(33333, uuid)

    token = request.headers.get('Basic auth')
    print(33333, uuid)
    if token == None or token != None:
        print(33311133, uuid)
        data_req = request.json
        order = data_req["data"]
        pre_proxy = order["shipments"][0]["items"]
        proxy = counter_items(pre_proxy)

        store_data = conn.execute_query_return_one(
            query_get_shop_campain_id, uuid)
        print(232323, type(store_data), store_data)
        client_id_ps = store_data[1]
        model = store_data[0]

        # проверяем наличие for order
        # stock = check_is_accept_sb(proxy)
        # order["count_items"] = stock[1]
        # if stock[0]:
        #     data = order_resp_sb(stock[0], True)

        data = order_resp_sb(True, True)
        order['status'],  \
            order['our_status'], order['count_items'] \
            = "NEW", "NEW", proxy
        # ref_data = reformat_data_order(order, 'Sber')
        ref_data = reformat_data_order_v2(order, 'Sber', model=model,
                                          client_id_ps=client_id_ps)
        print(123, type(ref_data[0]),  ref_data[0])
        print(123, type(ref_data[1]),  ref_data[1])
        print(123, type(ref_data[2]),  ref_data[2])
        await execute_query_v3(query_write_order, ref_data[0])
        await executemany_query(query_write_items, ref_data[1])
        await execute_query_v3(query_write_customer, ref_data[2])
        # data_confirm = confirm_data_sb(order)
        # post_smth_sb('order/confirm', data_confirm)

        response = app.response_class(
            json.dumps(data[0]),
            status=200,
            content_type='application/json'
        )

        # else:
        #     data = order_resp_sb(False, True)
        #     print('response_order_new', data[0])
        #     response = app.response_class(
        #         json.dumps(data),
        #         status=200,
        #         content_type='application/json'
        #     )


    else:
        response = app.response_class(
            status=403
        )

    return response


@app.route('/order/cancel', methods=['GET', 'POST'])
def cancel_order_sber():
    pass


@app.route('/webhook', methods=['GET', 'POST'])
async def avito_webhook():
    # headers = request.headers
    if request.headers.get('X-Avito-Messenger-Signature'):
        hook = request.get_json()
        logging.info('WE_GET_HOOK_from_avito {} '.format(hook))

        author_id = hook.get('payload').get('value').get('author_id')
        chat_id = hook.get('payload').get('value').get('chat_id')
        msg_id = hook.get('payload').get('value').get('id')
        # check = await check_is_exist_message_answer_v2(msg_id, chat_id)
        check = check_is_exist_message_in_db_v2(msg_id, chat_id)
        logging.info('CheckFromMain {} {} {} '.format(check, chat_id, msg_id))
        try:

            ## system message from avito or our
            if author_id == 1 or check[0]:  # or (author_id in sender_ids and msg != bot_answer):
                return app.response_class(
                    status=200
                )

            user_id = hook.get('payload').get('value').get('user_id')
            msg = hook.get('payload').get('value').get('content').get('text')
            # is_phone = await get_phone(msg)
            ## our message or first
            if author_id in sender_ids and (msg == bot_answer or msg == bot_rota_answer):
                chat_id = hook.get('payload').get('value').get('chat_id')
                await rewrite_leads_v2(chat_id, user_id)
                msg_id = hook.get('payload').get('value').get('id')
                await re_write_link_v2(chat_id, msg_id)
                # await get_avito_current_chat_v2(hook, (False, True))
                return app.response_class(
                    status=200
                )

            ## random message, not first, not our
            else:
                try:
                    await get_avito_current_chat_v2(hook, check)
                    logging.info('get_avito_current_chat_v2 {} {} {}'
                                 .format(hook, check, chat_id))
                    return app.response_class(
                        status=200
                    )
                except Exception as err:
                    logging.error('ERROR_GET_AVITO_CURRENT_CHAT {}, hook {}, {} {} {} {}'.
                                  format(err, hook, check, msg_id, chat_id, user_id))
                    return app.response_class(
                        status=200
                    )
        except Exception as error:
            logging.error('Web_hook_fuckup {} {}'.format(error, hook))
            return app.response_class(
                status=200
            )
    else:
        print('WHOIS', request.get_data())
        print('WHOIS', request.headers)
        return app.response_class(
            status=402
        )


##status order from site 3431
@app.route('/check', methods=['get', 'POST'])
def check_status():
    if request.headers.get('X-Real-Ip') == '77.246.158.248':
        try:
            hook_id = request.headers.get('PS-WEBHOOK_EVENT-ID')
            form = request.form.to_dict()
            # status = form.get('status')
            if form.get('status') != 'Размещено у поставщика':
                logging.info('we get form {} {}'.format(hook_id, form))
            if form.get('clientId') in ['715', '235', '710']:
                pass
                # make_pipeline(form)
            # print('WE GET ORDER_form', form)
            # write_result(form)

        except:
            print('ERROR_GET_WEBHOOK_PS')

        return app.response_class(
            status=200
        )

    return "Ok, we await data"


@app.route('/leads', methods=['get', 'post'])
def get_new_leads_amo():
    try:
        headers = request.headers
        data = request.get_json()
        print('WE_GET_NEW_LEADS_from_AMO', data, headers)
    except:
        result = request.form.to_dict()
        # print(3333333, result, type(result))

    return 'OK'


@app.route('/location/', methods=['GET', 'POST'])
async def wait_amo_hook():
    if request.method == "POST":
        data_json = request.get_json()
        logging.info('WE_GET_DATA_FROM_AMO {}'.format(data_json))
        try:
            await make_data_for_avito_v2(data_json)
        except Exception as err:
            logging.error('WHAT_is_FUCK_UP_error from endpoint location {}'.format(err))
            send_get('WHAT_is_error from endpoint location {}'.format(err))

        return app.response_class(
            status=200
        )
    else:
        return "we wait data"


@app.route('/bonus', methods=['post'])
async def bonus_hook():
    if request.method == 'POST':
        # try:
        form = request.form.to_dict()
        lead_id = form.get('leads[status][0][id]')
        subdomain = form.get('account[subdomain]')
        await make_bonus(subdomain, int(lead_id))
        logging.info('Make_bonus {} {}'.format(subdomain, lead_id))
        response = app.response_class(
            status=200
        )
    else:
        # print(33333333333, request.get_data(as_text=True))
        response = app.response_class(
            status=402
        )

    return response


@app.route('/load/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@app.route('/file', methods=['get', 'post'])
async def download():
    download_link = ''
    if request.method == 'POST':
        # print(111111111111111, request.form.to_dict())
        market = request.form.get('market')
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

            if check[1] == 'csv':
                try:
                    encode = 'utf-8'
                    with open(UPLOAD_FOLDER + filename, 'r', encoding=encode) as read_file:
                        reader = csv.reader(read_file, delimiter=';')
                        shorter_data(reader, 'csv')
                        print(2323, encode)
                        flash("File upload successfuly")
                        return redirect(request.url)

                except:
                    encode = "windows-1251"
                    with open(UPLOAD_FOLDER + filename, 'r', encoding=encode) as read_file:
                        reader = csv.reader(read_file, delimiter=';')
                        shorter_data(reader)
                        print(2323, encode)
                        flash("File upload successfuly")
                        return redirect(request.url)

            elif check[1] == 'xlsx':
                if not market:
                    flash("Выберите маркетплейс для загружаемого файла")
                    return redirect(request.url)
                # data = read_xlsx(file)
                data = read_xlsx_v2(file, market)
                await make_data_for_request_v2(data, market)
                if data:
                    flash("File upload successfully")
                    return redirect(request.url)

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # download_link = redirect(url_for('download_file', name=filename))
            # return redirect(request.url), download_link
        return redirect(url_for('download'))

    return render_template('index.html')


@app.route('/add_store', methods=['get', 'post'])
async def add_store():
    if request.method == 'POST':
        print(22222222222222222, request.form.to_dict())
        data = request.form.to_dict()
        market = data.get('market')
        store_id = data.get('store_id')
        key_store = data.get('key_store')
        api_key_ps = data.get('api_key_ps')
        upload_link = data.get('upload_link')


        if (market == '235' or market == '2063') \
                and store_id != '' and key_store != '' and upload_link != '':
            result = conn.execute_query_v2(query_add_settings_ym,
                                           (market,
                                            key_store,
                                            store_id,
                                            api_key_ps,
                                            upload_link))
            if result[0]:
                flash('Настройки удачно сохранены')
            else:
                flash(f"Ошибка сохранения {result[1]}")

        elif market != '' and key_store != '' and upload_link != '':
            random_uuid = str(uuid.uuid4())
            url = request.url
            target_url_new = url.rsplit('/', 1)[0] + f'/external_orders/{random_uuid}/new'
            target_url_cancel = url.rsplit('/', 1)[0] + f'/external_orders/{random_uuid}/cancel'
            print(33333333, market, key_store, store_id, upload_link,
                  random_uuid, target_url_new, target_url_cancel, url)
            try:
                conn.execute_query_v2(query_add_settings_without_ym,
                                               (market,
                                                key_store,
                                                random_uuid,
                                                api_key_ps,
                                                upload_link))
                flash(f'Настройки удачно сохранены. Ссылка для новых заказов {target_url_new}.'
                      f' \n Ссылка для отмены заказов {target_url_cancel}.')
            except IntegrityError as e:
                if isinstance(e, UniqueViolation):
                    flash(f"Ошибка сохранения {e}")

            # if result:
            #     flash(f'Настройки удачно сохранены. Ссылка для новых заказов {url}')
            # else:
            #     flash(f"Ошибка сохранения {result}")
        else:
            flash("Проверьте полноту введенных данных")

        return redirect('/add_store')

    return render_template('/add-store.html')


if __name__ == '__main__':
    # #Debug/Development
    # run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=8880)
    # Production
    # http_server = WSGIServer(('', 8880), app)
    # http_server.serve_forever()
