import datetime
import sys
import requests
import json
import xmltodict
from project import DATA_PATH

def get_new_pages_v2():
    resp = requests.get(link)
    data = xmltodict.parse(resp.text)
    data_product = data['data']['product']
    # print(data['data']['product'][0], sep='\n')
    # print(datetime.datetime.now(), 'data_product2 - ', len(data_product))
    # post_smth(data_product, 0, '0')
    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open(DATA_PATH + "data_product.json", "w") as write_file:
        json.dump(data_product, write_file)  # encode dict into JSON

    return data_product


def check_and_write_v4(standart_data):
    # data_from = get_new_pages_v2()
    # standart = standart_product_v2(data_from)
    # standart_copy = standart.copy()
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
    # 
    # return standart_copy


def standart_product_v2(without_db=False):
    list_wheels_json = get_new_pages_v2()
    global_result = {}
    proxy = []
    for dictionary in list_wheels_json:
        try:
            name = dictionary['name'].strip('"')
            type = dictionary.get('type').strip('"').split(' ')[-1]
            if type == 'диски':
                category = 5
            else:
                category = 0
            try:
                description = dictionary.get('description')[:-145]
            except:
                description = ''
            if not description:
                description = name
            vendor = dictionary.get('vendor').replace('"', '')
            category_id = categories_wheels\
                .get(vendor, cats_wheels_upper.get(vendor.upper(), 7000))
            price_opt = int(dictionary.get('price').strip('"').replace('\xa0', '').split('.')[0])
            price = float(dictionary.get('RoznicaPrice').strip('"').replace('\xa0', '').split('.')[0])
            rule = False
            if price_opt * 1.18 >= price:
                rule = True
            in_stock = int(dictionary.get('rest').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest2').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest3').strip('"').replace('>', '').replace('<', ''))
            if in_stock >= 4:
                enabled = 1
            else:
                enabled = 0
            name_picture = '88888888'
            product_code = dictionary['vendor_code'].strip('"').strip('-')
            image_url = dictionary['foto'].strip('"')
            if image_url:
                # index = image_url.rfind('/')
                # name_picture = 'colrad-' + image_url[index + 1:]
                name_picture = vendor.strip() + '_' + product_code + '.png'
            image_tuple = (name_picture, image_url)
            koeff = 1
            meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            params = 1
            provider = 'colrad'
            options = {
                'et': 'ET' + dictionary.get('et').strip('"'),
                "bolts_spacing": dictionary.get('pcd1').strip('"')
                                 + '/' + dictionary.get('pcd2').strip('"'),
                'diameter': dictionary.get('diameter').strip('"').strip('0').strip(','),
                'dia': 'D' + dictionary.get('dia').strip('"'),
                'width': dictionary.get('width').strip('"')
            }

            global_result.update({vendor.strip() + product_code: (
                [
                    category_id, name, description, price, in_stock,
                    enabled, product_code, vendor, meta_d, meta_k,
                    params, koeff, meta_h1, provider, category
                ],
                image_tuple,
                options,
                rule,
                price_opt)})

        except:
            # print("FUCKUP_standart_product_v2", dictionary)
            continue


    rewrite_standart_data(global_result)
    
    if not without_db:
        check_and_write_v4(global_result)

    return global_result


