import logging
import os
import sys

import pandas as pd
from lxml import etree
from requests.auth import HTTPBasicAuth

import bot_tg
from cred import admin_ps_login, admin_ps_pass, ps_link
from base64 import b64encode
import requests
from requests import Session
import xmltodict
from urllib.request import urlopen
from typing import List, Dict


# from bot_tg import send_get


def basic_auth():
    token = b64encode(f"{admin_ps_login}:{admin_ps_pass}".encode('utf-8')).decode("ascii")
    return token


def get_client():
    session = Session()
    session.auth = (admin_ps_login, admin_ps_pass)

    return session.auth


def get_smth(metod):
    url = ps_link + metod
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.get(url, auth=token_ps)

    # print(3111133, answer.text)
    return answer.json()


async def change_status(ids: str):
    url = ps_link + '/order_items/change_status'
    data = {
        "order_item_ids": ids,
        "status_id": 8
    }
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.post(url=url, auth=token_ps, data=data)
    print('answer_changed_status', answer.text)
    if answer.ok:
        return True
    else:
        return False


def change_status_v2(ids: str, status_id=0):
    url = ps_link + '/order_items/change_status'
    data = {
        "order_item_ids": ids,
        "status_id": status_id
    }
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.post(url=url, auth=token_ps, data=data)
    print('answer_changed_status', answer.text)
    if answer.ok:
        return True
    else:
        return False


def get_orders_v2(customer_id: str,
                  marketplace_id: str = None,
                  filter_status: List = None):
    """
    We are requesting orders from parts-soft for get items ids
    :param customer_id:
    id customer in parts-soft
    :param marketplace_id:
    order id (shipment id) from marketplace
    :param filter_status:
    "id": 7, "name": "Пришло на центральный склад", "code": "prishlo"
    "id": 21, "name": "Готово к выдаче", "code": "prishlo"
    "id": 22, "name": "Резерв. Готов к выдаче", "code": "prishlo"
    "id": 27, "name": "Подготовка к возврату по просрочке.", "code": "prishlo"
    :return:
    string items ids
    """
    result, result_list = '', []
    page, error = 0, 0
    if customer_id == '710' or customer_id == '715' \
            or customer_id == '235':
        while marketplace_id != result:
            params = {
                'search[customer_id_eq]': customer_id,
                'search[marketplace_id_eq]': str(marketplace_id),
                'per_page': 20,
                'page': page
            }
            url = ps_link + "/orders.json"
            token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
            answer = requests.get(url, auth=token_ps, params=params)
            if answer.ok:
                # print(333, answer.text)
                data = answer.json()
                result_list = [i for i in data.get('orders')
                               if i.get('marketplace_id') == marketplace_id]
                # print(555, result_list[0])
                if len(result_list) > 0:
                    result = marketplace_id
                else:
                    page += 1
                    # print('page ', page)
                if page >= 3:
                    bot_tg.send_get('Не найдено отправление {} для {}. '
                                    'Требуется ручная обработка для изменения статуса на Выдано'
                                    .format(marketplace_id, customer_id))
                    break
            else:
                error += 1
                logging.info('Some trouble with access parts-soft - status {} text {}'
                             .format(answer.status_code, answer.text))
                bot_tg.send_get('Some trouble with access parts-soft - status {} text {}'
                                .format(answer.status_code, answer.text))
                if page >= 5:
                    break

    elif customer_id == '2063' or customer_id == '2504':
        while marketplace_id != result:
            params = {
                'search[customer_id_eq]': customer_id,
                # 'search[order_items_attributes][0][comment_eq]': marketplace_id,
                'search[order_items_comment_eq]': marketplace_id,
                'per_page': 20,
                'page': page
            }
            url = ps_link + "/orders.json"
            token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
            answer = requests.get(url, auth=token_ps, params=params)

            if answer.ok:
                data = answer.json()
                result_list = data.get('orders')
                if result_list:
                    result = marketplace_id
                else:
                    page += 1
                    print('page ', page)
                if page >= 3:
                    bot_tg.send_get('Не найдено отправление {} для {}. '
                                    'Требуется ручная обработка для изменения статуса на Выдано'
                                    .format(marketplace_id, customer_id))
                    break
            else:
                error += 1
                logging.info('Some trouble with access parts-soft - status {} text {}'
                             .format(answer.status_code, answer.text))
                bot_tg.send_get('Some trouble with access parts-soft - status {} text {}'
                                .format(answer.status_code, answer.text))
                if page >= 3:
                    break

    proxy = 0
    datas = ''
    try:
        line = get_smth("/order_status_types.json").get("order_status_types")
        proxy = result_list[0].get('order_id')
        if not filter_status:
            datas = ' '.join([str(i.get('id')) for i in result_list[0].get('order_items')])
        else:
            for item in result_list[0].get('order_items'):
                if item.get('status_id')  in filter_status:
                    # datas = ' '.join(str(item.get('id')))
                    datas += ' ' + str(item.get('id')).strip()
                elif item.get('status_id') == 8:
                    bot_tg.send_get("Заказ {} уже выдан.".format(proxy))
                else:
                    status = [i.get('name') for i in line if i.get('id') == item.get("status_id")]
                    bot_tg.send_get("Заказ {} в статусе {} для {}. "
                                    "Выдача заказа возможна только из группы Пришло."
                                    .format(proxy, status[0], customer_id))

    except Exception as error:
        print(222222222222222222, proxy)
        print('datas_error', error)
    print('datas', datas)
    return datas


async def make_data_for_request_v2(data_file, market):
    count = 0
    proxy = ''
    shipment_date = data_file[1]
    for number in data_file[0]:
        item_ids = get_orders_v2(market, 
                                 marketplace_id=str(number),
                                 filter_status = [7, 21, 22, 27])
        if item_ids:
            proxy += item_ids.strip() + ' '
            count += 1
        else:
            continue

    if len(proxy) > 0:
        result = await change_status(proxy.strip())
        if result:
            logging.info("All_ride_Rewrite {} statuses for all {} from market {} at {}"
                         .format(count, len(data_file[0]), market, shipment_date))
            bot_tg.send_get("Удачно выдано {} заказов из общего количества {} для {} на {}"
                            .format(count, len(data_file[0]), market, shipment_date))
        else:
            bot_tg.send_get("Error_Rewrite {} statuses for all {} from market {} at {}"
                            .format(count, len(data_file[0]), market, shipment_date))
    else:
        bot_tg.send_get("Не найдено заказов для {} на {}."
                        .format(market, shipment_date))

    print('All_order_items', proxy)


## FOR VERSION 1 API - CLIENT ONLY!
basket = '/api/v1/baskets/'
add_basket = "/api/v1/baskets"


def get_current_client_smth(metod, key=None):
    url = "https://3431.ru" + metod
    # token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    params = {
        "api_key": key
    }
    answer = requests.get(url, params=params)

    print(answer.text)


def send_current_basket_to_order(key: str = None):
    url = "https://3431.ru/api/v1/baskets/order"
    headers = {
        "api_key": key}
    data = {
        "api_key": key
    }
    answer = requests.post(url, headers=headers, data=data)

    print("FINAL_result {}".format(answer.text))
    if answer.ok:
        return answer.json().get('data')
    else:
        return None


def make_basket(qnt=None, exter_order_id=None, key=None, propousal=None):
    # print(777777777, qnt, exter_order_id, key, propousal )
    url = "https://3431.ru/api/v1/baskets"
    headers = {
        "api_key": key}
    data = {
        "api_key": key,
        "oem": propousal.get('oem'),
        "make_name": propousal.get('make_name'),
        "detail_name": propousal.get('detail_name'),
        "qnt": str(qnt),
        "comment": str(exter_order_id),
        "min_delivery_day": str(propousal.get('min_delivery_day')),
        "max_delivery_day": str(propousal.get('max_delivery_day')),
        "api_hash": propousal.get('hash_key')
    }
    answer = requests.post(url, headers=headers, data=data)
    print("!!!!!!!!!!!!!!!!", answer.text)

    return answer.status_code


def choice_function(items, full_items, qnt):
    listing = sorted(items.values())[:5]
    # print(322222233, listing)
    result = []
    for item in full_items:
        if item["cost"] in listing and item['qnt'] >= qnt:
            result.append(item)

    return result


# from lxml import etree
# root = etree.fromstring("https://3431.ru/system/unload_prices/33/yandex_market.xml")
# print(root)

def get_oem_from_xml(offer_id, link=None):
    brand, oem = '', ''
    print("OFFER ID", offer_id)
    with urlopen(link) as xml:
        doc = xmltodict.parse(xml)
        for row in doc['yml_catalog']['shop']['offers']['offer']:
            if row["@id"] == offer_id:
                # print(type(row), *row.keys(), sep='\n')
                print('$' * 50)
                brand = row['vendor']
                oem = row['vendorCode']
                price = row['price']
                print(44444444444, brand, oem, price)
                break

    return brand, oem

def get_oem_from_xml_v2(offer_id, link=None):
    brand, oem = '', ''
    print("OFFER ID", offer_id)
    with urlopen(link) as xml:
        doc = xmltodict.parse(xml)
        for row in doc['yml_catalog']['shop']['offers']['offer']:
            if row["@id"] == offer_id:
                print('$' * 50)
                brand = row['vendor']
                oem = row['vendorCode']
                price = row['price']
                print(44444444444, brand, oem, price)
                break

        if not oem and brand:
            result = False
            while result:
                count = 1
                offer_id = offer_id[:-count]
                print(offer_id)
                for row in doc['yml_catalog']['shop']['offers']['offer']:
                    if offer_id[: - count] == row["@id"][: - count]:

                        print(type(row), *row.items(), sep='\n')
                        brand = row['vendor']
                        oem = row['vendorCode'][:-count] + offer_id[- count:]
                        print(44444444444, brand, oem, offer_id)

                        break
                    else:
                        count += 1

                    if count >= 5:
                        result = True

    return brand, oem

def get_vendor_code_from_xlm(offer_id, link=None):
    link = 'https://3431.ru/system/unload_prices/33/yandex_market.xml'
    # link = 'https://3431.ru/system/unload_prices/21/sbermegamarket.xml'
    # link = 'https://3431.ru/system/unload_prices/17/yandex_market1.xml'
    vendor, vendor_code = '', ''
    data = pd.read_xml(link, xpath=f'//offer')
    count = 0
    for row in data.values:
        if row[0] == offer_id:
            vendor = row[12]
            vendor_code = row[13]
            break

    return vendor, vendor_code


#
print(get_oem_from_xml_v2("LUZARLRAC2601",
                         link = 'https://3431.ru/system/unload_prices/33/yandex_market.xml'))

def create_resp_if_not_exist(list_items, link, key=None,
                             external_order_id=None):
    # exter_order_id = external_order_id
    count_items = 0
    global_result_make_basket = False
    for item in list_items:
        # vendor_data = get_vendor_code_from_xlm(item.get('offer_id)'), link=link)
        offer_id = item.get('offerId')
        vendor_data = get_oem_from_xml(item.get('offerId'), link=link)
        oem = vendor_data[1]
        brand = vendor_data[0]
        qnt = item.get("count")
        print(3333, offer_id, oem, brand, qnt)
        # sys.exit()
        if oem:
            params = {
                "api_key": key,
                "oem": oem,
                "make_name": brand,
                "without_cross": True
            }
            metod = "/backend/price_items/api/v1/search/get_offers_by_oem_and_make_name"
            url = "http://3431.ru" + metod
            answer = requests.get(url, params=params)

            try:
                need_data = answer.json()["data"]
            except Exception as error:
                print("ERROR get data from json {}, oem {}, brand {}, qnt {}"
                      .format(answer.text, oem, brand, qnt))
                need_data = []
            if len(need_data) > 0:
                propousal = {i['hash_key']: i['cost'] for i in need_data if
                             (i["oem"] == oem and i['make_name'] == brand)}
                list_propousal = choice_function(propousal, need_data, qnt)

                # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
                #       *list_propousal[0].items(), sep='\n')
                # print(len(propousal))

                result_make_basket = make_basket(propousal=list_propousal[0],
                                                 qnt=qnt, key=key,
                                                 exter_order_id=external_order_id)
                if result_make_basket == 200:
                    count_items += 1
                else:
                    print("Make basket failed {} {}".format(result_make_basket, item))

            else:
                print('SOME FUCKUP GET PROPOUSAL {}'.format(answer.text))
        else:
            bot_tg.send_get('Проблема обработки заказа {}. Not found oem for offer_id {}'
                            .format(item.get('offerId'), external_order_id))

    if count_items == len(list_items):
        # print("Result result_make_basket successfully {}".format(count_items))
        global_result_make_basket = True
    else:
        print("Result result_make_basket UNsuccessfully {}".format(count_items))

    return global_result_make_basket


def create_order_ps_if_not_exist(list_items, link, key=None,
                                 external_order_id=None):
    # exter_order_id = external_order_id
    count_items = 0
    global_result_make_basket = False
    for item in list_items:
        list_propousal = []
        # vendor_data = get_vendor_code_from_xlm(item.get('offer_id)'), link=link)
        if item.get('offerId') != 'delivery':
            vendor_data = get_oem_from_xml(item.get('offerId'), link=link)
            oem = vendor_data[1]
            brand = vendor_data[0]
            qnt = item.get("count")
            print("oem---brand---qnt", oem, brand, qnt)
            # sys.exit()
            if not oem:
                bot_tg.send_get('.Проблема обработки заказа {}. Not found oem for offer_id {}'
                                .format(item.get('offerId'), external_order_id))
            else:
                params = {
                    "api_key": key,
                    "oem": oem,
                    "make_name": brand,
                    "without_cross": True
                }
                metod = "/backend/price_items/api/v1/search/get_offers_by_oem_and_make_name"
                url = "http://3431.ru" + metod
                answer = requests.get(url, params=params)

                try:
                    need_data = answer.json()["data"]
                except Exception as error:
                    print("ERROR get data from partsoft {}, oem {}, brand {}, qnt {}"
                          .format(answer.text, oem, brand, qnt))
                    need_data = []
                if len(need_data) > 0:
                    propousal = {i['hash_key']: i['cost'] for i in need_data if
                                 (i["oem"] == oem and i['make_name'] == brand)}
                    list_propousal = choice_function(propousal, need_data, qnt)

                    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
                    #       *list_propousal[0].items(), sep='\n')
                    # print(len(propousal))

                    result_make_basket = make_basket(propousal=list_propousal[0],
                                                     qnt=qnt, key=key,
                                                     exter_order_id=external_order_id)
                    if result_make_basket == 200:
                        count_items += 1
                    else:
                        print("Make basket failed {} {}".format(result_make_basket, item))

                else:
                    print('SOME FUCKUP GET PROPOUSAL {}'.format(answer.text))
        else:
            count_items += 1
            continue  # TODO make order delivery

    if count_items == len(list_items):
        # print("Result result_make_basket successfully {}".format(count_items))
        global_result_make_basket = True
    else:
        print("Result result_make_basket UNsuccessfully {}".format(count_items))

    return global_result_make_basket


# send_current_basket_to_order()

# create_resp_is_exist(brand="STELLOX", oem="42140459SX", qnt=2, external_id=451642783)
# get_current_client_smth(basket)

ym_orders = [459439792, 459438203, 459412869, 459372108, 459349047, 459339840, 459295293, 459282888, 459271641,
             459270442, 459234214, 459203644, 459196400, 459188985, 459188686, 459179825, 459170546, 459158382,
             459097786, 459091113, 459086634, 459051043, 459049573, 459048159, 459048159, 459037290, 459007002,
             458955474, 458936875, 458883613, 458811366, 458520720, 458426347, 458355458, 458355264, 458250383,
             458172884]
ym_orders_short = [459439792, 459438203, 459412869, 459372108, 459349047, 459339840, 459295293, 459282888, 459271641]

# get_orders_v2(710, marketplace_id='9009797416999')
# get_orders_v2("2063", marketplace_id="462477099", filter_status=[7, 21, 22, 27])

# get_smth('/regions.json')
# get_smth("/orders.json")
# get_smth("/order_status_types.json")

#  {"id":8,"name":"Выдано","code":"vydano"}

# post_smth()
