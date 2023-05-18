from __future__ import print_function

import csv
import datetime
# from pictures import write
import json
import mysql.connector
from main import get_wheels
import requests
from getcsv import get_tyres_csv
from categories import categories_summer, categories_wheels, categories_winter, categories_allseason


def write(smth):
    # with open('log.txt', 'a') as file:
    with open('/usr/local/bin/fuck_debian/tyres_wheels/log.txt', 'a') as file:
        how_time = datetime.datetime.now()
        file.write(str(how_time) + '-' + smth + '\n')


# count quantity > 4 for sale
def is_in_stocks(dictionary):
    quantity = dictionary.get('in_stocks')
    if quantity is None:
        quantity = 0
        stock = dictionary.get('stocks')
        if stock is not None:
            for i in range(len(stock) - 1):
                if stock[i]['quantity'].isdigit():
                    in_stock = int(stock[i]['quantity'])
                elif stock[i]['quantity'][1:].isdigit():
                    in_stock = int(stock[i]['quantity'][1:])
                else:
                    continue

                quantity += in_stock

    return quantity


# def isin_stock(list_data):
#     pass


def write_pictures_data(listt):
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as file:
            json.dump(listt, file)
    except:
        with open('dict_images.json', "w") as file:
            json.dump(listt, file)


def rewrite_pictures_data(listt):
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "r") as read_file:
            data_list = json.load(read_file)
            print('file_images_read', len(data_list))
    except:
        with open('dict_images.json', "r") as read_file:
            data_list = json.load(read_file)
            print('file_images_read', len(data_list))

    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as write_file:
            data_list.extend(listt)
            json.dump(data_list, write_file)
            write_file.close()
            print('file_images_write_1', len(data_list))

    except:
        with open('dict_images.json', "w") as write_file:
            data_list.extend(listt)
            json.dump(data_list, write_file)
            write_file.close()
            print('file_images_write', len(data_list))


def prepare_get_image(last_id, tuple):
    dict_images = {}
    dict_images[last_id] = tuple

    return dict_images


# create data wheels
def standart_product(dictionary, in_stock):
    result = False
    for _ in dictionary:
        name = dictionary['name']
        description = dictionary['description'][:-145]
        vendor = dictionary['vendor']
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            break
        # check category wheels and tyres
        category_id = dictionary.get('category_id')
        if category_id is None:
            category_id = categories_wheels.get(vendor)
        price = dictionary.get('price_b2b')
        if price is None:
            price = dictionary['price']['rrc'] - 400
            price = round(price, 0)

        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        product_code = dictionary['vendorCode']
        default_picture = dictionary['picture']
        image_tuple = (0,)
        if default_picture[-2:] == '0.':
            default_picture = 88888888
        else:
            # default_picture = 88888888
            image_url = dictionary['picture']
            index = image_url.rfind('/')
            name_picture = image_url[index + 1:]
            if len(name_picture) < 10:
                name_picture = "11" + name_picture
            image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1

        result = [category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1], image_tuple

    return result


# create dictonary options wheels from
def params_data(dict_param):
    our_data = {}
    for i in range(len(dict_param['params']) - 1):
        name = dict_param['params'][i]['name']
        value = dict_param['params'][i]['value']
        our_data[name] = value

    return our_data


# def params_optyres(dictionary, product_id):

# data_options_tyres = []
# radius = dictionary['diameter']
# width_tyres = dictionary['width']  # 14 #tyres only
# h_profil = dictionary['profile']  # 15 #tyres only
# option_ids = [16, 15, 14]
# for option in option_ids:
#     if option == 16:
#         data_options_tyres.append((option, product_id, radius))
#     elif option == 15:
#         data_options_tyres.append((option, product_id, width_tyres))
#     elif option == 14:
#         data_options_tyres.append((option, product_id, h_profil))

# return data_options_tyres


def params_options_tyres(dictionary, product_id):
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


def params_options_wheels(dictionary, product_id):
    # params = {'product_id': product_id}
    # # url = 'http://super-puper.ml:8080/params/options/wheels'
    # url = 'http://localhost:7770/params/options/wheels'
    # response = requests.post(url, params=params, json=dictionary)
    # data = response.json()
    data_options = []
    diametr = dictionary["diameter"]  # 16
    bolts = dictionary["bolts_spacing"]  # 17,
    et = dictionary["et"]  # 18
    hole = dictionary['dia']  # 19
    width_wheel = dictionary['width']

    option_ids = [16, 17, 18, 19, 20]  # = (diametr, bolts, et, hole, width_wheel)
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


def params_optwheels(dictionary, product_id):
    params = {'product_id': product_id}
    url = 'http://super-puper.ml:5000/params/options/wheels'
    # url = 'http://localhost:7770/params/options/wheels'
    response = requests.post(url, params=params, json=dictionary)
    data = response.json()

    return data


# Insert  options product information # приведение прилетающих данных к виду на сайте
def params_options(dictionary, product_id):
    data_options = []
    for _ in dictionary:
        if dictionary.get('ET') is not None and dictionary.get('PCD') is not None:
            diametr = dictionary["D (размер обода)"].replace('x', '').replace(',', '.')  # 16
            bolts = dictionary["PCD"]  # 17,
            et = dictionary["ET"]  # 18
            hole = dictionary['DIA'].replace('d-', 'D')  # 19
            width_wheel = dictionary['LZ (ширина обода)']  # 20
        # 20
        elif dictionary.get('ET') is not None:
            diametr = dictionary["D (размер обода)"].replace('x', '').replace(',', '.')  # 16
            bolts = 0  # 17,
            et = dictionary["ET"]  # 18
            hole = dictionary['DIA'].replace('d-', 'D')  # 19
            width_wheel = dictionary['LZ (ширина обода)']  # 20
        else:
            diametr = dictionary["D (размер обода)"].replace('x', '').replace(',', '.')  # 16
            bolts = 0  # 17,
            et = 0  # 18
            hole = dictionary['DIA'].replace('d-', 'D')  # 19
            width_wheel = dictionary['LZ (ширина обода)']  # 20

            # ('14'=>'Ширина шины','15'=>'Профиль','16'=>'Диаметр','17'=>'Крепеж','18'=>'Вылет', '19'=>'Центральное отверстие','20'=>'Ширина диска')

        option_ids = [16, 17, 18, 19, 20]  # = (diametr, bolts, et, hole, width_wheel)

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

        result = data_options

        return result


def create_connection():
    connx = None
    try:
        connx = mysql.connector.connect(user='root', database='db1000koles',
                                      password='toor_Pass1!', host='localhost')  #password='12345678',
        # connx = mysql.connector.connect(user='kolesru', database='kolesru',
        #                                 password='9fUev3XGWb18glvs', host='localhost')
    except ConnectionError as error:
        print(f'We have ERROR CREATE_CONN {error}')

    return connx


def make_query_get_id(connection, query, data_query):
    cursor = connection.cursor(buffered=True)
    lastrow_id = None
    try:
        cursor.execute(query, data_query)
        connection.commit()
        lastrow_id = cursor.lastrowid
        # print("Query executed successfully from make_query_get_id")
        # connection.close()
    except Exception as e:
        print(f"The error MAKE_QUERY'{e}' occurred")

    cursor.close()
    return lastrow_id


def make_query(connection, query, data_query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query, data_query)
        connection.commit()
        # print("Query executed successfully from make_query")
        # connection.close()
    except Exception as e:
        print(f"The error '{data_query}'MAKE_QUERY WITHOUT ID'{e}' occurred")

    cursor.close()


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Exception as e:
        print(f"The error DATABASE CREATE '{e}' occurred")


# cursor = cnx.cursor(buffered=True)

# current structure db for wheels
add_product = ("INSERT INTO avl_products "
               "(categoryID, name, description, Price, in_stock, enabled, product_code, date_added, date_modified, eproduct_filename, meta_description, meta_keywords, params, koeff, meta_h1) "  # params
               "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

add_pictures = ("INSERT INTO avl_product_pictures (productID, filename)"
                "VALUES (%s, %s)")

add_product_picture = ("UPDATE avl_products SET default_picture = %s  WHERE productID = %s")
#  ("INSERT INTO avl_products (default_picture)"
# "VALUES (%s)"
# "WHERE productID = %s")

add_options = ("INSERT INTO avl_product_options_values (optionID, productID, option_value)"
               "VALUES (%s, %s, %s)")

query_check = (" SELECT in_stock, productID, Price  FROM avl_products"
               " WHERE categoryID = %s AND product_code = %s")

update = (
    "UPDATE avl_products SET Price = %s, in_stock = %s, enabled = %s,"
    " date_modified = NOW()  WHERE categoryID = %s AND product_code = %s")  # product_ID = %(product_id)s


def check_is_exist(product_code, categoryID):
    result = None
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query_check, [categoryID, product_code])
    for (in_stock, product_id, price_site) in cursor:
        if product_id:
            result = (True, in_stock, price_site)  # cursor.execute(update, data)

    return result


def get_magic_link():
    link = 'http://super-puper.ml/data_product.json'
    return link


def data_products():
    get_wheels()
    get_tyres_csv()
    # magic_link = get_magic_link()
    # data_resp = requests.get(magic_link)
    # data_product = data_resp.json()
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/data_product.json', 'r') as file:
            data_product = json.load(file)
    except:
        with open('data_product.json', 'r') as file:
            data_product = json.load(file)

    print(datetime.datetime.now(), 'file read')
    return data_product


def check_and_write():
    data_from = data_products()
    ij_data = []
    count = 0
    connection = create_connection()
    for data_product in data_from:
        # try:
        category = data_product.get('category')
        quantity = is_in_stocks(data_product)
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            # try:
            data = standart_product(data_product, quantity)
            if data is not False:
                is_exist = check_is_exist(data[0][6], data[0][0])
                if is_exist is None and quantity >= 4:
                    product_id = make_query_get_id(connection, add_product, data[0])  # cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data[1]))
                    # print("pictures -", product_id, data[1][0])
                    # cursor.execute(add_pictures, [product_id, data[1][0]])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    # cursor.execute(add_product_picture, proxy_data)
                    make_query(connection, add_product_picture, proxy_data)
                    # write_pictures_data(ij_data)
                    dict_options = params_data(data_product)
                    data_options = params_options(dict_options, product_id)
                    for option in data_options:
                        # cursor.execute(add_options, option)
                        make_query(connection, add_options, option)


                elif is_exist is not None:
                    category_id = categories_wheels[data[0][7]]
                    product_code = data[0][6]
                    price_for_site = data[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
                        print(is_exist[1], is_exist[2], 'quantity2 -', quantity, data[0][3])
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity3 -', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)


        elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
            try:
                data = standart_product(data_product, quantity)
                # print('tires', data[0][6], data[0][3], quantity, data[0][0])
                is_exist = check_is_exist(data[0][6], data[0][0])
                if is_exist is None and quantity >= 4:
                    print('tires', data[0][6], data[0][3], quantity, data[0][0])
                    # cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data[0])  # cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data[1]))
                    # print("pictures -", product_id, data[1][0])
                    # cursor.execute(add_pictures, [product_id, data[1][0]])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    make_query(connection, add_product_picture,
                               proxy_data)  # cursor.execute(add_product_picture, proxy_data)
                    # write_pictures_data(ij_data)
                    # dict_options = params_data(data_product)

                    data_options_tyres = params_options_tyres(data_product, product_id)
                    for option in data_options_tyres:
                        make_query(connection, add_options, option)  # cursor.execute(add_options, option)
                elif is_exist is not None:
                    category_id = data[0][0]  # because we get data from csv and has category_id
                    product_code = data[0][6]
                    price_for_site = data[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
                        print(is_exist[1], is_exist[2], 'quantity222 -', quantity, data[0][3])
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        print(is_exist[1], 'quantity333 -', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print(str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print(str(data_product))
                continue

        else:
            # print('pass', category)
            continue

        # except KeyError as e:
        #     write("Something went wrong KeyError2: {}".format(e))
        #     write(str(data_product))
        #     print("Something went wrong KeyError2: {}".format(e))
        #     print(str(data_product))
        #     count += 1
        #     continue

    # print(data_product[:5], sep='\n')

    # Make sure data is committed to the database
    # cnx.commit()
    #
    # cursor.close()
    connection.close()
    # smth get
    write_pictures_data(ij_data)
    print('write_pictures_data', len(ij_data))
    # write('from_check_and_write errors ' +  str(count))
    print('from_check_and_write errors', count)


def check_write_json(data_from_json):
    ij_data = []
    count = 0
    connection = create_connection()
    for data_product in data_from_json:
        # try:
        category = data_product[0].pop(-1)  # [-1]
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if is_exist is None and quantity >= 4:
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                ij_data.append(prepare_get_image(product_id, data_product[1]))
                print('ij_data-1,4', len(ij_data), ij_data[-1])
                picture_id = make_query_get_id(connection, add_pictures,
                                               [product_id, data_product[1][0]])  # cursor.lastrowid
                proxy_data = [picture_id, product_id]
                # cursor.execute(add_product_picture, proxy_data)
                make_query(connection, add_product_picture, proxy_data)
                print('ij_data-5,7', len(ij_data))
                # write_pictures_data(ij_data)
                # data_options = params_options_wheels(data_product[2], product_id)
                data_options = params_optwheels(data_product[2], product_id)
                for option in data_options:
                    # cursor.execute(add_options, option)
                    make_query(connection, add_options, option)

            elif is_exist is not None:
                category_id = categories_wheels[data_product[0][7]]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    print(is_exist[1], is_exist[2], 'quantity12 -', quantity, data_product[0][3])
                    enabled = 1
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                elif quantity <= 4 and is_exist[1] != quantity:
                    print(is_exist[1], 'quantity13 -', quantity)
                    enabled = 0
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  # cursor.execute(update, new_data)


        elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if is_exist is None and quantity >= 4:
                    # cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data_product[1]))
                    # print('ij_data-12', len(ij_data), ij_data[-1])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data_product[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    make_query(connection, add_product_picture,
                               proxy_data)  # cursor.execute(add_product_picture, proxy_data)
                    print('ij_data-12-2', len(ij_data))
                    # write_pictures_data(ij_data)
                    # dict_options = params_data(data_product)

                    data_options_tyres = params_options_tyres(data_product[2], product_id)
                    for option in data_options_tyres:
                        make_query(connection, add_options, option)  # cursor.execute(add_options, option)
                elif is_exist is not None:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        print(is_exist[1], is_exist[2], 'before_quantity22',
                              category_id, product_code, ' -now', quantity, data_product[0][3])
                        enabled = 1
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print(str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print(str(data_product))
                continue

        else:
            # print('pass', category)
            continue

        # except KeyError as e:
        #     write("Something went wrong KeyError2: {}".format(e))
        #     write(str(data_product))
        #     print("Something went wrong KeyError2: {}".format(e))
        #     print(str(data_product))
        #     count += 1
        #     continue

    # print(data_product[:5], sep='\n')

    # Make sure data is committed to the database
    # cnx.commit()
    #
    # cursor.close()
    connection.close()
    # smth get
    write_pictures_data(ij_data)
    print('write_pictures_data_2', len(ij_data))
    # write('from_check_and_write errors ' +  str(count))
    print('from_check_and_write errors', count)

def get_smth_please():
    # params = {'product_id': product_id}
    url = 'http://super-puper.ml:5000/get/smth'
    # url = 'http://localhost:7770/get/smth'
    response = requests.post(url)
    data = response.json()

    return data

def check_for_json():
    ij_data = []
    count = 0
    connection = create_connection()
    data_from_json = get_smth_please()
    # data_product =
    for data_product in data_from_json:
        # try:
        category = data_product[0].pop(-1)  # [-1]
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if is_exist is None and quantity >= 4:
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                ij_data.append(prepare_get_image(product_id, data_product[1]))
                print('ij_data-1,4', len(ij_data), ij_data[-1])
                picture_id = make_query_get_id(connection, add_pictures,
                                               [product_id, data_product[1][0]])  # cursor.lastrowid
                proxy_data = [picture_id, product_id]
                # cursor.execute(add_product_picture, proxy_data)
                make_query(connection, add_product_picture, proxy_data)
                print('ij_data-5,7', len(ij_data))
                # write_pictures_data(ij_data)
                # data_options = params_options_wheels(data_product[2], product_id)
                data_options = params_optwheels(data_product[2], product_id)
                for option in data_options:
                    # cursor.execute(add_options, option)
                    make_query(connection, add_options, option)

            elif is_exist is not None:
                category_id = categories_wheels[data_product[0][7]]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    print(is_exist[1], is_exist[2], 'quantity12 -', quantity, data_product[0][3])
                    enabled = 1
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                elif quantity <= 4 and is_exist[1] != quantity:
                    print(is_exist[1], 'quantity13 -', quantity)
                    enabled = 0
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  # cursor.execute(update, new_data)


        elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if is_exist is None and quantity >= 4:
                    # cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data_product[1]))
                    # print('ij_data-12', len(ij_data), ij_data[-1])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data_product[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    make_query(connection, add_product_picture,
                               proxy_data)  # cursor.execute(add_product_picture, proxy_data)
                    print('ij_data-12-2', len(ij_data))
                    # write_pictures_data(ij_data)
                    # dict_options = params_data(data_product)

                    data_options_tyres = params_options_tyres(data_product[2], product_id)
                    for option in data_options_tyres:
                        make_query(connection, add_options, option)  # cursor.execute(add_options, option)
                elif is_exist is not None:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        print(is_exist[1], is_exist[2], 'before_quantity22',
                              category_id, product_code, ' -now', quantity, data_product[0][3])
                        enabled = 1
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  # cursor.execute(update, new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print(str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print(str(data_product))
                continue

        else:
            # print('pass', category)
            continue

        # except KeyError as e:
        #     write("Something went wrong KeyError2: {}".format(e))
        #     write(str(data_product))
        #     print("Something went wrong KeyError2: {}".format(e))
        #     print(str(data_product))
        #     count += 1
        #     continue

    # print(data_product[:5], sep='\n')

    # Make sure data is committed to the database
    # cnx.commit()
    #
    # cursor.close()
    connection.close()
    # smth get
    write_pictures_data(ij_data)
    print('write_pictures_data_2', len(ij_data))
    # write('from_check_and_write errors ' +  str(count))
    print('from_check_and_write errors', count)