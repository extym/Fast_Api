import json
import sys

import wget
import csv
import datetime



category_wheels = {'Скад': 1926, 'КиК': 1782, 'Legeartis Optima': 2000, 'Dezent': 2000, 'Remain': 2000, 'Vector': 2000, 'K7': 2000, 'Legeartis Concept': 2000, 'ALCAR STAHLRAD (KFZ)': 2000, 'iFree': 628, 'AEZ': 2000, 'ALCAR HYBRIDRAD': 2000, 'ACCURIDE': 1972, 'Magnetto': 723, 'Venti': 1718, 'NEO': 1786, 'Tech Line': 1735, 'RST': 1960, 'Прома': 2000, 'Dotz': 2000, 'Yamato Segun': 2000, 'Replay': 2000, 'TREBL': 2000, 'Replica FR': 1181, 'Yamato': 1145, 'Yamato Samurai': 1146, 'ТЗСК': 2000, 'RPLC': 2000, 'Alcasta': 1130, 'NZ': 1134, 'Cross Street': 1873, 'PDW': 1182, 'RC Racing': 2000, 'X-trike': 2000, 'X-trikeRST': 2000, 'RPLC-Wheels': 2000, 'Wheels UP': 2000, 'Alutec': 1736, 'MAK': 1739, 'OZ Racing': 1798, 'Replica H': 2000, 'DOTZ 4X4 STAHLRADER': 2000, 'Nitro': 1876, 'Replica OS': 2000, 'Enzo': 2000, 'Borbet': 1738, 'Kronprinz': 2000, 'N2O': 1720, 'ARRIVO': 1939, 'Top Driver': 2000, 'ASTERRO': 1883, 'YST': 1144, 'X-RACE': 1874, 'Yokatta': 1143, 'Megami': 2000, 'HARP': 1889, 'ГАЗ': 2000, 'Top Driver S-series': 2000, 'Vissol': 1925, 'STEGER': 1879}
#tyres['sku', 'title', 'brand_sku', 'gtin', 'season', 'brand', 'model', 'diameter', 'width', 'profile', 'load_index', 'speed_index', 'pins', 'runflat', 'homologation', 'production_year', 'sale', 'price', 'price_retail', 'price_msrp', 'photo_url', 'amount_total', 'amount_local', 'amount shopId 1', 'amount shopId 7', 'amount shopId 8', 'amount shopId 9', 'amount shopId 10', 'amount shopId 12', 'amount shopId 13', 'amount shopId 14', 'amount shopId 15', 'amount shopId 16', 'amount shopId 17', 'amount shopId 19', 'amount shopId 20', 'amount shopId 21', 'amount shopId 22', 'amount shopId 23', 'amount shopId 24', 'amount shopId 25', 'amount shopId 26', 'amount shopId 30', 'amount shopId 33', 'amount shopId 35', 'amount shopId 36', 'amount shopId 37', 'amount shopId 635', 'amount shopId 667', 'amount shopId 671', 'amount shopId 678', 'amount shopId 714', 'amount shopId 716', 'amount shopId 718', 'amount shopId 719', 'amount shopId 722', 'amount shopId 723', 'amount shopId 728', 'amount shopId 3012']]
#wheels['sku', 'title', 'brand_sku', 'brand', 'model', 'type', 'color', 'diameter', 'pn', 'pcd', 'pcd2', 'et', 'centerbore', 'sale', 'price', 'price_retail', 'photo_url', 'amount_total', 'amount_local', 'amount shopId 1', 'amount shopId 4', 'amount shopId 7', 'amount shopId 8', 'amount shopId 9', 'amount shopId 10', 'amount shopId 12', 'amount shopId 13', 'amount shopId 14', 'amount shopId 15', 'amount shopId 16', 'amount shopId 17', 'amount shopId 19', 'amount shopId 20', 'amount shopId 21', 'amount shopId 22', 'amount shopId 23', 'amount shopId 24', 'amount shopId 25', 'amount shopId 26', 'amount shopId 30', 'amount shopId 33', 'amount shopId 35', 'amount shopId 36', 'amount shopId 37', 'amount shopId 635', 'amount shopId 667', 'amount shopId 671', 'amount shopId 678', 'amount shopId 712', 'amount shopId 714', 'amount shopId 716', 'amount shopId 718', 'amount shopId 719', 'amount shopId 722', 'amount shopId 723', 'amount shopId 728', 'amount shopId 3012']

category_summer = {'Tunga': 1753, 'Bridgestone': 1756, 'Toyo': 1764, 'Kumho': 1924, 'Michelin': 1755, 'BFGoodrich': 1162, 'Nokian Tyres': 1754, 'Gislaved': 1985, 'Goodyear': 1154, 'Dunlop': 1228, 'Yokohama': 1757, 'Sava': 1855, 'Continental':1763, 'Maxxis': 1717, 'Hankook': 1748, 'Pirelli': 1156, 'Cordiant': 1719, 'Tigar': 1166, 'Matador': 1161, 'Falken': 1962, 'Кама': 933, 'Viatti': 1857, 'Nitto': 1765, 'Sunfull': 1923, 'Delinte': 1984, 'Laufenn': 1750, 'Aosen': 1983, 'Headway': 1177}

category_winter = {'Bridgestone': 1723, 'Toyo': 1770, 'Kumho': 1773, 'Michelin': 1976, 'BFGoodrich': 1214, 'Nokian Tyres': 1721, 'Gislaved': 1192, 'Goodyear': 1977, 'Dunlop': 1188, 'Yokohama': 1208, 'Sava': 1772, 'Continental':1210, 'Maxxis': 1776, 'Hankook': 1206, 'Pirelli': 1207, 'Cordiant': 1189, 'Tigar': 1771, 'Matador': 1732, 'Falken': 1978, 'Кама': 509, 'Viatti': 1195, 'Nitto': 1194, 'Sunfull': 1769, 'Delinte': 1980, 'Laufenn': 1913, 'Aosen': 1981, 'Headway': 1982}
category_allseason = {}


tn = datetime.datetime.now()
ts = datetime.datetime.timestamp(tn) * 1000
date = str(ts)[:13]
type_data = ['wheels', 'tyres']
url = 'https://duplo.shinservice.ru/xml/shinservice-b2b-tyres.csv?id=88964843&t=' + date
#url = 'https://duplo.shinservice.ru/xml/shinservice-b2b-wheels.csv?id=88964843&t=' + date
#
# result  = wget.download(url, out='./proxy_wheels.csv')
# result  = wget.download(url, out='./proxy_tyres.csv')

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




with open('./proxy_wheels.csv', 'r') as file:
    count = 0
    liist = []
    reader = csv.reader(file, delimiter = '\t')
    for row in reader:
        if  row[3] not in liist and row[3] != 'brand':
            liist.append(row[3])
            count += 1
        elif row[3] == 'brand':
           # print(row)
            pass


def get_data_csv():
    with open('./proxy_tyres (1).csv', 'r') as file:
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
def get_tyres_csv():
    with open('data_product.json', 'r') as  read_file:
        proxy_data = json.load(read_file)
        print('proxy_data form get_tyres_csv----', type(proxy_data))
        data = get_data_csv()
        for i in range(1, len(data)):
            liist = {}
            if int(data[i][22]) >= 4:
                try:
                    if data[i][4] == 'S':
                        liist['category_id'] = category_summer[data[i][5]]
                    elif data[i][4] == "W":
                        liist['category_id'] = category_winter[data[i][5]]
                    else:
                        liist['category_id'] = category_allseason[data[i][5]]
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


        with open('data_product.json', 'w') as  write_file:
            json.dump(proxy_data, write_file)

        # mem = sys.getsizeof(proxy_data)
        print(type(proxy_data), len(proxy_data), type(proxy_data[0]), len(proxy_data[0])) #, proxy_data[0])
        # print(mem / 1000, 'Kb--')
        # return proxy_data


# mems = sys.getsizeof(get_tyres_csv())
# print(mems / 1000, 'Kb')
get_tyres_csv()