import sys
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
from excel_read import read_xlsx
import csv
from avito import *
from amo import *
import urllib3
import logging
from bot_tg import send_get
from parts_soft import make_data_for_request_v2
import connect as conn


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


# print(asyncio.run(check_is_exist_message_answer_v2('ad6c351403976b0f6175b81965221000', 'u2i-PalCq8X5aU0iwwKcwfUAqQ' )))

#
# def make_lead(data):
#     creds = get_creds()
#     access_token = creds.get('access_token')
#     data_send = make_data(data)
#     headers = {
#         'Authorization': 'Bearer ' + access_token
#     }
#     metod = '/api/v4/leads'
#     link = url + metod
#     answer = requests.post(link, headers=headers, json=data_send)
#     print(2345, answer.text)
#
#     return answer.text
#
#
# def make_lead_complex(data):
#     creds = get_creds()
#     access_token = creds.get('access_token')
#     data_send = make_compex_data(data)
#     headers = {
#         'Authorization': 'Bearer ' + access_token
#     }
#     metod = '/api/v4/leads/complex'
#     link = url + metod
#     answer = requests.post(link, headers=headers, json=data_send)
#     result = answer.text
#     # print(result)
#     write_result(result)
#
#     return result


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

#
# @app.route('/form-data', methods=['POST'])
# def get_data():
#     addr = request.headers.get('X-Forwarded-For')
#     if addr == '195.16.42.18' or addr == '185.2.32.202':
#         data = request.form
#         # print('data', type(data), data)
#         try:
#             sity = data.get('form_fields[32119][values][0]')
#             name = data.get('form_fields[32121][values][0]')
#             phone = data.get("form_fields[32127][values][0]")  # "('caller_num')
#             source = data.get('form_fields[32120][values][0]')
#             mark = data.get('form_fields[32124][values][0]')
#             first_name = data.get('form_fields[32126][values][0]')  # ('caller_name')
#             call_result = data.get('form_fields[32122][values][0]')
#             comment = data.get('form_fields[32123][values][0]')
#             target = data.get('form_fields[32121][values][0]')
#             proxy = (sity, name, phone, source, mark, first_name, call_result, comment, target)
#             # print('sity', sity,  type(proxy), proxy)
#             result = make_lead_complex(proxy)
#             write_incoming(proxy)
#             print('result_send_data', result)
#         except:
#             print('ERROR make lead')
#
#         return 'OK'
#
#     else:
#         print('response from ', addr)
#         return app.response_class(status=402)


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
            if author_id == 1 or check[0]: # or (author_id in sender_ids and msg != bot_answer):
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
                                 .format(hook,check, chat_id))
                    return app.response_class(
                        status=200
                    )
                except Exception as err:
                    logging.error('ERROR_GET_AVITO_CURRENT_CHAT {}, hook {}, {} {} {} {}'.
                                  format(err, hook, check, msg_id, chat_id, user_id))
                    return app.response_class(
                        status=200
                    )
        except Exception as  error:
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
                data = read_xlsx(file)
                # print(2222222222222, data)
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
        print(33333333, market, key_store, store_id, upload_link)

        if (market == '235' or market == '2063' or market == '2063')\
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
            result = conn.execute_query_v2(query_add_settings_without_ym,
                                        (market,
                                         key_store,
                                         api_key_ps,
                                         upload_link))
            if result[0]:
                flash('Настройки удачно сохранены')
            else:
                flash(f"Ошибка сохранения {result[1]}")
        else:
            flash("Проверьте полноту введенных данных")

        return redirect('/add_store')

    return render_template('/add-store.html')


if __name__ == '__main__':
    # #Debug/Development
    #run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=8880)
    # Production
    # http_server = WSGIServer(('', 8880), app)
    # http_server.serve_forever()
