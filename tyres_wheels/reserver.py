import sys

from gevent import monkey
monkey.patch_all()

import random
import string
import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from time import sleep
#from cred import token_market_dbs, token_market_fbs
import urllib3
urllib3.disable_warnings()


app = Flask(__name__)
#for develop ONLY!
#app.debug = True


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'OK'

string_add_product_picture = ("UPDATE avl_products SET default_picture = %s  WHERE productID = %s")

string_update = ("UPDATE avl_products SET Price = %s, in_stock = %s, enabled = %s, date_modified = NOW()  "
                 "WHERE categoryID = %s AND product_code = %s")

string_add_options = ("INSERT INTO avl_product_options_values (optionID, productID, option_value) VALUES (%s, %s, %s)")

@app.route('/random/choice', methods=['POST'])
def random_choice():
    data = request.get_json()
    print('random_choice_data', data)
    if data == 'add_product_picture':
        return string_add_product_picture
    elif data == 'update':
        return string_update
    elif data == 'add_options':
        return string_add_options
    else:
        return 402


@app.route('/params/options/wheels', methods=['POST'])
def params_optinels():
    product_id = request.args.get('product_id')
    # print('product_id', product_id)
    dictionary = request.get_json()
    # print('dictionary', dictionary)
    data_options = []
    diametr = dictionary["diameter"]  # 16
    bolts = dictionary["bolts_spacing"]  # 17,
    et = dictionary["et"]  # 18
    hole = dictionary['dia']  # 19
    width_wheel = dictionary['width']

    option_ids = [16, 17, 18, 19, 20]  # = (diametr, bolts, et, hole, width_w
    for j in range(len(option_ids)):
        if option_ids[j] == 16:
            data_options.append((option_ids[j], product_id, diametr))
        elif option_ids[j] == 17:
            data_options.append((option_ids[j], product_id, bolts))
        elif option_ids[j] == 18:
            data_options.append((option_ids[j], product_id, et))
        elif option_ids[j] == 19:
            data_options.append((option_ids[j], product_id, hole))
        elif option_ids[j] == 20:
            data_options.append((option_ids[j], product_id, width_wheel))

    return data_options


@app.route('/params/options/tyres', methods=['POST'])
def params_opttyres():
    product_id = request.args.get('product_id')
    print('product_id', product_id)
    dictionary = request.get_json()
    data_options_tyres = []
    radius = dictionary['diameter']
    width_tyres = dictionary['width']  # 14 #tyres only
    h_profil = dictionary['profile']  # 15 #tyres only
    option_ids = [16, 15, 14]
    for option in option_ids:
        if option == 16:
            data_options_tyres.append((option, product_id, radius))
        elif option == 15:
            data_options_tyres.append((option, product_id, h_profil))
        elif option == 14:
            data_options_tyres.append((option, product_id, width_tyres))

    return data_options_tyres



@app.route('/json', methods=['POST'])
def get_data():
    ip_addr = request.environ.get('REMOTE_ADDR')  ##
    data_product = []
    addr = request.headers.get('X-Forwarded-For')

    if ip_addr == '::ffff:77.72.131.69' or ip_addr == '77.72.131.69' \
            or ip_addr == '62.76.102.53' or ip_addr == '::ffff:127.0.0.1':
        data_product = request.get_json()

        print(datetime.now(), '--', len(data_product))

        with open("/var/www/html/wheels/data_product.json", "w") as write_file:
            json.dump(data_product, write_file)
            write_file.close()
        mems = sys.getsizeof(data_product)
        print('111', mems / 1000, 'Kb')
        return 'OK'

    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')




if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 7770), app)
    http_server.serve_forever()
