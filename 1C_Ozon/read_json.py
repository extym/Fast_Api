import json
#from prepare_data import read_price
import requests
#import requests as requests
#


# r = requests.get('http://super-good.ml/test_json.json')
# data = r.json()

link = 'http://stm-json.i-bots.ru/test_json.json'
#processing TEST data from json (proxy file) for price & etc.
def process_json_list():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for keys, value in data.items():
        id_1c = keys
        vendor_code = value[0]
        price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        outlets = value[4]
        # outlets = [key for key in value[3].keys()]
        proxy = (id_1c, vendor_code, price, quantity, outlets) # id_1C, vendor_vode (SKU), price, quantity
        #if quantity is not None:
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
        price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        outlets = value[4]
        # outlets = [key for key in value[3].keys()]
        proxy[vendor_code] = (id_1c, price, quantity, outlets) # id_1C, vendor_vode (SKU), price, quantity
        #if quantity is not None:
        result_dict.update(proxy)

    return result_dict

def read_json_wb():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for keys, value in data.items():
        outlets = value[4]
        if 'WB.НашсклСТМ'  in outlets.keys():  # or 'WB.СверхГБсклСТМ'  in outlets.keys():
            id_1c = keys
            vendor_code = value[0]
            price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
            outlets = value[4]
            quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
            if quantity < 0:
                quantity = 0
            proxy = (id_1c, vendor_code, price, quantity, outlets)
            if vendor_code != '' or vendor_code is not None:
                result_list.append(proxy)


    return result_list

#read_json_wb()

def read_json_lm():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for keys, value in data.items():
        outlets = value[4]
        if 'LM.ЛеруаМерлен' in  outlets.keys():
            id_1c = keys
            vendor_code = value[0]
            price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
            quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
            if quantity < 0:
                quantity = 0
            proxy = (id_1c, price, quantity) # id_1C, vendor_vode (SKU), price, quantity
            result_dict[vendor_code] = proxy

    return result_dict

#read_json_lm()


wh_list = ['OZ.RFBSнашсклДЛ', 'OZ.RFBSНашсклСДЭК', 'OZ.НашадостМиМО',
      'OZ.ОктКГnew', 'OZ.ОснКурьер', 'OZ.ДостКГ']
from proxy import ozon_wh_id

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
        quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        in_outlets = [ozon_wh_id[out][0] for out in ozon_wh_id if out in outlets]
        proxy = (id_1c, price, quantity, in_outlets)
        result_dict[vendor_code] = proxy

    print('result_dict_on', len(result_dict))
    return result_dict

#read_json_on()

def read_json_sper():
    r = requests.get(link)
    data = r.json()
    result_list = []
    for key, value in data.items():
        outlets = value[4]
        if 'SBMM.Сбермегамаркет' in  outlets.keys():
            id_1c = key
            vendor_code = value[0]
            price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
            quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
            if quantity < 0:
                quantity = 0
            proxy = (id_1c, vendor_code, price, quantity) # id_1C, vendor_vode (SKU), price, quantity
            #result_dict[vendor_code] = proxy
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
        quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        result_dict[vendor_code] = (id_1c, price, quantity)

    return result_dict



def read_order_json():
    with open('orders.json', 'r') as file:
        result_dict = json.load(file)
    #printt('result_dict ', len(result_dict), type(result_dict))
    return result_dict

#processing data from request (proxy file) for price & etc.
def processing_request():
    with open('request.json', 'r') as file:
        request_data = json.load(file)
        result_list = []
        for key, value in request_data.items():
            id_1c = key
            vendor_code = value[0]
            price = value[1][u'Цена']  #["\u0426\u0435\u043d\u0430"]
            quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
            if quantity < 0:
                quantity = 0
            proxy = (id_1c, vendor_code, price, quantity) # id_1C, vendor_vode (SKU), price, quantity
            result_list.append(proxy)

        #printt(len(result_list))

    return result_list
