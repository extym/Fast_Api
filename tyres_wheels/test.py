import csv
import datetime

kolrad_prev_api = {
    "date": "2020-03-19 13:27",
    "portal_name": "b2b.kolrad.ru",
    "currency": "rur", "pages": 6,
    "categories": [
        {
          "id": 5,
          "name": "Литые диски",
          "parent": 0
        },
        {
          "id": 7,
          "name": "Штампованные диски",
          "parent": 0
        },
        {
          "id": 4,
          "name": "Легкогрузовые диски",
          "parent": 0
        },
        {
          "id": 1,
          "name": "Грузовые диски",
          "parent": 0
        },
        {
          "id": 3,
          "name": "Комплектующие",
          "parent": 0
        },
        {
          "id": 2,
          "name": "Датчики давления CUB",
          "parent": 0
        },
        {
          "id": 6,
          "name": "Материалы для шиномонтажа",
          "parent": 0
        },
        {}
    ]
}


new_data_colrad = {
    'code': '00045061',
    'name': '"Евродиск (75J55X) 6,5Jx16H2 5/114,3 ET55 d-64 Silver (UZB) Honda Civic, Accord (03-08)"',
    'type': '"Штампованные диски"',
    'vendor': '"Евродиск"',
    'model': '"75J55X"',
    'width': '"6,5"',
    'diameter': '"x16"',
    'pcd1': '"5"',
    'pcd2': '"114,3"',
    'et': '"55"',
    'dia': '"64,0"',
    'scolor': '"Серебристый"',
    'color': '"Silver"',
    'vendor_code': '"75J55X"',
    'rest': '"0"',
    'rest2': '"3"',
    'rest3': '"0"',
    'sales': '"1"',
    'price': '"850.00"',
    'RoznicaPrice': '"1\xa0029.00"',
    'foto': '""'
}


row_from_get_whells_csv = {
    0: '999048',
    1: 'Legeartis Concept B564 20 / 8.5J PCD 5x112.00 ET 35.00 ЦО 66.60 Литой / Черный с полированной лицевой поверхностью',
    2: '9303903',
    3: 'Legeartis Concept',
    4: 'B564',
    5: 'Литой / Черный с полированной лицевой поверхностью',
    6: 'BFP',
    7: '20 / 8.5J',
    8: '5',
    9: '112',
    10: '0',
    11: '35.00',
    12: '66.60',
    13: '0',
    14: '13000',
    15: '15000',
    16: 'https://www.shinservice.ru/catalog/disk/legeartis_concept/B564.bfp.jpg',
    17: '20',
    18: '20',
    19: '0', 20: '0', 21: '0', 22: '0', 23: '0', 24: '0', 25: '0', 26: '0', 27: '4', 28: '4', 29: '0', 30: '0', 31: '0', 32: '0', 33: '0', 34: '4', 35: '0', 36: '0', 37: '3', 38: '0', 39: '4', 40: '4', 41: '0', 42: '0', 43: '0', 44: '4', 45: '4', 46: '0', 47: '0', 48: '0', 49: '0', 50: '0', 51: '0', 52: '0', 53: '0', 54: '0', 55: '0', 56: '0'}


product_bitrix = {
    'iblockId': 49,
    'id': 302841,
    'name': '225/65R17 102H G Fit EQ+ LK41 TL',
    'property574': {'value': '9630.00', 'valueId': '201473'},
    'property575': {'value': '9630.00', 'valueId': '201474'},
    'property576': None, 'property577': None, 'property578': None,
    'property579': None, 'property580': None, 'property582': None,
    'property583': None, 'property584': None, 'property585': None,
    'property586': None, 'property587': None, 'property588': None,
    'property589': None,
    'property590': {'value': '1033939', 'valueId': '176881'}, # артикул
    'property591': None, 'property592': None, 'property593': None,
    'property594': None, 'property595': None, 'property596': None,
    'property597': None, 'property598': None, 'property599': None,
    'property600': None,
    'property601': {'value': '218', 'valueId': '201475'},  # IS_STOCK
    'property602': None, 'property603': None, 'property604': None,
    'property605': None, 'property606': None, 'property607': None,
    'property608': None, 'property609': None, 'property610': None,
    'property611': None, 'property612': None, 'property613': None,
    'property614': None,
    'property737': {'value': 'Hankook Laufenn', 'valueId': '176882'},
    'property738': {'value': '65', 'valueId': '176884'},
    'property739': {'value': 'G Fit EQ+ LK41', 'valueId': '176883'},
    'property740': {'value': 'R17', 'valueId': '176885'},
    'property741': {'value': '102', 'valueId': '176886'},
    'property742': {'value': 'H', 'valueId': '176887'},
    'property743': {'value': 'Летняя', 'valueId': '176888'},
    'property744': {'value': 'Легковая', 'valueId': '176889'},
    'property745': {'value': '0', 'valueId': '176890'}, #	DIAMETER_OUT
    'property755': {'value': '111', 'valueId': '241390'},  # расстояние между болтами
    'property756': {'value': '55', 'valueId': '241391'},   # вылет
    'property757': {'value': '60', 'valueId': '241392'},  # hole
    'property746': None, 'property747': None, 'property748': None,
    'property749': None,
    'property750': {'value': 'R', 'valueId': '176891'},
    'property751': None, 'property752': None,
    'property753': {'value': '225', 'valueId': '205997'},
    'property754': None,
    'property755': None,
    'property756': None, 'property757': None}

image = {'detailPicture':
             {'id': '98854',
              'url': '/rest/catalog.product.download?fields%5BfieldName%5D=detailPicture&fields%5BfileId%5D=98854'
                     '&fields%5BproductId%5D=302841',
              'urlMachine': '/rest/catalog.product.download?fields%5BfieldName%5D=detailPicture&fields%5BfileId%5D'
                            '=98854&fields%5BproductId%5D=302841'}}


# def rewrite_catagory(category):
#     proxy = {key.upper(): value for key, value in category.items()}
#     print(proxy)
#
# from categories import *
#
# rewrite_catagory(categories_wheels)

prod = 'category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k, params, koeff, meta_h1, provider, category'
def split_prod():
    data = prod.split(", ")
    for row in data:
        print(f'"{row}": {row},')

split_prod()
def read_csv():
    with open('categories_allseason.csv', 'r') as file:
        reader = csv.reader(file)
        data = {i[0].split(";")[3]: int(i[0].split(";")[0]) for i in reader}
        # for i in reader:
        #     print(type(i), i)
        #     data.update({i[3]: i[0]})
    print(data)

# read_csv()