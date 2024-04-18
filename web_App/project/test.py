import json
import os

import requests

ozon_wh_id = []

test_data_prod = {
    'result': {
        'id': 312005667,
        'name': 'Камера видеонаблюдения HiWatch DS-T107 (2.8-12)',
        'offer_id': 'hiwatcht107',
        'barcode': 'OZN624116313',
        'buybox_price': '',
        'category_id': 17036196,
        'created_at': '2022-06-22T14:01:23.316153Z',
        'images': [],
        'marketing_price': '3296.0000',
        'min_ozon_price': '',
        'old_price': '4499.0000',
        'premium_price': '',
        'price': '3899.0000',
        'recommended_price': '',
        'min_price': '3899.0000',
        'sources': [],

    },
    'errors': [],
    'vat': '0.200000',
    'visible': True,
    'visibility_details': {
        'has_price': True,
        'has_stock': True,
        'active_product': False
    },
    'price_index': '0.00',
    'commissions': [
        {
            'percent': 15.5,
            'min_value': 0,
            'value': 604.35,
            'sale_schema': 'fbo',
            'delivery_amount': 0,
            'return_amount': 0
        },
        {
            'percent': 16.5,
            'min_value': 0,
            'value': 643.34,
            'sale_schema': 'fbs',
            'delivery_amount': 0,
            'return_amount': 0
        },
        {
            'percent': 16.5,
            'min_value': 0,
            'value': 643.34,
            'sale_schema': 'rfbs',
            'delivery_amount': 0,
            'return_amount': 0
        }
    ],
    'volume_weight': 1,
    'is_prepayment': False,
    'is_prepayment_allowed': True,
    'images360': [],
    'color_image': '',
    'primary_image': 'https://cdn1.ozone.ru/s3/multimedia-q/6356082758.jpg',
    'status': {
        'state': 'price_sent',
        'state_failed': '',
        'moderate_status': 'approved',
        'decline_reasons': [],
        'validation_state': 'success',
        'state_name': 'Продается',
        'state_description': '',
        'is_failed': False,
        'is_created': True,
        'state_tooltip': '',
        'item_errors': [],
        'state_updated_at': '2022-10-21T12:00:46.106007Z'
    },
    'state': '',
    'service_type': 'IS_CODE_SERVICE',
    'fbo_sku': 0,
    'fbs_sku': 0,
    'currency_code': 'RUB',
    'is_kgt': False,
    'discounted_stocks': {
        'coming': 0,
        'present': 0,
        'reserved': 0
    },
    'is_discounted': False,
    'has_discounted_item': False,
    'barcodes': ['OZN624116313'],
    'updated_at': '2024-01-17T11:04:46.795742Z',
    'price_indexes': {
        'price_index': 'NON_PROFIT',
        'external_index_data': {
            'minimal_price': '2112.0000',
            'minimal_price_currency': 'RUB',
            'price_index_value': 1.31
        },
        'ozon_index_data': {
            'minimal_price': '',
            'minimal_price_currency':
                'RUB', 'price_index_value': 0
        },
        'self_marketplaces_index_data': {
            'minimal_price': '',
            'minimal_price_currency': 'RUB',
            'price_index_value': 0
        }
    },
    'sku': 624116311,
    'description_category_id': 17028914,
    'type_id': 95694
}

prod_lp = {"id": 580733565, "name": "Конфеты Raffaello миндаль и кокос, 500 г",
           "offer_id": "LPКонфRaffaelloМинКок500г/1105", "barcode": "OZN1093790544", "buybox_price": "",
           "category_id": 55459914, "created_at": "2023-07-23T16:21:53.415454Z",
           "images": ["https://cdn1.ozone.ru/s3/multimedia-7/6710778619.jpg",
                      "https://cdn1.ozone.ru/s3/multimedia-1/6710778613.jpg",
                      "https://cdn1.ozone.ru/s3/multimedia-4/6710778616.jpg",
                      "https://cdn1.ozone.ru/s3/multimedia-x/6710778609.jpg",
                      "https://cdn1.ozone.ru/s3/multimedia-2/6710778614.jpg"], "marketing_price": "2885.0000",
           "min_ozon_price": "", "old_price": "8876.0000", "premium_price": "", "price": "2885.0000",
           "recommended_price": "", "min_price": "2885.0000", "sources": [],
           "stocks": {"coming": 0, "present": 0, "reserved": 0}, "errors": [], "vat": "0.0", "visible": True,
           "visibility_details": {"has_price": True, "has_stock": False, "active_product": False},
           "price_index": "0.00", "commissions": [
        {"percent": 9.5, "min_value": 0, "value": 274.08, "sale_schema": "fbo", "delivery_amount": 0,
         "return_amount": 0},
        {"percent": 10.5, "min_value": 0, "value": 302.93, "sale_schema": "fbs", "delivery_amount": 0,
         "return_amount": 0},
        {"percent": 10.5, "min_value": 0, "value": 302.93, "sale_schema": "rfbs", "delivery_amount": 0,
         "return_amount": 0},
        {"percent": 10.5, "min_value": 0, "value": 302.93, "sale_schema": "fbp", "delivery_amount": 0,
         "return_amount": 0}], "volume_weight": 2.1, "is_prepayment": False, "is_prepayment_allowed": True,
           "images360": [], "color_image": "", "primary_image": "https://cdn1.ozone.ru/s3/multimedia-3/6710778615.jpg",
           "status": {"state": "price_sent", "state_failed": "", "moderate_status": "approved", "decline_reasons": [],
                      "validation_state": "success", "state_name": "Готов к продаже",
                      "state_description": "Нет на складе", "is_failed": False, "is_created": True,
                      "state_tooltip": "Поставьте товар на склад Ozon или укажите его количество на своем складе",
                      "item_errors": [], "state_updated_at": "2023-07-23T16:35:34.334347Z"}, "state": "",
           "service_type": "IS_CODE_SERVICE", "fbo_sku": 0, "fbs_sku": 0, "currency_code": "RUB", "is_kgt": False,
           "discounted_stocks": {"coming": 0, "present": 0, "reserved": 0}, "is_discounted": False,
           "has_discounted_item": False, "barcodes": ["OZN1093790544"], "updated_at": "2024-01-26T12:10:15.667559Z",
           "price_indexes": {"price_index": "NON_PROFIT",
                             "external_index_data": {"minimal_price": "1975.0000", "minimal_price_currency": "RUB",
                                                     "price_index_value": 1.32},
                             "ozon_index_data": {"minimal_price": "3231.0000", "minimal_price_currency": "RUB",
                                                 "price_index_value": 0.89},
                             "self_marketplaces_index_data": {"minimal_price": "3747.0000",
                                                              "minimal_price_currency": "RUB",
                                                              "price_index_value": 0.77}},
           "sku": 1093790547,
           "description_category_id": 17028773,
           "type_id": 96044}

# from datetime import datetime
#
# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# print(os.getcwd())

# data = {"message_type": "TYPE_NEW_POSTING", "seller_id": 172781, "warehouse_id": 1020001060644000, "posting_number": "46231993-0568-11", "in_process_at": "2024-04-09T05:08:35Z", "products": [{"sku": 1047250917, "quantity": 2}]}

# datas = json.dumps(data)
# print(datas)
def ping(link):
    # data = {"message_type":"TYPE_PING", "time":"123456789"}
    # datas = json.dumps(data)
    # print(datas)
    # header = {
    #     'Client-Id': 1278621,
    #     'Api-Key': '7857dda7-bdb2-4340-9502-3ee73c78118e',
    #     'Content-Type': 'application/json'
    # }
    answer = requests.post(url=link, json=data)
    print(answer.text)


# ping('https://samoesladkoe.i-bots.ru/api/on')
# ping('http://localhost:3000/api/on')
