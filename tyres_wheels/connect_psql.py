from __future__ import print_function

import csv
import datetime
# from pictures import write
import json
import psycopg2
from main import get_wheels, get_new_pages, get_new_pages_v2
import requests
from cred import *
# from getcsv import get_tyres_csv
from categories import *
from pictures import dowload_images


create_new_product = """
CREATE TABLE IF NOT EXISTS products (
id SERIAL PRIMARY KEY,
vendor_code varchar,
active TEXT,
available varchar,
bundle varchar,
canBuyZero varchar,
code varchar,
createdBy varchar,
dateActiveFrom varchar,
dateActiveTo varchar,
dateCreate varchar,
detailPicture varchar,
detailText varchar,
detailTextType varchar,
height varchar,
iblockId int,
iblockSectionId int,
id_bitrix int,
id_price int,
length_prod varchar,
measure varchar,
modifiedBy varchar,
name_prod varchar,
previewPicture varchar,
previewText varchar,
previewTextType varchar,
property574 varchar,
property575 varchar,
property576 varchar,
property577 varchar,
property578 varchar,
property579 varchar,
property580 varchar,
property582 varchar,
property583 varchar,
property584 varchar,
property585 varchar,
property586 varchar,
property587 varchar,
property588 varchar,
property589 varchar,
property590 varchar,
property591 varchar,
property592 varchar,
property593 varchar,
property594 varchar,
property595 varchar,
property596 varchar,
property597 varchar,
property598 varchar,
property599 varchar,
property600 varchar,
property601 varchar,
property602 varchar,
property603 varchar,
property605 varchar,
property606 varchar,
property607 varchar,
property610 varchar,
property612 varchar,
property614 varchar,
property737 varchar,
property738 varchar,
property739 varchar,
property740 varchar,
property741 varchar,
property742 varchar,
property743 varchar,
property744 varchar,
property745 varchar,
property746 varchar,
property747 varchar,
property748 varchar,
property749 varchar,
property750 varchar,
property751 varchar,
property752 varchar,
property753 varchar,
property754 varchar,
property755 varchar,
property756 varchar,
property757 varchar,
purchasingCurrency varchar,
purchasingPrice varchar,
quantity int,
quantityReserved int,
quantityTrace varchar,
sort int,
subscribe varchar,
timestampX varchar,
type_prod varchar,
vatId varchar,
vatIncluded varchar,
weight varchar,
width varchar,
xmlId int,
UNIQUE (id)
)
"""
def write(smth):
    try:
        with open('log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time) + '-' + smth + '\n')
    except:
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


def write_pictures_data(listt):
    with open(DATA_PATH + '/dict_images.json', "w") as file:
        json.dump(listt, file)


def rewrite_pictures_data(listt):
    with open(DATA_PATH + '/dict_images.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_images_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/dict_images.json', "w") as write_file:
        data_list.extend(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_images_write_1', len(listt))

    print('file_images_rewrite', len(data_list))


def rewrite_standart_data(listt):
    with open(DATA_PATH + '/standart_data.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_standart_data_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/standart_data.json', "w") as write_file:
        # data_list.extend(listt)
        data_list.update(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_standart_data_write_1', len(listt))

    print('file_standart_data_rewrite', len(data_list))


def prepare_get_image(last_id, tuple):
    dict_images = {}
    dict_images[last_id] = tuple

    return dict_images


# create data wheels
def standart_product(dictionary, in_stock):
    result = False
    for _ in dictionary:
        name = dictionary['name'].strip('"')
        try:
            description = dictionary.get('description')[:-145]
        except:
            description = ''
        vendor = dictionary['vendor'].replace('"', '')
        if vendor == 'Carwel' or not description:
            description = name
        elif vendor == '':
            break
        # check category wheels and tyres
        category_id = categories_wheels.get(vendor)
        if category_id is None:
            category_id = cats_wheels_upper.get(vendor.upper(), 4000)
        price = dictionary.get('price').strip('"').replace('\xa0', '')

        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        product_code = dictionary['vendor_code'].strip('"').strip('-')
        default_picture = dictionary['foto'].strip('"')
        image_tuple = (0,)
        if default_picture == '""':
            default_picture = '88888888'
        else:
            # default_picture = 88888888
            image_url = dictionary['foto'].strip('"')
            index = image_url.rfind('/')
            name_picture = vendor.lower().strip() + "-" + image_url[index + 1:]
            image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1

        result = [category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1], image_tuple

    return result


def standart_product_v2(list_wheels_json):
    global_result = {}
    proxy = []
    for dictionary in list_wheels_json:
        try:
            name = dictionary['name'].strip('"')
            type = dictionary.get('type').strip('"').split(' ')[-1]
            if type == 'диски':
                category = 5
            else:
                category = 0
            try:
                description = dictionary.get('description')[:-145]
            except:
                description = ''
            if not description:
                description = name
            vendor = dictionary.get('vendor').replace('"', '')
            category_id = categories_wheels \
                .get(vendor, cats_wheels_upper.get(vendor.upper(), 7000))
            price_opt = int(dictionary.get('price').strip('"').replace('\xa0', '').split('.')[0])
            price = float(dictionary.get('RoznicaPrice').strip('"').replace('\xa0', '').split('.')[0])
            rule = False
            if price_opt * 1.18 >= price:
                rule = True
            in_stock = int(dictionary.get('rest').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest2').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest3').strip('"').replace('>', '').replace('<', ''))
            if in_stock >= 4:
                enabled = 1
            else:
                enabled = 0
            name_picture = '88888888'
            product_code = dictionary['vendor_code'].strip('"').strip('-')
            image_url = dictionary['foto'].strip('"')
            if image_url:
                # index = image_url.rfind('/')
                # name_picture = 'colrad-' + image_url[index + 1:]
                name_picture = vendor.strip() + '_' + product_code + '.png'
            image_tuple = (name_picture, image_url)
            koeff = 1
            meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            params = 1
            provider = 'colrad'
            options = {
                'et': 'ET' + dictionary.get('et').strip('"'),
                "bolts_spacing": dictionary.get('pcd1').strip('"')
                                 + '/' + dictionary.get('pcd2').strip('"'),
                'diameter': dictionary.get('diameter').strip('"').strip('0').strip(','),
                'dia': 'D' + dictionary.get('dia').strip('"'),
                'width': dictionary.get('width').strip('"')
            }

            global_result.update({vendor.strip() + product_code: (
                [
                    category_id, name, description, price, in_stock,
                    enabled, product_code, vendor, meta_d, meta_k,
                    params, koeff, meta_h1, provider, category
                ],
                image_tuple,
                options,
                rule,
                price_opt)})

            # result = ([category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
            #            params, koeff, meta_h1, category], image_tuple, options)
            # global_result.append(result)

        except:
            # print("FUCKUP_standart_product_v2", dictionary)
            continue

    write(str(set(proxy)))
    rewrite_standart_data(global_result)

    return global_result


# create dictonary options wheels from
def params_data(dict_param):
    our_data = {}
    for i in range(len(dict_param['params']) - 1):
        name = dict_param['params'][i]['name']
        value = dict_param['params'][i]['value']
        our_data[name] = value

    return our_data


def params_optyres(dictionary, product_id):
    params = {'product_id': product_id}
    url = opt_tyres
    # url = 'http://localhost:7770/params/options/tyres'
    response = requests.post(url, params=params, json=dictionary)
    data = response.json()

    return data


def params_optwheels(dictionary, product_id):
    params = {'product_id': product_id}
    url = url_params
    # url = 'http://localhost:7770/params/options/wheels'
    response = requests.post(url, params=params, json=dictionary)
    # print('resp_params_optwheels', response.text)
    data = response.json()

    return data


# Insert  options product information # приведение прилетающих данных к виду на сайте
def params_options(dictionary, product_id):
    data_options = []
    for row in dictionary:
        try:
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
                hole = dictionary.get('DIA').replace('d-', 'D')  # 19
                width_wheel = dictionary['LZ (ширина обода)']  # 20
            else:
                diametr = dictionary["D (размер обода)"].replace('x', '').replace(',', '.')  # 16
                bolts = 0  # 17,
                et = 0  # 18
                hole = dictionary['DIA'].replace('d-', 'D')  # 19
                width_wheel = dictionary['LZ (ширина обода)']  # 20
        except KeyError as error:
            print('row_err', row, error)
            continue
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

    return data_options


def create_connection():
    connect = None
    try:
        if LOCAL_MODE:
            with psycopg2.connect(user=local_user_pg,
                                  database=local_name_pg,
                                  password=local_pass_pg,
                                  host=local_host_pg) as connect:
                return connect
        else:
            with psycopg2.connect(user=user_db_pg,
                                  database=name_db_pg,
                                  password=pass_db_pg,
                                  host=host_db_pg) as connect:
                return connect

    except ConnectionError as error:
        print(f'We have ERROR CREATE_CONN {error}')


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
        print(f"The error--MAKE_QUERY'{e}' occurred", data_query)

    cursor.close()
    return lastrow_id


def make_query_get_id_v2(query, data_query):
    connection = create_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(query, data_query)
        connection.commit()
        lastrow_id = cursor.lastrowid
        cursor.close()

        connection.close()

    return lastrow_id


def make_query_v2(query, data_query):
    connection = create_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(query, data_query)
        connection.commit()

        cursor.close()
        connection.close()


def make_query_many_v2(query, data_query):
    connection = create_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.executemany(query, data_query)
        connection.commit()

        cursor.close()
        connection.close()


def makery(connection, query, data):
    cursor = connection.cursor(buffered=True)
    # url = 'http://localhost:7770/random/choice'
    url = url_random_choice
    answer = requests.post(url, json=query)
    datas = answer.text
    try:
        cursor.execute(datas, data)
        connection.commit()
        # print('ALL RIGTH____!!!!!!!!!!!')
    except Exception as e:
        print(f"The error '{data}'MAKE_QUERY WITHOUT ID'{e}' occurred")

    cursor.close()


def create_query(query):
    connection = create_connection()
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            print("Query created successfully")
        except Exception as e:
            print(f"The error CREATE '{e}' occurred")


add_product_picture = ("UPDATE avl_products SET default_picture = %s  WHERE productID = %s")

update = ("UPDATE avl_products SET Price = %s, in_stock = %s, enabled = %s, date_modified = NOW()  "
          "WHERE categoryID = %s AND product_code = %s")

add_options = ("INSERT INTO avl_product_options_values (optionID, productID, option_value) VALUES (%s, %s, %s)")

add_product = ("INSERT INTO avl_products "
               "(categoryID, name, description, Price, in_stock, enabled, product_code, date_added, date_modified, eproduct_filename, meta_description, meta_keywords, params, koeff, meta_h1) "  # params
               "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

add_pictures = ("INSERT INTO avl_product_pictures (productID, filename)"
                "VALUES (%s, %s)")

query_check = (" SELECT in_stock, productID, Price  FROM avl_products"
               " WHERE categoryID = %s AND product_code = %s")


def check_is_exist(product_code, categoryID):
    result = (False, 0, 0)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query_check, [categoryID, product_code])
    for (in_stock, product_id, price_site) in cursor:
        if product_id:
            result = (True, in_stock, price_site)  # cursor.execute(update, data)

    return result


def get_magic_link():
    link = magic_link
    return link


def data_products():
    # get_wheels()
    get_new_pages()

    with open(DATA_PATH + 'data_product.json', 'r') as file:
        data_product = json.load(file)

    print(datetime.datetime.now(), 'file read')
    return data_product


def read_data_products():
    some_data = get_new_pages_v2()

    with open(DATA_PATH + 'standart_data.json', 'r') as file:
        data_product = json.load(file)

    print(datetime.datetime.now(), 'file read', len(data_product) + len(some_data))
    return data_product.extend(some_data)


def check_and_write_v3():
    data_from = get_new_pages_v2()
    standart = standart_product_v2(data_from)
    standart_copy = standart.copy()
    ij_data, proxy = [], []
    count = 0
    connection = create_connection()
    for key, data_product in standart.items():
        # try:
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                # ij_data.append(prepare_get_image(product_id, data_product[1]))
                ij_data.append({product_id: data_product[1]})
                # print('ij_data-13,4', len(ij_data), ij_data[-1])
                picture_id = make_query_get_id(connection, add_pictures,
                                               [product_id, data_product[1][0]])  # cursor.lastrowid
                proxy_data = [picture_id, product_id]
                makery(connection, 'add_product_picture', proxy_data)
                # print('ij_data-53,7', len(ij_data))
                data_options = params_optwheels(data_product[2], product_id)
                for option in data_options:
                    makery(connection, 'add_options', option)

            elif is_exist[0]:
                # category_id = categories_wheels[data_product[0][7]]
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    # print(is_exist[1], is_exist[2], 'quantity12 -', quantity, data_product[0][3])
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    makery(connection, 'update', new_data)
                    # print('Is_exist_product {} in_stock {}, price {}, income_data from {} -in_stock {}, price {}'
                    #       .format(product_code, is_exist[1], is_exist[2], provider, quantity, price_for_site))
                elif quantity < 4 and is_exist[1] != quantity:
                    # print(is_exist[1], 'quantity13 -', quantity)
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    makery(connection, 'update', new_data)
                    del standart_copy[key]
                    # print('len7777', len(standart_copy))
                    # print(key, data_product)

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                    # ij_data.append(prepare_get_image(product_id, data_product[1]))
                    ij_data.append({product_id: data_product[1]})
                    # print('ij_data-12', len(ij_data), ij_data[-1])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data_product[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    makery(connection, 'add_product_picture', proxy_data)
                    # print('ij_data-12-12', len(ij_data))

                    data_options_tyres = params_optyres(data_product[2], product_id)
                    for option in data_options_tyres:
                        makery(connection, 'add_options', option)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        # print(is_exist[1], is_exist[2], 'before_quantity22',
                        #       category_id, product_code, ' -now', quantity, data_product[0][3])
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        makery(connection, 'update', new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        makery(connection, 'update', new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                # write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                # write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

        # except KeyError as e:
        #     write("Something went wrong Error22: {}".format(e))
        #     proxy.append(str(e))
        #     write(str(data_product) + str(set(proxy)))
        #     print('PROXY_key_wrong_22', set(proxy))
        #     print("Something went wrong KeyError22: {}".format(e))
        #     print(str(data_product))
        #     count += 1
        #     continue

    # print(data_product[:5], sep='\n')

    connection.close()
    rewrite_pictures_data(ij_data)
    print('For_write_pictures_data', len(ij_data))
    # write('from_check_and_write errors ' +  str(count))
    print('from_check_and_write_2_errors', count)
    # dowload_images()

    return standart_copy


def check_and_write_v4():
    data_from = get_new_pages_v2()
    standart = standart_product_v2(data_from)
    standart_copy = standart.copy()
    ij_data, proxy = [], []
    count = 0
    for key, data_product in standart.items():
        # try:
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id_v2(add_product, data_product[0])
                ij_data.append({product_id: data_product[1]})
                picture_id = make_query_get_id_v2(add_pictures,
                                                  [product_id, data_product[1][0]])
                proxy_data = [picture_id, product_id]
                make_query_v2(add_product_picture, proxy_data)
                data_options = params_optwheels(data_product[2], product_id)
                # for option in data_options:
                #     make_query_v2(add_options, option)
                make_query_many_v2(add_options, data_options)

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                elif quantity < 4 and is_exist[1] != quantity:
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                    del standart_copy[key]

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id_v2(add_product, data_product[0])
                    ij_data.append({product_id: data_product[1]})
                    picture_id = make_query_get_id_v2(add_pictures,
                                                      [product_id, data_product[1][0]])
                    proxy_data = [picture_id, product_id]
                    make_query_v2(add_product_picture, proxy_data)

                    data_options_tyres = params_optyres(data_product[2], product_id)
                    # for option in data_options_tyres:
                    #     make_query_v2(add_options, option)
                    make_query_many_v2(add_options, data_options_tyres)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                # write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                # write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

    rewrite_pictures_data(ij_data)
    print('For_write_pictures_data', len(ij_data))
    print('from_check_and_write_4_errors', count)
    # dowload_images()

    return standart_copy


def check_write_json(data_from_json):
    rewrite_standart_data(data_from_json)
    ij_data, proxy = [], []
    count = 0
    connection = create_connection()
    for key, data_product in data_from_json.items():
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                ij_data.append({product_id: data_product[1]})
                picture_id = make_query_get_id(connection, add_pictures,
                                               [product_id, data_product[1][0]])  # cursor.lastrowid
                proxy_data = [picture_id, product_id]
                makery(connection, 'add_product_picture', proxy_data)
                data_options = params_optwheels(data_product[2], product_id)
                for option in data_options:
                    makery(connection, 'add_options', option)

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    makery(connection, 'update', new_data)
                    # print('Is_exist_product {} in_stock {}, price {}, income_data from {} -in_stock {}, price {}'
                    #       .format(product_code, is_exist[1], is_exist[2], provider, quantity, price_for_site))
                elif quantity < 4 and is_exist[1] != quantity:
                    # print(is_exist[1], 'quantity13 -', quantity)
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    makery(connection, 'update', new_data)

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                    ij_data.append({product_id: data_product[1]})
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data_product[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    makery(connection, 'add_product_picture', proxy_data)
                    data_options_tyres = params_optyres(data_product[2], product_id)
                    for option in data_options_tyres:
                        makery(connection, 'add_options', option)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        makery(connection, 'update', new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        makery(connection, 'update', new_data)

            except mysql.connector.Error as err:
                # write("S_thing went wrong connector tyres: {}".format(err))
                # write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                # write("S_thing went wrong KeyError tyres---: {}".format(e))
                #                 # write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

        # except KeyError as e:
        #     write("Something went wrong KeyError2: {}".format(e))
        #     proxy.append(str(e))
        #     write(str(data_product) + str(set(proxy)))
        #     print('PROXY_key_wrong_2', set(proxy))
        #     print("Something went wrong KeyError2: {}".format(e))
        #     print(8765, str(data_product))
        #     count += 1
        #     continue
    # print(data_product[:5], sep='\n')

    connection.close()
    rewrite_pictures_data(ij_data)
    print('write_pictures_link_2', len(ij_data))
    # write('from_check_and_write errors ' +  str(count))
    print('from_check_and_write_errors_json', count)


def check_write_json_v4(data_from_json):
    rewrite_standart_data(data_from_json)
    ij_data, proxy = [], []
    count = 0
    for key, data_product in data_from_json.items():
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id_v2(add_product, data_product[0])
                ij_data.append({product_id: data_product[1]})
                picture_id = make_query_get_id_v2(add_pictures,
                                                  [product_id, data_product[1][0]])
                proxy_data = [picture_id, product_id]
                make_query_v2(add_product_picture, proxy_data)
                data_options = params_optwheels(data_product[2], product_id)
                # for option in data_options:
                #     make_query_v2(add_options, option)
                make_query_many_v2(add_options, data_options)

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                elif quantity < 4 and is_exist[1] != quantity:
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id_v2(add_product, data_product[0])
                    ij_data.append({product_id: data_product[1]})
                    picture_id = make_query_get_id_v2(add_pictures,
                                                      [product_id, data_product[1][0]])
                    proxy_data = [picture_id, product_id]
                    make_query_v2(add_product_picture, proxy_data)
                    data_options_tyres = params_optyres(data_product[2], product_id)
                    # for option in data_options_tyres:
                    #     make_query_v2(add_options, option)
                    make_query_many_v2(add_options, data_options_tyres)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)

            except mysql.connector.Error as err:
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

    rewrite_pictures_data(ij_data)
    print('write_pictures_link_4', len(ij_data))
    print('from_check_and_write_v4_errors_json', count)


def get_smth_please():
    # params = {'product_id': product_id}
    url = get_smth_url
    # url = 'http://localhost:7770/get/smth'
    response = requests.post(url)
    data = response.json()

    return data


create_query(create_new_product)