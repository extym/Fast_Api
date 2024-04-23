import json
#from prepare_data import read_price
import requests
from proxy import proxy_dicty
from cred import link


# r = requests.get('http://super-good.ml/test_json.json')
# data = r.json()


#dict: key = sku, value = min_quantity

# link = 'http://artol-json.i-bots.ru/test_json.json'
# link = 'http://super-puper.ml/test_json.json'
#processing data from json (proxy file) for price & etc.
def processing_json():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        id_1c = key
        #print(value)
        sku = value[3]['АртикулЯндекс']
        vendor_code = value[0]
        price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток')
        booked = value[2].get(u'Резерв')
        if quantity is not None and booked is not None:
            quantity -= booked
        min_quantity = proxy_dicty.get(sku)

        result_dict[sku] = {'id_1c': id_1c, 'vendor_code': vendor_code, 'price_ym': price,
                            'stock': quantity, 'min_quantity': min_quantity}
    #print(sku, result_dict[sku])
    print('result_dict_artol_procces_json ', len(result_dict))   #, result_dict)
    return result_dict


def read_json_ids():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        id_1c = key
        sku = value[3][u'АртикулЯндекс']
        price = value[1].get(u'Цена')
        quantity = value[2].get(u'Остаток', 0)  - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        result_dict[sku] = (id_1c, price, quantity)

    return result_dict


def read_json_on():
    r = requests.get(link)
    data = r.json()
    result_dict = {}
    for key, value in data.items():
        # outlets = value[4].keys()
        id_1c = key
        sku = value[3][u'АртикулЯндекс']
        # vendor_code = value[0]
        price = value[1].get(u'Цена')  # ["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток', 0) - value[2].get(u'Резерв', 0)
        if quantity < 0:
            quantity = 0
        # in_outlets = [ozon_wh_id[out][0] for out in ozon_wh_id if out in outlets]
        result_dict[sku] = (id_1c, price, quantity)

    print('result_dict_on', len(result_dict))
    return result_dict


def read_order_json():
    try:
        with open("/var/www/html/artol/orders.json", 'r') as file:
            result_dict = json.load(file)
    except:
        with open("orders.json", 'r') as file:
            result_dict = json.load(file)
    print('result_read_order ', len(result_dict), result_dict.keys())
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
            quantity = value[2][u'Остаток']
            proxy = (id_1c, vendor_code, price, quantity) # id_1C, vendor_vode (SKU), price, quantity
            result_list.append(proxy)

        #print(len(result_list))

    return result_list


# processing_json()