import json
#from prepare_data import read_price
import requests
from proxy import proxy_dicty


# r = requests.get('http://super-good.ml/test_json.json')
# data = r.json()


#dict: key = sku, value = min_quantity


#processing data from json (proxy file) for price & etc.
def processing_json():
    r = requests.get('http://super-puper.ml/test_json.json')
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
    print('result_dict_from_procces_json ', len(result_dict))   #, result_dict)
    return result_dict


def read_order_json():
    # with open("orders.json", 'r') as file:
    with open("/var/www/html/artol/orders.json", 'r') as file:
        result_dict = json.load(file)
    print('result_read_order ', len(result_dict), type(result_dict))
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