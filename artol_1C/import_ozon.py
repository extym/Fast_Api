import csv
import json
from datetime import datetime
from time import sleep

import pytz
import requests

from cred import api_key_ozon_admin, client_id_onon


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open('/home/userbe/artol/no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    except:
        f = open('no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()

    # return liist

def write_json(string, object):
    with open(f'./cats/{string}.json', 'w') as file:
        json.dump(object, file)

    print(f'file {string}.json writed')

spravka = {'ee': 0, 'err': 1, 'Ваш SKU *': 2, 'Название товара *': 3,
           'Ссылка на изображение *': 4, 'Описание товара *': 5,
           'Категория в вашем магазине *': 6, 'Бренд *': 7, 'Штрихкод *': 8,
           'Страна производства': 9, 'Артикул производителя': 10,
           'Вес с упаковкой, кг': 11, 'Габариты с упаковкой, см': 12,
           'Товар занимает больше одного места': 13, 'Срок годности': 14,
           'Комментарий к сроку годности': 15, 'Срок службы': 16,
           'Комментарий к сроку службы': 17, 'Гарантийный срок': 18,
           'Комментарий к гарантийному сроку': 19, 'Номер документа на товар': 20,
           'Код ТН ВЭД': 21, 'Тип ресейл-товара': 22, 'Внешний вид товара': 23,
           'Описание состояния товара': 24, 'Основная цена': 25, 'Цена до скидки': 26,
           'Особый тип товара': 27, 'С какого возраста пользоваться': 28,
           'Товар для взрослых': 29, 'Характеристики товара': 30,
           'SKU на Маркете': 31}


##get vendor_vode (SKU), name, barcode from price
def read_price(file):
    # with open('./price.csv', 'r') as file:
    with open(file, 'r') as fill:
        count = 0
        product = []
        categories = {}
        reader = csv.reader(fill, delimiter=";")
        for row in reader:
            if row[0] == 'Ошибки' or row[0] == 'ee' or len(row) < 34:
                continue
            else:
                count += 1
                vendor_code = row[2]
                name = row[3]
                image_link = row[4]
                description = row[5]
                brend = row[7]
                barcode = row[8]
                weight = int(float(row[11]) * 1000)
                gabarit = row[12].split('/')
                if len(gabarit) == 3:
                    try:
                        height = str(float(gabarit[1]) * 10).split('.')[0]
                        width = str(float(gabarit[2]) * 10).split('.')[0]
                        depth = str(float(gabarit[0]) * 10).split('.')[0]

                    except:
                        height, width, depth = 100, 100, 100
                else:
                    height, width, depth = 100, 100, 100
                price = row[25]
                price_before = row[26]

                # print('row', len(row), row)
                category_o3on = row[32]
                # print(category_o3on)
                # proxy = {'vendor_code': vendor_code, "name": name, "image_link": image_link,
                # "description": description, "barcode": barcode, "weight": weight,
                # "height": height, "width": width, "depth": depth, "price": price,
                # "price_before": price_before, "category_o3on": category_o3on}

                # print('count', count)
                pro = (vendor_code, name, image_link,
                       description, brend, barcode, weight,
                       height, width, depth, price,
                       price_before, category_o3on)
                product.append(pro)
        print('product', len(product))

        return product


# read_price('assortment_copy-2.csv')
# read_price('asso_Group.csv')


def make_categories():
    list_data = read_price('asso_Group.csv')
    cats = [prod[-1] for prod in list_data]
    cots = set(cats)
    # make dict categories where {category: [products]}
    categories = {category: [pro for pro in list_data if pro[-1] == category] for category in cots}
    print('make_categories', len(categories.keys()))
    crats = [int(num) for num in cots if num != '']  # the list categories
    print('len_categories', len(crats))  # , crats)
    return categories, crats


# make_categories()


headers = {
    "Client-Id": client_id_onon,
    "Api-Key": api_key_ozon_admin
}


def required_cat(cat_id):
    print('rec_cat', cat_id)
    url = 'https://api-seller.ozon.ru/v3/category/attribute'
    data = {
        "attribute_type": "REQUIRED",
        "category_id": [cat_id],
        #   "category_id": cat_id,   #if we get in to func a list
        "language": "DEFAULT"}
    need = {}
    answer = requests.post(url, headers=headers, json=data)
    result = answer.json().get("result")
    print('required_cat', cat_id, type(result))
    if result is not None:
        need = result[0]
    else:
        print('answer-----', answer.text)

    return need


# required_cat(17033420)

# get attributes for all categories
def create_list_attr():
    data = make_categories()
    need_list = data[1]
    cats = []
    for i in range(len(need_list)):
        result = required_cat(need_list[i])
        sleep(1)
        if result is not None:
            cats.append(result)
            print('create_list_attr', len(cats))

    with open('attributes.json', 'w') as file:
        json.dump(cats, file)

    crats = {row["category_id"]: row['attributes'] for row in cats}
    with open('atts.json', 'w') as file:
        json.dump(crats, file)

    print(f'write {len(cats)} attributes')
    print(f'write 2 {len(crats)} attributes')


# create_list_attr()

# get values attributes
def get_cat_value(id, cat_id, last_value_id):
    url = 'https://api-seller.ozon.ru/v2/category/attribute/values'
    datas = {
        "attribute_id": id,
        "category_id": cat_id,
        "language": "DEFAULT",
        "last_value_id": last_value_id,
        "limit": 5000
    }
    answer = requests.post(url, headers=headers, json=datas)
    result = answer.json()
    if result.get('result') is None:
        print('----------aswer', id, cat_id, last_value_id, answer.text)
    return result


def create_cats_value():
    with open('attributes.json', 'r') as read_file:
        list_cats = json.load(read_file)
        our_res = []
        count = 0
        for cat in list_cats:
            id_cat = cat['category_id']
            attributes = cat.get("attributes")
            if attributes is not None:
                for attr in attributes:
                    at_id = attr['id']
                    dictionary_id = attr['dictionary_id']
                    proxy = []
                    # if dictionary_id != 0 and at_id != 0:
                    if at_id != 0 and at_id != 9048:
                        sleep(1)
                        value = get_cat_value(at_id, id_cat, 0)
                        result = value.get('result')
                        has_next = value.get('has_next')
                        if at_id == 85:
                            while has_next is True:
                                proxy.extend(result)
                                print(has_next)
                                if len(result) > 0:
                                    last_id = result[-1]['id']
                                    value = get_cat_value(at_id, id_cat, last_id)
                                    result = value.get('result')
                                    has_next = value.get('has_next')
                                print('create_cats_value', len(proxy))

                            proxy.extend(result)
                            with open(f'./cats/{id_cat}-attr.json', 'w') as write_file:
                                json.dump(proxy, write_file)
                            count += 1
                            print(has_next, 'count', count, 'maybe_write', len(proxy), id_cat)
                        elif at_id != 85:
                            our_res = {id_cat: [at_id, result[:5]]}

                            continue
                    else:
                        continue


# create_cats_value()



def read_attr(category_id):
    try:
        with open(f'./cats/{category_id}-attr.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = None
        print(F'ERROR_READ_FILE ./cats/{category_id}-attr.json')

    return data


def get_attr_value(id_cat, brend):
    with open('atts.json', 'r') as read_file:
        dict_cats = json.load(read_file)
        attributes = dict_cats.get(id_cat)
        res = []
        if attributes is not None:
            for attr in attributes:
                at_id = attr['id']
                dictionary_id = attr['dictionary_id']
                proxy = []
                # if dictionary_id != 0 and at_id != 0:
                if at_id != 0:
                    sleep(1)
                    value = get_cat_value(at_id, id_cat, 0)
                    result = value.get('result')
                    has_next = value.get('has_next')
                    if at_id == 85:
                        try:
                            proxy = read_attr(id_cat)
                        except:
                            while has_next is True:
                                proxy.extend(result)
                                if len(result) > 0:
                                    last_id = result[-1]['id']
                                    value = get_cat_value(at_id, id_cat, last_id)
                                    result = value.get('result')
                                print('fack_debug', len(proxy))
                                has_next = False
                            with open(f'./cats/{id_cat}-attr.json', 'w') as write_file:
                                json.dump(proxy, write_file)

                        for row in proxy:
                            if row['value'].lower() == brend.lower():
                                result_brend = row
                            elif brend != '':
                                result_brend = {"id": 126745801, "value": brend}
                            else:
                                result_brend = {"id": 126745801, "value": 'Нет бренда'}
                        result_g = {id_cat: [at_id, [result_brend]]}
                        res.append(result_g)
                        continue
                    elif at_id != 85:
                        if result is not None:
                            our_res = {id_cat: [at_id, result[:5]]}
                        else:
                            our_res = {id_cat: [at_id, [{'id':0}]]}
                        res.append(our_res)
                        # print(id_cat, len(our_res))

                else:
                    continue
            # break        17029512
    # {id_cat: {at_id: result_brend}}, {id_cat: {at_id: result[:5]}}
    return res


# create_cats_value('string_prod_name_vendor')

def send_data(items):
    url = 'https://api-seller.ozon.ru/v2/product/import'
    answer = requests.post(url, headers=headers, json=items)
    result = answer.json().get('result')
    if result is not None:
        print('result_SEND', result)
        write_smth(str(result))
        write_json(result['task_id'], items)
    else:
        print(answer.text)
        write_smth(answer.text)


def make_send_data():
    data_prod_from_cats = make_categories()[0]  # data products in categories
    with open('atts.json', 'r') as file:
        attributes = json.load(file)  # list dictionary {'category': [{"id": 85, "name": "\'}]
        itemses = []
        for key, value in attributes.items():
            if key != '17029512':  # FOR TEST - SEND ONE CATEGORY PRODUCTS
                product_group = data_prod_from_cats[key]  # list product from the category
                for product in product_group:
                    link_str = product[2]
                    links = ['https:' + str(st) for st in link_str.split(',')]
                    attr = []
                    brend_prod = product[4]
                    values = get_attr_value(key, brend_prod)  # [{id_cat: [at_id: [value]]}]
                    for val in values:
                        for k, v in val.items():
                            if v[0] != 9048:
                                at = {
                                    "complex_id": 0,
                                    "id": v[0],
                                    "values": [
                                        {
                                            "dictionary_value_id": v[1][0]['id'],
                                            "value": v[1][0].get('value')
                                        }
                                    ]
                                }
                                attr.append(at)
                            elif v[0] == 9048:
                                at = {
                                    "complex_id": 0,
                                    "id": v[0],
                                    "values": [
                                        {
                                            "value": product[1]
                                        }
                                    ]
                                }
                                attr.append(at)
                    data = [
                        {
                            "attributes": attr,
                            "barcode": str(product[5]),
                            "category_id": key,
                            "color_image": "",
                            "complex_attributes": [],
                            "currency_code": "RUB",
                            "depth": product[9],
                            "dimension_unit": "mm",
                            "height": product[7],
                            "images": links,  #[],
                            "images360": [],
                            "name": product[1],
                            "offer_id": product[0],
                            "old_price": product[11],
                            "pdf_list": [],
                            "premium_price": "",
                            "price": product[10],
                            "primary_image": "",
                            "vat": "0.2",
                            "weight": str(product[6]),
                            "weight_unit": "g",
                            "width": str(product[8])
                        }
                    ]
                    items_send = {"items": itemses}

                    if len(itemses) < 100:
                        itemses.extend(data)

                    else:
                        print('SEND_DATA', items_send)
                        send_data(items_send)
                        print('len+ITEMS_2', len(itemses))
                        itemses.clear()
                        continue

                # items_send = {"items": itemses}
                print('SEND_DATA_2', len(itemses), items_send)
                send_data(items_send)
                itemses.clear()


# create_list_attr()
make_send_data()
