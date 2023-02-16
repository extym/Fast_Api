import json
from connect import check_and_write, check_write_json
import requests
import random
import string

categories_wheels = {'Inverno': 1988, 'Jantsa': 1989, 'FR replica': 1181, 'RADIUS': 1990, 'ГАЗ': 1991, 'LF Works': 1992,
              'Remain': 1993, 'rtr': 1994, 'BLACK RHINO': 1995, 'BEYERN': 1897, 'REDBOURNE': 1901, 'LUMARAI': 1898,
              'COVENTRY': 1903, 'VICTOR': 1893, 'Accuride': 1972, 'Asterro': 1974, 'Lemmerz/Maxion': 1973,
              'Maxion': 1973, 'Tracston': 1975, 'Alutec': 1736, 'ANTERA': 64, 'ATS': 1081, 'BBS': 1737, 'Borbet': 1738,
              'Carwel': 1969, 'FONDMETAL': 1084, 'Fondmetal': 1084, 'iFree': 628, 'KHOMEN': 1968, 'MAK': 1739, 'MANDRUS': 1887,
              'MOMO': 1785, 'MSW': 1885, 'Neo': 1786, 'OZ': 55, 'Replay': 1221, 'Rial': 1777, 'RST': 1960,
              'Sparco': 1970, 'Tech Line': 1735, 'Venti': 1718, 'K&K': 1782, 'OE': 1883, 'Скад': 1926, 'TSW': 1083,
              'Magnetto': 723, 'Евродиск': 62, 'LS': 1139, 'LegeArtis': 1138, 'LegeArtis Concept': 1140, 'Trebl': 532,
              'Yamato': 1145, 'N2O': 1720, 'PDW': 1182, 'CrossStreet': 1873, 'Yokatta': 1143, "NZ": 1134, 'Alcasta': 1130,
              'Race Ready' : 1128, 'Arrivo': 1939, 'Antera': 64, 'Next': 1788, 'X-Race': 1874, 'Hayes Lemmerz' : 1884,
              'Aero': 1875, 'Steger': 1879, 'Buffalo': 1882, 'ТЗСК': 1996, 'Harp': 1889, 'Off-Road Wheels': 1997,
              'Khomen Wheels': 1968, 'LS FlowForming': 1139, 'Better': 1986, 'Lizardo': 1987, 'YST': 827, 'LS Forged': 1998}

categories_summer = {'Tunga': 1753, 'Bridgestone': 1756, 'Toyo': 1764, 'Kumho': 1924, 'Michelin': 1755, 'BFGoodrich': 1162,
                     'Nokian Tyres': 1754, 'Gislaved': 1985, 'Goodyear': 1154, 'Dunlop': 1228, 'Yokohama': 1757, 'Sava': 1855,
                     'Continental':1763, 'Maxxis': 1717, 'Hankook': 1748, 'Pirelli': 1156, 'Cordiant': 1719, 'Tigar': 1166,
                     'Matador': 1161, 'Falken': 1962, 'Кама': 933, 'Viatti': 1857, 'Nitto': 1765, 'Sunfull': 1923, 'Delinte': 1984,
                     'Laufenn': 1750, 'Aosen': 1983, 'Headway': 1177, 'Kormoran': 1160, 'Nexen': 1150, 'Marshal': 1850, 'Formula': 1167,
                     'Kama': 933, 'Vredestein': 1839, 'Triangle': 1856, 'Altenzo': 1859, 'Compasal': 1871,
                     'GT Radial': 1766, 'Onyx': 2001, 'Sailun': 1225, 'Cachland': 1743, 'HiFly': 2002, 'Rapid': 1742, 'Roadhiker': 2005,
                     'Goodride': 2003, 'Tracmax': 2004, 'Doublestar': 2006}

categories_winter = {'Bridgestone': 1723, 'Toyo': 1770, 'Kumho': 1773, 'Michelin': 1976, 'BFGoodrich': 1214, 'Nokian Tyres': 1721,
                     'Gislaved': 1192, 'Goodyear': 1977, 'Dunlop': 1188, 'Yokohama': 1208, 'Sava': 1772, 'Continental':1210, 'Maxxis': 1776,
                     'Hankook': 1206, 'Pirelli': 1207, 'Cordiant': 1189, 'Tigar': 1771, 'Matador': 1732, 'Falken': 1978, 'Кама': 509,
                     'Viatti': 1195, 'Nitto': 1194, 'Sunfull': 1769, 'Delinte': 1980, 'Laufenn': 1913, 'Aosen': 1981, 'Headway': 1982,
                     'Dunlop JP': 1849, 'Kormoran': 1196, 'Marshal': 1191, 'Kama': 509, 'Nexen': 1213, 'Formula': 1197, 'Triangle': 859,
                     'Altenzo': 1141, 'Onyx': 1999, 'GT Radial': 1200, 'Sailun': 1232, 'Cachland': 1767, 'HiFly': 2000}
categories_allseason = {}
# #data = json.loads('https://b2b.4tochki.ru/export_data/M28420.json')  #'http://super-good.ml/test_json.json')

##WORK
r = requests.get('https://b2b.4tochki.ru/export_data/M28420.json')
data = r.json()

wheels = data['rims']
tires = data['tires']
print('wheels', len(wheels))
print('tires', len(tires))
print(wheels[0])
print(tires[-1])


def count(row):  #dictionary
    in_stock = 0
    if row.get('rest_yamka') is not None and isinstance(row.get('rest_yamka'), int):
        in_stock += row['rest_yamka']
    elif row.get('rest_yamka') is not None and 'более ' in row.get('rest_yamka'):
        # row['rest_yamka'].replace('более ', '')
        in_stock += int(row['rest_yamka'].replace('более ', ''))

    if row.get('price_mkrs') is not None  and isinstance(row.get('price_mkrs'), int):
        in_stock += row['price_mkrs']
    elif row.get('price_mkrs') is not None and 'более ' in row.get('price_mkrs'):
        row['price_mkrs'].replace('более ', '')
        in_stock += int(row['price_mkrs'])

    return in_stock


def get_price(product):
    price = 0
    if product.get('price_yamka') is not None and isinstance(product.get('price_yamka'), int):
        price = product['price_yamka'] * 1.18 - 400
    elif product.get('price_mkrs') is not None and isinstance(product.get('price_mkrs'), int):
        price = product['price_mkrs'] * 1.18 - 400
    price = round(price, 0)

    return price

def id_generator(size=8, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def wheels_from_json(wheels):
    diction = []
    for prod in wheels:
        in_stock = count(prod)
        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        name = prod['name']
        vendor = prod['brand']
        description = vendor + ' ' + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            break
        # check category wheels and tyres
        category_id = prod.get('category_id')
        if category_id is None:
            category_id = categories_wheels[vendor]

        price = get_price(prod)

        product_code = prod['cae']
        image_url = prod.get('img_big_my')
        name_picture = id_generator() + '.png'
        image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'литые диски ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'литые диски, легкосплавные диски, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1
        category = 5
        options = {
            'et': prod.get('et'),
            "bolts_spacing": prod.get('bolts_spacing'),
            'diameter': prod.get('diameter'),
            'dia': prod.get('dia'),
            'width': prod.get('width')
        }

        result = [category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1, category], image_tuple, options
        diction.append(result)

    #print(diction)
    return diction


def tires_from_json(tyres):
    diction = []
    for prod in tyres:
        print('tires_from_json', prod)
        in_stock = count(prod)
        if in_stock >= 4:
            enabled = 1
        else:
            enabled = 0
        name = prod['name']
        vendor = prod['brand']
        description = vendor + ' ' + name
        if vendor == 'Carwel':
            description = name
        elif vendor == '':
            continue  #break
        # check category wheels and tyres
        category_id = prod.get('category_id')
        if category_id is None and prod.get('season') == 'Летняя':
            category_id = categories_summer[vendor]
        elif category_id is None and prod.get('season') == 'Зимняя':
            category_id = categories_winter[vendor]
        elif vendor in categories_summer.keys():
            category_id = categories_summer[vendor]
        else:
            category_id = 3000
        price = get_price(prod)
        category = 12
        product_code = prod['cae']
        image_url = prod.get('img_big_my')
        name_picture = id_generator() + '.png'
        image_tuple = (name_picture, image_url)
        koeff = 1
        meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
        meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
        meta_h1 = ' '
        params = 1
        options = {
            'diameter': prod.get('diameter'),
            'width': prod.get('width'),
            'profile': prod.get('height')
        }

        result = [category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
                  params, koeff, meta_h1, category], image_tuple, options
        diction.append(result)

    # print('tires_from_json', diction)
    return diction

wwwheels = wheels_from_json(wheels)
#tttires = tires_from_json(tires)
# check_write_json(tttires)
check_write_json(wwwheels)