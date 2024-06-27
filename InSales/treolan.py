import asyncio

import xml.etree.ElementTree as ET
import zeep
from zeep import helpers as Help
from zeep.helpers import serialize_object as Helper
import os
import csv
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.settings import Settings
from zeep.transports import Transport
from conn import executemany_query, execute_query_return, query_write_vendors
from conn_maintenance import *
from creds import treolan_login, treolan_password, CSV_PATH

DEMO = 'https://demo-api.treolan.ru/ws/service.asmx?wsdl'
PROD = 'https://api.treolan.ru/ws/service.asmx?wsdl'


def write_excel(data):
    with open('treolan_cats.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print('ALL_RIDE_treolan')


def write_excel_v2(data, remote=True):
    if not remote:
        with open('logic_categories.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            path_file = str(os.getcwd()) + 'logic_cats.csv'
            print('ALL_RIDE')

    else:
        with open(CSV_PATH + 'logic_categories.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            print('ALL_RIDE')
            path_file = CSV_PATH + 'logic_cats.csv'

    return path_file


async def save_categories_treolan():
    data_list = get_categories_treolan()
    write_data = [('treolan', i.get('name'), i.get('id'), i.get('parent_id', '0'))
                  for i in data_list if i.get('name') != 'UNKNOW']
    write_excel_v2(write_data)
    if await executemany_query(query_write_vendors, write_data):
        print('Categories tried saved')
    else:
        print("XS")


def write_categories_treolan():
    data_list = get_categories_treolan()
    write_data = [('treolan', i.get('name'), i.get('id'), i.get('parent_id', '0'))
                  for i in data_list if i.get('name') != 'UNKNOW']
    write_excel_v2(write_data)
    print('ALL_RIDE')


def get_client_treolan():
    session = Session()
    # session.auth = HTTPBasicAuth(treolan_login, treolan_password)
    client = Client(PROD,
                    transport=Transport(session=session))

    return client


def get_categories_treolan():  # GetCategories
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client(PROD, settings=settings)
    category_list = client.service.GetCategories(treolan_login, treolan_password)
    datas = Help.serialize_object(category_list).get('Result')
    lissst = datas.split('</category>')
    data = [i.replace(':', '').replace('</catalog', '').replace('<category ', '').replace('/>', '')
            .replace('>', '').replace('\n', '').strip() for i in lissst if not i.startswith('<catalog ')]
    # print(len(data))
    proxy = []
    faxy = {}
    for j in data:
        jj = j.split('sortindex=')
        jjj = jj[0].split('name="')
        try:
            faxy['name'] = jjj[1].strip().rstrip('"')
        except IndexError:
            faxy['name'] = 'UNKNOW'

        jjjj = jjj[0].split('parentid="')
        try:
            faxy['parent_id'] = jjjj[1].strip().rstrip('"')
        except IndexError:
            faxy['parent_id'] = '0'
            # print('jjj', jjj)
        try:
            faxy['id'] = jjjj[0].split('id="')[1].strip().rstrip('"')
        except IndexError:
            faxy['id'] = '0'

        proxy.append(faxy.copy())
    # write_excel(proxy)
    # print(*proxy, sep='\n')
    return proxy


def get_items_from_categories(id):
    client = get_client_treolan()
    response = client.service.GenCatalogV2(treolan_login, treolan_password, category=id, vendorid="0",
                                           keywords='', criterion=1, inArticul=False, inName=False,
                                           inMark=False, showNc=1, freeNom=1)

    return Helper(response)

from collections import OrderedDict

def get_product_info(articul : str):
    client = get_client_treolan()
    response = client.service.ProductInfoV2(treolan_login, treolan_password, Articul=articul)

    return Helper(response).get('Result')




def create_csv_for_category_from_treolan():
    list_cats = execute_query_return(query_get_actual_cats_v3, ('treolan',))
    category_ids = {}
    category_groups = {}
    # print('list_cats', list_cats)
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    # site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'Name', 'target_price', 'quantity', 'Brand', 'Vendor_part',
                   'published', 'full_price', 'currency', 'images']
    # date = get_shipment_dates()  # 2023-11-19
    allpro = []
    for key in category_groups.keys():
        result_list = []
        rewrite_properties = {}
        for category_id in category_groups.get(key):
            if category_id:
                # try:
                site_category_name = category_ids[category_id][1]
                data = get_items_from_categories(category_id).get('Result')
                root = ET.fromstringlist(data)
                child = [i.attrib for i in root.iter('category') if i.attrib.get('vetomrazdele') != '0']
                # print(child)
                item = [j.attrib for j in root.iter('position')]
                for prod in item:
                    # print(232323, prod)
                    proxy = dict()
                    proxy['published'] = category_ids[category_id][2]
                    proxy['category_id'] = site_category_name
                    try:
                        proxy['target_price'] = round(float(prod.get('price')) * 1.05, 2)
                    except:
                        print("Error not found price treolan", prod)
                        continue
                    currency = prod.get('recommendedcurrency', prod.get('currency'))
                    proxy['full_price'] = str(proxy['target_price']) + ' ' + currency
                    if currency == 'RUB':
                        proxy['currency'] = "RUR"
                    articul = prod.get('articul')
                    add_data = get_product_info(articul)
                    sub_root = ET.fromstring(add_data)
                    tr = {ii.attrib.get('Name'): ii.attrib.get('Value') for ii in sub_root.iter('Property')}
                    proxy['images'] = ''.join([images.attrib.get('Link') for images in sub_root.iter('row') if images.attrib.get('Link')])
                    ######################################################################
                    proxy.update(prod)
                    proxy.update(tr)
                    rewrite_properties.update(prod)
                    rewrite_properties.update(tr)
                    result_list.append(proxy.copy())
                    ######################################################################

                # print('*' * 50)
                # print(type(prod), prod)

                # except Exception as err:
                #     print(category_id, prod)
                #     print('Some_fuckup_treolan {}'.format(err))

        fields = base_fields.copy()
        # pr = set([i.strip().capitalize() for i in set(rewrite_properties.keys())])
        pr = sorted(set(rewrite_properties.keys()))
        fields.extend(pr)
        print(f'fields_treolan_{key}', fields)

        with open(CSV_PATH + f'treolan_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', dialect='excel',
                                    restval='', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)

        # break

        allpro.extend(result_list.copy())

    with open(CSV_PATH + f'treolan-all.csv', 'w') as file:
        writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                extrasaction='ignore', fieldnames=base_fields)
        writer.writeheader()
        writer.writerows(allpro)


# get_categories_treolan()
# get_cats_treolan()
# asyncio.run(save_categories_treolan())
# create_csv_for_category_from_treolan()

# get_product_info('US.RSUTA.00P')
