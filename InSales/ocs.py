import json
from conn import executemany_query, execute_query_return, execute_query_return_v2
from conn_maintenance import *
import requests
import asyncio

key = {'X-API-Key': 'juSYkZFINJDyvImhYkP6A-7v1GaYfJ'}
link = 'https://connector.b2b.ocs.ru'
from test import osc_category


async def save_categories_vendor(data):
    data_list = [i for i in data['children'] if data['children']]
    write_data = [('ocs', i.get('name'), i.get('category'), i.get('children'), i.get('leaf', False))
                  for i in data_list]
    if await executemany_query(query_write_vendor_logic, write_data):
        print('Categories tried saved')
    else:
        print("XS")


# asyncio.run(save_categories_vendor(osc_category))

def get_smth(method):
    url = link + method
    headers = {}
    data = {}
    answer = requests.post(url, headers=headers, data=data)
    try:
        resp = answer.json()
    except:
        resp = json.loads(answer.text)
    print(answer.text)
    print(resp)

    return resp


def get_categories():
    method = '/api/v2/catalog/categories'
    url = link + method
    headers = {
        'accept': 'application/json',
        'X-API-Key': 'juSYkZFINJDyvImhYkP6A-7v1GaYfJ'}

    answer = requests.get(url, headers=headers)
    try:
        resp = answer.json()
    except:
        resp = ''

    return resp


def get_product(categories):
    method = f'/api/v2/catalog/categories/{categories}/products'
    url = link + method
    headers = {'X-API-Key': 'juSYkZFINJDyvImhYkP6A-7v1GaYfJ'}
    data = {}
    params = {
        'shipmentcity': '',
        'onlyavailable': True,
        'includeregular': True,
        'includeuncondition': False,
        'withdescriptions': True  # TODO maybe for stocks need False?
    }
    answer = requests.post(url, headers=headers, data=data, params=params)
    try:
        resp = answer.json()
    except:
        resp = ''
    print(answer.text)
    print(resp)

    return resp


async def save_categories_vendors():
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

    write_data = [('ocs', i.get('name'), i.get('category'), i.get('parentId', '0'),
                   i.get('leaf', False)) for i in proxy]

    print('write_data', write_data)
    if await executemany_query(query_write_vendors, write_data):
        print('Categories tried saved')
    else:
        print("XS")


# get_categories()
asyncio.run(save_categories_vendors())