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

prod_wb = {'nmID': 225359889,
           'imtID': 202837256,
           'nmUUID': '018ef325-60c8-753c-b27e-2332fd6a82d2',
           'subjectID': 3441,
           'subjectName': 'Напитки газированные',
           'vendorCode': 'ССЕгНаи3ГазиНапиIRNBRUп330млExt/255',
           'brand': 'IRN-BRU',
           'title': 'Набор из 3 газированных напитков по 330 мл (Extra)',
           'description': 'Набор из 3 газированных напитков IRN-BRU по 330 мл (Extra) IRN-BRU - '
                          'напиток №1 в Шотландии. Он прочно занимает место в сердцах людей'
                          ' и так же широко известен, как «Национальный Напиток Шотландии» .'
                          ' В 1889 году был запущен BARRS IRON-BREW, содержащий в себе'
                          ' 32 ингредиента, включая железо в своем составе. '
                          'Журнал The Grocer признал IRN-BRU самым популярным онлайн FMCG'
                          ' брендом в Великобритании. Секретный состав IRN-BRU знают '
                          'только три человека в мире: наследники создателя компании '
                          'Робин и Джули Барр, а также один из членов правления.'
                          ' Так же хорошо, как и в России, IRN-BRU продается на многих '
                          'рынках, включая США, Канаду, Европу, Австралию и Объединенные '
                          'Арабские Эмираты.',
           'dimensions': {'width': 10, 'height': 10, 'length': 30},
           'characteristics': [{'id': 14177451, 'name': 'Страна производства', 'value': ['Великобритания']},
                               {'id': 128711, 'name': 'Степень газирования воды', 'value': ['Среднегазированная']},
                               {'id': 85571, 'name': 'Упаковка', 'value': ['Жестяная банка', 'Картонная коробка']},
                               {'id': 378533, 'name': 'Комплектация', 'value': ['3']},
                               {'id': 15000001, 'name': 'ТНВЭД', 'value': ['2202100000']},
                               {'id': 126208, 'name': 'Срок годности', 'value': ['365']},
                               {'id': 14177450, 'name': 'Состав', 'value': ['Указан на упаковке']},
                               {'id': 88952, 'name': 'Вес товара с упаковкой (г)', 'value': 1010},
                               {'id': 116713, 'name': 'Минимальная температура хранения', 'value': ['0']},
                               {'id': 63669, 'name': 'Объем (мл)', 'value': 990},
                               {'id': 113701, 'name': 'Вкус', 'value': ['Экстра']},
                               {'id': 88927, 'name': 'Пищевая ценность углеводы', 'value': 1},
                               {'id': 179792, 'name': 'Количество предметов в упаковке', 'value': ['3']},
                               {'id': 94785, 'name': 'Особенности продукта', 'value': ['Натуральный продукт']},
                               {'id': 88930, 'name': 'Энергетическая ценность калории (на 100 гр.)', 'value': 1},
                               {'id': 15001405, 'name': 'Ставка НДС', 'value': ['0']},
                               {'id': 59623, 'name': 'Тип подарка', 'value': ['На праздник']},
                               {'id': 88928, 'name': 'Пищевая ценность белки', 'value': 1},
                               {'id': 116714, 'name': 'Максимальная температура хранения', 'value': ['25']}],
           'sizes': [{'chrtID': 357063925, 'techSize': '0', 'wbSize': '', 'skus': ['2039857435947']}],
           'createdAt': '2024-04-18T21:38:21.374243Z',
           'updatedAt': '2024-04-18T22:12:47.022969Z'}

prod_wb_photo = {'nmID': 225634469,
                 'imtID': 203076613,
                 'nmUUID': '018ef88b-4ade-799c-89d5-ce8b54e356cd',
                 'subjectID': 3149,
                 'subjectName': 'Оливки',
                 'vendorCode': 'ВВНаОлиEcoGreeceХалЗелСК250г1шт/395',
                 'brand': 'EcoGreece',
                 'title': 'Оливки Халкидики зеленые с косточкой, 250 г',
                 'description': 'Оливки EcoGreece Халкидики зеленые с косточкой, 250 г Уникальный вкус '
                                'оливокHalkidikiдостигается благодаря проверенным временем рецептам их приготовления '
                                '- их маринуют в слабом растворе морской соли с добавлением традиционных греческих '
                                'специй. Обладая сочной мякотью и легко отделяемой косточкой, '
                                'оливки Халкидикисервируются как отличная закуска, в том числе к коктейлям, '
                                'превосходный ингредиент для салатов и замечательное дополнение к другим блюдам. '
                                'Оливки богаты витаминами группы В (рибофлавином, тиамином, ниацином, пантотеновой '
                                'кислотой, пиридоксином), также фолиевой кислотой; в них содержится витамин Е, '
                                'в меньшей степени А. Они являются антиоксидантами, участвуют в борьбе со свободными '
                                'радикалами. В оливках содержатся микроэлементы: натрий, кальций, калий, магний, '
                                'фосфор, медь, железо, цинк, селен. Также оливки богаты ненасыщенными жирными '
                                'кислотами: олеиновой, линолевой.',
                 'photos': [{'big': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/big/1.jpg',
                             'c246x328': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c246x328/1.jpg',
                             'c516x688': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c516x688/1.jpg',
                             'square': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/square/1.jpg',
                             'tm': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/tm/1.jpg'},
                            {'big': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/big/2.jpg',
                             'c246x328': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c246x328/2.jpg',
                             'c516x688': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c516x688/2.jpg',
                             'square': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/square/2.jpg',
                             'tm': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/tm/2.jpg'},
                            {'big': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/big/3.jpg',
                             'c246x328': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c246x328/3.jpg',
                             'c516x688': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/c516x688/3.jpg',
                             'square': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/square/3.jpg',
                             'tm': 'https://basket-15.wbbasket.ru/vol2256/part225634/225634469/images/tm/3.jpg'}],
                 'dimensions': {'width': 10, 'height': 10, 'length': 30},
                 'characteristics': [{'id': 116713, 'name': 'Минимальная температура хранения', 'value': ['0']},
                                     {'id': 59623, 'name': 'Тип подарка', 'value': ['На праздник']},
                                     {'id': 88929, 'name': 'Пищевая ценность жиры', 'value': 18},
                                     {'id': 88928, 'name': 'Пищевая ценность белки', 'value': 2},
                                     {'id': 88952, 'name': 'Вес товара с упаковкой (г)', 'value': 270},
                                     {'id': 59611, 'name': 'Назначение подарка',
                                      'value': ['Родным', 'Маме', 'Бабушке']},
                                     {'id': 378533, 'name': 'Комплектация', 'value': ['1']},
                                     {'id': 14177451, 'name': 'Страна производства', 'value': ['Греция']},
                                     {'id': 88930, 'name': 'Энергетическая ценность калории (на 100 гр.)',
                                      'value': 183}, {'id': 15001405, 'name': 'Ставка НДС', 'value': ['0']},
                                     {'id': 59615, 'name': 'Повод',
                                      'value': ['На праздник', 'На Новый Год', 'На день рождения']},
                                     {'id': 94785, 'name': 'Особенности продукта', 'value': ['Натуральный продукт']},
                                     {'id': 14177450, 'name': 'Состав', 'value': ['Указан на упаковке']},
                                     {'id': 88927, 'name': 'Пищевая ценность углеводы', 'value': 4},
                                     {'id': 116714, 'name': 'Максимальная температура хранения', 'value': ['25']},
                                     {'id': 85571, 'name': 'Упаковка',
                                      'value': ['Картонная коробка', 'Вакуумная упаковка']},
                                     {'id': 89008, 'name': 'Вес товара без упаковки (г)', 'value': 250},
                                     {'id': 126208, 'name': 'Срок годности', 'value': ['240']}],
                 'sizes': [{'chrtID': 357416295, 'techSize': '0', 'wbSize': '', 'skus': ['2039863176759']}],
                 'createdAt': '2024-04-19T22:47:50.744639Z', 'updatedAt': '2024-04-19T22:50:54.412964Z'}


# from datetime import datetime
#
# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# print(os.getcwd())


# datas = json.dumps(data)
# print(datas)
def ping(link):
    data = {"message_type": "TYPE_NEW_POSTING", "seller_id": 172781,
            "warehouse_id": 1020001060644000,
            "posting_number": "46231993-0568-11",
            "in_process_at": "2024-04-09T05:08:35Z",
            "products": [{"sku": 1047250917, "quantity": 2}]}
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
