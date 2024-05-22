import json
import string
import sys
import random
from cred import DATA_PATH, magic_link_csv, magic_link_csv2
import wget
import csv
import datetime
from connect import check_write_json, check_write_json_v4
from categories import *
from urllib.request import urlretrieve
import urllib3
urllib3.disable_warnings()

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


tn = datetime.datetime.now()
ts = datetime.datetime.timestamp(tn) * 1000
date = str(ts)[:13]
type_data = ['wheels', 'tyres']
url2 = magic_link_csv + date
url = magic_link_csv2 + date

# print(url, url2)
# sys.exit()

# try:
#     result = wget.download(url, out=DATA_PATH + '/proxy_wheels.csv')
#     result2 = wget.download(url2, out=DATA_PATH + '/proxy_tyres.csv')
# except:
#     print('Fuck_up download csv')

name = ['sku', 'title', 'brand_sku', 'gtin', 'season', 'brand', 'model', 'diameter', 'width', 'profile', 'load_index',
        'speed_index', 'pins', 'runflat', 'homologation', 'production_year', 'sale', 'price', 'price_retail',
        'price_msrp', 'photo_url', 'amount_total', 'amount_local', 'amount shopId 7', 'amount shopId 12',
        'amount shopId 13', 'amount shopId 14', 'amount shopId 17', 'amount shopId 20', 'amount shopId 21',
        'amount shopId 22', 'amount shopId 23', 'amount shopId 25', 'amount shopId 33', 'amount shopId 36',
        'amount shopId 667', 'amount shopId 714', 'amount shopId 718', 'amount shopId 3012']

listt = ['1251539', 'Headway 225/40 R18 SNOW-UHP HW508 92H', '3PN02254018E000002', '06930213605119', 'W', 'Headway',
         'SNOW-UHP HW508', 'R18', '225', '40', '92', 'H', 'N', 'N', '', '', 'N', '5389', '6420', '6420',
         'https://www.shinservice.ru/catalog/headway/uhp-5081.jpg', '20', '19', '0', '0', '0', '4', '0', '2', '4', '4',
         '4', '4', '0', '4', '4', '0', '8', '4', '4', '8', '0', '4', '0', '4', '4', '4', '4', '0', '4', '0', '4', '4',
         '4', '4', '0', '4', '0', '0']


# print('index', listt.index('5389'))


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def get_data_csv():
    proxy = []
    try:
        # result2 = wget.download(url2, out=DATA_PATH + '/proxy_tyres.csv')
        # with open(DATA_PATH + '/proxy_tyres (1).csv', 'r') as file:
        path2, data = urlretrieve(url2)
        with open(path2, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                proxy.append(row)
        print(' get_data_csv_tyres ', '-------- ', len(proxy))
    except:
        print('Fuck_up download tyres csv')

    return proxy



def get_data_wheels_csv():
    proxy = []
    try:
        # result = wget.download(url, out=DATA_PATH + '/proxy_wheels.csv')
        # with open(DATA_PATH + '/proxy_wheels (1).csv', 'r') as file:

        path, data = urlretrieve(url)
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                proxy.append(row)
        print('get_data_wheels_csv ', '-------- ', len(proxy))
    except:
        print('Fuck_up download wheels csv')

    return proxy



# get_data_wheels_csv()


def count_price(string, size):
    if string.isdigit():
        if size[1:].isdigit() and int(size[1:]) <= 16:
            price = int(string) * 1.12  # result float
        elif size[1:].isdigit() and int(size[1:]) >= 17:
            price = int(string) * 1.10
        else:
            price = int(string) * 1.10

        price = round(price, 0)

        return price


# /usr/local/bin/fuck_debian/tyres_wheels/
def standart_tyres_csv():
    proxy_data, proxy = [], []
    global_result = {}
    data = get_data_csv()
    for i in range(1, len(data)):
        try:
            if data[i][1] == 'title':
                continue
            else:
                in_stock = int(data[i][22])
                if in_stock >= 4:
                    enabled = 1
                else:
                    enabled = 0
                name = data[i][1]
                vendor = data[i][5]
                if vendor == 'Carwel':
                    description = name
                elif vendor == '':
                    continue
                else:
                    description = data[i][1]
                category_id = 7000
                if data[i][4] in ['S', 's', 'Летняя']:
                    category_id = cats_summer_upper.get(vendor.upper(), 4000)
                elif data[i][4] in ["W", 'Зимняя']:
                    category_id = cats_winter_upper.get(vendor.upper(), 5000)
                elif data[i][4] in ["allseason", 'Всесезонная']:
                    category_id = cats_allseason_upper.get(vendor.upper(), 6000)
                else:
                    print('1212_category_id', data[i][4])
                category = 12
                rule = False
                # check category wheels and tyres
                product_code = data[i][2]
                size = data[i][7]  # 16 'diameter'
                width = data[i][8]  # 14
                height = data[i][9]  # 15
                sku = data[i][0]
                name_picture = '88888888'
                image_url = data[i][20]  # image_link
                if image_url:
                    # name_picture = 'shins-' + id_generator() + '.png'
                    name_picture = 'shins-' + product_code + '.png'
                image_tuple = (name_picture, image_url)
                price = count_price(data[i][17], size)
                koeff = 1
                meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
                meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
                meta_h1 = ' '
                provider = 'shins'
                params = 1
                options = {
                    'diameter': size,
                    'width': width,
                    'profile': height
                }

                global_result.update({vendor.strip() + product_code:
                    (
                        [category_id, name, description, price,
                         in_stock, enabled, product_code, vendor, meta_d, meta_k,
                         params, koeff, meta_h1, provider, category],
                        image_tuple,
                        options,
                        rule
                    )})
                # result = ([category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                #  params, koeff, meta_h1, category], image_tuple, options)
                # proxy_data.append(result)

        except KeyError as error:
            print("Something went wrong KeyError from getcsv: {}".format(error))
            # write(str(data))
            print(str(data[i]))
            continue

    mem = sys.getsizeof(proxy_data)

    print(mem / 1000, 'Kb--')
    print("ALL_RIDE_get_tyres_csv ()".format(len(global_result)))
    return global_result


def standart_wheels_csv(without_db=False):
    data = get_data_wheels_csv()
    global_result = {}
    for i in range(1, len(data)):
        if data[i][1] == 'title':
            continue
        else:
            try:
                in_stock = int(data[i][17]) + int(data[i][18])
                if in_stock >= 4:
                    enabled = 1
                else:
                    enabled = 0
                name = data[i][1]
                vendor = data[i][3]
                description = name
                category_id = categories_wheels.get(vendor)
                if category_id is None:
                    category_id = cats_wheels_upper.get(vendor.upper(), 4000)
                category = 5
                # check category wheels and tyres
                product_code = data[i][2]
                diameter = data[i][7].split(' / ')[0]  # 16 'diameter'
                width = data[i][7].split(' / ')[1].strip("0").replace('.', ',').strip(',')  # 20
                hole = 'D' + data[i][12].strip("0").replace('.', ',')  # 19
                bolts_spacing = data[i][8] + '/' + \
                                data[i][9].strip("0").replace('.', ',')  # 17
                et = 'ET' + data[i][11].strip("0").replace('.', ',').strip(',')  # 18
                sku = data[i][0]
                name_picture = '777777777'
                image_url = data[i][16]  # image_link
                if image_url:
                    name_picture = 'shins-' + product_code + '.png'
                image_tuple = (name_picture, image_url)
                price_rrc = data[i][15]
                price = float(price_rrc)
                price_opt = data[i][14]
                rule = False
                if int(price_opt) * 1.18 >= int(price_rrc):
                    rule = True
                koeff = 1
                meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
                meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
                meta_h1 = ' '
                params = 1
                provider = 'shins'
                options = {
                    'et': et,  # 18
                    "bolts_spacing": bolts_spacing,  # 17
                    'diameter': diameter,  # 16
                    'dia': hole,  # 19
                    'width': width  # 20
                }
                global_result.update({vendor.strip() + product_code:
                    (
                        [category_id, name, description, price, in_stock,
                         enabled, product_code, vendor, meta_d, meta_k,
                         params, koeff, meta_h1, provider, category],
                        image_tuple,
                        options,
                        rule,
                        price_opt
                    )})
                # result = ([category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                #            params, koeff, meta_h1, category], image_tuple, options)
                # proxy_data.append(result)
            except Exception as er:
                print('fuckup standart getcsv {} {}'.format(er, data[i]))

    if not without_db:
        check_write_json_v4(global_result)
        data = standart_tyres_csv()
        mems = sys.getsizeof(data)
        print('from_csv', mems / 1000, 'Kb')
        check_write_json_v4(data)

    print('ALL_RIDE_get_wheels_csv ', len(global_result))
    return global_result


# data = standart_tyres_csv()
# mems = sys.getsizeof(data)
# print('from_csv', mems / 1000, 'Kb')
# check_write_json(data)

# data = get_data_wheels_csv()
# mems = sys.getsizeof(data)
# print('from_csv_wheels', mems / 1000, 'Kb')
# standart_wheels_csv()
