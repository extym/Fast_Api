import datetime
import sys
import requests
import json

import xmltodict

from cred import *

vendor = 0

# for production only
requests.packages.urllib3.disable_warnings()


def get_pages():
    link = address + "page0" + contract + 'token=' + Token + '&vendor=' + str(vendor)  # + '&category=3'
    resp = requests.get(link, verify=False)
    some_data = resp.text
    # print(some_data)
    pages = ''
    try:
        main_data = resp.json()
        pages = int(main_data['pages'])  # get how many pages
    except:
        print("some fuck up")
        return pages


def get_new_pages():
    resp = requests.get(link_kolrad)
    data = xmltodict.parse(resp.text)
    data_product = data['data']['product']
    print(data['data']['product'][0], sep='\n')

    # print(datetime.datetime.now(), 'data_product2 - ', len(data_product))
    # post_smth(data_product, 0, '0')
    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open(DATA_PATH + "data_product.json", "w") as write_file:
        json.dump(data_product, write_file)  # encode dict into JSON


def get_new_pages_v2():
    resp = requests.get(link_kolrad)
    data = xmltodict.parse(resp.text)
    data_product = data['data']['product']
    # print(data['data']['product'][0], sep='\n')
    # print(datetime.datetime.now(), 'data_product2 - ', len(data_product))
    # post_smth(data_product, 0, '0')
    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open(DATA_PATH + "data_product.json", "w") as write_file:
        json.dump(data_product, write_file)  # encode dict into JSON

    return data_product




# for future name image
time_e = datetime.datetime.now().timestamp()
name_img = str(round(time_e, 2)).replace('.', '-')
# https://b2b.kolrad.ru/json/hannover/page0/contract944/?token=token&category[]=5
# https://b2b.kolrad.ru/json/hannover/page0/contract944/?token=$1$mOhvpapi$DcuRbWQEdMq3ivCJHcbD10
count = 0


# from get_data import post_smth
# Получаем все данные по page
def get_wheels():
    pages = get_pages()
    data_product = []
    for i in range(pages):
        try:
            params = {
                "token": Token,
                "vendor": 0
            }
            links = address + 'page' + str(i) + contract
            resp = requests.post(links, params=params, verify=False)
            data = resp.json()
            page_data = data['offers']
            proxy = []
            for j in range(len(page_data)):
                if page_data[j].get('category') in [1, 4, 5, 7]:
                    proxy.append(page_data[j])

            data_product.extend(proxy)
            # post_smth(data_product, 0,'0')
            print(datetime.datetime.now(), '--', i, '--', len(page_data), '--', len(data_product), '--', len(proxy))

        except Exception as error:
            print(f'page--{i}', 'Fuck JSON DECODE: {}'.format(error))
            continue

    # print(datetime.datetime.now(), 'data_product2 - ', len(data_product))
    # post_smth(data_product, 0, '0')
    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open("data_product.json", "w") as write_file:
        # with open("/usr/local/bin/fuck_debian/tyres_wheels/data_product.json", "w") as write_file:
        json.dump(data_product, write_file)  # encode dict into JSON

    # return data_product

# print('get_whells[0]', type(get_wheels()[0]))

#

# get_wheels()

# login()
