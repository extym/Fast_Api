import sys
from cred import *
# from cred_update import creds
from gevent import monkey
monkey.patch_all()
from datetime import datetime
import random
import string
import json
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from gevent.pywsgi import WSGIServer
from datetime import datetime, timedelta
import requests
from maintenance import shorter_data, read_xls
import csv
from test_data import get_creds
from amo import *
import urllib3
urllib3.disable_warnings()

# url = 'https://zakazjpexpressru.amocrm.ru'
ALLOWED = {'csv', 'xls', 'xlsx'}
if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH = '/home/userbe/phone/'



refresh = creds.get('refresh')


def check_allowed_filename(filename):
    result = '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED
    curr_name = filename.rsplit('.', 1)[1]
    print(result)
    return result, curr_name



def make_data(resp_data):
    data = [
        {
            "name": resp_data.get('form_fields[32121][name]'),
            'pipeline_id': 5420530,
            'custom_fields_values': [
                {
                    "field_id": 1277277,  #sity - now make on field address
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
    data = [  #(sity, name, phone, source, mark, first_name, call_result, comment, target)
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
    with open(PATH + 'result.txt', 'a') as file:
        file.write(str(datetime.now()) + str(result))
        file.write('\n')


def write_incoming(proxy_tuple):
    with open(PATH + 'incoming.txt', 'a') as file:
        file.write(str(datetime.now()) + str(proxy_tuple))
        file.write('\n')



def make_lead(data):
    creds = get_creds()
    access_token = creds.get('access_token')
    data_send = make_data(data)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    metod = '/api/v4/leads'
    link = url + metod
    answer = requests.post(link, headers=headers, json=data_send)
    print(answer.text)

    return answer.text


def make_lead_complex(data):
    creds = get_creds()
    access_token = creds.get('access_token')
    data_send = make_compex_data(data)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    metod = '/api/v4/leads/complex'
    link = url + metod
    answer = requests.post(link, headers=headers, json=data_send)
    result = answer.text
    # print(result)
    write_result(result)

    return result



app = Flask(__name__, template_folder='template/')
app.secret_key = import_key

#for develop ONLY!
# app.debug = True


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


@app.route('/token', methods=['get', 'post'])
def get_token():
    data  = request.json
    print('data_token', data)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'OK phone'


@app.route('/form-data', methods=['POST'])
def get_data():
    addr = request.headers.get('X-Forwarded-For')
    if addr == '195.16.42.18' or addr == '185.2.32.202':
        data = request.form
        # print('data', type(data), data)
        try:
            sity = data.get('form_fields[32119][values][0]')
            name = data.get('form_fields[32121][values][0]')
            phone = data.get("form_fields[32127][values][0]")  #"('caller_num')
            source = data.get('form_fields[32120][values][0]')
            mark = data.get('form_fields[32124][values][0]')
            first_name = data.get('form_fields[32126][values][0]')  #('caller_name')
            call_result = data.get('form_fields[32122][values][0]')
            comment = data.get('form_fields[32123][values][0]')
            target = data.get('form_fields[32121][values][0]')
            proxy = (sity, name, phone, source, mark, first_name, call_result, comment, target)
            # print('sity', sity,  type(proxy), proxy)
            result = make_lead_complex(proxy)
            write_incoming(proxy)
            print('result_send_data', result)
        except:
            print('ERROR make lead')

        return 'OK'

    else:
        print('response from ', addr )
        return app.response_class(status=402)



@app.route('/webhook', methods=['GET', 'POST'])
def avito_webhook():
    # headers = request.headers
    if request.headers.get('X-Avito-Messenger-Signature'):
        print(request.headers)
        try:
            result = request.get_json()
            print(1, type(result))
        except:
            result = request.get_data()
            print(2, type(result))
        print(result)

        return 'Ok'
    else:
        print('WHOIS', request.get_data())
        print('WHOIS', request.headers)
        return app.response_class(
            status=402
        )


##status order from site 3431
@app.route('/check', methods=['get', 'POST'])
def check_status():
    if request.method == 'POST':
        write_result(request.headers)
        try:
            form = request.form
            write_result(form)
            print('FFFFFFFFFFF', form)
            data = request.data
            need = json.loads(data)
            print('EEEEEEEEEEE', type(need), need)


        except:
            print('ERRRROOOOR')

        return app.response_class(
            status=200
        )

    return "Ok, we await data"


@app.route('/location/<int:scope_id>', methods=['GET', 'POST'])
def wait_amo_hook(scope_id):
    data = request.get_data()
    print("WE GETS SOMETHING", scope_id, request.url, request.method, data)

    return app.response_class(
        status=200
    )





@app.route('/load/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@app.route('/file', methods=['get', 'post'])
def download():
    download_link = ''
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

            if check[1] == 'csv':
                try:
                    encode = 'utf-8'
                    with open(UPLOAD_FOLDER + filename, 'r', encoding=encode) as read_file:
                        reader = csv.reader(read_file, delimiter=';')
                        shorter_data(reader, 'csv')
                        print(encode)
                        flash("File upload successfuly")
                        return redirect(request.url)

                except:
                    encode = "windows-1251"
                    with open(UPLOAD_FOLDER + filename, 'r', encoding=encode) as read_file:
                        reader = csv.reader(read_file, delimiter=';')
                        shorter_data(reader)
                        print(encode)
                        flash("File upload successfuly")
                        return redirect(request.url)

            # elif check[1] == 'xlsx':
            #     data = read_xls(file)
            #     result = shorter_data(data, 'xlsx')
            #     if result:
            #         flash("File upload successfuly")
            #         return redirect(request.url)

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # download_link = redirect(url_for('download_file', name=filename))
            # return redirect(request.url), download_link

    return render_template('index.html')



if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8880), app)
    http_server.serve_forever()
