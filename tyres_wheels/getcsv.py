import json
import string
import sys
import random

import wget
import csv
import datetime
from copy_connect import check_write_json
from categories import categories_summer, categories_wheels, categories_winter, categories_allseason


tn = datetime.datetime.now()
ts = datetime.datetime.timestamp(tn) * 1000
date = str(ts)[:13]
type_data = ['wheels', 'tyres']
url2 = 'https://duplo.shinservice.ru/xml/shinservice-b2b-tyres.csv?id=88964843&t=' + date
url = 'https://duplo.shinservice.ru/xml/shinservice-b2b-wheels.csv?id=88964843&t=' + date
#

try:
    result = wget.download(url, out='/usr/local/bin/fuck_debian/tyres_wheels/proxy_wheels.csv')
    result2 = wget.download(url2, out='/usr/local/bin/fuck_debian/tyres_wheels/proxy_tyres.csv')
except:
    result = wget.download(url, out='./proxy_wheels.csv')
    result2 = wget.download(url2, out='./proxy_tyres.csv')

name = ['sku', 'title', 'brand_sku', 'gtin', 'season', 'brand', 'model', 'diameter', 'width', 'profile', 'load_index', 'speed_index', 'pins', 'runflat', 'homologation', 'production_year', 'sale', 'price', 'price_retail', 'price_msrp', 'photo_url', 'amount_total', 'amount_local', 'amount shopId 7', 'amount shopId 12', 'amount shopId 13', 'amount shopId 14', 'amount shopId 17', 'amount shopId 20', 'amount shopId 21', 'amount shopId 22', 'amount shopId 23', 'amount shopId 25', 'amount shopId 33', 'amount shopId 36', 'amount shopId 667', 'amount shopId 714', 'amount shopId 718', 'amount shopId 3012']

listt = ['1251539', 'Headway 225/40 R18 SNOW-UHP HW508 92H', '3PN02254018E000002', '06930213605119', 'W', 'Headway', 'SNOW-UHP HW508', 'R18', '225', '40', '92', 'H', 'N', 'N', '', '', 'N', '5389', '6420', '6420',
'https://www.shinservice.ru/catalog/headway/uhp-5081.jpg', '20', '19', '0', '0', '0', '4', '0', '2', '4', '4', '4', '4', '0', '4', '4', '0', '8', '4', '4', '8', '0', '4', '0', '4', '4', '4', '4', '0', '4', '0', '4', '4', '4', '4', '0', '4', '0', '0']
#print('index', listt.index('5389'))


def id_generator(size=8, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# with open('./proxy_wheels (1).csv', 'r') as file:
#     count = 0
#     liist = []
#     reader = csv.reader(file, delimiter = '\t')
#     for row in reader:
#         if  row[3] not in liist and row[3] != 'brand':
#             liist.append(row[3])
#             count += 1
#         elif row[3] == 'brand':
#            # print(row)
#             pass


def get_data_csv():
    with open('./proxy_tyres (1).csv', 'r') as file:
    # with open('/usr/local/bin/fuck_debian/tyres_wheels/proxy_tyres (1).csv', 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        proxy = []
        for row in reader:
            proxy.append(row)
    print(type(row), '--------',  len(proxy))
    return proxy

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


#/usr/local/bin/fuck_debian/tyres_wheels/
def get_tyres_csv():
    proxy_data = []
    data = get_data_csv()
    for i in range(1, len(data)):
        # try:
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
            if data[i][4] == 'S':
                category_id = categories_summer[vendor]
            elif data[i][4] == "W":
                category_id = categories_winter[vendor]
            else:
                category_id = categories_allseason[vendor]
            category = 12
            description = data[i][1]
            # check category wheels and tyres
            product_code = data[i][2]
            size = data[i][7] #16 'diameter'
            width = data[i][8] #14
            height = data[i][9] #15
            sku = data[i][0]
            image_url = data[i][20]  #image_link
            name_picture = id_generator() + '.jpg'
            image_tuple = (name_picture, image_url)
            price = count_price(data[i][17], size)
            koeff = 1
            meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            params = 1
            options = {
                'diameter': size,
                'width': width,
                'profile': height
            }
            result = ([category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
             params, koeff, meta_h1, category], image_tuple, options)
            proxy_data.append(result)

        # except KeyError as error:
        #     print("Something went wrong KeyError from getcsv: {}".format(error))
        #     # write(str(data))
        #     print(str(data[i]))
        #     continue

    mem = sys.getsizeof(proxy_data)
    #print('proxy_data', type(proxy_data), len(proxy_data), type(proxy_data[0]), len(proxy_data[0])) #, proxy_data[0])
    print(mem / 1000, 'Kb--')
    return proxy_data


data = get_tyres_csv()
mems = sys.getsizeof(data)
print(mems / 1000, 'Kb')
check_write_json(data)
