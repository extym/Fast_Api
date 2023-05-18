import json
from copy_connect import check_and_write, check_write_json
import requests
import random
import string


# #data = json.loads('https://b2b.4tochki.ru/export_data/M28420.json')  #'http://super-good.ml/test_json.json')
from categories import categories_summer, categories_wheels, categories_winter, categories_allseason

magic_link_json = 'https://b2b.4tochki.ru/export_data/M28420.json'
##WORK
r = requests.get(magic_link_json)
data = r.json()

wheels = data['rims']
tires = data['tires']
# print('wheels', len(wheels))
# print('tires', len(tires))
# print(wheels[0])
# print(tires[-1])


def count(row):  #dictionary
    in_stock = 0
    if row.get('rest_yamka') is not None and isinstance(row.get('rest_yamka'), int):
        in_stock += row['rest_yamka']
    elif row.get('rest_yamka') is not None and 'более ' in row.get('rest_yamka'):
        # row['rest_yamka'].replace('более ', '')
        in_stock += int(row['rest_yamka'].replace('более ', ''))

    if row.get('rest_mkrs') is not None  and isinstance(row.get('rest_mkrs'), int):
        in_stock += row['rest_mkrs']
    elif row.get('rest_mkrs') is not None and 'более ' in row.get('rest_mkrs'):
        cnt = row['rest_mkrs'].replace('более ', '')
        in_stock += int(cnt)

    return in_stock


def get_price(product):
    price = 0
    if product.get('price_yamka') is not None and isinstance(product.get('price_yamka'), int):
        price = product['price_yamka'] * 1.18 - 400
    elif product.get('price_mkrs') is not None and isinstance(product.get('price_mkrs'), int):
        price = product['price_mkrs'] * 1.18 - 400
    price = round(price, 0)

    return price


def get_price_tires(product):
    pre_price = 0
    if product.get('price_yamka') is not None and isinstance(product.get('price_yamka'), int):
        pre_price = product['price_yamka']
    elif product.get('price_mkrs') is not None and isinstance(product.get('price_mkrs'), int):
        pre_price = product['price_mkrs']

    if product.get('diameter').replace('R', '')\
            .replace('C', '').replace('Z', '') >= '17':
        price = pre_price * 1.10
    else:
        price = pre_price * 1.12

    price = round(price, 0)

    return price

def id_generator(size=8, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def wheels_from_json(wheels):
    diction = []
    for prod in wheels:
        in_stock = count(prod)
        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        name = prod['name']
        vendor = prod['brand']
        description = vendor + ' ' + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            break
        # check category wheels and tyres
        category_id = prod.get('category_id')
        if category_id is None:
            category_id = categories_wheels[vendor]

        price = get_price(prod)

        product_code = prod['cae']
        image_url = prod.get('img_big_my')
        name_picture = id_generator() + '.png'
        image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1
        category = 5
        options = {
            'et': prod.get('et'),
            "bolts_spacing": prod.get('bolts_spacing'),
            'diameter': prod.get('diameter'),
            'dia': prod.get('dia'),
            'width': prod.get('width')
        }

        result = [category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1, category], image_tuple, options
        diction.append(result)

    #print(diction)
    return diction


def tires_from_json(tyres):
    diction = []
    for prod in tyres:
        #print('tires_from_json', prod)
        in_stock = count(prod)
        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        name = prod['name']
        vendor = prod['brand']
        description = vendor + ' ' + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            continue  #break
        # check category wheels and tyres
        category_id = prod.get('category_id')
        if category_id is None and prod.get('season') == 'Летняя':
            category_id = categories_summer[vendor]
        elif category_id is None and prod.get('season') == 'Зимняя':
            category_id = categories_winter[vendor]
        elif vendor in categories_summer.keys():
            category_id = categories_summer[vendor]
        else:
            category_id = 3000
        price = get_price_tires(prod)
        category = 12
        product_code = prod['cae']
        image_url = prod.get('img_big_my')
        name_picture = id_generator() + '.png'
        image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1
        options = {
            'diameter': prod.get('diameter'),
            'width': prod.get('width'),
            'profile': prod.get('height')
        }

        result = ([category_id, name, description, price, in_stock, enabled,
                   product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1, category], image_tuple, options)
        diction.append(result)

    # print('tires_from_json', diction)
    return diction

wwwheels = wheels_from_json(wheels)
tttires = tires_from_json(tires)
check_write_json(tttires)
check_write_json(wwwheels)