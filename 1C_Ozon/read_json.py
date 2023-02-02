import json
#from prepare_data import read_price
import requests
#import requests as requests
#
# wh_ozon = {'casual': ['OWLM200201', 'OWLM200300', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN50', 'ИМRUNN40', 'OWLM200302', 'OWLM200100', 'OWLM200301', 'OWLM200202', 'OWLT190301/2', 'OWLT190303/2', 'OWLT190402/2', 'OWLT190702/2', 'OWLT200901/2', 'OWLT190901/2', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'ИМALS80', 'OWLT190305'],
#            'kgt': ['OWLT190101', 'OWLT190302', 'OWLT190403S', 'OWLT190304', 'ИМOWLT190901', 'ИМOWLT200901', 'ИМMAL80', 'ИМHELLS65', 'ИМRUNN60', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200101', 'OWLM200102', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190303', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSS100', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190303', 'OWLT190402', 'OWLT190702', 'OWLT200901', 'OWLT190901', 'TOWLT190302', 'OWLT190201']
#            }

# r = requests.get('http://super-good.ml/test_json.json')
# data = r.json()


#processing TEST data from json (proxy file) for price & etc.
def processing_json():
    r = requests.get('http://super-good.ml/test_json.json')
    data = r.json()
    result_list = []
    for keys, value in data.items():
        #print('value----------===============', value)
        id_1c = keys
        vendor_code = value[0]
        price = value[1].get(u'Цена')  #["\u0426\u0435\u043d\u0430"]
        quantity = value[2].get(u'Остаток')
        outlets = value[3]
        # outlets = [key for key in value[3].keys()]
        proxy = (id_1c, vendor_code, price, quantity, outlets) # id_1C, vendor_vode (SKU), price, quantity
        #if quantity is not None:
        result_list.append(proxy)

    print('data', len(data), value)
    print('result_list', len(result_list))
    return result_list

#processing_json()


def read_order_json():
    with open('orders.json', 'r') as file:
        result_dict = json.load(file)
    print('result_dict ', len(result_dict), type(result_dict))
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
