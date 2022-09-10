from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
#from mysql import connector

#for test
data_product = {
    "name":"КиК Секунда (КС222) 6,5x15 5/139,7 ET40 d-98,5 ауди (Арт.A0408)",
    "currency":"rur",
    "category":5,
    "vendor":"КиК",
    "vendorCode": "00000952",
    "picture": "https://b2b.kolrad.ru/dbpics/0.",
    "sale":False,
    "discounted":False,
    "params":
    [
            {
        "name": "D (размер обода)",
        "value": "x15"
        },
            {
        "name": "Цвет для поиска",
        "value": "Серебристый тёмный"
        },
            {
        "name": "Модель",
        "value": "Секунда (КС222)"
        },
            {
        "name": "Цвет",
        "value": "ауди"
        },
            {
        "name": "DIA",
        "value": "d-98,5"
        },
            {
        "name": "ET",
        "value": "ET40"
        },
            {
        "name": "LZ (ширина обода)",
        "value": "6,5"
        },
            {
        "name": "PCD",
        "value": "5/139,7"
        },
            {}
    ],
    "price" :
    {
    "rrc":1212.00,
    "regular":0.00,
    "b2b":1212.00    },
    "stocks":
    [
            {}
    ],

    "description":"<p>\u041e\u041e\u041e &laquo;\u041a\u0438\u041a&raquo; - \u0441\u0430\u043c\u044b\u0439 \u043a\u0440\u0443\u043f\u043d\u044b\u0439 \u0432 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u043e\u0434\u0438\u043d \u0438\u0437 \u0432\u0435\u0434\u0443\u0449\u0438\u0445 \u0432 \u043c\u0438\u0440\u0435 \u0437\u0430\u0432\u043e\u0434\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0443 \u043b\u0435\u0433\u043a\u043e\u0441\u043f\u043b\u0430\u0432\u043d\u044b\u0445 \u043a\u043e\u043b\u0435\u0441\u043d\u044b\u0445 \u0434\u0438\u0441\u043a\u043e\u0432 \u043f\u043e \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 \u043b\u0438\u0442\u044c\u044f \u043f\u043e\u0434 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435\u043c. 25-\u043b\u0435\u0442\u043d\u0438\u0439 \u043e\u043f\u044b\u0442 \u0440\u0430\u0431\u043e\u0442\u044b, \u0432\u044b\u0441\u043e\u043a\u043e\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u043d\u043e\u0435 \u043e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u0438 \u0433\u0438\u0431\u043a\u043e\u0441\u0442\u044c \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0440\u0435\u0448\u0435\u043d\u0438\u0439 \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u044e\u0442 \u043d\u0430\u043c \u0431\u044b\u0442\u044c \u043b\u0438\u0434\u0435\u0440\u043e\u043c \u043e\u0442\u0440\u0430\u0441\u043b\u0438 \u0438 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u044c \u043b\u0438\u0442\u044b\u0435 \u0434\u0438\u0441\u043a\u0438 \u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u043e \u0432\u044b\u0441\u043e\u043a\u043e\u0433\u043e \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430.\u041b\u0438\u0442\u044b\u0435 \u0434\u0438\u0441\u043a\u0438 \u043e\u0442 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438 &laquo;\u041a\u0438\u041a&raquo; \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u043f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u043d\u044b \u0432 \u0420\u043e\u0441\u0441\u0438\u0438. \u041c\u044b &ndash; \u0435\u0434\u0438\u043d\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c \u043a\u043e\u043b\u0435\u0441\u043d\u044b\u0445 \u0434\u0438\u0441\u043a\u043e\u0432, \u043f\u0440\u0435\u0434\u043e\u0441\u0442\u0430\u0432\u043b\u044f\u044e\u0449\u0438\u0439 \u043f\u043e\u0436\u0438\u0437\u043d\u0435\u043d\u043d\u0443\u044e \u0433\u0430\u0440\u0430\u043d\u0442\u0438\u044e \u043d\u0430 \u043c\u0435\u0442\u0430\u043b\u043b \u0438 \u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u044e \u043a\u043e\u043b\u0435\u0441\u0430.<\/p><p>\u0421\u0430\u0439\u0442 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f&nbsp; &nbsp;<a href=&apos;https:\/\/kolesa-kik.ru\/&apos;>https:\/\/kolesa-kik.ru\/<\/a><\/p><p>\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0442\u043e\u0440&nbsp; <a href=&apos;https:\/\/kolesa-kik.ru\/ru\/configurator\/&apos;>https:\/\/kolesa-kik.ru\/ru\/configurator\/<\/a><\/p>"

    }


#create data wheels
def product_data(dictionary):
    #product = ()
    for i in range(len(dictionary) - 1):
        name = dictionary['name']
        categoryID = dictionary['category']
        description = dictionary['description']
        vendor = dictionary['vendor']
        price = dictionary['price']['b2b'] * 1.18
        price = round(price, 0)
        in_stock = 0#dictionary['stocks'][0]
        if dictionary['stocks'] is True:
            in_stock = dictionary['stocks']['quantity']
            if in_stock.isdigit():
                in_stock = int(in_stock)
            elif in_stock.isalnum():
                in_stock = int(in_stock[1:])
            else:
                in_stock = 1
        enabled = 0
        if in_stock >= 4:
            enabled = 1
        product_code = dictionary['vendorCode']
        default_picture = dictionary['picture']
        if default_picture[-2:] == '0.':
            default_picture = 88888888
        else:
            default_picture = 88888888
        params = 0
        koeff = 1
        meta_h1 = ' '
        result = [categoryID, name, description, price, in_stock, enabled, product_code, default_picture, params, koeff, meta_h1]
    return result

print(product_data(data_product))

#create dictonary options wheels
def params_data(dictionary):
    our_data = {}
    for i in range(len(dictionary['params']) - 1):
        name = dictionary['params'][i]['name']
        value = dictionary['params'][i]['value']
        our_data[name] = value
    return our_data


cnx = mysql.connector.connect(user='root', database='db1000koles', password='12345678', host='localhost')
cursor = cnx.cursor(buffered=True)


#tomorrow = datetime.now().date() + timedelta(days=1)

#current structure db for wheels
add_product = ("INSERT INTO avl_products "
               "(productID, categoryID, name, description, Price, in_stock, enabled, product_code, default_picture, params, koeff, meta_h1) "  #params
               "VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
get_prod_id = ("LAST_INSERT_ID()")#("SELECT MAX('productID') FROM avl_products")
add_options = ("INSERT INTO avl_product_options_values (optionID, productID, option_value)"
              "VALUES (%s, %s, %s)")
              #"VALUES (%(diametr)s, %(bolts)s,  %(et)s, %(hole)s,  %(width_wheel)s")


# cursor.execute(add_options, data_option) #work
data = product_data(data_product)
cursor.execute(add_product, data)
#global product_id
product_id = cursor.lastrowid


# Insert options product information
for i in params_data(data_product):
    # приведение прилетающих данных к виду на сайте
    # data_for_options ?= data_option = (diametr, bolts, et, hole, width_wheel)
    # width_tyres = params_data(data_product)  # 14 #tyres only
    # h_profil = params_data(data_product)  # 15 #tyres only
    diametr = params_data(data_product)["D (размер обода)"].replace('x', 'R')  # 16
    bolts = params_data(data_product)["PCD"]  # 17,
    et = params_data(data_product)["ET"]  # 18
    hole = params_data(data_product)['DIA'].replace('d-', 'D')  # 19
    width_wheel = params_data(data_product)['LZ (ширина обода)']  # 20
    data_options = []
    #('14'=>'Ширина шины','15'=>'Профиль','16'=>'Диаметр','17'=>'Крепеж','18'=>'Вылет', '19'=>'Центральное отверстие','20'=>'Ширина диска')
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
print(data_options)

for option in data_options:
    cursor.execute(add_options, option)
    # cnx.commit()

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()