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
    try:
        for line in open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', 'r'):
            pages = json.loads(line)
    except:
        for line in open('dict_images.json', 'r'):
            pages = json.loads(line)

    return pages


def write(smth):
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time)+ '-' + smth)
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


def dowload_images():
    pages = read_image_address()
    print('from_pictures', len(pages))
    count = len(pages)
    for address in pages:  #[:10]:
        for key in address:
            if address.get(key) != [0] and \
                    address[key][1] is not None and \
                    address[key][1] != '':
                count -= 1
                name, url = address[key]
                get_image(str(name), url)
                # write(str(name))
                print('get_image',count, name, url)
                time.sleep(1)
            else:
                continue
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

    print('clean_file-len_list',  len(listt))


def create_need_data(without_db=False, shop_name=None):
    json_data, csv_data, data = {}, {}, {}
    if not without_db:
        try:
            csv_data = shins.standart_wheels_csv()
        except:
            print("We don't get csv")
        try:
            json_data = tochki.standart_wheels_from_json()
        except:
            print("We don't get json")
        # data = standart.standart_product(shop_name=shop_name)
        try:
            data = kolrad.standart_product_v2()
        except:
            print("We don't ger kolrad data")

    else:
        try:
            csv_data = shins.standart_wheels_csv(without_db=True)
        except:
            pass
        try:
            json_data = tochki.standart_wheels_from_json(without_db=True)
        except:
            pass
        try:
            data = kolrad.standart_product_v2(without_db=True)
        except:
            print("We don't ger kolrad data")
    # if we don't get data from distributors, we make feed from database
    if len(json_data) == 0 and len(csv_data) == 0 and len(data) == 0:
        data = standart.standart_product()
        #sys.exit   # more variants

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


def standart_product(shop_name=None):
    proxy_data, proxy = [], []
    global_result = {}
    with Session(engine) as session:
        data = session.scalars(select(Product)
                               .where(Product.shop_name == shop_name))\
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


def check_and_write_v4(standart_data):
    # data_from = get_new_pages_v2()
    # standart = standart_product_v2(data_from)
    standart_copy = standart_data.copy()
    ij_data, proxy = [], []
    count = 0
    for key, data_product in standart_data.items():
        # try:
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id_v2(add_product, data_product[0])
                ij_data.append({product_id: data_product[1]})
                picture_id = make_query_get_id_v2(add_pictures,
                                               [product_id, data_product[1][0]])
                proxy_data = [picture_id, product_id]
                make_query_v2(add_product_picture,  proxy_data)
                data_options = params_optwheels(data_product[2], product_id)
                # for option in data_options:
                #     make_query_v2(add_options, option)
                make_query_many_v2(add_options, data_options)

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                elif quantity < 4 and is_exist[1] != quantity:
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                    del standart_copy[key]

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id_v2(add_product, data_product[0])
                    ij_data.append({product_id: data_product[1]})
                    picture_id = make_query_get_id_v2(add_pictures,
                                                   [product_id, data_product[1][0]])
                    proxy_data = [picture_id, product_id]
                    make_query_v2(add_product_picture, proxy_data)

                    data_options_tyres = params_optyres(data_product[2], product_id)
                    # for option in data_options_tyres:
                    #     make_query_v2(add_options, option)
                    make_query_many_v2(add_options, data_options_tyres)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        # print(is_exist[1], 'quantity23 -', category_id, product_code, ' -now', quantity)
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)

            except mysql.connector.Error as err:
                write("S_thing went wrong connector tyres: {}".format(err))
                # write(str(data_product))
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                write("S_thing went wrong KeyError tyres---: {}".format(e))
                # write(str(data_product))
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

    rewrite_pictures_data(ij_data)
    print('For_write_pictures_data', len(ij_data))
    print('from_check_and_write_4_errors', count)
    # dowload_images()

    return standart_copy


def check_write_json_v4(data_from_json):
    rewrite_standart_data(data_from_json)
    ij_data, proxy = [], []
    count = 0
    for key, data_product in data_from_json.items():
        category = data_product[0].pop(-1)  # [-1]
        provider = data_product[0].pop(-1)
        quantity = data_product[0][4]
        if category in [1, 4, 5, 7]:  # and quantity >= 4: ###wheels only
            is_exist = check_is_exist(data_product[0][6], data_product[0][0])
            if not is_exist[0] and quantity >= 4:
                product_id = make_query_get_id_v2(add_product, data_product[0])
                ij_data.append({product_id: data_product[1]})
                picture_id = make_query_get_id_v2(add_pictures,
                                               [product_id, data_product[1][0]])
                proxy_data = [picture_id, product_id]
                make_query_v2(add_product_picture, proxy_data)
                data_options = params_optwheels(data_product[2], product_id)
                # for option in data_options:
                #     make_query_v2(add_options, option)
                make_query_many_v2(add_options, data_options)

            elif is_exist[0]:
                category_id = data_product[0][0]
                product_code = data_product[0][6]
                price_for_site = data_product[0][3]
                if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                    enabled = 1
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)
                elif quantity < 4 and is_exist[1] != quantity:
                    enabled = 0
                    new_data = [price_for_site, quantity, enabled, category_id, product_code]
                    make_query_v2(update, new_data)

        elif category == 12:
            try:
                is_exist = check_is_exist(data_product[0][6], data_product[0][0])
                if not is_exist[0] and quantity >= 4:
                    product_id = make_query_get_id_v2(add_product, data_product[0])
                    ij_data.append({product_id: data_product[1]})
                    picture_id = make_query_get_id_v2(add_pictures,
                                                   [product_id, data_product[1][0]])
                    proxy_data = [picture_id, product_id]
                    make_query_v2(add_product_picture, proxy_data)
                    data_options_tyres = params_optyres(data_product[2], product_id)
                    # for option in data_options_tyres:
                    #     make_query_v2(add_options, option)
                    make_query_many_v2(add_options, data_options_tyres)
                elif is_exist[0]:
                    category_id = data_product[0][0]  # because we get data from csv and has category_id
                    product_code = data_product[0][6]
                    price_for_site = data_product[0][3]
                    if quantity >= 4 and [is_exist[1], is_exist[2]] != [quantity, data_product[0][3]]:
                        enabled = 1
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)
                    elif quantity < 4 and is_exist[1] != quantity:
                        enabled = 0
                        new_data = [price_for_site, quantity, enabled, category_id, product_code]
                        make_query_v2(update, new_data)

            except mysql.connector.Error as err:
                print("S_thing went wrong connector tyres: {}".format(err))
                print('wrong connector tyres', str(data_product))
                continue
            except KeyError as e:
                print("S_thing went wrong KeyError tyres---: {}".format(e))
                print('wrong connector tyres3', str(data_product))
                continue

        else:
            print('pass', category)
            continue

    rewrite_pictures_data(ij_data)
    print('write_pictures_link_4', len(ij_data))
    print('from_check_and_write_v4_errors_json', count)



# clean()
# dowload_images()