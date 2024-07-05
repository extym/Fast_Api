import json
import sys

# from connect import check_write_json_v4
import requests
import random
import string
import project.conn as conn

# #data = json.loads('http://super-good.ml/test_json.json')
# from categories import *


def get_data_from_json(link_json):
    r = requests.get(link_json)
    data = r.json()

    wheels = data['rims']
    tires = data['tires']

    return wheels, tires



def count(row):  # dictionary
    in_stock = 0
    if row.get('rest_yamka') is not None and isinstance(row.get('rest_yamka'), int):
        in_stock += row['rest_yamka']
    elif row.get('rest_yamka') is not None and 'более ' in row.get('rest_yamka'):
        # row['rest_yamka'].replace('более ', '')
        in_stock += int(row['rest_yamka'].replace('более ', ''))

    if row.get('rest_mkrs') is not None and isinstance(row.get('rest_mkrs'), int):
        in_stock += row['rest_mkrs']
    elif row.get('rest_mkrs') is not None and 'более ' in row.get('rest_mkrs'):
        cnt = row['rest_mkrs'].replace('более ', '')
        in_stock += int(cnt)

    return in_stock


def count_2(row):  # dictionary
    in_stock = 0
    if row.get('rest_yamka') and isinstance(row.get('rest_yamka'), int):
        in_stock += row['rest_yamka']
    elif row.get('rest_yamka') and 'более ' in row.get('rest_yamka'):
        in_stock += int(row['rest_yamka'].replace('более ', ''))

    if row.get('rest_mkrs') and isinstance(row.get('rest_mkrs'), int):
        in_stock += row['rest_mkrs']
    elif row.get('rest_mkrs') and 'более ' in row.get('rest_mkrs'):
        in_stock += int(row['rest_mkrs'].replace('более ', ''))

    return in_stock


def get_price(product):
    price, price_opt = 0, 0
    rule = False
    if product.get('price_yamka_rozn') is not None and isinstance(product.get('price_yamka_rozn'), int):
        price = product['price_yamka_rozn']
    elif product.get('price') is not None and isinstance(product.get('price'), int):
        price = product['price']
    price = round(float(price), 2)

    if product.get('price_yamka') is not None and isinstance(product.get('price_yamka'), int):
        price_opt = product['price_yamka']
    elif product.get('price_mkrs') is not None and isinstance(product.get('price_mkrs'), int):
        price_opt = product['price_mkrs']
    price_opt = round(price_opt, 0)

    if price / 1.18 >= price_opt:
        rule = True

    return price, rule, price_opt


def get_price_tires(product):
    pre_price = 0
    if product.get('price_yamka') is not None and isinstance(product.get('price_yamka'), int):
        pre_price = product['price_yamka']
    elif product.get('price_mkrs') is not None and isinstance(product.get('price_mkrs'), int):
        pre_price = product['price_mkrs']

    if product.get('diameter').replace('R', '') \
            .replace('C', '').replace('Z', '') >= '17':
        price = pre_price * 1.10
    else:
        price = pre_price * 1.12

    opt_price = round(pre_price, 0)

    return opt_price, price


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def standart_wheels_from_json(shop_name=None,
                            name_price=None):
    link_downloads = conn.get_distibutor_price_data('4tochki', 'json', 'wheels_tires')
    wheels = get_data_from_json(link_downloads)[0]
    diction, proxy = {}, []
    for prod in wheels:
        try:
            in_stock = count(prod)
            if in_stock >= 4:
                enabled = 1
            else:
                enabled = 0
            name = prod['name']
            vendor = prod['brand']
            description = prod.get("rim_type") + ' диск ' + vendor + name
            if vendor == 'Carwel':
                description = name
            elif vendor == '':
                break
            # check category wheels and tyres
            # category_id = categories_wheels.get(vendor, categories_wheels_upper.get(vendor.upper()))
            # if not category_id:
            #     category_id = cats_wheels_upper.get(vendor.upper(), 4000)
            #     print(444000, prod)
            category_id = prod.get("rim_type")
            price_data = get_price(prod)
            price = price_data[0]
            rule = price_data[1]
            price_opt = price_data[2]
            name_picture = '77777777'
            product_code = prod['cae']
            image_url = prod.get('img_big_my')
            if image_url:
                name_picture = vendor.replace(' ', '') + '_' + product_code + '.png'
            image_tuple = (name_picture, image_url)
            koeff = 1
            meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            params = 1
            provider = '4tochki'
            category = 5
            options = {
                'et': 'ET' + str(prod.get('et')).replace('.', ','),  # 18
                "bolts_spacing": str(prod.get('bolts_count'))  # 17
                                 + '/' +
                                 str(prod.get('bolts_spacing'))
                                 .replace('.', ','),
                'diameter': str(prod.get('diameter')),
                'dia': 'D' + str(prod.get('dia')).replace('.', ','),
                'width': str(prod.get('width')).replace('.', ',')
            }

            diction.update({vendor.strip() + product_code:
                (
                    [
                        category_id, name, description, price, in_stock,
                        enabled, product_code, vendor, meta_d, meta_k,
                        params, koeff, meta_h1, provider, category
                    ],
                    image_tuple,
                    options,
                    rule,
                    price_opt
                )})

        except Exception as error:
            print('Some fuckup_standart_wheels_from_json {} {}'
                  .format(error, prod))
            continue

    print("ALL_RIDE_get_wheels_json {}".format(len(diction.keys())))

    return diction


def standart_addons_from_json(without_db=True, data=None):
    if not data:
        data = get_data_from_json()[0]
    diction, proxy = {}, []
    for prod in data:
        # try:
        in_stock = count(prod)
        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        name = prod['name']
        vendor = prod['brand']
        description = name  # prod.get("rim_type") + ' диск ' + vendor + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            break
        # check category wheels and tyres
        category_id = 4
        price_data = get_price(prod)
        price = price_data[0]
        rule = price_data[1]
        price_opt = price_data[2]
        name_picture = '77777777'
        product_code = prod['cae']
        image_url = prod.get('img_big_my')
        if image_url:
            name_picture = vendor.replace(' ', '') + '_' + product_code + '.png'
        image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1
        provider = '4tochki'
        category = 5

        options = {}

        diction = (
            [
                category_id, name, description, price, in_stock,
                enabled, product_code, vendor, meta_d, meta_k,
                params, koeff, meta_h1, provider, category
            ],
            image_tuple,
            options,
            rule,
            price_opt
        )

    return diction


# print(standart_addons_from_json(without_db=True, data=ventil_LS))


def standart_tires_from_json(name_price=None):
    type_data = 'wheels_tires'
    provider = '4tochki'
    price_type = 'json'
    # TODO make provider&price
    get_distibutor_data = conn.get_distibutor_price_data(provider,
                                                   price_type,
                                                   name_price)
    price_murkup = get_distibutor_data[1]
    link = get_distibutor_data[0]
    tyres = get_data_from_json(link)[1]
    diction = {}
    for prod in tyres:
        in_stock = count(prod)
        name = prod['name']
        vendor = prod['brand']
        description = vendor + ' ' + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            continue  # break
        opt_price = get_price_tires(prod)[0]
        category = prod.get('season')
        tiretype = prod.get('tiretype')
        category_id = 12
        rule = False
        product_code = prod['cae']
        name_picture = '88888888'
        image_url = prod.get('img_big_my')
        if image_url:
            name_picture = vendor.strip() + '_' + product_code + '.png'
        image_tuple = (name_picture, image_url)
        articul_product = vendor.strip() + '_' + product_code
        id_1c = ''
        provider = '4tochki'
        options = {
            'diameter': prod.get('diameter'),
            'width': prod.get('width'),
            'profile': prod.get('height')
        }

        diction.update({vendor.strip() + product_code:
            (
                (category_id, name, description,
                 opt_price, in_stock,
                 product_code, vendor, category,
                 articul_product, id_1c, image_url,
                 price_murkup),
                image_tuple,
                options,
                provider
            )})

    return diction

