from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from main import get_wheels

def is_in_stocks():
    pass

#create data wheels
def product(dictionary):
    # categoryID, price, in_stock, enabled, default_picture, params = 0, 0, 0, 0, 0, 0
    # name, product_code, description = '', '', ''
    # koeff = 1
    # meta_h1 = ' '
    #for param in dictionary:
    for _ in dictionary:
        categoryID = dictionary['category']
        name = dictionary['name']
        description = dictionary['description'][:-145]
        vendor = dictionary['vendor']
        price = dictionary['price']['b2b'] * 1.18
        price = round(price, 0)
        # if dictionary['stocks'] is True:
        #     in_stock = dictionary['stocks']['quantity']
        #     if in_stock.isdigit():
        #         in_stock = int(in_stock)
        #     elif in_stock.isalnum():
        #         in_stock = int(in_stock[1:])
        #     else:
        #         in_stock = 1
        in_stock = 1
        enabled = 1
        # if in_stock >= 4:
        #     enabled = 1
        # else:
        #     enabled = 0
        product_code = dictionary['vendorCode']
        default_picture = dictionary['picture']
        if default_picture[-2:] == '0.':
            default_picture = 88888888
        else:
            default_picture = 88888888
        koeff = 1
        meta_h1 = ' '
        params = 0

        result = [categoryID, name, description, price, in_stock, enabled, product_code, default_picture, params,
                  koeff, meta_h1]

    return result


#create dictonary options wheels from
def params_data(dict_param):
    our_data = {}
    for i in range(len(dict_param['params']) - 1):
        name = dict_param['params'][i]['name']
        value = dict_param['params'][i]['value']
        our_data[name] = value
    #print(our_data)
    return our_data


# Insert  options product information # приведение прилетающих данных к виду на сайте
def params_options(dictionary):
    data_options = []
    for _ in dictionary:
        # width_tyres = params_data(data_product)  # 14 #tyres only
        # h_profil = params_data(data_product)  # 15 #tyres only
        if dictionary.get('ET') is not None:
            diametr = dictionary["D (размер обода)"].replace('x', 'R')  # 16
            bolts = dictionary["PCD"]  # 17,
            et = dictionary["ET"]  # 18
            hole = dictionary['DIA'].replace('d-', 'D')  # 19
            width_wheel = dictionary['LZ (ширина обода)']  # 20
        else:
            diametr = dictionary["D (размер обода)"].replace('x', 'R')  # 16
            bolts = dictionary["PCD"]  # 17,
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
        # for option in data_options:
        #     cursor.execute(add_options, option)
        result = data_options

        return result


cnx = mysql.connector.connect(user='root', database='db1000koles', password='12345678', host='localhost')
cursor = cnx.cursor(buffered=True)


#current structure db for wheels
add_product = ("INSERT INTO avl_products "
               "(categoryID, name, description, Price, in_stock, enabled, product_code, default_picture, params, koeff, meta_h1) "  #params
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
get_prod_id = ("LAST_INSERT_ID()")#("SELECT MAX('productID') FROM avl_products")
add_options = ("INSERT INTO avl_product_options_values (optionID, productID, option_value)"
              "VALUES (%s, %s, %s)")
              #"VALUES (%(diametr)s, %(bolts)s,  %(et)s, %(hole)s,  %(width_wheel)s")


# можно ли это сократить?
data_from = get_wheels()  #Получаем данные с сайта в видет списка словарей
print('data_from - ', len(data_from))
print('data_from[0] - ', len(data_from[0]))
print('data_from[0]["category"] - ', type(data_from[0]['category']))

for data_product in data_from:
    category = data_product["category"]
    if category in [1, 4, 5, 7]:
        try:
            data = product(data_product)
            #print('data - ', data)
            cursor.execute(add_product, data)
            product_id = cursor.lastrowid
            #print('product_id - ', product_id)
            dict_options = params_data(data_product)
            #print(dict_options)
            data_options = params_options(dict_options)

            for option in data_options:
                cursor.execute(add_options, option)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            print('data_product - ', data_product)
            continue
        except KeyError as e:
            print("Something went wrong: {}".format(e))
            print('data_product - ', data_product, 'data_options -' ,data_options)
            continue

    else:
        print('pass', category)
        continue

#print(data_product[:5], sep='\n')


# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()