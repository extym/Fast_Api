import asyncio
import csv
import json

import zeep
from zeep.helpers import serialize_object as Helper
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from suds.client import Client as SudsClient
from suds.transport.https import HttpAuthenticated

from base64 import b64encode
from creds import merlion_username, merlion_password, CSV_PATH
from conn import executemany_query, execute_query_return, query_write_vendors
from conn_maintenance import *

url_test_dl = 'https://apitest.merlion.com/dl/mlservice3?wsdl'  # (стиль document/literal)
url_test_re = 'https://apitest.merlion.com/re/mlservice3?wsdl'  # (стиль rpc/encoded)
url_test_rl = 'https://apitest.merlion.com/rl/mlservice3?wsdl'  # (стиль rpc/literal)

url_dl = 'https://api.merlion.com/dl/mlservice3?wsdl'  # (стиль document/literal)
url_re = 'https://api.merlion.com/re/mlservice3?wsdl'  # (стиль rpc/encoded)
url_rl = 'https://api.merlion.com/rl/mlservice3?wsdl'  # (стиль rpc/literal)

shipment_method = 'К_S11МСК_Д'
image_link = 'http://img.merlion.ru/items/'

def basic_auth():
    token = b64encode(f"{merlion_username}:{merlion_password}".encode('utf-8')).decode("ascii")
    return token


def write_excel(data):
    with open('./merlion_cats.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_client_merlion(url):
    session = Session()
    session.auth = HTTPBasicAuth(merlion_username, merlion_password)
    client = Client(url, transport=Transport(session=session), )

    return client



def get_client_suds():
    client = SudsClient(url=url_re,
                    transport=HttpAuthenticated(username=merlion_username, password=merlion_password))
    response = client.service.getShipmentMethods(code='')
    print(response)
    return client

# print(get_client_suds(url_re))

def get_catalog_merlion():
    client = get_client_merlion(url_test_re)
    response = client.service.getCatalog(cat_id='All')
    data = Helper(response)

    return data


#
def write_categories_merlion():
    data_list = get_catalog_merlion()
    write_data = [('merlion', i.get('Description'), i.get('ID'), i.get('ID_PARENT', '0'))
                  for i in data_list]
    write_excel(write_data)
    print('ALL_RIDE')


async def save_categories_vendor():
    data_list = get_catalog_merlion()
    write_data = [('merlion', i.get('Description'), i.get('ID'), i.get('ID_PARENT', '0'))
                  for i in data_list]
    write_excel(write_data)
    if await executemany_query(query_write_vendors, write_data):
        print('Categories tried saved')
    else:
        print("XS")


def get_current_category(id):
    client = get_client_merlion(url_test_re)
    response = client.service.getItems(cat_id=id, item_id='', shipment_method=shipment_method,
                                       page=0, rows_on_page=10000, last_time_change='')

    return Helper(response)


def get_available_stock_price(id, date):
    # date = get_shipment_dates()
    client = get_client_merlion(url_test_re)
    data = client.service.getItemsAvail(cat_id=id, shipment_method=shipment_method,
                                        shipment_date=date, only_avail=1, item_id='')
    pro_data = {i['No']: {key: value for key, value in i.items()} for i in Helper(data) if i['No']}
    re_data = {i['No']: {'PriceClientRUB': i['PriceClientRUB'], 'AvailableClient': i['AvailableClient']}
               for i in data if i['No']}
    # print('7777777777_merlion', re_data)
    return re_data, pro_data



def get_shipment_dates():
    client = get_client_merlion(url_re)
    response = client.service.getShipmentDates(code='', ShipmentMethodCode='')

    return Helper(response)


# print(get_shipment_dates())

def get_images(cat_id):
    client = get_client_merlion(url_test_re)
    data = client.service.getItemsImages(cat_id=cat_id, item_id='', page=0, rows_on_page=5000,
                                         last_time_change='', ViewType='v', SizeType='m, b, s')

    return {i['No']: i['FileName'] for i in Helper(data)}


def get_shipment_methods():
    client = get_client_merlion(url_test_re)
    response = client.service.getShipmentMethods(code='')
    # ([('Code', 'К_S11МСК_Д'), ('Description', 'Доставка кросс со склада Санкт-Петербург'), ('IsDefault', 1)])
    return Helper(response)


# ML200303
def create_csv_for_category_from_merlion():
    list_cats = execute_query_return(query_get_actual_cats_v3, ('merlion',))
    category_ids = {}
    category_groups = {}
    count, count_price = 0, 0
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    # site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'Name', 'item_id', 'quantity', 'Brand', 
                   'Vendor_part', 'price', 'published', 'image', 'currency']
    date = get_shipment_dates()  # 2023-11-19
    allpro = []
    for key in category_groups.keys():
        result_list = []
        rewrite_properties = {}
        for category_id in category_groups.get(key):
            if category_id:
                prod = {}
                try:
                    site_category_name = category_ids[category_id][1]
                    add_data = get_available_stock_price(category_id, date[0].get('Date'))
                    # print(category_id, add_data)
                    data = get_current_category(category_id)
                    image_data = get_images(category_id)
                    print('merlion_image_data {} for category {}'.format(len(image_data), category_id))

                    for prod in data:
                        # if key == 1 or key == '1':
                        #     print(1122, type(prod), prod)
                        count += 1
                        proxy = dict()
                        proxy['published'] = category_ids[category_id][2]
                        proxy['category_id'] = site_category_name
                        item_id = prod.get('No')
                        proxy['item_id'] = item_id
                        pre_data = add_data[0].get(item_id)
                        price, quantity = 0, 0
                        if pre_data:
                            quantity = pre_data.get('AvailableClient')
                            if pre_data.get('PriceClientRUB'):
                                price = pre_data.get('PriceClientRUB') * 1.05
                                count_price += 1
                            # print('price_data_merlion', pre_data)
                        proxy['quantity'] = quantity
                        proxy['price'] = price
                        proxy['currency'] = 'RUR'
                        if image_data.get(item_id):
                            proxy['image'] = image_link + image_data.get(item_id)
                        else:
                            proxy['image'] = 'Merlion_not_send_image'

                            ######################################################################
                        if quantity and price:
                            proxy.update(prod)
                            rewrite_properties.update(prod)
                            result_list.append(proxy.copy())
                        ######################################################################

                except Exception as err:
                    print(category_id, prod)
                    print('Some_fuckup_merlion {}'.format(err))

        fields = base_fields.copy()
        # pr = set([i.strip().capitalize() for i in set(rewrite_properties.keys())])
        pr = sorted(set(rewrite_properties.keys()))
        fields.extend(pr)
        print('fields_merlion_{} all_product {}, product_with_price {}, {}'
              .format(key, count, count_price, fields))

        with open(CSV_PATH + f'merlion_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', dialect='excel',
                                    restval='', fieldnames=set(fields))
            writer.writeheader()
            writer.writerows(result_list)


        # if key == 1 or key == '1':
        #     print(*result_list, sep='\n')

        # break

        allpro.extend(result_list.copy())

    with open(CSV_PATH + f'merlion-all.csv', 'w') as file:
        writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                extrasaction='ignore', fieldnames=base_fields)
        writer.writeheader()
        writer.writerows(allpro)


# get_catalog_merlion(url_test_re)
# write_categories_merlion()
# asyncio.run(save_categories_vendor())
# get_shipment_methods()
# create_csv_for_category_from_merlion()
