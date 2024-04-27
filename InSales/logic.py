import requests
import csv
from creds import *
import zeep
import os
from suds.client import Client as SudsClient
from suds.transport.https import HttpAuthenticated
from suds.xsd.doctor import Import, ImportDoctor
from suds.sudsobject import asdict
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from conn import executemany_query, execute_query_return, query_write_vendors
from conn_maintenance import *
import asyncio
from brand import *

# wsdl = 'https://3logic.ru/ws/soap/soap.php?wsdl'
# client = zeep.Client(wsdl=wsdl)
#

add_link = 'https://3logic.ru/'


def write_excel(data):
    with open('logic_cats.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print('ALL_RIDE')


async def save_categories_vendor():
    data_list = get_category_list()
    write_data = [('logic', i.get('category_name'), i.get('category_id'), i.get('parent_id', '0'))
                  for i in data_list]
    write_excel(write_data)
    if await executemany_query(query_write_vendors, write_data):
        print('Categories tried saved')
    else:
        print("XS")


def write_categories_vendor():
    data_list = get_category_list()
    write_data = [('logic', i.get('category_name'), i.get('category_id'), i.get('parent_id', '0'))
                  for i in data_list]
    write_excel(write_data)
    print('ALL_RIDE')


def get_client_logic():
    session = Session()
    session.auth = HTTPBasicAuth(login, password)
    client = Client('https://3logic.ru/ws/soap/soap.php?wsdl',
                    transport=Transport(session=session))

    return client


def get_category_list():  # getCategoryList
    category_list = get_client_logic().service.getCategoryList()
    data_list = zeep.helpers.serialize_object(category_list)
    # print('getCategoryList', len(data_list), data_list, sep='\n')
    print('getCategoryList', len(data_list))
    return data_list


def get_product_list(category_id: int):
    get_image = True
    get_description = True
    product_list = get_client_logic().service.getProductList(category_id, get_image, get_description)

    # print('getProductList', len(product_list))
    return zeep.helpers.serialize_object(product_list)


def get_price_list(mat_ids):
    client = SudsClient(url='https://3logic.ru/ws/soap/soap.php?wsdl',
                    transport=HttpAuthenticated(username=login, password=password))
    response = client.service.getPriceList(mat_ids)
    # ll = [asdict(i) for i in response]

    return {i['mat_id']: {'price': i['price'] * 1.05, 'stock': i['remain']} for i in response if
              (i['no_price'] != 1 and i['remain'] != 0)}


def get_brand_list():
    product_list = get_client_logic().service.getBrandList()
    # print('getBrandList', len(product_list), product_list)
    result = {i['brand_id']: i['brand_name'] for i in product_list}
    print('getBrandList', len(result), result)
    return result


def rewrite_description(description: str):
    proxy = description.replace(';', ',').split('\n')
    faxy, maxy, prx = {}, {}, {}
    for pos in proxy:
        try:
            if pos.rstrip()[-1] == ':':
                paxy = []
                index = proxy.index(pos)
                while proxy[index + 1].startswith('   '):
                    paxy.append(proxy[index + 1])
                    faxy[pos] = '\n'.join(paxy).replace(';', '')
                    index += 1
                    # print('faxy', faxy)
            elif ":" in pos:
                ps = pos.split(':', 1)
                maxy[ps[0]] = ps[1]
            else:
                ps = pos.split('0')
                maxy[ps[0]] = ' '.join(ps[1:])
        except IndexError:
            for i in proxy:
                xs = i.replace('\r', '').replace(' / ', '/').replace(' : ', ': ')
                try:
                    prx.update(dict(xs.split(': ')))
                except:
                    print(i, 2222, xs)
                    continue

                faxy.update(prx)
            # print(pos, 111113, proxy)
            continue

    maxy.update(faxy)
    # print(457, maxy)

    return maxy


def create_csv_for_category_from_logic():  ##for import goods only (maybe)
    list_cats = execute_query_return(query_get_actual_cats_v2, ('logic',))
    category_ids = {}
    category_groups = {}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    site_category_path = {key: value[2] for key, value in category_ids.items()}
    base_fields = ['category_id', 'brand', 'full_name', 'quantity', 'price', 'published',
                   'image_short', 'image_additional', 'image_main', 'id', 'stock']
    allpro = []
    for key in category_groups.keys():
        count = 0
        result_list, ids = [], []
        rewrite_properties, prod = {}, {}
        for category_id in category_groups.get(key):
            site_category_name = category_ids[category_id][1]
            try:
                data = get_product_list(category_id)
            except:
                continue

            for prod in data:
                proxy = dict()
                ids.append(prod.get('product_id'))
                proxy['id'] = prod.get('product_id')
                proxy['published'] = site_category_path[category_id]
                proxy['category_id'] = site_category_name  # category_id
                proxy['quantity'] = prod.get('product_remain')
                proxy['price'] = prod.get('product_price_dealer') * 1.05
                proxy['brand'] = logic_brand_list.get(prod.get('brand_id'))
                proxy['full_name'] = prod.get('product_full_name')
                # proxy['id'] = prod.get('product_id')
                pre_descr = prod.get('product_description')
                if pre_descr:
                    description = rewrite_description(prod.pop('product_description'))
                    ########### extend fields. Is it need? #############

                    # print('description_logic', description)
                    proxy.update(description)
                    rewrite_properties.update(description)  # TODO It's need if size fields is not constant
                ####################################################
                # else:
                #     description = prod.get('product_full_name')
                #     print('FUCK_UP_description', prod)
                if prod.get('product_image_main'):
                    proxy['image_main'] = add_link + prod.get('product_image_main')
                else:
                    proxy['image_main'] = 'NOT_FOUND'

                if prod.get('product_image_short'):
                    proxy['image_short'] = add_link + prod.get('product_image_short')
                else:
                    proxy['image_short'] = 'NOT_FOUND'

                if prod.get('product_image_additional'):
                    proxy['image_additional'] = add_link + prod.get('product_image_additional')
                else:
                    proxy['image_additional'] = 'NOT_FOUND'

                count += 1
                result_list.append(proxy.copy())

                # print(f'prod_{key} ', len(prod.keys()), prod.keys())
            try:
                rewrite_properties.update(prod)
            except Exception as error:
                print('Some_fuck_up_logic {} \n {}'.format(error, prod))
                continue
        # print(3311111133, len(ids), ids)
        price_list = get_price_list(ids)
        # print(3333333, len(price_list), price_list)
        pro_result_list = []
        for item in result_list.copy():
            id_item = item.get('id')
            if id_item in price_list.keys():
                item.update(price_list[id_item])
                pro_result_list.append(item)
        # pro_result_list = [i.update(price_list.get(i['id'])) for i in result_list
        #                   if i['id'] in price_list.keys()]
        # print(5555555555555, len(pro_result_list), pro_result_list)

        fields = base_fields.copy()
        # pr = set([i.strip().capitalize() for i in set(rewrite_properties.keys())])
        pr = sorted(set(rewrite_properties.keys()))
        fields.extend(pr)
        print(count, '_all_prod_group')
        print('fields_logic_{}_group {} {}'.format(key, len(fields), fields))

        with open(CSV_PATH + f'logic_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', dialect='excel',
                                    restval='', fieldnames=fields)
            writer.writeheader()
            writer.writerows(pro_result_list)    #(result_list)

        print(count, '_all_prod_logic', key)

        # break

        allpro.extend(result_list.copy())

    with open(CSV_PATH + f'logic-all.csv', 'w') as file:
        writer = csv.DictWriter(file, dialect='excel', restval='', delimiter=';',
                                extrasaction='ignore', fieldnames=base_fields)
        writer.writeheader()
        writer.writerows(allpro)


# dss = ['Операционная система:  Andoid 12, MIUI Pad 13', 'Тип дисплея:  IPS', 'Диагональ дисплея, дюйм:  10.61', 'Разрешение дисплея:  2000x1200', 'Яркость, кд/м2:  400', 'Процессор:  MediaTek Helio G99', 'Видеокарта:  ARM Mali-G57 MC2', 'Оперативная память, ГБ:  4', 'Хранение данных, ГБ:  128', 'Беспроводное подключение:  ', '   WiFi:  WLAN 802.11a/b/g/n/ac', '   Bluetooth:  5.3', 'Проводное подключение:  ', '   USB Type-C:  1', 'Слоты:  ', '   Слот для карт памяти:  1 x microSD (до 1ТБ)', 'Тыловая камера, Мп:  8', 'Фронтальная камера, Мп:  8', 'Микрофон:  Да', 'Динамики:  4 динамика с поддержкой Dolby Atmos', 'Датчики, сенсоры:  датчик света, акселерометр, компас, гироскоп, сканер отпечатков пальцев, распознавание лица', 'Основной цвет:  Серый', 'Материал:  Металл', 'Питание:  Аккумулятор: емкость - 8000 мАч', 'Габариты:  ', '   Высота, мм:  254.7', '   Ширина, мм:  166.3', '   Толщина, мм:  6.9', 'Вес нетто, грамм:  511', 'Особенности:  Поддержка быстрой зарядки до 18W', 'Ссылка на описание:  https://ru-mi.com/product/42837/', 'Комплект поставки:  Планшет, документация, зарядное устройство, кабель USB-C, скрепка']
# desc = '\n'.join(dss)
# rewrite_description(desc)

# desc_str = 'Тип инструмента:  Насадка-пистолет\nОбласть применения:  Накачивание шин, надувных лодок, мячей и пр.\nМаксимальное давление:  16 Bar\nИндикаторы/приборы:  Манометр psi/bar\nВыходной коннектор:  Быстросъемный универсальный наконечник для автошин\nОсновной материал:  Алюминиевый сплав\nОсновные цвета:  Черный\nПитание:  Не требуется\nОсобенности:  Габариты в упаковке - 160x340 мм\nКомплект поставки:  Насадка-пистолет, инструкция'
# print(rewrite_description(desc_str))

# ids = [70910, 70918, 70919, 70920, 70921, 75093, 80366, 80367, 80371, 80372, 80373, 80374, 80375, 81038, 81039, 81040, 81041, 82357, 82358, 82359, 82363, 82364, 82365, 82393, 82400, 82402, 82403, 82404, 82405, 82406, 82408, 82409, 82412, 82415, 82416, 82419, 82420, 82421, 82426, 82427, 82432, 82476, 82489, 82493, 83020, 83262, 83970, 84686, 84876, 84877, 84878, 84879, 85372, 86835, 86836, 86837, 86838, 86899, 87040, 90295, 90570, 91017, 91018, 91838, 91839, 91840, 91842, 92277, 92916, 92945, 93838, 93839, 93840, 93841, 93905, 95592, 95596, 95597, 95884, 95886, 95930, 96219, 97843, 99043, 99044, 99449, 99450, 100948, 101856, 102858, 104741, 104742, 104743, 106224, 106225, 106435, 106436, 106633, 106639, 107538, 107540, 107544, 107798, 107799, 107825, 107826, 107827, 108522, 108890, 109279, 110139, 110359, 110745, 111058, 111059, 111334, 111335, 112414, 112416, 112417, 112419, 112420, 112421, 112424, 113843, 113932, 114816, 115404, 115611, 115910, 116044, 116045, 116048, 116083, 116245, 116246, 116247, 116248, 116269, 116281, 116283, 116285, 116291, 116292, 116318, 116433, 116436, 116437, 116438, 116440, 116441, 116509, 117210, 117582, 117657, 118400, 118401, 118402, 118403, 118404, 118405, 118407, 118408, 118412, 118633, 118634, 118662, 118787, 118921, 119148, 119345, 119476, 119477, 119763, 120520, 120531, 121031, 121137, 121196, 121197, 121199, 121375, 121604, 121722, 121776, 121827, 122111, 122438, 122439, 122576, 123053, 123054, 123055, 123056, 123058, 123059, 123062, 123093, 123204, 123437, 123469, 125647, 126066, 126067, 126069, 126323, 127097, 128751, 128954, 128972, 128973, 128975, 128976, 128977, 128980, 129184, 129773, 130160, 130161, 130177, 130189, 130240, 130241, 130429, 130664, 130727, 131190, 131200, 132152, 132591, 133179, 133479, 133911, 133916, 134777, 134778, 134779, 135011, 136578, 138773, 140050, 140602, 140604, 140857, 140858, 140859, 141859, 141897, 141900, 143095, 143404, 42752, 70912, 70914, 73802, 80377, 81030, 81035, 81037, 82367, 82370, 82371, 82372, 82373, 82374, 82375, 82377, 82378, 82396, 82397, 82437, 82440, 82447, 82450, 82451, 82454, 82456, 82458, 82460, 82463, 82466, 82467, 82506, 82523, 84881, 84882, 84883, 84884, 84885, 84886, 84888, 84889, 85625, 85626, 85627, 86834, 87041, 87042, 89979, 90300, 91006, 91539, 91837, 92479, 92775, 92944, 93015, 94371, 95762, 95939, 99448, 101054, 101588, 104740, 105155, 106371, 106373, 106755, 107537, 107542, 107543, 107545, 107804, 109384, 109385, 109821, 109823, 109825, 109996, 110257, 110484, 111332, 111333, 111850, 112411, 112412, 112698, 112811, 112957, 113732, 115624, 116056, 116249, 116250, 116287, 116288, 116290, 116294, 116478, 118112, 118415, 118417, 118418, 118419, 118422, 118632, 118635, 118637, 118788, 119154, 119478, 120521, 121140, 121198, 122055, 122324, 122826, 123061, 123063, 123064, 123094, 123190, 123191, 126070, 128987, 134776, 135030, 135082, 135874, 136076, 138774, 138908, 140601, 140855, 141898, 141899, 143132, 145152, 53443, 53655, 53656, 53657, 53658, 53659, 59371, 59372, 103627, 103628, 103629]
# dds = [{'mat_id': i, 'value': ids[i]} for i in range(len(ids))]
# get_price_list(ids)

# get_category_list()
# get_product_list(177)
# get_brand_list()
# asyncio.run(save_categories_vendor(data_list))
# create_csv_for_category_from_logic()
# write_categories_vendor()
