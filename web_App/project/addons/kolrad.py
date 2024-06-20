import datetime
import sys
import requests
import json
import xmltodict
from project import DATA_PATH
import project.conn as conn


def get_kolrad_xml(link):
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





def standart_product(name_price=None):
    provider = 'kolrad'
    price_type = 'xml'
    distrib_data = conn.get_distibutor_data(provider,
                                           price_type,
                                           name_price)
    link = distrib_data[0]
    price_murkup = distrib_data[1]
    list_wheels_json = get_kolrad_xml(link)
    global_result = {}
    proxy = []
    for dictionary in list_wheels_json:
        try:
            name = dictionary['name'].strip('"')
            type = dictionary.get('type').strip('"').split(' ')[-1]
            if type == 'диски':
                category_id = 5
            else:
                category_id = 0

            try:
                description = dictionary.get('description')[:-145]
            except:
                description = ''
            if not description:
                description = name
            vendor = dictionary.get('vendor').replace('"', '')
            category = dictionary.get('type').strip('"')
            opt_price = int(dictionary.get('price').strip('"').replace('\xa0', '').split('.')[0])
            price = float(dictionary.get('RoznicaPrice').strip('"').replace('\xa0', '').split('.')[0])
            rule = False
            if opt_price * 1.18 >= price:
                rule = True
            in_stock = int(dictionary.get('rest').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest2').strip('"').replace('>', '').replace('<', '')) \
                       + int(dictionary.get('rest3').strip('"').replace('>', '').replace('<', ''))
            name_picture = '88888888'
            product_code = dictionary['vendor_code'].strip('"').strip('-')
            image_url = dictionary['foto'].strip('"')
            if image_url:
                name_picture = vendor.strip() + '_' + product_code + '.png'
            image_tuple = (name_picture, image_url)
            id_1c = ''
            provider = 'colrad'
            articul_product = vendor.strip() + '_' + product_code
            options = {
                'et': 'ET' + dictionary.get('et').strip('"'),
                "bolts_spacing": dictionary.get('pcd1').strip('"')
                                 + '/' + dictionary.get('pcd2').strip('"'),
                'diameter': dictionary.get('diameter').strip('"').strip('0').strip(','),
                'dia': 'D' + dictionary.get('dia').strip('"'),
                'width': dictionary.get('width').strip('"')
            }

            global_result.update({articul_product:
                    (
                        (category_id, name, description,
                         opt_price, in_stock,
                         product_code, vendor, category,
                         articul_product, id_1c, image_url,
                         price_murkup),
                        image_tuple,
                        options,
                        provider
                    )})

        except:
            # print("FUCKUP_standart_product_v2", dictionary)
            continue

    return global_result
