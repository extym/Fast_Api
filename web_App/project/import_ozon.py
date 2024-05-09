import csv
import json
import os
import time
from datetime import datetime
from time import sleep

import psycopg2
import pytz
import requests
import sqlalchemy
from sqlalchemy.orm import Session

from project.bot_tg import send_get
from project.models import *
from project.creds import *
from project.database import Data_base_connect as Db
from sqlalchemy import insert, create_engine, select, update, text
from project import engine
import traceback  # Used for printing the full traceback | Better for debug.
from psycopg2 import errors
from psycopg2._psycopg import IntegrityError

UniqueViolation = errors.lookup('23505')


# engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")


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


headers_stm = {
    "Client-Id": client_id_onon_stm,
    "Api-Key": api_key_ozon_admin_stm
}

headers_artol = {
    "Client-Id": client_id_oson_artol,
    "Api-Key": api_key_oson_prod_artol
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
                            our_res = {id_cat: [at_id, [{'id': 0}]]}
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
                            "images": links,  # [],
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


def get_product_list():
    metod = 'https://api-seller.ozon.ru/v2/product/list'
    last_id = ""
    data = {
        "filter": {
            "visibility": "ALL"
        },
        "last_id": "",
        "limit": 1000
    }
    answer = requests.post(url=metod, headers=headers_artol, json=data)
    assortment = answer.json()
    # print(answer.text)

    return assortment.get('result').get('items')


def get_product_list_v2(seller_id=None, shop_name=None, company_id=None):
    metod = 'https://api-seller.ozon.ru/v2/product/list'
    stmt, row, items = [], [], []
    if seller_id:
        stmt = select(Marketplaces.key_mp, Marketplaces.shop_name) \
            .where(Marketplaces.seller_id == seller_id).where(Marketplaces.company_id == company_id)
    elif shop_name:
        stmt = select(Marketplaces.key_mp, Marketplaces.shop_id) \
            .where(Marketplaces.shop_name == shop_name).where(Marketplaces.company_id == company_id)
    with Session(engine) as session:
        row = session.execute(stmt).first()
    # os.abort()
    if row:
        api_key = row[0]
    else:
        api_key = ''
    headers = {
        "Client-Id": seller_id,
        "Api-Key": api_key
    }
    last_id = ""
    requesting = True
    count = 0
    while requesting:
        data = {
            "filter": {
                "visibility": "ALL"
            },
            "last_id": last_id,
            "limit": 1000
        }
        try:
            answer = requests.post(url=metod, headers=headers, json=data)
            if answer.ok:
                assortment = answer.json()
                proxy = assortment.get('result').get('items')
                last_id = assortment.get('result').get('last_id')
                if len(proxy) > 999:
                    items.extend(proxy)
                    print(888888888888888, len(items))
                else:
                    requesting = False
                    items.extend(proxy)
            else:
                print('We are sleep and got {}'.format(answer.text))
                try:
                    data = json.loads(answer.text)
                    if data.get('code') == 7 and data.get('message') == "Invalid Api-Key, please contact support":
                        print('Error Api_Key for seller_id{}  shop {} get {}'
                              .format(seller_id, shop_name, answer.text))
                        send_get('Error Api_Key for seller_id{}  shop {} get {}'
                                 .format(seller_id, shop_name, answer.text))
                except Exception as err:
                    print('Error get data for seller_id {}  shop {} get {}'
                          .format(seller_id, shop_name, answer.text))
                    send_get('Error get data for seller_id {}  shop {} get {}'
                             .format(seller_id, shop_name, answer.text))
                finally:
                    count += 1
                    time.sleep(1)
                    if count >= 10:
                        requesting = False
                    continue
        except:
            count += 1
            time.sleep(1)
            if count >= 10:
                requesting = False
            continue
    print("We got from oson items", len(items))
    return items


def get_product_info(product_id=None, offer_id=None, seller_data=None):
    metod = 'https://api-seller.ozon.ru/v2/product/info'
    headers_lp = {
        "Client-Id": seller_data[0],
        "Api-Key": seller_data[1]
    }
    data = {
        "offer_id": offer_id,
        "product_id": product_id,
        "sku": 0
    }
    result = None
    answer = requests.post(metod, headers=headers_lp, json=data)
    if answer.ok:
        result = answer.json()
    else:
        print('Some_Error_from_get_product_info {}, product_id {}, offer_id {} '
              .format(answer.text, product_id, offer_id))
        send_get('Some_Error_from_get_product_info {}, product_id {}, offer_id {} '
                 .format(answer.text, product_id, offer_id))

    return result


def import_oson_data_prod(user_id=None, shop_name=None, company_id=None, update_base_price=None):
    # seller_id = db.session.execute(select(Marketplaces.seller_id)
    #                                .where(Marketplaces.shop_name == shop_name)).first()
    count = 0
    try:
        seller_data = db.session \
            .execute(select(Marketplaces.seller_id, Marketplaces.key_mp)
                     .where(Marketplaces.shop_name == shop_name)) \
            .first()

        current_products = get_product_list_v2(seller_id=seller_data[0], company_id=company_id)

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid_edit_user = user_id
        for prod in current_products:
            data = get_product_info(prod.get("product_id"), prod.get("offer_id"), seller_data)
            # print("ALL_DATA", data)
            if data and update_base_price is None:
                data_prod = data.get('result')
                offer_id = data_prod.get("offer_id")
                if offer_id.isdigit():
                    offer_id = "AAA" + offer_id
                product = {
                    'articul_product': offer_id,
                    'shop_name': shop_name,  # data_prod.get(""),
                    'store_id': seller_data[0],
                    'quantity': data_prod.get("stocks").get('present'),
                    'discount': 0.0,
                    'description_product': data_prod.get(""),
                    'photo': data_prod.get("primary_image"),
                    'id_1c': "",
                    'date_added': time_now,
                    'date_modifed': time_now,
                    'selected_mp': 'ozon',
                    'name_product': data_prod.get("name"),
                    'status_mp': 'enabled',
                    'images_product': data_prod.get("images"),
                    'price_add_k': 0.0,
                    'discount_mp_product': 0.0,
                    'set_shop_name': data_prod.get("name"),
                    'external_sku': data_prod.get("sku"),
                    'alias_prod_name': data_prod.get("name"),
                    'status_in_shop': data_prod.get("status").get("state_name"),
                    'uid_edit_user': uid_edit_user,
                    'final_price': data_prod.get('price'),
                    'description_category_id': data_prod.get("description_category_id"),
                    'volume_weight': data_prod.get("volume_weight"),
                    'type_id': data_prod.get("type_id"),
                    'barcode': data_prod.get("barcode")
                }

                count_error = 0
                with Session(engine) as session:
                    session.begin()
                    smth = insert(Product).values(product)
                    try:
                        session.execute(smth)
                        time.sleep(0.1)
                        count += 1
                        # print(555555555555)
                    except sqlalchemy.exc.IntegrityError as error:
                        session.rollback()
                        session.begin()
                        update_prod = update(Product).where(Product.articul_product == product.get('articul_product')) \
                            .where(Product.store_id == product.get('store_id')) \
                            .values(product)
                        session.execute(update_prod)
                        count_error += 1
                        # print(22222222222222, count_error)
                    finally:
                        session.commit()

                # os.abort()
                count += 1

            elif data and update_base_price == 'on':
                data_prod = data.get('result')
                offer_id = data_prod.get("offer_id")
                old_price = data_prod.get("old_price").split('.')[0]
                base_price = int(int(old_price) / 8)
                print(old_price, base_price, offer_id)
                if offer_id.isdigit():
                    offer_id = "AAA" + offer_id
                product = {
                    'articul_product': offer_id,
                    'shop_name': shop_name,  # data_prod.get(""),
                    'store_id': seller_data[0],
                    'quantity': data_prod.get("stocks").get('present'),
                    'price_product_base': base_price,
                    'final_price': data_prod.get('price'),
                    'old_price': old_price,
                    'discount': 0.0,
                    'description_product': data_prod.get(""),
                    'photo': data_prod.get("primary_image"),
                    'id_1c': "",
                    'date_added': time_now,
                    'date_modifed': time_now,
                    'selected_mp': 'ozon',
                    'name_product': data_prod.get("name"),
                    'status_mp': 'enabled',
                    'images_product': data_prod.get("images"),
                    'price_add_k': 0.0,
                    'discount_mp_product': 0.0,
                    'set_shop_name': data_prod.get("name"),
                    'external_sku': data_prod.get("sku"),
                    'alias_prod_name': data_prod.get("name"),
                    'status_in_shop': data_prod.get("status").get("state_name"),
                    'uid_edit_user': uid_edit_user,
                    'description_category_id': data_prod.get("description_category_id"),
                    'volume_weight': data_prod.get("volume_weight"),
                    'type_id': data_prod.get("type_id"),
                    'barcode': data_prod.get("barcode")
                }

                count_error = 0
                with Session(engine) as session:
                    session.begin()
                    smth = insert(Product).values(product)
                    try:
                        session.execute(smth)
                        time.sleep(0.1)
                        count += 1
                        # print(555555555555)
                    except sqlalchemy.exc.IntegrityError as error:
                        session.rollback()
                        session.begin()
                        update_prod = update(Product).where(Product.articul_product == product.get('articul_product')) \
                            .where(Product.store_id == product.get('store_id')) \
                            .values(product)
                        session.execute(update_prod)
                        count_error += 1
                        # print(22222222222222, count_error)
                    finally:
                        session.commit()

                # os.abort()
                count += 1

            else:
                time.sleep(0.1)
                continue

        print('Successfully import {} from {} store'.format(count, shop_name))
        return 'success {}'.format(count)
    except Exception as error:
        send_get('Error import {} from {} store'.format(count, shop_name))
        return 'errors {}'.format(error)


def check_import_limit(seller_id):
    pass


def make_internal_import_oson_product(donor=None, recipient=None, k=1,
                                      source=None, donor_mp=None, recipient_mp=None):
    # metod = 'https://api-seller.ozon.ru/v3/product/import'
    metod = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    if donor is not None and recipient is not None:
        data = []
        with Session(engine) as session:
            session.begin()
            recipient_data = session.execute(select(Marketplaces.seller_id,
                                                    Marketplaces.key_mp)
                                             .where(Marketplaces.shop_name == recipient)) \
                .first()
            product_data = session.query(Product).filter_by(shop_name=donor).all()

        if product_data:
            for row in product_data:
                # print(22222, row )
                #############################3
                # Make price ended for '9'
                price = int(row.price) * (1 + k / 100)
                price = str(price).split('.')[0][:-1] + "9"
                old_price = str(int(price) * 4)
                ##############################3
                item = {
                    'name': row.name_product,
                    'articul_product': row.articul_product,
                    'price': price,
                    'old_price': old_price,
                    'external_sku': row.external_sku,
                    'vat': '0',  # TODO make it's not magic num
                    'currency_code': 'RUB'
                }
                data.append(item)

            header = {
                'Client-Id': recipient_data[0],
                'Api-Key': recipient_data[1],
                'Content-Type': 'application/json'
            }

            if source is None:
                print('Client-Id {} from internal import oson'.format(header.get('Client-Id')))
                os.abort()

            elif donor_mp == 'ozon' and recipient_mp == 'ozon':
                answer = requests.post(url=metod,
                                       headers=header,
                                       json=data)
                if answer.ok:
                    data_json = answer.json()
                    result = data_json.get('result')
                    if result:
                        sku_list = result.get('unmatched_sku_list')
                        count, count_error = 0, 0
                        for product in product_data:
                            price = int(product.price_product_base) * (1 + k / 100)
                            final_price = str(price).split('.')[0][:-1] + "9"
                            old_price = str(int(price) * 4)
                            new_prod = {
                                'articul_product': product.articul_product,
                                'shop_name': recipient,
                                'store_id': recipient_data[0],
                                'quantity': product.quantity,
                                'reserved': product.reserved,
                                'price_product_base': product.price_product_base,
                                'final_price': final_price,
                                'old_price': old_price,
                                'discount': product.discount,
                                'description_product': product.description_product,
                                'photo': product.photo,
                                'id_1c': product.id_1c,
                                'date_added': datetime.now(),
                                'date_modifed': datetime.now(),
                                'selected_mp': product.selected_mp,
                                'name_product': product.name_product,
                                'status_mp': product.status_mp,
                                'images_product': product.images_product,
                                'price_add_k': product.price_add_k,
                                'discount_mp_product': product.discount_mp_product,
                                'set_shop_name': product.set_shop_name,
                                'external_sku': product.external_sku,
                                'alias_prod_name': product.alias_prod_name,
                                'status_in_shop': product.status_in_shop,
                                'shop_k_product': product.shop_k_product,
                                'discount_shop_product': product.discount_shop_product,
                                'quantity_for_shop': product.quantity_for_shop,
                                'description_product_add': product.description_product_add,
                                'uid_edit_user': product.uid_edit_user,
                                'description_category_id': product.description_category_id,
                                'type_id': product.type_id,
                                'volume_weight': product.volume_weight,
                                'barcode': product.barcode
                            }
                            if int(product.external_sku) in sku_list:

                                # print(3333, product.shop_name, product.id, product.external_sku)
                                # print(777777777, *product.as_dict(), sep=':,\n')
                                with Session(engine) as session:
                                    session.begin()
                                    smth = insert(Product).values(new_prod)
                                try:
                                    session.execute(smth)
                                    count += 1
                                    print('We are write {} product'.format(count))
                                except sqlalchemy.exc.IntegrityError as error:
                                    session.rollback()
                                    ## TODO We need know is nessasery update product
                                    # session.begin()
                                    # update_prod = update(Product)\
                                    #     .where( Product.articul_product == new_prod.get('articul_product')) \
                                    #     .where(Product.store_id == new_prod.get('store_id')) \
                                    #     .values(new_prod)
                                    # session.execute(update_prod)
                                    count_error += 1
                                    print(22222222222222, count_error)
                                    continue
                                finally:
                                    session.commit()

                            else:
                                # print(5555, product.external_sku)
                                continue

                        return "Всё ок", count, len(result), count_error

                else:
                    return "Что-то пошло не так", \
                        answer.status_code, \
                        answer.text, \
                        recipient_mp

            elif donor_mp == 'ozon' and recipient_mp == 'wb':
                pass

            else:
                return 'Check you data', donor, donor_mp, recipient_mp


def make_import_export_oson_price(donor=None, recipient=None,
                                  k=1, send_to_mp=False):
    # metod = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    if donor is not None and recipient is not None:
        data = []
        with Session(engine) as session:
            session.begin()
            recipient_data = session.execute(select(Marketplaces.seller_id,
                                                    Marketplaces.key_mp)
                                             .where(Marketplaces.shop_name == recipient)) \
                .first()
            product_data = session.query(Product).filter_by(shop_name=donor).all()

        if product_data:
            for row in product_data:
                # print(22222, row )
                #############################3
                # Make price ended for '9'
                price = int(row.final_price) * (1 + k / 100)
                price = str(price).split('.')[0][:-1] + "9"
                old_price = str(int(price) * 4)
                ##############################3
                item = {
                    'final_price': price,
                    'old_price': old_price,
                    "date_modifed": datetime.now()
                }

                with Session(engine) as session:
                    session.begin()
                    session.execute(update(Product)
                                    .where(Product.articul_product==row.articul_product)
                                    .where(Product.shop_name==recipient).values(item))
                    session.commit()

# make_import_export_oson_price(donor='Low Price', recipient='Полиция Вкуса', k=0)

# print(make_internal_import_oson(donor='ImportGoods', recipient='Ф-фторник'))


# def product_info_price(id_mp, seller_id):  # product_id, offer_id
#     # url = 'https://api-seller.ozon.ru/v4/product/info/prices'
#     # data = {"filter": {
#     #             "offer_id": [offer_id],
#     #             "product_id": [str(product_id)],
#     #             "visibility": "ALL"
#     #         },
#     #         "last_id": "",
#     #         "limit": 100}
#     api_key = db.session.execute(select(Marketplaces.key_mp)
#                                      .where(Marketplaces.seller_id == seller_id))
#     print(api_key, type(api_key))
#     headers = {
#         'Client-Id': seller_id,
#         'Api-Key': api_key,
#         'Content-Type': 'application/json'
#     }
#     url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'
#     data = {
#         "posting_number": id_mp,
#         "with": {
#             "analytics_data": False,
#             "barcodes": False,
#             "financial_data": False,
#             "product_exemplars": False,
#             "translit": False}}
#     # resp = requests.post(url=url, headers=headers, json=data)
#     # result = resp.json()
#     # print('product_id_offer_id', result)
#     # # price = result.get("result")["items"][0]["price"]["marketing_price"][:-2]
#     # order = result.get("result")
#     # return order


# product_info_price('34253142-0058-7', 1713959)
# import_oson_data_prod("1", "1278621", "1")

# get_product_list()

# create_list_attr()
# make_send_data()
