import asyncio
import datetime
from time import sleep
import requests

from conn import executemany_query, execute_query_return, execute_query_return_v2
from conn_maintenance import *
from creds import *
import base64
import json
import csv


# from maintenance import data_vendor


def encode_base64():
    target_strintg = 'profit_Baza:profit1302'
    target_strintg = 'aleksandr@corpprofit.ru:123456'
    message_bytes = target_strintg.encode('ascii')
    base64_bite = base64.b64encode(message_bytes)
    base64_message = base64_bite.decode('ascii')

    print(base64_message)


def get_netlab_token():
    url = 'http://services.netlab.ru/rest/authentication/token.json?'
    params = {'username': nick, 'password': passw}
    answer = requests.get(url, params=params)
    # print(answer.text)
    tokenResponse = json.loads(answer.text[5:])
    fresh_token = tokenResponse.get('tokenResponse').get("data").get('token')
    if fresh_token:
        write_token(fresh_token)
    else:
        print('WE FUCK UP to get netlab token')

    # print(fresh_token)
    # print(answer.json())


def write_token(tokken):
    try:
        fresh_token = {
            'netlab_token': tokken
        }
        f = open(CRED_PATH + 'netlab_token.json', 'w')
        f.write(json.dumps(fresh_token))
        f.close()
        print('ALL RIDE to update netlab token')
        result = True
    except:
        print('Smth FUCK UP to update netlab token')
        result = False

    return result


def read_netlab_access_token():
    with open(CRED_PATH + 'netlab_token.json', 'r') as file:
        data = json.load(file)
        tokken = data.get('netlab_token')
        # print(tokken)
        return tokken


def create_path_for_csv(row_list):
    '''
    [{'id': 30966270, 'parent_id': 29253025, 'title': 'Мой склад', 'created_at': '2023-06-06T12:50:29.000+03:00',
    'updated_at': '2023-06-06T12:50:29.000+03:00', 'position': 17}]
    :param row_list:
    :return: path for site
    itis create path from insales to insales location
    '''
    result = []
    row_dict = {row['id']: row for row in row_list}
    for raw in row_list:
        pre_path = raw.get('title')
        path = raw.get('path', pre_path)
        parent_id = raw.get('parent_id')
        while parent_id is not None:
            re_path = row_dict.get(parent_id).get('title') + '/' + path
            parent_id = row_dict.get(parent_id).get('parent_id')
            path = re_path
            raw['path'] = re_path
        else:
            raw['path'] = 'Каталог' + raw.get('path', '').replace('Склад', '')

        result.append(raw)
        print('raw-', raw)

    return result


def category_action(catalog_name: str, category_id: int):
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/{catalog_name}/{category_id}.json?oauth_token={oauth_token}'
    resp = requests.get(url)
    catalog_resp = resp.text[5:]
    data = json.loads(catalog_resp)
    if data.get('categoryResponse').get('status').get("code") == "8" and \
            data.get('categoryResponse').get('status').get("message") == "Authorization Exception:incorrect token":
        get_netlab_token()
    # print('catalog_resp', catalog_resp)
    return data.get('categoryResponse').get('data')


def create_csv_file_from_netlab(site_category_name, category_ids: list):  # category_id: int):
    catalog_name = "В наличии"  # "Прайс-лист"
    result_list = []
    for category_id in category_ids:
        data = category_action(catalog_name, category_id)
        site_category_path_data = execute_query_return(read_path_categories, ('netlab',))
        site_category_path = {i[1]: i[0] for i in site_category_path_data if i[0]}
        if data:
            product_list = data.get('goods')
            for prod in product_list:
                proxy = {}
                proxy['published'] = site_category_path[category_id]
                proxy['category_id'] = site_category_name  # category_id
                proxy['name'] = prod.get('properties').get('название')
                proxy['quantity'] = prod.get('properties').get('количество на Калужской', 0) + prod.get(
                    'properties').get(
                    'количество на Курской', 0) + prod.get('properties').get('количество на Лобненской', 0)
                proxy['id'] = prod.get('id')
                proxy['warranty'] = prod.get('properties').get('гарантия', '1 год')
                proxy['price'] = prod.get('properties').get('цена по категории D') * 1.08
                # proxy.update(prod.get('properties'))
                result_list.append(proxy.copy())
        else:
            continue

    today = str(datetime.datetime.today()).replace(' ', '_')[:-7]
    fields = ['category_id', 'name', 'warranty', 'quantity', 'price', 'id', 'published']
    with open(CSV_PATH + f'netlab_{category_id}_{today}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_list)


def create_csv_file_from_netlab_v2():  # data_cats: list): #category_id: int):
    list_cats = execute_query_return_v2(query_get_actual_cats)
    category_ids = {i[0]: i for i in list_cats}

    catalog_name = "В наличии"  # "Прайс-лист"
    result_list = []
    for category_id in category_ids.keys():
        data = category_action(catalog_name, category_id)
        site_category_path_data = execute_query_return(read_path_categories, ('netlab',))
        site_category_path = {i[1]: i[0] for i in site_category_path_data if i[0]}
        product_list = data.get('goods')
        site_category_name = category_ids[category_id][1]
        for prod in product_list:
            proxy = {}
            proxy['published'] = site_category_path[category_id]
            proxy['category_id'] = site_category_name  # category_id
            proxy['name'] = prod.get('properties').get('название')
            proxy['quantity'] = prod.get('properties').get('количество на Калужской', 0) \
                                + prod.get('properties').get('количество на Курской', 0) \
                                + prod.get('properties').get('количество на Лобненской', 0)
            proxy['id'] = prod.get('id')
            proxy['warranty'] = prod.get('properties').get('гарантия', '1 год')
            proxy['price'] = prod.get('properties').get('цена по категории D') * 1.08
            # proxy.update(prod.get('properties'))
            result_list.append(proxy.copy())
    fields = ['category_id', 'name', 'warranty', 'quantity', 'price', 'id', 'published']
    # with open(CSV_PATH + f'netlab_{category_id}.csv', 'w') as file:
    #     writer = csv.DictWriter(file, fieldnames=fields)
    #     writer.writeheader()
    #     writer.writerows(result_list)
    today = str(datetime.datetime.today()).replace(' ', '_')[:-7]

    with open(CSV_PATH + f'netlab.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_list)


def check_len_properties(properties, props):
    proxy = {key: value for key, value in properties.items() if key not in props.keys()}
    return props.update(proxy)


def create_csv_for_category_from_netlab_v3():  ##for import goods only (maybe)
    list_cats = execute_query_return(query_get_actual_cats_v2, ('netlab',))
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    # site_category_path = {key: value[2] for key, value in category_ids.items()}
    catalog_name = "В наличии"  # "Прайс-лист" #
    base_fields = ['category_id', 'quantity', 'price', 'id', 'published', 'name', 'images']
    for key in category_groups.keys():
        # if key == 1:
        result_list, fields = [], []
        rewrite_properties = {}
        prod_id, prod = 0, {}
        for category_id in category_groups.get(key):
            site_category_name = category_ids[category_id][1]
            try:
                data = category_action(catalog_name, int(category_id))
                if data:
                    product_list = data.get('goods')
                    for prod in product_list:
                        proxy = {}
                        prod_id = prod.get('id')
                        proxy['published'] = category_ids[category_id][2]  # site_category_path[category_id]
                        proxy['category_id'] = site_category_name  # category_id
                        proxy['quantity'] = prod.get('properties').get('количество на Калужской', 0) + prod.get(
                            'properties').get(
                            'количество на Курской', 0) + prod.get('properties').get('количество на Лобненской', 0)
                        proxy['id'] = prod_id
                        proxy['price'] = prod.get('properties').get('цена по категории D') * 1.05
                        image_list = get_goods_images(prod_id)
                        if image_list[0]:
                            proxy['images'] = ', '.join(image_list[1])
                        else:
                            proxy['images'] = 'Image not found'
                        proxy['name'] = prod.get('properties').get('название').replace(';', '')
                        # print(prod)
                        # proxy['warranty'] = prod.get('properties').get('гарантия', '1 год')
                        properties = goods_description_by_uid(prod_id)
                        # if properties[0]:
                        proxy.update(properties[1])
                        rewrite_properties.update(properties[1])
                        result_list.append(proxy.copy())

                    # fields = base_fields.copy()
                    # pr = set(rewrite_properties.keys())
                    # fields.extend(pr)
                    # print(f'netlab_fields_{key}', fields)

                else:
                    continue

            except Exception as error:
                print('fuck_up_netlab_123 {}'.format(error))
                # continue

            # break  #FIX IT - REMOVE FOR PRODUCTION

        fields = base_fields.copy()
        pr = sorted(set([i.strip('<b>').strip('</b>') for i in rewrite_properties.keys()]))
        fields.extend(pr)
        print('netlab_fields_{} {} {}'.format(key, len(fields), fields))
        with open(CSV_PATH + f'netlab_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                    extrasaction='ignore', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)

            # if prod_id == 11008078:
            #     print(222222222, prod)
        #     write_smth(result_list)
        #     break  # FIX IT -  FOR PRODUCTION
        #
        # else:
        #     print('key', key)
        #     continue


def create_csv_for_category_from_netlab_v4():  ##for import goods only (maybe)
    list_cats = execute_query_return(query_get_actual_cats_v2, ('netlab',))
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    # site_category_path = {key: value[2] for key, value in category_ids.items()}
    catalog_name = "В наличии"  # "Прайс-лист" #
    base_fields = [
        'category_id',
        'quantity',
        'price',
        'id',
        'published',
        'name',
        'images',
        'partNumber'
    ]
    pro_fields = [
        'ПРЕДУПРЕЖДЕНИЕ',
        'Производитель',
        'Модель',
        'Тип оборудования',
        'Цвет',
        'Операционная система',
        'Процессор',
        'Модель процессора',
        'Частота (ГГц)',
        'Количество ядер',
        'Оперативная память',
        'Объем жесткого диска (ГБ)',
        'Объем жесткого диска 2 (ГБ)',
        'Объем жесткого диска SSD (ГБ)',
        'Объем жесткого диска iSSD (ГБ)',
        'Диагональ (дюймов)',
        'Поверхность',
        'Разрешение',
        'USB 2.0',
        'USB 3.0',
        'USB 3.1',
        'USB 3.2',
        'USB-C 3.0',
        'USB-C 3.1',
        'USB-C 3.2',
        'USB-C 4',
        'USB-C (Thunderbolt 3)',
        'USB-C (Thunderbolt 4)',
        'D-Sub',
        'mini D-Sub',
        'HDMI'
    ]
    allpro = []
    fields = base_fields.copy()
    for key in category_groups.keys():
        # if key == 1:
        result_list = []
        rewrite_properties = {}
        prod_id, prod = 0, {}
        for category_id in category_groups.get(key):
            site_category_name = category_ids[category_id][1]
            try:
                data = category_action(catalog_name, int(category_id))
            except Exception as  error:
                print('Fuckup_category_id {} {} '.format(category_id, error))
                continue
            if data:
                product_list = data.get('goods')
                for prod in product_list:

                    prod_id = prod.get('id')
                    proxy = {
                        'published': category_ids[category_id][2],
                        'category_id': site_category_name,
                        'quantity': prod.get('properties').get('количество на Калужской', 0) +
                                    prod.get('properties').get('количество на Курской', 0) +
                                    prod.get('properties').get('количество на Лобненской', 0),
                        'id': prod_id,
                        'price': prod.get('properties').get('цена по категории D') * 1.05,
                        'name': prod.get('properties').get('название').replace(';', '')
                    }
                    image_list = get_goods_images(prod_id)
                    if image_list[0]:
                        proxy['images'] = ', '.join(image_list[1])
                    else:
                        proxy['images'] = 'Image not found'

                    properties = goods_description_by_uid(prod_id)
                    proxy['Процессор'] = properties[1].get('Процессор', properties[1].get('Процессор ноутбука'))

                    proxy.update(properties[1])
                    # # if prod_id == 1989672 or prod_id == 1986676:
                    #     print(33333333333333, proxy)
                    rewrite_properties.update(properties[1])
                    result_list.append(proxy.copy())

            else:
                continue

        pr = sorted(set([i.strip('<b>').strip('</b>') for i in rewrite_properties.keys() if i != '-']))
        ffr = sorted(rewrite_properties.keys())
        # fields.extend(pr) # make 10/04/2024 for base fields only
        print('netlab_fields_{} {} {}'.format(key, len(fields), fields))
        with open(CSV_PATH + f'netlab-2_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                    extrasaction='ignore', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)

        allpro.extend(result_list.copy())

    with open(CSV_PATH + f'netlab-all.csv', 'w') as file:
        writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                extrasaction='ignore', fieldnames=fields)
        writer.writeheader()
        writer.writerows(allpro)





def write_excel(data):
    with open('natlab_cats.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print('ALL_RIDE')


def write_smth(smth):
    with open(CSV_PATH + 'prod_log', 'w') as file:
        json.dump(smth, file)


def make_task():
    list_cats = execute_query_return(query_get_actual_cats)


def get_netlab_catalog():
    catalog_name = "В наличии"  # "Прайс-лист"  #
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/{catalog_name}.json?oauth_token=' + oauth_token
    answer = requests.get(url)
    data_resp = json.loads(answer.text[5:])
    data = data_resp.get('catalogResponse').get("data").get("category")
    print(len(data))  # 2846
    # print(*sorted(data, key=xy), sep='\n')
    # main_category = [i for i in data if i.get('parentId') == '0']
    # print(len(main_category))
    # second_category = [i for i in data if len(i.get('parentId')) <= 2 and i.get('parentId') != '0']
    # print(len(second_category))
    # deep_category = [i for i in data if len(i.get('parentId')) >= 2 and i.get('parentId') != '0']
    # print(len(deep_category))
    # print(*sorted(deep_category, key=xy), sep='\n')

    return data


async def save_categories_vendors():
    data = get_netlab_catalog()
    write_data = [('netlab', i.get('name'), i.get('id'), i.get('parentId', '0')) for i in data]
    write_excel(write_data)
    if await executemany_query(query_write_vendors, write_data):
        print('Categories tried saved')
    else:
        print("XS")


async def save_data_netlab():
    proxy, faxy, maxy = [], [], []
    catalog_name = "В наличии"
    pre_vendor_categories = execute_query_return(query_read_need_category, ('netlab',))
    [maxy.extend(i) for i in pre_vendor_categories]
    # print('vendor_categories', maxy)
    for cat in maxy:
        data = category_action(catalog_name, int(cat))
        goods = data.get('goods')
        if goods:  # List
            for prod in goods:
                props = prod.get('properties')
                print('props', props)
                price = props.get('цена по категории D') * 1.08
                stocks = props.get('количество на Лобненской') + props.get('количество на Калужской')
                need_goods = (props['id'], props.get('производитель'), price,
                              'netlab', int(cat), props.get('название'), stocks)
                # props.get('цена по категории N'), props.get('цена по категории D'),
                # props.get('PN'), props.get('НДС'),
                proxy.append(need_goods)
        elif not goods and not data.get('leaf'):  # FIXME is it check sub_category??
            # faxy.append(int(cat))
            faxy.append((cat, goods))
            # sub_category = await execute_query_return(query_read_category, ('netlab', cat))
            # print(333333, cat, goods, data, faxy)
        else:
            continue

    await executemany_query(query_write_product, proxy)

    print('GET-', len(proxy), len(faxy))

    return proxy


def get_goods_properties(category_id, product_id):
    catalog_name = "В наличии"  # "Прайс-лист"  #
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/{catalog_name}/{category_id}/{product_id}.json?oauth_token=' + oauth_token
    answer = requests.get(url)
    data = json.loads(answer.text[5:])

    print('goodsAction', data)
    properties = {key: value for key, value in data.get('goodsResponse').get('data').get('properties').items() if
                  value != '-'}
    print(len(data.get('goodsResponse').get('data').get('properties').keys()), len(properties.keys()))


def goods_description_by_uid(uid):
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/goodsDescriptionByUid/{uid}.json?oauth_token=' + oauth_token
    try:
        answer = requests.get(url)
        data = json.loads(answer.text[5:])

        properties = data.get('goodsResponse').get('data').get('properties').items()
        proxy = {key: value for key, value in properties}
        # print(777777777, proxy)
        return True, proxy #properties  # {key: value for key, value in data.get('goodsResponse').get('data').get('properties').items() if  value != '-'}
    except:
        return False, {}
    # print(len(data.get('goodsResponse').get('data').get('properties').keys()), len(properties.keys()))

    # return properties


def goods_description_by_category(category_id):
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/goodsDescriptionByUid/{category_id}.json?oauth_token=' + oauth_token
    answer = requests.get(url)
    data = json.loads(answer.text[5:])

    print('goodsDescriptionByCategory', data)


def get_goods_images(product_id):
    oauth_token = read_netlab_access_token()
    url = f'http://services.netlab.ru/rest/catalogsZip/goodsImages/{product_id}.json?oauth_token=' + oauth_token
    sleep(0.02)
    answer = requests.get(url)
    data = json.loads(answer.text[5:])
    """{'entityListResponse': {
        'status': {
            'code': '200', 'message': ''
            }, 
        'data': {
            'items': 
            [
                {
                'id': 1, 
                'properties': {
                    'id': '1974813', 
                    'Url': 'http://serv02.netlab.ru/ISAPI/TestISAPI19.dll?572083&1&91', 
                    'lastUpdateTime': 1695424610037, 
                    'Heigth': None, 
                    'Width': None, 
                    'numberOfImages': 2, '
                    Size': 125249
                    }
                }, 
                {
                'id': 2, 
                'properties': {
                    'id': '1974813', 
                    'Url': 'http://serv02.netlab.ru/ISAPI/TestISAPI19.dll?572083&2&91', 
                    'lastUpdateTime': 1695424610037, 
                    'Heigth': None, 
                    'Width': None, 
                    'numberOfImages': 2,
                     'Size': 9213
                     }
                }
            ]
        }}}
    """
    try:
        image_url_list = data.get('entityListResponse').get('data').get('items')
        result = [i.get('properties').get('Url') for i in image_url_list]
        global_result = True
    except:
        # print('get_goods_images', data)
        global_result = False
        result = []

    return global_result, result


# get_netlab_token()
# # get_goods_images(1974813)
# # goods_description_by_uid(1974813)
# # goods_description_by_category(1974806)
# # get_goods_properties(1974806, 1974813)
# # asyncio.run(save_data_netlab())
# # create_csv_file_from_netlab_v2()
# # create_csv_file_from_netlab('Прайс-лист', [1974806])  #127955)
# # create_csv_for_category_from_netlab_v3()
# create_csv_for_category_from_netlab_v4()
# asyncio.run(save_categories_vendors())
# 11008078
