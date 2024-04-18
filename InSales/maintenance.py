import asyncio

import wget
import base64
import json
from creds import *
import requests
import csv
import zipfile
import pandas as pd
from conn import *


oauth_token = 'ae348fe6-ea23-4191-82c1-61ddf0042269'

headers = {'Content-Type': 'application/json', 'Authorization': 'Basic '+ basic_auth}
header = {'Authorization': 'Basic '+ basic_auth}


# def get_netlab_token():
#     url = 'http://services.netlab.ru/rest/authentication/token.json'
#     params = {'username': nick, 'password': passw}
#     answer = requests.get(url, params=params)
#
#     print(answer.text)

CSV_PATH = './'


def get_catalogs():
    url = 'http://services.netlab.ru/rest/catalogsZip/list.json?oauth_token=' + oauth_token
    # params = {'username': nick, 'password': passw}
    answer = requests.get(url)

    print(answer.text)

# get_catalogs()


def xy(x):
    return int(x.get('id'))


def yy(x):
    result = x.get('leaf')
    return x.get('id')


def get_catalog_exist():
    catalog_name = "В наличии"  #"Прайс-лист"
    url = f'http://services.netlab.ru/rest/catalogsZip/{catalog_name}.json?oauth_token=' + oauth_token
    answer = requests.get(url)
    data_resp = json.loads(answer.text[5:])
    data = data_resp.get('catalogResponse').get("data").get("category")
    print(len(data), type(data))  #2846
    # print(*sorted(data, key=xy), sep='\n')

    return data


# def write_data_catalogs():
#     data = get_catalog()
#     print('DATA', type(data))
#     if data:
#         with open('net_catalogs.txt', 'w') as file:
#             file.write(str(data))
#         with open('net_catalogs.json', 'w') as write_file:
#             json.dump(data, write_file)
#
#         print("DATA write succesfully")
#     else:
#         print("DATA WRONG")


def create_path_for_csv(row_list):
    '''
    [{'id': 30966270, 'parent_id': 29253025, 'title': 'Мой склад', 'created_at': '2023-06-06T12:50:29.000+03:00',
    'updated_at': '2023-06-06T12:50:29.000+03:00', 'position': 17}]
    :param row_list:
    :return:
    '''
    result = []
    row_dict = {row['id']: row for row in row_list}
    for raw in row_list:
        pre_path = raw.get('title')
        path = raw.get('path', pre_path)
        parent_id = raw.get('parent_id')
        while parent_id is not None:
            re_path = row_dict.get(parent_id).get('title') + '/' + path
            parent_id = row_dict.get(parent_id).get('parent_id')
            path = re_path
            raw['path'] = re_path
        else:
            raw['path'] = 'Каталог' + raw.get('path', '').replace('Склад', '')

        # print('raw11', raw)
        result.append(raw)

    return result


def get_categories_from_site():
    link = 'https://myshop-cay359.myinsales.ru/'
    metod = '/admin/categories.json'
    url = link + metod
    answer = requests.get(url, headers=header)
    data = answer.json()

    # print(len(data), type(data))
    # print(*sorted(data, key=xy), sep='\n')
    # create_path_for_csv(data)
    return create_path_for_csv(data)



##it's we create path and save categories from insales
# for web & compare categories insales & vendor
async def save_categories_from_site(vendor):
    data = get_categories_from_site()
    write_data = [('how_now', i.get('id'), i.get('title'), i.get('parent_id'), i.get('position'), i.get('path'), vendor) for i in data]
    if await executemany_query(query_write_site_categories, write_data):
        print("ALL RIDE")
    else:
        print('XS')


async def update_categories_from_site(vendor):
    data = get_categories_from_site()
    write_data = [(i.get('title'), i.get('parent_id'), i.get('position'), i.get('path'), i.get('id'), vendor) for i in data]
    if await executemany_query(query_update_site_categories, write_data):
        print("ALL_RIDE_update_categories_from_site", vendor)
    else:
        print('XS')
        
        

async def update_categories_from_site_v2(vendor):
    data = get_categories_from_site()
    write_data = [('how_now', i.get('id'), i.get('title'), i.get('parent_id'),
                   i.get('position'), i.get('path'), vendor) for i in data]
    if await execute_query_update(write_data):
        print("ALL_RIDE_update_categories_from_site_v2", vendor)
    else:
        print('XS')


def read_xlsx():
    link = 'http://www.netlab.ru/products/dealerd.zip'
    xlsx = requests.get(link)
    with open('price.zip', "wb") as output:
        output.write(xlsx.content)

    data = wget.download(link, out='wget_xls.zip')

    print(type(data))


def wget_xlsx():
    link = 'http://www.netlab.ru/products/dealerd.zip'
    # data = wget.download(link, out='wget_xls.zip')
    zipfile.ZipFile('wget_xls.zip').extractall('./')
    read_file = pd.read_excel('DealerD.xlsx')


    print(type(read_file), len(read_file))


# encode_base64()

# get_catalog()
# get_categories_from_site()
# compare_categories()
# get_netlab_token()
# asyncio.run(save_categories_from_site('netlab'))
# asyncio.run(save_categories_from_site('logic'))  ## maybe wrong logic
# asyncio.run(update_categories_from_site('netlab'))
# asyncio.run(save_categories_from_site('ocs'))
# asyncio.run(update_categories_from_site('ocs'))
# asyncio.run(save_categories_from_site('marvel'))
# asyncio.run(save_categories_from_site('treolan'))
# asyncio.run(save_categories_from_site('merlion'))
# make_csv(cats)
# wget_xlsx()
# asyncio.run(get_data_netlab())
# asyncio.run(get_categories_from_site('netlab'))
# write_data_catalogs()
# get_catalog_exist()

# get_categories_from_site()