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





app = Flask(__name__)
#for develop ONLY!
#app.debug = True

@app.route('/test', methods=['GET', 'POST'])
def test():
    response = 'OK'
    # response = app.response_class(
    #     json.dumps('OK'),
    #     status=200,
    #     content_type='application/json'
    # )
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


if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 9900), app)
    http_server.serve_forever()
