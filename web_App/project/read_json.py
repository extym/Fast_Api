import datetime
import json
# from prepare_data import read_price
import requests
import csv
from project.creds import link
from project.addons.wh_data import ozon_wh_id

# r = requests.get('http://super-good.ml/test_json.json')
# data = r.json()
# link = 'http://super-good.ml/test_json.json'


# processing TEST data from json (proxy file) for price & etc.
def process_json_list():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for keys, value in data.items():
        id_1c = keys
        vendor_code = value[0]
        price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
        if quantity < 3:
            quantity = 0

        outlets = value[4]
        # outlets = [key for key in value[3].keys()]
        proxy = (id_1c, vendor_code, price, quantity, outlets)  # id_1C, vendor_vode (SKU), price, quantity
        # if quantity is not None:
        result_list.append(proxy)

    return result_list


# processing_json()

def process_json_dict():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for keys, value in data.items():
        proxy = {}
        id_1c = keys
        vendor_code = value[0]
        price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
        if quantity < 3:
            quantity = 0

        outlets = value[4]
        # outlets = [key for key in value[3].keys()]
        proxy[vendor_code] = (id_1c, price, quantity, outlets)  # id_1C, vendor_vode (SKU), price, quantity
        # if quantity is not None:
        result_dict.update(proxy)

    return result_dict


# process_json_dict()


def process_json_dict_v2(outlet):
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        proxy = {}
        outlets = value[4]
        if outlets.get(outlet):
            vendor_code = value[0]
            price = value[1].get(u'Цена')
            quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
            if quantity < 3:
                quantity = 0
            proxy[vendor_code] = (key, price, quantity, outlets)  # id_1C, vendor_vode (SKU), price, quantity
            result_dict.update(proxy)
        else:
            continue

    return result_dict


# process_json_dict_v2(u'YM.СТМ')

def read_json_wb():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for keys, value in data.items():
        outlets = value[4]
        if 'WB.НашсклСТМ' in outlets.keys() or 'WB.СверхГБсклNEW' in outlets.keys():
            id_1c = keys
            vendor_code = value[0]
            price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
            outlets = value[4]
            barcode = value[3].get(u'Штрихкод')
            quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
            if quantity < 3:
                quantity = 0
            # quantity = 0
            proxy = (id_1c, vendor_code, barcode, quantity, outlets)
            if vendor_code != '' or vendor_code is not None:
                result_list.append(proxy)

    return result_list


lisst = ['OW06.07.00', 'OW06.04.00', 'ИМNYB80', 'ИМMAL80', 'OW03.09.05', 'OW07.05.00', 'ИМRUNN60', 'OW06.04.00',
         'ИМRUNN40', 'OW25.30.00', 'OW25.10.00', 'OW25.20.00', 'ИМSJEL100', 'ИМSJEL65', 'ИМSJEL80', 'OW25.06.00',
         'OW23.06.00', 'OW23.08.00', 'ИМVIND80', 'OW23.10.00', 'OW23.20.00', 'OW23.30.00', 'OW23.50.00', 'OW22.05.00',
         'OW22.06.00', 'OW24.04.02', 'OW24.04.01', 'ИМHELL100', 'ИМHELL65', 'OW29.50.12', 'OW29.60.12', 'OW29.70.12']
sub_vendor_code = {'ИМOWLIB191101': 'OWLIB191101', 'ИМOWLIB191102': 'OWLIB191102',
                   'ИМOWLIB191108': 'OWLIB191108'}  # 'ИМOWLIB191107': 'OWLIB191107',


def read_json_lm():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for keys, value in data.items():
        outlets = value[4]
        if 'LM.ЛеруаМерлен' in outlets.keys():
            id_1c = keys
            vendor_code = value[0]
            quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
            if quantity < 3 and vendor_code not in lisst:
                quantity = 0
            # vendor_code = sub_vendor_code.get(vendor_code, vendor_code)
            price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
            # if vendor_code in sub_vendor_code.values():
            #     print('all_ride_sub_vendor_code')
            # if vendor_code in sub_vendor_code:
            #     print('fuck_up_sub_vendor_code')
            proxy = (id_1c, price, quantity)  # id_1C, vendor_vode (SKU), price, quantity
            result_dict[vendor_code] = proxy

    return result_dict


# read_json_lm()

def read_json_lm_v2():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for id_1c, value in data.items():
        outlets = value[4]
        vendor_code = value[0]
        # vendor_code = sub_vendor_code.get(vendor_code, vendor_code)
        price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]

        if 'LM.ЛеруаМерлен' in outlets.keys():
            quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
            if quantity < 3 and vendor_code not in lisst:
                quantity = 0
        else:
            quantity = 0

        result_dict[vendor_code] = (id_1c, price, quantity)

    return result_dict


# read_json_lm_v2()

wh_list = ['OZ.RFBSнашсклДЛ', 'OZ.RFBSНашсклСДЭК', 'OZ.НашадостМиМО',
           'OZ.ОктКГnew', 'OZ.ОснКурьер', 'OZ.ДостКГ']



# def read_json_on():
#     r = requests.get(link)
#     data = r.json()
#     result_dict = {}
#     for key, value in data.items():
#         outlets = value[4]
#         for wh in wh_list:
#             pr = []
#             if wh in outlets.key():
#                 pr.append(wh)
#                 id_1c = key
#                 vendor_code = value[0]
#                 price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
#                 quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
#                     if quantity < 0:
#                         quantity = 0
#                 in_outlet = ozon_wh_id[wh][0]
#                 # out = [key for key in value[4].keys()]
#                 proxy = (id_1c, price, quantity, in_outlet)
#                 result_dict[vendor_code] = proxy
#     print('result_dict', len(result_dict), in_outlet, result_dict)
#     return result_dict

def read_json_on():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        outlets = value[4].keys()
        id_1c = key
        vendor_code = value[0]
        price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
        if quantity < 3:
            quantity = 0

        in_outlets = [ozon_wh_id[out][0] for out in ozon_wh_id if out in outlets]
        proxy = (id_1c, price, quantity, in_outlets)
        result_dict[vendor_code] = proxy

    print('result_dict_on', len(result_dict))
    return result_dict


# read_json_on()

def read_json_sper():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for key, value in data.items():
        outlets = value[4]
        if 'SBMM.Сбермегамаркет' in outlets.keys():
            id_1c = key
            vendor_code = value[0]
            price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
            quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
            if quantity < 3:
                quantity = 0
            proxy = (id_1c, vendor_code, price, quantity)  # id_1C, vendor_vode (SKU), price, quantity
            # result_dict[vendor_code] = proxy
            result_list.append(proxy)

    return result_list


def read_json_ids():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        id_1c = key
        vendor_code = value[0]
        price = value[1].get(u'Цена')
        quantity = value[2].get(u'Остаток', 0)  # - value[2].get(u'Резерв', 0)
        if quantity < 3:
            quantity = 0

        result_dict[vendor_code] = (id_1c, price, quantity)

    return result_dict


def read_order_json():
    with open('orders.json', 'r') as file:
        result_dict = json.load(file)
    # printt('result_dict ', len(result_dict), type(result_dict))
    return result_dict


# processing data from request (proxy file) for price & etc.
def processing_request():
    with open('request.json', 'r') as file:
        request_data = json.load(file)
        result_list = []
        for key, value in request_data.items():
            id_1c = key
            vendor_code = value[0]
            price = value[1][u'Цена']  # ["\u0426\u0435\u043d\u0430"]
            quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
            if quantity < 0:
                quantity = 0
            proxy = (id_1c, vendor_code, price, quantity)  # id_1C, vendor_vode (SKU), price, quantity
            result_list.append(proxy)

        # printt(len(result_list))

    return result_list


# with open('11.csv', 'r') as file:
#     reader = csv.reader(file, delimiter=';')
#     # for row in reader:
#     #     print(row)
#     lisst = [str(i[0]) for i in reader]
#     print(lisst)
import os
# def make_log():
#     # PATH = '/var/www/html/stm/'
#     today = str(datetime.datetime.today()).replace(' ', '_')[:-7]
#     try:
#         os.system(f'cp /var/www/html/stm/test_json.json /var/www/html/stm/test_json_{today}.json')
#         print("ALL_RIDE_make_log_json")
#     except:
#         print("FACK_UP_make_log_json")
