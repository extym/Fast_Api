from __future__ import print_function

import csv
import datetime
# from pictures import write
import json
import mysql.connector
from main import get_wheels
import requests
from getcsv import get_tyres_csv

# category_summer = {'Tunga': 1753, 'Bridgestone': 1756, 'Toyo': 1764, 'Kumho': 1924, 'Michelin': 1755, 'BFGoodrich': 1162, 'Nokian Tyres': 1754, 'Gislaved': 1985, 'Goodyear': 1154, 'Dunlop': 1228, 'Yokohama': 1757, 'Sava': 1855, 'Continental':1763, 'Maxxis': 1717, 'Hankook': 1748, 'Pirelli': 1156, 'Cordiant': 1719, 'Tigar': 1166, 'Matador': 1161, 'Falken': 1962, 'Кама': 933, 'Viatti': 1857, 'Nitto': 1765, 'Sunfull': 1923, 'Delinte': 1984, 'Laufenn': 1750, 'Aosen': 1983, 'Headway': 1177}
# category_winter = {'Bridgestone': 1723, 'Toyo': 1770, 'Kumho': 1773, 'Michelin': 1976, 'BFGoodrich': 1214, 'Nokian Tyres': 1721, 'Gislaved': 1192, 'Goodyear': 1977, 'Dunlop': 1188, 'Yokohama': 1208, 'Sava': 1772, 'Continental':1210, 'Maxxis': 1776, 'Hankook': 1206, 'Pirelli': 1207, 'Cordiant': 1189, 'Tigar': 1771, 'Matador': 1732, 'Falken': 1978, 'Кама': 509, 'Viatti': 1195, 'Nitto': 1194, 'Sunfull': 1769, 'Delinte': 1980, 'Laufenn': 1913, 'Aosen': 1981, 'Headway': 1982}
# category_allseason = {}

categories = {'Inverno': 1988, 'Jantsa': 1989,  'rFR': 1181, 'RADIUS': 1990, 'ГАЗ': 1991, 'LF Works': 1992,
              'Remain': 1993, 'rtr': 1994, 'BLACK RHINO': 1995, 'BEYERN': 1897, 'REDBOURNE': 1901, 'LUMARAI': 1898,
              'COVENTRY': 1903, 'VICTOR': 1893, 'Accuride': 1972, 'Asterro': 1974, 'Lemmerz/Maxion': 1973,
              'Maxion': 1973, 'Tracston': 1975, 'Alutec': 1736, 'ANTERA': 64, 'ATS': 1081, 'BBS': 1737, 'Borbet': 1738,
              'Carwel': 1969, 'FONDMETAL': 1084, 'iFree': 628, 'KHOMEN': 1968, 'MAK': 1739, 'MANDRUS': 1887,
              'NEO': 1786, 'REPLAY': 1221, 'Tech-Line': 1735, 'Venti': 1718, 'КиК': 1782, 'Евродиск': 62,
              'MOMO': 1785, 'MSW': 1885, 'Neo': 1786, 'OZ': 55, 'Replay': 1221, 'Rial': 1777, 'RST': 1960,
              'Sparco': 1970, 'Tech Line': 1735,'K&K': 1782, 'OE': 1883, 'Скад': 1926, 'TSW': 1083, 'Magnetto': 723,
              'LS': 1139, 'LegeArtis': 1138, 'LegeArtis Concept': 1140, 'Trebl': 532, 'FR replica': 1181,
              'Yamato': 1145, 'N2O': 1720, 'PDW': 1182, 'CrossStreet': 1873, 'Yokatta': 1143, "NZ": 1134, 'Alcasta': 1130,
              'Race Ready' : 1128, 'Arrivo': 1939, 'Antera': 64, 'Next': 1788, 'X-Race': 1874, 'Hayes Lemmerz' : 1884,
              'Aero': 1875, 'Steger': 1879, 'Buffalo': 1882, 'ТЗСК': 1996, 'Harp': 1889, 'Off-Road Wheels': 1997,
              'Khomen Wheels': 1968, 'LS FlowForming': 1139, 'Better': 1986, 'Lizardo': 1987, 'YST': 827, 'LS Forged': 1998}


def write(smth):
    with open('log.txt', 'a') as file:
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
    with open('dict_images.json', "w") as file:
        json.dump(listt, file)


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
            category_id = categories[vendor]
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


def params_optinos_wheels(dictionary, product_id):
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
        print("Query executed successfully from make_query_get_id")
        #connection.close()
    except Exception as e:
        print(f"The error MAKE_QUERY'{e}' occurred")

    cursor.close()
    return lastrow_id


def make_query(connection, query, data_query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query, data_query)
        connection.commit()
        print("Query executed successfully from make_query")
        #connection.close()
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

#cursor = cnx.cursor(buffered=True)

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


def data_products():
    get_wheels()  # Получаем данные с сайта в виде списка словарей
    get_tyres_csv()
    with open('data_product.json', 'r') as file:
        data_product = json.load(file)

    print(datetime.datetime.now(), 'file read')
    return data_product


# def data_product_compare(smth_dict, smth_list):
#     if smth_dict['vendorCode'] != smth_list[2]:
#         result = False
#     elif smth_dict['vendorCode'] == smth_list[2]:
#         quantity = is_in_stocks(smth_dict)
#         if quantity == smth_list[20] and smth_list[3] == smth_dict['price']['rrc'] - 400:
#             result = False
#         elif quantity != smth_list[20] and smth_list[3] != smth_dict['price']['rrc'] - 400:
#
#             result = True
#     return result
#
# def product_compare():
#     '''сравниваем диски разных поставщиков и разные форматы данных'''
#     data = data_products()
#     with open('./proxy_wheels.csv', 'r') as file:
#         reader = csv.reader(file, delimiter='\t')
#         count = 0
#         count2 = 0
#         for row_dict in data:
#             for row in reader:
#                 if row == 0:
#                     print(row)
#                     continue
#                 elif row[3] in categories.keys():  # row_dict['vendorCode']:
#                     data_product_compare(row_dict, row)
#                     count += 1
#                 elif row[3] not in categories.keys():
#                     count += 1
#
#
#         print (count2, 'count_row--', count, type(row), len(row), row)
#
#
# product_compare()

# можно ли это сократить?
# data_from = data_products()
# data_from = get_tyres_csv()

# ij_data = []
# count = 0
# for data_product in data_from:
#     try:
#         category = data_product.get('category')
#         quantity = is_in_stocks(data_product)
#         if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
#             # try:
#             data = product(data_product, quantity)
#             if data is not False:
#                 is_exist = check_is_exist(data[0][6], data[0][0])
#                 if is_exist is None and quantity >= 4:
#                     cursor.execute(add_product, data[0])
#                     product_id = cursor.lastrowid
#                     ij_data.append(prepare_get_image(product_id, data[1]))
#                     # print("pictures -", product_id, data[1][0])
#                     cursor.execute(add_pictures, [product_id, data[1][0]])
#                     picture_id = cursor.lastrowid
#                     proxy_data = [picture_id, product_id]
#                     cursor.execute(add_product_picture, proxy_data)
#                     write_pictures_data(ij_data)
#                     dict_options = params_data(data_product)
#                     data_options = params_options(dict_options)
#                     for option in data_options:
#                         cursor.execute(add_options, option)
#                 elif is_exist is not None:
#                     category_id = categories[data[0][7]]
#                     product_code = data[0][6]
#                     price_for_site = data[0][3]
#                     if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
#                         # print(is_exist[1], is_exist[2], 'quantity2 -', quantity, data[0][3])
#                         enabled = 1
#                         new_data = [quantity, enabled, category_id, product_code, price_for_site]
#                         cursor.execute(update, new_data)
#                     elif quantity <= 4 and is_exist[1] != quantity:
#                         # print(is_exist[1], 'quantity3 -', quantity)
#                         enabled = 0
#                         new_data = [quantity, enabled, category_id, product_code, price_for_site]
#                         cursor.execute(update, new_data)
#
#             # except mysql.connector.Error as err:
#             #     write("Something went wrong connector: {}".format(err))
#             #     write(str(data_product))
#             #     print ("Something went wrong connector: {}".format(err))
#             #     print (str(data_product))
#             #     continue
#             # except KeyError as e:
#             #     write("Something went wrong KeyError: {}".format(e))
#             #     write(str(data_product))
#             #     print ("Something went wrong KeyError: {}".format(e))
#             #     print (str(data_product))
#             #     continue
#
#         elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
#             try:
#                 data = product(data_product, quantity)
#                 print('1111', data[0][6], data[0][3], quantity, data[0][0])
#                 is_exist = check_is_exist(data[0][6], data[0][0])
#                 if is_exist is None and quantity >= 4:
#                     cursor.execute(add_product, data[0])
#                     product_id = cursor.lastrowid
#                     ij_data.append(prepare_get_image(product_id, data[1]))
#                     # print("pictures -", product_id, data[1][0])
#                     cursor.execute(add_pictures, [product_id, data[1][0]])
#                     picture_id = cursor.lastrowid
#                     proxy_data = [picture_id, product_id]
#                     cursor.execute(add_product_picture, proxy_data)
#                     write_pictures_data(ij_data)
#                     #dict_options = params_data(data_product)
#
#                     data_options_tyres = params_options_tyres(data_product)
#                     for option in data_options_tyres:
#                         cursor.execute(add_options, option)
#                 elif is_exist is not None:
#                     category_id = data[0][0]  # because we get data from csv and has category_id
#                     product_code = data[0][6]
#                     price_for_site = data[0][3]
#                     if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
#                         # print(is_exist[1], is_exist[2], 'quantity2 -', quantity, data[0][3])
#                         enabled = 1
#                         new_data = [quantity, enabled, category_id, product_code, price_for_site]
#                         cursor.execute(update, new_data)
#                     elif quantity <= 4 and is_exist[1] != quantity:
#                         # print(is_exist[1], 'quantity3 -', quantity)
#                         enabled = 0
#                         new_data = [quantity, enabled, category_id, product_code, price_for_site]
#                         cursor.execute(update, new_data)
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
#     except KeyError as e:
#         write("Something went wrong KeyError2: {}".format(e))
#         write(str(data_product))
#         # print("Something went wrong KeyError2: {}".format(e))
#         # print(str(data_product))
#         count += 1
#         continue
#
# # print(data_product[:5], sep='\n')
#
# # Make sure data is committed to the database
# cnx.commit()
#
# cursor.close()
# cnx.close()
# # smth get
# print('from_prepare_data', count)


def check_and_write():
    data_from = data_products()
    ij_data = []
    count = 0
    connection = create_connection()
    for data_product in data_from:
        #try:
        category = data_product.get('category')
        quantity = is_in_stocks(data_product)
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            # try:
            data = standart_product(data_product, quantity)
            if data is not False:
                is_exist = check_is_exist(data[0][6], data[0][0])
                if is_exist is None and quantity >= 4:
                    # cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data[0])  # cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data[1]))
                    # print("pictures -", product_id, data[1][0])
                    # cursor.execute(add_pictures, [product_id, data[1][0]])
                    picture_id = make_query_get_id(connection, add_pictures,
                                                   [product_id, data[1][0]])  # cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    # cursor.execute(add_product_picture, proxy_data)
                    make_query(connection, add_product_picture, proxy_data)
                    write_pictures_data(ij_data)
                    dict_options = params_data(data_product)
                    data_options = params_options(dict_options, product_id)
                    for option in data_options:
                        # cursor.execute(add_options, option)
                        make_query(connection, add_options, option)


                elif is_exist is not None:
                    category_id = categories[data[0][7]]
                    product_code = data[0][6]
                    price_for_site = data[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
                        print(is_exist[1], is_exist[2], 'quantity2 -', quantity, data[0][3])
                        enabled = 1
                        new_data = [quantity, enabled, category_id, product_code, price_for_site]
                        make_query(connection, update, new_data)  #cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity3 -', quantity)
                        enabled = 0
                        new_data = [quantity, enabled, category_id, product_code, price_for_site]
                        make_query(update, new_data)  #cursor.execute(update, new_data)


        elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
            try:
                data = standart_product(data_product, quantity)
                print('tires', data[0][6], data[0][3], quantity, data[0][0])
                is_exist = check_is_exist(data[0][6], data[0][0])
                if is_exist is None and quantity >= 4:
                      #cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data[0])  #cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data[1]))
                    # print("pictures -", product_id, data[1][0])
                      #cursor.execute(add_pictures, [product_id, data[1][0]])
                    picture_id = make_query_get_id(connection, add_pictures, [product_id, data[1][0]])  #cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    make_query(connection, add_product_picture, proxy_data)  #cursor.execute(add_product_picture, proxy_data)
                    write_pictures_data(ij_data)
                    # dict_options = params_data(data_product)

                    data_options_tyres = params_options_tyres(data_product, product_id)
                    for option in data_options_tyres:
                        make_query(connection, add_options, option)  #cursor.execute(add_options, option)
                elif is_exist is not None:
                    category_id = data[0][0]  # because we get data from csv and has category_id
                    product_code = data[0][6]
                    price_for_site = data[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data[0][3]]:
                        # print(is_exist[1], is_exist[2], 'quantity2 -', quantity, data[0][3])
                        enabled = 1
                        new_data = [quantity, enabled, category_id, product_code, price_for_site]
                        make_query(connection, update, new_data)  #cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity3 -', quantity)
                        enabled = 0
                        new_data = [quantity, enabled, category_id, product_code, price_for_site]
                        make_query(connection, update, new_data)  #cursor.execute(update, new_data)

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
    print('from_check_and_write errors', count)


def check_write_json(data_from_json):
    ij_data = []
    count = 0
    connection = create_connection()
    for data_product in data_from_json:
        #try:
        category = data_product[0].pop(-1)  #[-1]
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if is_exist is None and quantity >= 4:
                product_id = make_query_get_id(connection, add_product, data_product[0])  # cursor.lastrowid
                ij_data.append(prepare_get_image(product_id, data_product[1]))
                picture_id = make_query_get_id(connection, add_pictures,
                                               [product_id, data_product[1][0]])  # cursor.lastrowid
                proxy_data = [picture_id, product_id]
                # cursor.execute(add_product_picture, proxy_data)
                make_query(connection, add_product_picture, proxy_data)
                write_pictures_data(ij_data)
                # dict_options = params_data(data_product)
                # data_options = params_options(dict_options, product_id)
                data_options = params_optinos_wheels(data_product[2], product_id)
                for option in data_options:
                    # cursor.execute(add_options, option)
                    make_query(connection, add_options, option)

            elif is_exist is not None:
                category_id = categories[data_product[0][7]]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    print(is_exist[1], is_exist[2], 'quantity12 -', quantity, data_product[0][3])
                    enabled = 1
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  #cursor.execute(update, new_data)
                elif quantity <= 4 and is_exist[1] != quantity:
                    print(is_exist[1], 'quantity13 -', quantity)
                    enabled = 0
                    new_data = [quantity, enabled, category_id, price_for_site, product_code]
                    make_query(connection, update, new_data)  #cursor.execute(update, new_data)


        elif category == 12:  # and quantity >= 4: ##category_id = 12  --it is tyres
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if is_exist is None and quantity >= 4:
                      #cursor.execute(add_product, data[0])
                    product_id = make_query_get_id(connection, add_product, data_product[0])  #cursor.lastrowid
                    ij_data.append(prepare_get_image(product_id, data_product[1]))
                    picture_id = make_query_get_id(connection, add_pictures, [product_id, data_product[1][0]])  #cursor.lastrowid
                    proxy_data = [picture_id, product_id]
                    make_query(connection, add_product_picture, proxy_data)  #cursor.execute(add_product_picture, proxy_data)
                    write_pictures_data(ij_data)
                    # dict_options = params_data(data_product)

                    data_options_tyres = params_options_tyres(data_product[2], product_id)
                    for option in data_options_tyres:
                        make_query(connection, add_options, option)  #cursor.execute(add_options, option)
                elif is_exist is not None:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        print(is_exist[1], is_exist[2], 'quantity22 -', quantity, data_product[0][3])
                        enabled = 1
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  #cursor.execute(update, new_data)
                    elif quantity <= 4 and is_exist[1] != quantity:
                        print(is_exist[1], 'quantity23 -', quantity)
                        enabled = 0
                        new_data = [quantity, enabled, category_id, price_for_site, product_code]
                        make_query(connection, update, new_data)  #cursor.execute(update, new_data)

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
    print('from_check_and_write errors', count)