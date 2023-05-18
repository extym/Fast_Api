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

string_update = ("UPDATE avl_products SET Price = %s, in_stock = %s, enabled = %s, date_modified = NOW()  WHERE categoryID = %s AND product_code = %s")

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
    print('product_id', product_id)
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
            data_options_tyres.append((option, product_id, width_tyres))
        elif option == 14:
            data_options_tyres.append((option, product_id, h_profil))

    return data_options_tyres



#
# @app.route('/check/write/json', methods=['POST'])
# def check_write_json(data_from_json):
#     ij_data = []
#     count = 0
#     # connection = create_connection()
#     for data_product in data_from_json:
#         # try:
#         category = data_product[0].pop(-1)  # [-1]
#         quantity = data_product[0][4]
#         if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
#             is_exist = check_is_exist(data_product[0][6], data_product[0][0])
#             if is_exist is None and quantity >= 4:
#                 product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
#                 ij_data.append(prepare_get_image(product_id, data_product[1]))
#                 print('ij_data-1,4', len(ij_data), ij_data[-1])
#                 picture_id = make_query_get_id(connection, add_pictures,
#                                                [product_id, data_product[1][0]])  # cursor.lastrowid
#                 proxy_data = [picture_id, product_id]
#                 # cursor.execute(add_product_picture, proxy_data)
#                 make_query(connection, add_product_picture, proxy_data)
#                 print('ij_data-5,7', len(ij_data))
#                 # write_pictures_data(ij_data)
#                 # data_options = params_options_wheels(data_product[2], product_id)
#                 data_options = params_optwheels(data_product[2], product_id)
#                 for option in data_options:
#                     # cursor.execute(add_options, option)
#                     make_query(connection, add_options, option)
#
#             elif is_exist is not None:
#                 category_id = categories_wheels[data_product[0][7]]
#                 product_code = data_product[0][6]
#                 price_for_site = data_product[0][3]
#                 if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
#                     print(is_exist[1], is_exist[2], 'quantity12 -', quantity, data_product[0][3])
#                     enabled = 1
#                     new_data = [quantity, enabled, category_id, price_for_site, product_code]
#                     make_query(connection, update, new_data)  # cursor.execute(update, new_data)
#                 elif quantity <= 4 and is_exist[1] != quantity:
#                     print(is_exist[1], 'quantity13 -', quantity)
#                     enabled = 0
#                     new_data = [quantity, enabled, category_id, price_for_site, product_code]
#                     make_query(connection, update, new_data)  # cursor.execute(update, new_data)
#
#
#         elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
#             try:
#                 is_exist = check_is_exist(data_product[0][6], data_product[0][0])
#                 if is_exist is None and quantity >= 4:
#                     # cursor.execute(add_product, data[0])
#                     product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
#                     ij_data.append(prepare_get_image(product_id, data_product[1]))
#                     # print('ij_data-12', len(ij_data), ij_data[-1])
#                     picture_id = make_query_get_id(connection, add_pictures,
#                                                    [product_id, data_product[1][0]])  # cursor.lastrowid
#                     proxy_data = [picture_id, product_id]
#                     make_query(connection, add_product_picture,
#                                proxy_data)  # cursor.execute(add_product_picture, proxy_data)
#                     print('ij_data-12-2', len(ij_data))
#                     # write_pictures_data(ij_data)
#                     # dict_options = params_data(data_product)
#
#                     data_options_tyres = params_options_tyres(data_product[2], product_id)
#                     for option in data_options_tyres:
#                         make_query(connection, add_options, option)  # cursor.execute(add_options, option)
#                 elif is_exist is not None:
#                     category_id = data_product[0][0]  # because we get data from csv and has category_id
#                     product_code = data_product[0][6]
#                     price_for_site = data_product[0][3]
#                     if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
#                         print(is_exist[1], is_exist[2], 'before_quantity22',
#                               category_id, product_code, ' -now', quantity, data_product[0][3])
#                         enabled = 1
#                         new_data = [quantity, enabled, category_id, price_for_site, product_code]
#                         make_query(connection, update, new_data)  # cursor.execute(update, new_data)
#                     elif quantity <= 4 and is_exist[1] != quantity:
#                         print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
#                         enabled = 0
#                         new_data = [quantity, enabled, category_id, price_for_site, product_code]
#                         make_query(connection, update, new_data)  # cursor.execute(update, new_data)
#
#             except mysql.connector.Error as err:
#                 write("S_thing went wrong connector tyres: {}".format(err))
#                 write(str(data_product))
#                 print("S_thing went wrong connector tyres: {}".format(err))
#                 print(str(data_product))
#                 continue
#             except KeyError as e:
#                 write("S_thing went wrong KeyError tyres---: {}".format(e))
#                 write(str(data_product))
#                 print("S_thing went wrong KeyError tyres---: {}".format(e))
#                 print(str(data_product))
#                 continue
#
#         else:
#             # print('pass', category)
#             continue
#
#         # except KeyError as e:
#         #     write("Something went wrong KeyError2: {}".format(e))
#         #     write(str(data_product))
#         #     print("Something went wrong KeyError2: {}".format(e))
#         #     print(str(data_product))
#         #     count += 1
#         #     continue
#
#     # print(data_product[:5], sep='\n')
#
#     # Make sure data is committed to the database
#     # cnx.commit()
#     #
#     # cursor.close()
#     connection.close()
#     # smth get
#     write_pictures_data(ij_data)
#     print('write_pictures_data_2', len(ij_data))
#     # write('from_check_and_write errors ' +  str(count))
#     print('from_check_and_write errors', count)


@app.route('/json', methods=['POST'])
def get_data():
    ip_addr = request.environ.get('REMOTE_ADDR')  ##
    data_product = []
    addr = request.headers.get('X-Forwarded-For')
    # print(ip_addr)
    # if ip_addr == '::ffff:77.72.131.69' or ip_addr == '77.72.131.69'\
    #         or ip_addr == '62.76.102.53':
    if ip_addr == '::ffff:77.72.131.69' or ip_addr == '77.72.131.69' \
            or ip_addr == '62.76.102.53' or ip_addr == '::ffff:127.0.0.1':
        data_product = request.get_json()
        # proxy =[]
        # proxy.append(request_data)
        # data_product.extend(proxy)

        print(datetime.now(), '--', len(data_product))

        # except Exception as error:
        # print(f'page--{i}', 'Fuck JSON DECODE: {}'.format(error))
        # continue

        # with open("/var/www/html/wheels/data_product.json", "r") as read_file:
        #     all_data = json.load(read_file)
        #     all_data.extend(data_product)
        #     print('all_data', len(all_data), len(data_product))
        #     read_file.close()
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
