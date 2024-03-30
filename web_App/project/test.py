import os

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


from datetime import datetime
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


print(os.getcwd())