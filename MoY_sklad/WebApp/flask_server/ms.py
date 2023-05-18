"""
MoySklad lib
"""
import sys
from typing import Dict, Union, List, Tuple, Any
import requests
import datetime
import logging
import time
import json
import base64
import os
from settings import TRY, MS_HEADERS, SLEEP_TIME, MS_LAST_DOCUMENTS


def requests_get(url, headers=MS_HEADERS):
    i = 0
    resp = None
    while i < TRY:
        try:
            resp = requests.get(url, headers=headers)
        except:
            logging.warning('Error making GET request to MS, try again')
            time.sleep(SLEEP_TIME)
            i += 1
        else:
            break
    return resp


def get_entity_meta(entity="organization"):
    """
    Получения meta словарей для сщуностей для последующего их использования в запросах
    entity =
        organization - Наши организации
        counterparty - Контрагенты
        customerorder - Заказы
        country
        store
    """
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/{entity}"
    resp = requests_get(url)
    # print(resp.text)
    res_dict = json.loads(str(resp.text))
    return res_dict['rows']


def get_products_info_list(sum=None) -> List:
    """
    Поулчение всех всех товаров из МС со словарем нужных данных
    """
    limit = 1000
    offset = 0
    size = 1001
    res = []
    i = 0
    while offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/product?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        try:
            res_dict = json.loads(str(resp.text))
        except:
            logging.info('Empty json from api request to MS')
            continue
        # print(resp.text)
        size = res_dict['meta']['size']
        # print(size)
        for elem in res_dict['rows']:
            # print(elem)
            res.append(elem)
            i += 1
            if i >= sum:
                size = 0
                break
        offset += 1000
    return res


def get_products_stock():
    """
    Поулчение остатков
    """
    limit = 1000
    offset = 0
    size = 1001
    res = {}
    while offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/report/stock/all?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        try:
            res_dict = json.loads(str(resp.text))
        except:
            logging.info('Empty json from api request to MS')
            continue
        # print(resp.text)
        size = res_dict['meta']['size']
        for elem in res_dict['rows']:
            print(elem)
            if 'meta' not in elem or 'stockByStore' not in elem:
                continue
            # href = elem['meta'].get('href')
            # id = href.split('/')[-1].split('?')[0]
            # if id:
            #     res[id] = {}
            #     res[id]['id'] = id
            #     for key in MS_STOCKS:
            #         res[id][MS_STOCKS[key] + "_stock"] = None
            #         res[id][MS_STOCKS[key] + "_reserve"] = None
            #         res[id][MS_STOCKS[key] + "_transit"] = None
            #     for stock in elem['stockByStore']:
            #         if 'meta' not in stock:
            #             continue
            #         stock_href = stock['meta'].get('href')
            #         if stock_href and stock_href in MS_STOCKS:
            #             res[id][MS_STOCKS[stock_href] + "_stock"] = int(stock['stock'])
            #             res[id][MS_STOCKS[stock_href] + "_reserve"] = int(stock['reserve'])
            #             res[id][MS_STOCKS[stock_href] + "_transit"] = int(stock['inTransit'])
            else:
                logging.info('Empty id in stock request in MS')

        offset += 1000
    return res


def get_product_by_code(code: str) -> str:
    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/assortment?filter=article={code}"
    resp = requests_get(request_url)
    if resp:
        try:
            res_dict = json.loads(str(resp.text))
            # print(res_dict)
            product = res_dict['rows'][0]['meta']['href']
            return product
        except:
            pass
    return None


def get_states_id_name_meta() -> List:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata"
    resp = requests_get(url)
    # print(resp.text)
    res = []
    try:
        res_list = json.loads(str(resp.text))['states']
    except:
        return res
    for elem in res_list:
        res.append([elem['id'], elem['name'], elem['meta']])
    return res


def get_prices_id_name_meta() -> List:
    url = f"https://online.moysklad.ru/api/remap/1.2/context/companysettings/pricetype"
    resp = requests_get(url)
    # print(resp.text)
    # return
    res = []
    try:
        res_list = json.loads(str(resp.text))
    except:
        return res
    for elem in res_list:
        res.append([elem['id'], elem['name'], elem['meta']])
    return res


def get_contragents() -> Dict:
    limit = 1000
    offset = 0
    size = 1001
    res = {}
    i = 0
    while limit + offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        try:
            res_dict = json.loads(str(resp.text))
            size = res_dict['meta']['size']
            rows = res_dict['rows']
        except:
            break
        for row in rows:
            name = row['name']
            meta = row['meta']
            res[name] = meta
        offset += 1000

    return res


def get_organizations():
    offset = 0
    res = {}

    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/organization?limit=10&offset={offset}"
    resp = requests_get(request_url)
    try:
        res_dict = json.loads(str(resp.text))
        rows = res_dict['rows']
    except:
        return res
    for row in rows:
        name = row['name']
        meta = row['meta']
        res[name] = meta

    return res


def get_entity_id_name_meta(entity='organization'):
    """
    organization, counterparty
    res = [[id: str, name: str, meta: Dict]]
    """
    limit = 1000
    offset = 0
    size = 1001
    res = []
    i = 0
    while offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/{entity}?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        # print(resp)
        try:
            res_dict = json.loads(str(resp.text))
            size = res_dict['meta']['size']
            rows = res_dict['rows']
        except:
            break
        for row in rows:
            res.append([row['id'], row['name'], row['meta']])
        offset += 1000
        # print(size, limit, offset)

    return res


def get_small_products_list(sum=None) -> List:
    """
    Поулчение всех всех товаров из МС со словарем нужных данных
    """
    limit = 1000
    offset = 0
    size = 1001
    res = []
    i = 0
    while offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/product?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        try:
            res_dict = json.loads(str(resp.text))
        except:
            logging.info('Empty json from api request to MS')
            continue
        # print(resp.text)
        size = res_dict['meta']['size']
        # print(size)
        for elem in res_dict['rows']:
            # print(elem)
            # barcodes = ''
            # barcodes_list = elem.get('barcodes')
            # if barcodes_list:
            #     for barcode in barcodes_list:
            res.append([elem['id'], elem['name'], elem.get('code'), elem.get('article'), elem.get('barcodes')])
            i += 1
            if sum and i >= sum:
                size = 0
                break
        offset += 1000
    return res


def get_small_service_list(sum=None) -> List:
    limit = 1000
    offset = 0
    size = 1001
    res = []
    i = 0
    while offset < size:
        request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/service?limit={limit}&offset={offset}"
        resp = requests_get(request_url)
        try:
            res_dict = json.loads(str(resp.text))
        except:
            logging.info('Empty json from api request to MS')
            continue
        # print(resp.text)
        size = res_dict['meta']['size']
        # print(size)
        for elem in res_dict['rows']:
            # print(elem)
            # barcodes = ''
            # barcodes_list = elem.get('barcodes')
            # if barcodes_list:
            #     for barcode in barcodes_list:
            res.append([elem['id'], elem['name'], elem.get('code'), elem.get('article'), elem.get('barcodes')])
            i += 1
            if sum and i >= sum:
                size = 0
                break
        offset += 1000
    return res


def make_products_meta(products: List[Dict], reserve: bool = False):
    """
    products = {price, quantity, href}
    "positions": [{
                "quantity": 10,
                "price": 100,
                "discount": 0,
                "vat": 0,
                "assortment": {
                  "meta": {
                    "href": "https://online.moysklad.ru/api/remap/1.2/entity/product/8b382799-f7d2-11e5-8a84-bae5000003a5",
                    "type": "product",
                    "mediaType": "application/json"
                  }
                },
                "reserve": 10
              }]
    """
    for i in range(len(products)):
        mshref = "https://online.moysklad.ru/api/remap/1.2/entity/product/" + products[i]['href']
        price = products[i]['price'] * 100
        quantity = products[i]['quantity']
        if reserve:
            reserve_num = quantity
        else:
            reserve_num = 0
        products[i] = {
                "quantity": quantity,
                "price": price,
                "discount": 0,
                "vat": 0,
                "assortment": {
                  "meta": {
                    "href": mshref,
                    "type": "product",
                    "mediaType": "application/json"
                  }
                },
                "reserve": reserve_num
        }
    return products


def make_service_meta(service: Dict):
    mshref = "https://online.moysklad.ru/api/remap/1.2/entity/service/" + service['href']
    price = service['price'] * 100
    quantity = service['quantity']
    return {
            "quantity": quantity,
            "price": price,
            "discount": 0,
            "vat": 0,
            "assortment": {
              "meta": {
                "href": mshref,
                "type": "service",
                "mediaType": "application/json"
              }
            }
    }


def post_order(contragent, products_meta, organization, comment, posting_number, store=None, project=None, sticker=None, moment=None, contract=None, status=None):
    url = "https://online.moysklad.ru/api/remap/1.2/entity/customerorder"

    data = {
        # "name": name,
        "description": comment,
        "positions": products_meta,
        "organization": {"meta": organization},
        "agent": {"meta": contragent},
        "vatEnabled": False,
    }
    if status:
        data['state'] = status
    if store:
        data['store'] = store
    if project:
        data['project'] = project
    if contract:
        data['contract'] = contract

    data['attributes'] = [
        {
            "meta": {
              "href" : "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/a1832bb9-7d66-11ea-0a80-02160017f08f",
              "type" : "attributemetadata",
              "mediaType" : "application/json"
            },
            "id": "a1832bb9-7d66-11ea-0a80-02160017f08f",
            "name": "Наша доставка",
            "type": "boolean",
            "value": True
        },
        {
            "meta": {
                "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/97ee826a-7d81-11ea-0a80-05b3001acb71",
                "type": "attributemetadata",
                "mediaType": "application/json"
            },
            "id": "97ee826a-7d81-11ea-0a80-05b3001acb71",
            "name": "Адрес",
            "type": "string",
            "value": posting_number
        }
    ]

    if sticker: #FIXME cc92ab9e-bed1-11.....
        data['attributes'].append({
          "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/cc92ab9e-bed1-11eb-0a80-006a00090059",
            "type": "attributemetadata",
            "mediaType": "application/json"
          },
          "value": sticker
        })

    if moment:
        # data['deliveryPlannedMoment'] = moment
        data['attributes'].append({
          "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/a1832f31-7d66-11ea-0a80-02160017f090",
            "type": "attributemetadata",
            "mediaType": "application/json"
          },
          "value": moment
        })

    # print(data) #FIXME
    # return

    resp = requests.post(url, headers=MS_HEADERS, json=data)
    # print(resp.text)
    res_dict = json.loads(resp.text)
    if resp.ok:
        logging.info(f"MS ok add lead {res_dict['name']}") #FIXME
        return res_dict['name'], res_dict['id']
    # print(resp.text)
    logging.warning(res_dict)
    logging.warning(data['moment'])
    return None, None


def get_opt_product_price(href: str) -> float:
    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/product/{href}"
    resp = requests_get(request_url)
    # print(resp.text)
    if resp:
        try:
            res_dict = json.loads(str(resp.text))
            # print(res_dict)
        except:
            return 0
        for price in res_dict['salePrices']:
            if price['priceType']['id'] == "0f5aaccb-e802-4ddd-9c3b-6dabf7525226":
                return price['value'] / 100
    return 0


def get_product_price(href: str, price_id: str) -> float:
    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/product/{href}"
    resp = requests_get(request_url)
    # print(resp.text)
    if resp:
        try:
            res_dict = json.loads(str(resp.text))
            # print(res_dict)
        except:
            return 0
        for price in res_dict['salePrices']:
            if price['priceType']['id'] == price_id:
                return price['value'] / 100
    return 0


def get_usluga_price(href: str) -> str:
    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/service/{href}"
    resp = requests_get(request_url)
    # print(resp.text)
    if resp:
        try:
            res_dict = json.loads(str(resp.text))
            # print(res_dict)
            return res_dict['minPrice']['value'] / 100
        except:
            return 0
    return 0


def post_order_file(order_href: str, file_path: str) -> bool:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}/files"

    filename = file_path.split('/')[-1]
    with open(file_path, 'rb') as outfile:
        res_content = outfile.read()
    res = base64.b64encode(res_content)
    content = res.decode()

    data = [{
        "filename": filename,
        "content": content
    }]
    resp = requests.post(url, headers=MS_HEADERS, json=data)
    # print(resp.text)
    if resp.ok:
        logging.info(f"MS ok add {filename} to {order_href}")
        return True
    # print(resp.text)
    logging.warning(f"MS KO add {filename} to {order_href}")
    return False


def get_last_orders_w_demand(search_limit=MS_LAST_DOCUMENTS) -> set: #TODO - make filter by date
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand?order=updated,desc&limit={search_limit}"
    resp = requests_get(url)
    res = set()
    if not resp.ok:
        return res
    try:
        res_list = json.loads(str(resp.text))['rows']
    except:
        return res
    # print(resp.text)
    for elem in res_list:
        # print(elem['created'])
        if 'customerOrder' in elem:
            res.add(elem['customerOrder']['meta']['href'].split('/')[-1])

    return res


def update_order_comment(order_href: str, comment_copy: str) -> bool:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}"
    data = {
        "description": comment_copy
    }
    resp = requests.put(url, headers=MS_HEADERS, json=data)
    if resp.ok:
        return True
    return False


def update_order_status(order_href: str, status_href: str):
    """
    'state': {
                    "meta": {
                        "href": f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/{status_fbs}",
                        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
                        "type": "state",
                        "mediaType": "application/json"
                    }
                }
    """
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}"
    data = {
        'state': {
                    "meta": {
                        "href": f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/{status_href}",
                        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
                        "type": "state",
                        "mediaType": "application/json"
                    }
                }
    }
    resp = requests.put(url, headers=MS_HEADERS, json=data)
    if resp.ok:
        return True
    return False


def get_order_attributes(order_id: str, attributes: List) -> Dict:
    """
    attributes - list of attribute id's
    """
    res = {i: None for i in attributes}

    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_id}"
    resp = requests_get(request_url)
    try:
        res_dict = json.loads(str(resp.text))
        order_attributes = res_dict["attributes"]
    except:
        return res
    for row in order_attributes:
        if row['id'] in attributes:
            res[row['id']] = row['value']

    return res


def get_order_params_and_attributes(order_id: str, params: List = [], attributes: List = []) -> Dict:
    """
    attributes - list of attribute id's
    """
    res = {i: None for i in attributes + params}

    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_id}"
    resp = requests_get(request_url)
    try:
        res_dict = json.loads(str(resp.text))
        order_attributes = res_dict.get("attributes")
    except:
        return res
    if params:
        for key in res_dict:
            if key in params:
                res[key] = res_dict[key]
    if attributes and order_attributes:
        for row in order_attributes:
            if row['id'] in attributes:
                res[row['id']] = row['value']

    return res


def get_demand_params_and_attributes(demand_id: str, params: List = [], attributes: List = []) -> Dict:
    """
    attributes - list of attribute id's
    """
    res = {i: None for i in attributes + params}

    request_url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand/{demand_id}"
    resp = requests_get(request_url)
    # print(resp.text)
    try:
        res_dict = json.loads(str(resp.text))
        order_attributes = res_dict.get("attributes")
    except:
        return res
    if params:
        for key in res_dict:
            if key in params:
                res[key] = res_dict[key]
    if attributes and order_attributes:
        for row in order_attributes:
            if row['id'] in attributes:
                res[row['id']] = row['value']

    return res


def get_demand_template(order_href: str) -> Dict:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand/new"
    data = {
            "customerOrder": {
              "meta": {
                "href": f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}",
                "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
                "type": "customerorder",
                "mediaType": "application/json"
              }
            }
          }
    resp = requests.put(url, headers=MS_HEADERS, json=data)
    try:
        return json.loads(str(resp.text))
    except:
        return {}


def post_demand(demand_dict: Dict) -> bool:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand"
    resp = requests.post(url, headers=MS_HEADERS, json=demand_dict)
    print(resp.text)
    return resp.ok


def post_demand_v2(demand_dict: Dict, state_href=None) -> bool:
    if state_href:
        demand_dict['state'] = {
            "meta" : {
              "href" : f"https://online.moysklad.ru/api/remap/1.2/entity/demand/metadata/states/{state_href}",
              "metadataHref" : "https://online.moysklad.ru/api/remap/1.2/entity/demand/metadata",
              "type" : "state",
              "mediaType" : "application/json"
            }
          }
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand"
    resp = requests.post(url, headers=MS_HEADERS, json=demand_dict)
    # print(resp.text)
    return resp.ok


def get_order_files(order_href: str) -> Dict:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}/files"
    resp = requests_get(url)
    res = {}
    try:
        raw_res = json.loads(str(resp.text))['rows']
    except:
        return res
    for elem in raw_res:
        try:
            href = elem['meta']['href'].split('/')[-1]
            res[elem['title']] = href
        except:
            continue
    return res


def delete_order_file(order_href: str, file_href: str) -> str:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/{order_href}/files/{file_href}"
    resp = requests.delete(url, headers=MS_HEADERS)
    # print(resp.text)
    if resp.ok:
        return 'ok'
    try:
        res = json.loads(str(resp.text))['errors'][0]['error']
    except:
        res = 'error'
    return res


def update_entity_main_param(entity: str, entity_href: str, param_name: str, param_value) -> bool:
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/{entity}/{entity_href}"
    data = {
        param_name: param_value
    }
    resp = requests.put(url, headers=MS_HEADERS, json=data)
    if resp.ok:
        return True
    return False


def get_contragent_orders(contargent_href: str, date_from: datetime = None, date_to: datetime = None) -> set:
    """
    2018-01-01 00:00:00
    """
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/demand?filter=agent=https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{contargent_href}"
    if date_from:
        url += f"&filter=updated>{date_from.strftime('%Y-%m-%d')} 00:00:01"
    if date_to:
        url += f"&filter=updated<{date_to.strftime('%Y-%m-%d')} 23:59:59"

    resp = requests_get(url)
    res = set()
    if not resp.ok:
        return res
    try:
        res_list = json.loads(str(resp.text))['rows']
    except:
        return res
    # print(resp.text)
    for elem in res_list:
        # print(elem['created'])
        if 'customerOrder' in elem:
            res.add(elem['customerOrder']['meta']['href'].split('/')[-1])

    return res