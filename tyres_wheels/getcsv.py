import json
import sys

import wget
import csv
import datetime

from categories import categories_summer, categories_wheels, categories_winter, categories_allseason


tn = datetime.datetime.now()
ts = datetime.datetime.timestamp(tn) * 1000
date = str(ts)[:13]
type_data = ['wheels', 'tyres']
url = 'https://duplo.shinservice.ru/xml/shinservice-b2b-tyres.csv?id=88964843&t=' + date
url = 'https://duplo.shinservice.ru/xml/shinservice-b2b-wheels.csv?id=88964843&t=' + date
#
# result  = wget.download(url, out='./proxy_wheels.csv')
# result  = wget.download(url, out='./proxy_tyres.csv')
result  = wget.download(url, out='/usr/local/bin/fuck_debian/tyres_wheels/proxy_wheels.csv')
result  = wget.download(url, out='/usr/local/bin/fuck_debian/tyres_wheels/proxy_tyres.csv')

listt = ['1251539', 'Headway 225/40 R18 SNOW-UHP HW508 92H', '3PN02254018E000002', '06930213605119', 'W', 'Headway', 'SNOW-UHP HW508', 'R18', '225', '40', '92', 'H', 'N', 'N', '', '', 'N', '5389', '6420', '6420',
'https://www.shinservice.ru/catalog/headway/uhp-5081.jpg', '20', '19', '0', '0', '0', '4', '0', '2', '4', '4', '4', '4', '0', '4', '4', '0', '8', '4', '4', '8', '0', '4', '0', '4', '4', '4', '4', '0', '4', '0', '4', '4', '4', '4', '0', '4', '0', '0']
print('index', listt.index('5389'))

# def product_tyres(product_list, in_stock):
#     name = product_list[2]
#     description = 'very good'
#     vendor = product_list[5]
#     #category_vendor = categories[vendor]
#     if product_list[4] == 'S':
#         category_id = category_summer[vendor]
#     elif product_list[4] == "W":
#         category_id = category_winter[vendor]
#     else:
#         category_id = category_allseason[vendor]
#     price = int(product_list[19]) - 400
#     product_code = product_list[2]




# with open('./proxy_wheels (1).csv', 'r') as file:
#     count = 0
#     liist = []
#     reader = csv.reader(file, delimiter = '\t')
#     for row in reader:
#         if  row[3] not in liist and row[3] != 'brand':
#             liist.append(row[3])
#             count += 1
#         elif row[3] == 'brand':
#            # print(row)
#             pass


def get_data_csv():
    # with open('./proxy_tyres (1).csv', 'r') as file:
    with open('/usr/local/bin/fuck_debian/tyres_wheels/proxy_tyres (1).csv', 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        proxy = []
        for row in reader:
            proxy.append(row)
    #print(type(row), '--------')
    return proxy

    #
    # print(row)
    # print(liist)
    # print('vendors_wheels', count)

#/usr/local/bin/fuck_debian/tyres_wheels/
def get_tyres_csv():
    # with open('data_product.json', 'r') as  read_file:
    with open('/usr/local/bin/fuck_debian/tyres_wheels/data_product.json', 'r') as read_file:
        proxy_data = json.load(read_file)
        #print('proxy_data form get_tyres_csv----', type(proxy_data), len(proxy_data))
        data = get_data_csv()
        for i in range(1, len(data)):
            liist = {}
            if int(data[i][22]) >= 4:
                try:
                    if data[i][4] == 'S':
                        liist['category_id'] = categories_summer[data[i][5]]
                    elif data[i][4] == "W":
                        liist['category_id'] = categories_winter[data[i][5]]
                    else:
                        liist['category_id'] = categories_allseason[data[i][5]]
                    liist['category'] = 12
                    liist['name'] = data[i][1]
                    liist['description'] = data[i][1]

                    liist['in_stock'] = int(data[i][22])
                    liist['enabled'] = data[i][1]
                    liist['vendorCode'] = data[i][2]
                    liist['vendor'] = data[i][5]
                    liist['diameter'] = data[i][7] #16
                    liist['width'] = data[i][8] #14
                    liist['profile'] = data[i][9] #15
                    liist['sku'] = data[i][0]
                    liist['season'] = data[i][4]
                    liist['picture'] = '0.'  #data[i][19]  #image_link
                    if data[i][17].isdigit():
                        if liist['diameter'][1:].isdigit() and int(liist['diameter'][1:]) <= 16:
                            price = int(data[i][17])  * 1.12   #result float
                        elif liist['diameter'][1:].isdigit() and int(liist['diameter'][1:]) >= 17:
                            price = int(data[i][17])  * 1.10
                        else:
                            price = int(data[i][17]) * 1.10
                    else:
                        liist['in_stock'] = 0

                    liist['price_b2b'] = round(price, 0)
                    if liist['in_stock'] != 0:
                        proxy_data.append(liist)

                except KeyError as error:
                    print("Something went wrong KeyError from getcsv: {}".format(error))
                    # write(str(data))
                    print(str(data[i]))
                    continue
            else:
                continue


        # with open('data_product.json', 'w') as  write_file:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/data_product.json', 'w') as write_file:
            json.dump(proxy_data, write_file)

        # mem = sys.getsizeof(proxy_data)
        #print(type(proxy_data), len(proxy_data), type(proxy_data[0]), len(proxy_data[0])) #, proxy_data[0])
        # print(mem / 1000, 'Kb--')
        # return proxy_data


# mems = sys.getsizeof(get_tyres_csv())
# print(mems / 1000, 'Kb')
# get_tyres_csv()