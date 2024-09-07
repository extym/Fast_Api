from datetime import datetime,  timedelta
import random
import string
import asyncio
from read_json import read_json_wb, read_json_ids
import requests
import json
from cred import wb_apikey, wh
from conn import *
from proxy import proxy_wb_orders
#data = read_json_wb()
#https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}
# link = 'https://suppliers-api.wildberries.ru'
link = 'https://marketplace-api.wildberries.ru'
l = 'https://suppliers-api.wildberries.ru/api/v3/supplies'

compare_id = {'Артикул поставщика': 'Штрихкод товара', 'OWLT190301/2': '6973720576435', 'OWLT190303/2': '6973720576442',
              'OWLT190402/2': '6973720577920', 'OWLT190702/2': '6973720577906',
              'OWLT190901/2': '6973720577982', 'OWLT200901/2': '6973720586526', 'д.к б.о н.с': '6973772601048',
              'д.к б.о ABS': '6973772601031', 'д.к с.о': '2000000185217', 'д.к с.о н.с': '6973772601062',
              'д.к с.о ABS': '6973772601055', 'OWLM200100': '4610029051226', 'OWLM200101': '4610029051233',
              'OWLM200102': '4610029051240', 'OWLM200103': '4610029051257', 'OWLM200200': '4610029051264',
              'OWLM200201': '4610029051271', 'OWLM200202': '4610029051288', 'OWLM200300': '4610029051295',
              'OWLM200301': '4610029051301', 'OWLM200302': '4660124924550', 'OWLM200400': '4610029051127',
              'OWLM200500': '4610029051134', 'OWLM200501': '4610029051172', 'OWLM200502': '4610029051189',
              'OWLM200600': '4610029051196', 'OWLM200601': '4610029051219', 'OWLM200602': '4610029051202',
              'OW03.11.05': '4610093021439', 'OW03.13.05': '4610093021446', 'OW06.05.00': '4610093021026',
              'OW06.07.00': '4610093021040', 'OW07.04.00': '4610093020982', 'OW07.05.00': '4610093020999',
              'OW23.10.00': '4610093020906', 'OW23.20.00': '4610093020913', 'OW23.30.00': '4610093020920',
              'OW23.40.00': '4610093020937', 'OW23.50.00': '4610093020944', 'OW24.20.00': '4610093021545',
              'OW25.10.00': '4610093020968', 'OW25.20.00': '4610093020975', 'OW25.30.00': '4610093020951',
              'OW29.50.12': '4610093020869', 'OW29.60.12': '4610093020876', 'OW29.70.12': '4610093020883',
              'ИМALS80': '2000000186238', 'ИМEL55': '2000000185514', 'ИМEL75': '2000000185538',
              'ИМHELL120': '2000000185552', 'ИМHELL65': '2000000185569', 'ИМHELLS100': '2000000185583',
              'ИМHELLS65': '2000000185606', 'ИМHELLS80': '2000000185613', 'ИМMAL100': '2000000185620',
              'ИМMAL80': '2000000185637', 'ИМRAG100': '2000000185675', 'ИМRAG85': '2000000185682',
              'ИМRUNN40': '2000000185699', 'ИМRUNN50': '2000000185705', 'ИМRUNN60': '2000000185712',
              'ИМSJEL100': '2000000185729', 'ИМSJEL65': '2000000185736', 'ИМSJEL80': '2000000185743',
              'ИМSS65': '2000000185767', 'ИМSS80': '2000000185774', 'ИМVESS105': '2000000185781',
              'ИМVESS75': '2000000185804', 'ИМVIND50': '2000000185897', 'ИМVIND60': '2000000185880',
              'ИМVIND70': '2000000185873', 'ИМVIND80': '2000000185866', 'ИМVINDS80': '2000000185828',
              'OW00.00.01': '4670015113109', 'OWLB191000': '6973720578354', 'OWLB191015': '6973720578194',
              'OWLT190305': '6973720589008', 'OWLB191032': '6973720590950', 'OWLB191033': '6973720590967',
              'OWLB191034': '6973720590974', 'OWLB191035': '6973720590981', 'OWLB191036': '6973720590998',
              'OWLB191037': '6973720591001', 'OWLB191038': '6973720591018', 'ИМSS100': '2000000185750',
              'OWLB191039': '6973720591025', 'OWLB191044': '6973720591070', 'OWLB191045': '6973720591087',
              'OWLB191046': '6973720591094', 'ИМOWLT190301': '2000000185453', 'ИМOWLT190303': '2000000185460',
              'ИМOWLT190402': '2000000185477', 'ИМOWLT190702': '2000000185484', 'ИМOWLT190901': '2000000185491',
              'ИМOWLT200901': '2000000185507', 'OWLT190101': '6973720575360', 'OWLT190302': '6973720575414',
              'OWLT190304': '6973720585482', 'OWLT190403S': '2000000185194',
              'OWLT190404': '6973720577975', 'OWLT190601': '6973720577883', 'OWLT190801': '6973720577944',
              'TOWLT190302': '6973772600959', 'OWLT190301': '6973720575407', 'OWLT190303': '6973720575421',
              'OWLT190402': '6973720577937', 'OWLT190702': '6973720577913', 'OWLT190901': '6973720577999',
              'OWLT200901': '6973720586519', 'OW03.09.05': '4610093020760', 'OW04.09.00': '4610093020784',
              'OW06.04.00': '4610093020777', 'OW22.05.00': '4610093020814', 'OW22.06.00': '4610093020845',
              'OW23.06.00': '4610093020807', 'OW23.08.00': '4610093020852', 'OW24.04.00': '4610093020753',
              'OW24.04.01': '4610093022849', 'OW24.04.02': '4610093022832', 'OW24.05.00': '4610093020821',
              'OW25.05.00': '4610093020838', 'OW25.06.00': '4610093020791', 'OW29.01.12': '4610093020746',
              'ИМHELL100': '2000000185545', 'ИМHELL80': '2000000185576', 'ИМHELLS120': '2000000185590',
              'ИМVINDS70': '2000000185835', 'ИМVINDL40': '2000000185859', 'ИМOWLT190305': '6973772605084',
              'OWLC19-007': '6973720577487', 'ИМOWLT190302': '6973772605077', 'OWLC19-014': '6973772600966',
              'OWLINSTNI+OWLT190403S': '2000000186122', "OWLC19-002": "6973720575742", "OWLC19-003": "6973720575759",
              "OWLC19-006": "6973720575780", "OWLC19-010": "6973720585239", "OWLC19-013": "6973772599925",
              "OWLC19-015": "6973772600973"}  # ,'OW06.06.00': '4610093021033', 'OWLT190305': '6973720575438'}

      #{"name_1C": "WB.СверхГБсклСТМ", "name":"Сверхгабаритный СТМ склад","id":664704}] # {"name":"Сверхгабаритный товар","id":730558, "name_1C": "WB.СверхГБсклNEW"}


def token_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)
    # print(pt)
    return pt

def day_for_stm(string):
    datta = datetime.strptime(string, '%Y-%m-%d')
    dat = datta.weekday()
    dtt = datta.strftime('%d-%m-%Y')
    if 1 <= dat <= 4:
        dtt = (datta - timedelta(1)).strftime('%d-%m-%Y')
    elif dat == 5:
        proxy = datta + timedelta(2)
        dtt = proxy.strftime('%d-%m-%Y')
    elif dat == 6:
        proxy = datta + timedelta(1)
        dtt = proxy.strftime('%d-%m-%Y')

    #print('datta',dat,  dtt)
    return dtt


def make_send_data():
    data = read_json_wb()
    # print('make_send_data_wb', len(data))
    warehouse = {}
    for string in wh:
        stocks = []
        w_house = string['id']
        warehouse[w_house] = {'stocks': stocks}
        for row in data:
            barcode = row[2]
            sku = compare_id.get(row[1], barcode) #barcode WB
            if sku is not None and string['name_1C'] in row[4].keys():
                proxy = {
                    'sku': sku,
                    'amount': row[3]
                }
                stocks.append(proxy)
            elif sku is None:
                print('ERROR_sku_WB', sku, row[1])

        warehouse[w_house] = {'stocks': stocks}

    print('warehouse[1072659]', len(warehouse[1072659]['stocks']))
    print('warehouse[989116]', len(warehouse[989116]['stocks']))
    # print(warehouse.keys())
    return warehouse

# make_send_data()

def send_stocks_wb():
    data = make_send_data()
    for key, value in data.items():
        metod = '/api/v3/stocks/'
        target = link + metod + str(key)
        headers = {'Content-type': 'application/json',
                   'Authorization': wb_apikey }
        print('SEND_WB', key, len(value['stocks']))
        answer = requests.put(target, data=json.dumps(value), headers=headers)
        re_data = answer.text

        print('send_stocks_wb', key, re_data, len(value['stocks']), value)

# send_stocks_wb()


def check_is_exist(id_mp, shop):
    data = check_order(query_read_order, (id_mp, shop))
    print(data, id_mp, shop)
    if len(data) > 0:
        result = True
    else:
        result = False

    return result


def get_new_supply_wb(next):
    headers = {'Content-type': 'application/json',
                   'Authorization': wb_apikey }
    params = {
        "next": next,  #0
        "limit": 500
    }
    metod = '/api/v3/supplies'
    url = link + metod
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    next_page = data['next']  #32899717
    print('get_new_supply_wb', response, data)
    return response, data, next_page


# get_new_supply_wb()
#https://suppliers-api.wildberries.ru/api/v3/supplies/{supply}/orders


def get_orders_from_supply_wb(supply_id):
    headers = {'Content-type': 'application/json',
                   'Authorization': wb_apikey }

    metod = '/api/v3/supplies/' + str(supply_id) + '/orders'
    url = link + metod
    response = requests.get(url, headers=headers)
    data = response.json()

    print('get_orders_from_supply_wb', response, len(data), data)
    return response, data

# get_new_orders_wb("WB-GI-41149707")

#https://suppliers-api.wildberries.ru/api/v3/orders/new
def get_new_orders_wb():
    headers = {'Content-type': 'application/json',
                   'Authorization': wb_apikey }

    metod = '/api/v3/orders/new'
    url = link + metod
    response = requests.get(url, headers=headers)
    data = {}
    if response.ok:
        data = response.json()
        print('ALL_RIDE_get_new_orders_wb', response, len(data), data, 'response', response.text)
    else:
        print('FUCK_UP_get_new_orders_wb ', response.status_code, 'response', response.text)
    return data

async def get_id_1c(vendor_code):
    data = read_json_ids()
    if vendor_code in data.keys():
        id_1c = data[vendor_code][0]

        return id_1c

async def processing_orders_wb():
    # orders = proxy_wb_orders["orders"]    # FOR TEST ONLY TODO
    orders = get_new_orders_wb().get("orders")
    if orders and len(orders) > 0:
        for order in orders:
            id_mp = str(order["id"])
            our_id = token_generator()
            shop_Name = "WB"
            check = check_is_exist(id_mp, shop_Name)
            if check:
                continue
            else:
                shipment_Date = proxy_time_1()   #order["createdAt"] #TODO plus 1 day?
                status = "CREATED"
                our_status = "NEW"
                payment_Type = "PREPAID"
                delivery = order.get("deliveryType", 'Not_Know')
                # list_items = order["skus"]
                summ_order = order["price"] / 100
                vendor_code = order["article"]
                quantity = order.get("quantity", 1)
                id_1c = await get_id_1c(vendor_code)
                result = (id_mp, our_id, shop_Name, shipment_Date,
                             status, our_status, payment_Type, delivery)
                await execute_query(query_write_order, result)
                items_data = (id_mp, our_id, shop_Name, "NEW", vendor_code,
                              id_1c, quantity, summ_order)
                print('items_data_WB', items_data)
                await executemany_query(query_write_items, [items_data])
        print(f"Write {len(orders)} orders WB")

    print("Not found orders WB now")

# asyncio.run(processing_orders_wb())

def get_wh():
    headers = {'Content-type': 'application/json',
               'Authorization': wb_apikey }
    # link = 'https://suppliers-api.wildberries.ru/api/v2/warehouses'
    link = 'https://marketplace-api.wildberries.ru/api/v3/warehouses'
    answer = requests.get(link, headers=headers)
    text = answer.text
    print(answer)
    print('get_wh', text)

# get_wh()