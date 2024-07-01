import json
import os

from conn import executemany_query, execute_query_return, execute_query_return_v2
from conn_maintenance import *
import requests
import asyncio
import csv
from creds import *
from time import sleep


key = {'X-API-Key': 'juSYkZFINJDyvImhYkP6A-7v1GaYfJ'}
link = 'https://connector.b2b.ocs.ru'
headers = {
    'accept': 'application/json',
    'X-API-Key': 'juSYkZFINJDyvImhYkP6A-7v1GaYfJ'}
from test import osc_category


def write_excel_2(data):
    fieldnames = ['ocs', 'name','category','parentId','children']
    with open('ocs.xls', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print('ALL_RIDE')
        
        
def write_excel(data):
    with open('ocs_cats.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print('ALL_RIDE')


def write_excel_v2(data, remote=True):
    if not remote:
        with open('ocs_categories.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            path_file = str(os.getcwd()) + 'ocs_categories.csv'
            print('ALL_RIDE', path_file)

    else:
        with open(CSV_PATH + 'ocs_categories.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            path_file = CSV_PATH + 'ocs_categories.csv'
            print('ALL_RIDE', path_file)

    return path_file


def get_smth(method):
    url = link + method
    sleep(0.3)
    answer = requests.get(url, headers=headers)
    try:
        resp = answer.json()
    except:
        print('ERROR', answer.text)

    # print(resp)

    return resp


def get_categories():
    method = '/api/v2/catalog/categories'
    url = link + method


    answer = requests.get(url, headers=headers)
    try:
        resp = answer.json()
    except:
        resp = ''

    return resp


def get_product(categories):
    method = f'/api/v2/catalog/categories/{categories}/products'
    url = link + method
    params = {
        'shipmentcity': 'Санкт-Петербург',
        'onlyavailable': True,
        'includeregular': True,
        'includeuncondition': False,
        'withdescriptions': True  # TODO maybe for stocks need False?
    }
    sleep(0.3)
    answer = requests.get(url, headers=headers, params=params)
    try:
        resp = answer.json()
    except:
        resp = ''
        print('Error answer server ocs', answer.text)

    return resp


def get_content_batch(list_ids):
    proxy = []
    method = '/api/v2/content/batch'
    url = link + method
    # print("categories_banch", len(categories), categories)

    answer = requests.post(url, json=list_ids, headers=headers)
    # print(444444444, type(answer.json().get('result')))
    return answer.json().get('result')


def get_product_banch(categories):
    method = '/api/v2/catalog/categories/batch/products'
    url = link + method
    # print("categories_banch", len(categories), categories)
    params = {
        'shipmentcity': 'Санкт-Петербург',
        'onlyavailable': True,
        'includeregular': True,
        'includeuncondition': False,
        'withdescriptions': True  # TODO maybe for stocks need False?
    }
    answer = requests.post(url, json=categories, headers=headers, params=params)
    if answer.ok:
        resp = answer.json()
        return answer.status_code, resp
    elif answer.status_code == 403:
        resp = answer.text
        print('Error answer server ocs for banch', answer.text)
        return answer.status_code, resp


async def save_categories_ocs():
    data = get_categories()
    proxy = []
    for cat in data:
        if len(cat['children']) > 0:
            for child in cat['children']:
                if len(child['children']) > 0:
                    for ch in child['children']:
                        proxy.append({"category": ch["category"], "name": ch["name"],
                                      "children": ch["children"], "parentId": child["category"]})
                else:
                    proxy.append({"category": child["category"], "name": child["name"],
                                  "children": child["children"], "parentId": cat["category"]})
        else:
            proxy.append({"category": cat["category"], "name": cat["name"],
                          "children": cat["children"], "parentId": None})

    write_data = [('ocs', i.get('name'), i.get('category'), i.get('parentId', '0')) for i in proxy]

    write_excel_v2(write_data)
    # print('write_data', write_data)
    try:
        await executemany_query(query_write_vendors, write_data)
        print('Categories tried saved_ocs')
    except:
        print("XS")


def create_csv_for_category_from_ocs():  ##for import goods only (maybe)
    list_cats = execute_query_return(query_get_actual_cats_v2, ('ocs',))
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'brand', 'id', 'name', 'quantity', 'price', 'published',
                   'image_short', 'image_additional', 'image_main', 'description']
    count_response = 0
    for key in category_groups.keys():
        result_list = []
        for category_id in category_groups.get(key):
            site_category_name = category_ids[category_id][1]
            try:
                data = get_product(category_id)
                if not isinstance(data['result'], str):
                    count_response += 1
                    for prod in data['result']:
                        proxy = dict()
                        proxy['published'] = site_category_path[category_id]
                        proxy['category_id'] = site_category_name
                        proxy['quantity'] = sum([i.get('quantity').get('value') for i in prod.get('locations') if i.get('description') in ('Москва','Санкт-Петербург')])
                        proxy['price'] = prod.get('price').get('order').get('value') * 1.05
                        proxy['brand'] = prod.get('product').get('producer')
                        proxy['id'] = prod.get('product').get('itemId')
                        name = prod.get('product').get('itemNameRus')
                        if name:
                            proxy['name'] = name
                        else:
                            proxy['name'] = prod.get('product').get('itemName')
                        description = prod.get('product').get('productDescription')
                        if not description:
                            description = prod.get('product').get('itemName')
                        proxy['description'] = description

                        result_list.append(proxy.copy())
                else:
                    print('count_response', count_response)
                    sleep(3600)
            except:

                continue

        fields = base_fields.copy()
        print(f'fields_ocs_{key}', fields)
        with open(CSV_PATH + f'ocs_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)


def create_csv_for_category_from_ocs_v2():  ##for import goods only (maybe)
    '''
    {'product': {'itemId': '1000433868', 'productKey': '1000433868', 'partNumber': 'H5562201', 'producer': 'Ricoh',
    'category': 'V0605', 'itemName': 'Задний упор направляющей пластины', 'itemNameRus': 'Задний упор направляющей
    пластины', 'productName': 'Ricoh H5562201', 'hsCode': '7326909807', 'traceable': False, 'condition': 'Regular',
    'vatPercent': 20.0, 'serialNumberAvailability': False, 'catalogPath': [{'category': 'V06', 'name': 'Расходные
    материалы'}, {'category': 'V0605', 'name': 'Запчасти для принтеров и МФУ'}]}, 'isAvailableForOrder': True,
    'packageInformation': {'weight': 0.001, 'width': 0.01, 'height': 0.01, 'depth': 0.01, 'volume': 1e-06,
    'multiplicity': 1, 'units': 'шт'}, 'price': {'priceList': {'value': 742.82, 'currency': 'RUR'}, 'order': {
    'value': 742.82, 'currency': 'RUR'}, 'discountB2B': 0.0}, 'locations': [{'location': 'МСК', 'description':
    'Москва', 'type': 'Local', 'quantity': {'value': 1, 'isGreatThan': False}, 'canReserve': True, 'deliveryDate':
    '2023-12-15T00:00:00'}]} :return:
    '''
    prod = {}
    list_cats = execute_query_return(query_get_actual_cats_v2, ('ocs',))
    # print('list_cats', list_cats)
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')

    # print(11, category_ids)
    # print(22, category_groups)
    site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'brand', 'id', 'name', 'quantity', 'price', 'published', 'description']
    for key in category_groups.keys():
        result_list = []
        rewrite_properties = {}
        try:
            data = get_product_banch(category_groups.get(key))[1]
            for prod in data['result']:
                price = str(prod.get('price').get('priceList').get('value'))
                if price:
                    proxy = dict()
                    proxy['published'] = site_category_path[prod.get('product').get('category')]
                    proxy['category_id'] = category_ids[prod.get('product').get('category')][1]
                    proxy['quantity'] = sum([i.get('quantity').get('value') for i in prod.get('locations') if i.get('description') in ('Москва','Санкт-Петербург', 'МСК')])
                    proxy['price'] = int(price.split('.')[0]) * 1.05
                    proxy['brand'] = prod.get('product').get('producer')
                    proxy['id'] = prod.get('product').get('itemId')
                    name = prod.get('product').get('itemNameRus')
                    if name:
                        proxy['name'] = name
                    else:
                        proxy['name'] = prod.get('product').get('itemName')
                    description = prod.get('product').get('productDescription')
                    if not description:
                        description = prod.get('product').get('itemName')
                    proxy['description'] = description

                    proxy.update(prod.get('product'))
                    rewrite_properties.update(prod.get('product'))
                    # print(121212, proxy)
                    result_list.append(proxy.copy())

                else:
                    print('null_price_prod', prod)
                    continue
        except Exception as error:
            print("Some_fuckup_ocs_bunch_v2 {}".format(error))
            continue

        fields = base_fields.copy()
        pr = set(rewrite_properties.keys())
        fields.extend(pr)
        print(f'fields_ocs_{key}', fields)
        with open(CSV_PATH + f'ocs_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)

        # break


def rewrite_content(content):
    result = {i.get('name'): str(i.get('value')) + ' ' + i.get('unit', '') for i in content}

    return result

def create_csv_for_category_from_ocs_v3():  ##for import goods only (maybe)
    '''
    {'product': {'itemId': '1000433868', 'productKey': '1000433868', 'partNumber': 'H5562201', 'producer': 'Ricoh',
    'category': 'V0605', 'itemName': 'Задний упор направляющей пластины', 'itemNameRus': 'Задний упор направляющей
    пластины', 'productName': 'Ricoh H5562201', 'hsCode': '7326909807', 'traceable': False, 'condition': 'Regular',
    'vatPercent': 20.0, 'serialNumberAvailability': False, 'catalogPath': [{'category': 'V06', 'name': 'Расходные
    материалы'}, {'category': 'V0605', 'name': 'Запчасти для принтеров и МФУ'}]}, 'isAvailableForOrder': True,
    'packageInformation': {'weight': 0.001, 'width': 0.01, 'height': 0.01, 'depth': 0.01, 'volume': 1e-06,
    'multiplicity': 1, 'units': 'шт'}, 'price': {'priceList': {'value': 742.82, 'currency': 'RUR'}, 'order': {
    'value': 742.82, 'currency': 'RUR'}, 'discountB2B': 0.0}, 'locations': [{'location': 'МСК', 'description':
    'Москва', 'type': 'Local', 'quantity': {'value': 1, 'isGreatThan': False}, 'canReserve': True, 'deliveryDate':
    '2023-12-15T00:00:00'}]} :return:
    '''
    prod = {}
    list_cats = execute_query_return(query_get_actual_cats_v2, ('ocs',))
    # print('list_cats', list_cats)
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')

    # print(11, category_ids)
    # print(22, category_groups)
    site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'brand', 'id', 'name',
                   'quantity', 'price', 'published', 'description']
    allpro = []
    for key in category_groups.keys():
        result_list, maxy = [], []
        rewrite_properties = {}
        try:
            datases = get_product_banch(category_groups.get(key))
            if datases[0] != 403:
                data = datases[1]
                for prod in data['result']:
                    price = str(prod.get('price').get('priceList').get('value'))
                    if price:
                        proxy = dict()
                        proxy['published'] = site_category_path[prod.get('product').get('category')]
                        proxy['category_id'] = category_ids[prod.get('product').get('category')][1]
                        proxy['quantity'] = sum([i.get('quantity').get('value') for i in prod.get('locations') if i.get('description') in ('Москва','Санкт-Петербург', 'МСК')])
                        proxy['price'] = int(price.split('.')[0]) * 1.05
                        proxy['brand'] = prod.get('product').get('producer')
                        id = prod.get('product').get('itemId')
                        proxy['id'] = id
                        maxy.append(id)
                        name = prod.get('product').get('itemNameRus')
                        if name:
                            proxy['name'] = name
                        else:
                            proxy['name'] = prod.get('product').get('itemName')
                        description = prod.get('product').get('productDescription')
                        if not description:
                            description = prod.get('product').get('itemName')
                        proxy['description'] = description

                        proxy.update(prod.get('product'))
                        rewrite_properties.update(prod.get('product'))
                        result_list.append(proxy.copy())

                    else:
                        # print('null_price_prod', prod)
                        continue

            # else:
            #     error = {'error': datases[1], 'key': key}
            #     result_list.append(error)
        except Exception as error:
            print("Some_fuckup_ocs_bunch_v3 {} {} {}".format(error, prod, key))
            continue
        try:
            add_data = get_content_batch(maxy)
            pre_data = {i.get('itemId'): i for i in add_data}
            for product in result_list:
                pr_id = product.get('itemId')
                if pr_id in pre_data.keys():
                    faxy = pre_data[pr_id]
                    properties = rewrite_content(faxy.pop('properties'))
                    product.update(faxy)
                    product.update(properties)

                rewrite_properties.update(product)

        except Exception as err:
            print("Some_fuckup_ocs_bunch_v3_1 {}".format(err))
            continue
        fields = base_fields.copy()
        pr = sorted(set(rewrite_properties.keys()))
        fields.extend(pr)
        print(f'fields_ocs_{key}', fields)
        with open(CSV_PATH + f'ocs_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', dialect='excel',
                                    restval='', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)

        # break

        allpro.extend(result_list.copy())

    with open(CSV_PATH + f'ocs-all.csv', 'w') as file:
        writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                extrasaction='ignore', fieldnames=base_fields)
        writer.writeheader()
        writer.writerows(allpro)


def check_len_keys(cats):
    for cat in cats.split(','):
        data = get_product(cat)
        print(78, cat, len(data.get('result')))
        proxy = [len(i['product'].keys()) for i in data.get('result')]
        pro = [i['product'].keys() for i in data.get('result')]
        print('proxy', cat, proxy)
        print(78, *pro, sep='\n')
    print(data.get('result')[0].keys())


# create_csv_for_category_from_ocs()
# check_len_keys('V0303,V0309')
# get_categories()
# asyncio.run(save_categories_vendors())
# get_smth('/api/v2/logistic/shipment/cities')
# get_product('all')
# get_product('V0303')
# create_csv_for_category_from_ocs_v2()
# create_csv_for_category_from_ocs()
# create_csv_for_category_from_ocs_v3()

