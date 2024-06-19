import os

from project import DATA_PATH

import datetime
import time
import requests
import json
import urllib3

import project.addons.shins as shins
import project.addons.four_tochki as tochki
import project.addons.standart_product as standart
import project.addons.kolrad as kolrad

import sys
from sqlalchemy import select
from sqlalchemy.orm import Session
from project import engine
from project.models import Product
import project.conn as conn

# for production only
requests.packages.urllib3.disable_warnings()


def rewrite_pictures_data(listt):
    with open(DATA_PATH + '/dict_images.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_images_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/dict_images.json', "w") as write_file:
        data_list.extend(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_images_write_1', len(listt))

    print('file_images_rewrite', len(data_list))


def rewrite_standart_data(listt):
    with open(DATA_PATH + '/standart_data.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_standart_data_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/standart_data.json', "w") as write_file:
        # data_list.extend(listt)
        data_list.update(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_standart_data_write_1', len(listt))

    print('file_standart_data_rewrite', len(data_list))


def read_image_address():
    pages = None
    for line in open(os.getcwd() + DATA_PATH + 'dict_images.json', 'r'):
        pages = json.loads(line)

    return pages


def write(smth):
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time) + '-' + smth)
    except:
        with open('log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time) + '-' + smth)


def get_image(name, url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            with open(PHOTO_DIR + name, "wb") as file:
                file.write(response.content)
        response.close()
    except:
        print('some_fuck_up_get_image', name, url)


def dowload_images(sleep=False):
    pages = read_image_address()
    print('from_pictures', len(pages))
    count = len(pages)
    for address in pages:  # [:10]:
        for key in address:
            if address.get(key) != [0] and \
                    address[key][1] is not None and \
                    address[key][1] != '':
                count -= 1
                name, url = address[key]
                get_image(str(name), url)
                # write(str(name))
                print('get_image', count, name, url)
                time.sleep(1)
            else:
                continue
    if sleep:
        for _ in range(30):
            print('We are sleep & wait clean')
            time.sleep(1)
    clean()


def clean():
    listt = []
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as file:
            json.dump(listt, file)

    except:
        with open('dict_images.json', "w") as file:
            json.dump(listt, file)

    print('clean_file-len_list', len(listt))


def create_need_data(without_db=False, shop_name=None,
                     name_price=None):
    json_data, csv_data, data = {}, {}, {}
    if not without_db:
        try:
            csv_data = shins.standart_wheels_csv()
        except:
            print("We don't get csv")
        check_and_write(csv_data, shop_name=shop_name)
        rewrite_standart_data(csv_data)

        try:
            json_data = tochki.standart_wheels_from_json()
        except:
            print("We don't get json")
        check_and_write(json_data, shop_name=shop_name)
        rewrite_standart_data(json_data)

        try:
            data = kolrad.standart_product_v2()
        except:
            print("We don't ger kolrad data")

        check_and_write(data, shop_name=shop_name)


    else:
        try:
            csv_data = shins.standart_wheels_csv(name_price=name_price)
        except:
            pass
        rewrite_standart_data(csv_data)

        try:
            json_data = tochki.standart_wheels_from_json(name_price=name_price)
        except:
            pass
        rewrite_standart_data(json_data)

        try:
            data = kolrad.standart_product(name_price=name_price)
        except:
            print("We don't ger kolrad data")
            rewrite_standart_data(data)

    # if we don't get data from distributors, we make feed from database
    if len(json_data) == 0 and len(csv_data) == 0 and len(data) == 0:
        data = standart_product()
        # sys.exit   # more variants

    pre_csv_data = {key: value for key, value in csv_data.items() if int(value[0][4]) >= 4}
    pre_json_data = {k: v for k, v in json_data.items() if int(v[0][4]) >= 4}
    need_data = dict()
    for ke, val in data.items():
        pre_count_json = pre_json_data.get(ke)
        if pre_count_json:
            count_json = int(pre_count_json[0][4])
        else:
            count_json = 0
            # print(111, ke, type(val[0][4]), val[0][4])
        pre_count_csv = pre_csv_data.get(ke)
        if pre_count_csv:
            count_csv = int(pre_count_csv[0][4])
        else:
            count_csv = 0
            # print(222, ke, type(val[0][4]), val[0][4])
        in_stok = int(val[0][4]) + count_json + count_csv
        new_data = val[0].copy()
        del new_data[4]
        new_data.insert(4, in_stok)
        need_data.update({ke: (new_data, val[1], val[2], val[3], val[4])})
    print('ALL_RIDE create_need_data ', len(need_data))

    return need_data


def standart_product(shop_name=None):  # standarting data product from db
    proxy_data, proxy = [], []
    global_result = {}
    with Session(engine) as session:
        data = session.scalars(select(Product)
                               .where(Product.shop_name == shop_name)) \
            .all()
    for row in data:
        prod = row.__dict__
        for key in prod.keys():
            print(key, f"= prod.get('{key}')")

        try:
            opt_price = prod.get('price_product_base')
            date_added = prod.get('date_added')
            set_shop_name = prod.get('set_shop_name')
            description_product_add = prod.get('description_product_add')
            brand_id = prod.get('brand_id')
            final_price = prod.get('final_price')
            date_modifed = prod.get('date_modifed')
            external_sku = prod.get('external_sku')
            uid_edit_user = prod.get('uid_edit_user')
            articul_product = prod.get('articul_product')
            old_price = prod.get('old_price')
            selected_mp = prod.get('selected_mp')
            alias_prod_name = prod.get('alias_prod_name')
            description_category_id = prod.get('description_category_id')
            id = prod.get('id')
            product_id = prod.get('product_id')
            name = prod.get('name_product')
            type_id = prod.get('type_id')
            volume_weight = prod.get('volume_weight')
            shop_name = prod.get('shop_name')
            discount = prod.get('discount')
            status_mp = prod.get('status_mp')
            status_in_shop = prod.get('status_in_shop')
            barcode = prod.get('barcode')
            store_id = prod.get('store_id')
            description = prod.get('description_product')
            images_product = prod.get('images_product')
            shop_k_product = prod.get('shop_k_product')
            cart_id = prod.get('cart_id')
            quantity = prod.get('quantity')
            photo = prod.get('photo')
            price_add_k = prod.get('price_add_k')
            discount_shop_product = prod.get('discount_shop_product')
            vendor = prod.get('brand')
            vendor_code = prod.get('vendor_code')
            reserved = prod.get('reserved')
            id_1c = prod.get('id_1c')
            discount_mp_product = prod.get('discount_mp_product')
            quantity_for_shop = prod.get('quantity_for_shop')
            in_stock = int(quantity) - int(reserved)
            if in_stock >= 4:
                enabled = 1
            else:
                enabled = 0
            if vendor == 'Carwel':
                description = name
            elif vendor == '':
                continue
            category_id = 7000

            if data[i][4] in ['S', 's', 'Летняя']:
                type_tyres = 'Летняя'
            elif data[i][4] in ["W", 'Зимняя']:
                type_tyres = 'Зимняя'
            elif data[i][4] in ["allseason", 'Всесезонная']:
                type_tyres = 'Всесезонная'
            else:
                print('1212_category_id', data[i][4])
            category = 12
            rule = False
            # check category wheels and tyres

            size = data[i][7]  # 16 'diameter'
            width = data[i][8]  # 14
            height = data[i][9]  # 15
            sku = data[i][0]
            name_picture = '88888888'
            image_url = data[i][20]  # image_link
            if image_url:
                # name_picture = 'shins-' + id_generator() + '.png'
                name_picture = 'shins-' + vendor_code + '.png'
            image_tuple = (name_picture, image_url)
            # price = count_price(data[i][17], size)
            koeff = 1
            meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            provider = 'shins'
            params = 1
            options = {
                'diameter': size,
                'width': width,
                'profile': height
            }

            global_result.update({vendor.strip() + vendor_code:
                (
                    [category_id, name, description, opt_price,
                     in_stock, enabled, vendor_code, vendor, meta_d, meta_k,
                     params, koeff, meta_h1, provider, category],
                    image_tuple,
                    options,
                    rule
                )})

        except KeyError as error:
            print("Something went wrong KeyError from getcsv: {}".format(error))
            # write(str(data))
            print(str(data[i]))
            continue

    mem = sys.getsizeof(proxy_data)

    print(mem / 1000, 'Kb--')
    print("ALL_RIDE_get_tyres_csv ()".format(len(global_result)))
    return global_result


def check_and_write(standart_data,
                    min_quan=1,
                    shop_name='all'):
    image_data, proxy = [], []
    count_success, count_error = 0
    for key, data_product in standart_data.items():
        try:
            category_id = data_product[0].pop(0)
            quantity = data_product[0][4]
            # check is exist in db and compare quantity & base price & final_price
            articul_product = data_product[0][8]
            is_exist = conn.check_product_is_exist_in_db(
                articul_product=articul_product,
                shop_name=shop_name
            )
            if not is_exist[0] and quantity >= min_quan:
                id_product = conn.make_query_get_id(
                    conn.query_add_product,
                    data_product[0]
                )
                # prepare for downlod images
                image_data.append({id_product: data_product[1]})
                # write options product
                if category_id in [1, 4, 5, 7]:  ###wheels
                    data_options = [value for value in data_product[2].values()] + [id_product]
                    conn.executemany_query_v3(conn.query_add_wheels_options,
                                              tuple(data_options))
                elif category_id == 12:
                    data_options = [value for value in data_product[2].values()] + [id_product]
                    conn.executemany_query_v3(conn.query_add_tyres_options,
                                              tuple(data_options))

                else:
                    print('pass', category_id)
                    continue

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= min_quan and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, product_code, shop_name]
                    conn.execute_query_v3(conn.update_product_price_qnt, new_data)
                elif quantity < min_quan and is_exist[1] != quantity:
                    enabled = 0
                    new_data = [price_for_site, quantity, category_id, product_code]
                    conn.execute_query_v3(conn.update_product_price_qnt, new_data)
                    # del standart_copy[key]

            count_success += 1

        except:
            count_error += 1

    rewrite_pictures_data(image_data)
    print('For_write_pictures_data', len(image_data))
    print('From_check_and_write_errors {} success {}, shop_name {}'
          .format(count_error, count_success, shop_name))
    # dowload_images()

    # return standart_copy
