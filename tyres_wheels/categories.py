import json

categories_wheels = {'Inverno': 1988, 'Jantsa': 1989, 'rFR': 1181, 'RADIUS': 1990, 'ГАЗ': 1991, 'LF Works': 1992,
                     'Remain': 1993, 'rtr': 1994, 'BLACK RHINO': 1995, 'BEYERN': 1897, 'REDBOURNE': 1901,
                     'LUMARAI': 1898, 'Nitro': 1876,
                     'COVENTRY': 1903, 'VICTOR': 1893, 'Accuride': 1972, 'Asterro': 1974, 'Lemmerz/Maxion': 1973,
                     'Maxion': 1973, 'Tracston': 1975, 'Alutec': 1736, 'ANTERA': 64, 'ATS': 1081, 'BBS': 1737,
                     'Borbet': 1738,
                     'Carwel': 1969, 'Fondmetal': 1084, 'iFree': 628, 'KHOMEN': 1968, 'MAK': 1739,
                     'MANDRUS': 1887, 'Premium Series': 4001, 'ZEPP 4х4': 4002, 'ZEPP': 4003, 'YZ': 4004,
                     'NEO': 1786, 'REPLAY': 1221, 'Tech-Line': 1735, 'Venti': 1718, 'КиК': 1782, 'Евродиск': 62,
                     'MOMO': 1785, 'MSW': 1885, 'Neo': 1786, 'OZ': 55, 'Replay': 1221, 'Rial': 1777, 'RST': 1960,
                     'Sparco': 1970, 'Tech Line': 1735, 'K&K': 1782, 'OE': 1883, 'Скад': 1926, 'TSW': 1083,
                     'Magnetto': 723,
                     'LS': 1139, 'LegeArtis': 1138, 'LegeArtis Concept': 1140, 'Trebl': 532, 'FR replica': 1181,
                     'Yamato': 1145, 'N2O': 1720, 'PDW': 1182, 'CrossStreet': 1873, 'Yokatta': 1143, "NZ": 1134,
                     'Alcasta': 1130,
                     'Race Ready': 1128, 'Arrivo': 1939, 'Antera': 64, 'Next': 1788, 'X-Race': 1874,
                     'Hayes Lemmerz': 1884,
                     'Aero': 1875, 'Steger': 1879, 'Buffalo': 1882, 'ТЗСК': 1996, 'Harp': 1889, 'Off-Road Wheels': 1997,
                     'Khomen Wheels': 1968, 'LS FlowForming': 1139, 'Better': 1986, 'Lizardo': 1987, 'YST': 827,
                     'LS Forged': 1998, 'Wheels UP': 2008,
                     'Race Ready Technology': 2009, 'SRW': 2010}

ex = [1782, 1181, 1139, 1735, 1968, 1973, 1084]

ventil_LS = [{"cae":"S022678",
             "price_yamka":11,
             "price_yamka_rozn":13,
             "rest_yamka":"более 40",
             "cae":"S022678",
             "brand":"LS",
             "name":"Вентиль TR414 SM, LS",
             "img_small":"https://4tochki.ru/pictures/other/Ventili/Ventili/small/S022678.png",
             "img_big_pish":"https://4tochki.ru/pictures/other/Ventili/Ventili/big/S022678.png",
             "img_big_my":"https://api-b2b.pwrs.ru/1614/pictures/other/Ventili/Ventili/src/big_S022678.png",
             "quantity":0,"weight":0,"applicability":"","color":"","material":"","shape":"","volume":0}]



special_wheels = {'Inverno': 1988, 'Jantsa': 1989, 'RADIUS': 1990, 'ГАЗ': 1991, 'LF Works': 1992,
                     'Remain': 1993, 'rtr': 1994, 'BLACK RHINO': 1995, 'BEYERN': 1897, 'REDBOURNE': 1901,
                     'LUMARAI': 1898, 'Nitro': 1876,
                     'COVENTRY': 1903, 'VICTOR': 1893, 'Accuride': 1972, 'Asterro': 1974, 'Lemmerz/Maxion': 1973,
                     'Tracston': 1975, 'Alutec': 1736, 'ATS': 1081, 'BBS': 1737, 'Borbet': 1738,
                     'Carwel': 1969, 'Fondmetal': 1084, 'iFree': 628, 'KHOMEN': 1968, 'MAK': 1739,
                     'MANDRUS': 1887, 'Venti': 1718, 'КиК': 1782, 'Евродиск': 62,
                     'MOMO': 1785, 'MSW': 1885, 'Neo': 1786, 'OZ': 55, 'Replay': 1221, 'Rial': 1777, 'RST': 1960,
                     'Sparco': 1970, 'Tech Line': 1735, 'OE': 1883, 'Скад': 1926, 'TSW': 1083,
                     'Magnetto': 723, 'Premium Series': 4001, 'ZEPP 4х4': 4002, 'ZEPP': 4003, 'YZ': 4004,
                     'LS': 1139, 'LegeArtis': 1138, 'LegeArtis Concept': 1140, 'Trebl': 532, 'FR replica': 1181,
                     'Yamato': 1145, 'N2O': 1720, 'PDW': 1182, 'CrossStreet': 1873, 'Yokatta': 1143, "NZ": 1134,
                     'Alcasta': 1130,
                     'Race Ready': 1128, 'Arrivo': 1939, 'Antera': 64, 'Next': 1788, 'X-Race': 1874,
                     'Hayes Lemmerz': 1884,
                     'Aero': 1875, 'Steger': 1879, 'Buffalo': 1882, 'ТЗСК': 1996, 'Harp': 1889, 'Off-Road Wheels': 1997,
                     'Better': 1986, 'Lizardo': 1987, 'YST': 827,
                     'LS Forged': 1998, 'Wheels UP': 2008, 'Race Ready Technology': 2009, 'SRW': 2010}

categories_wheels_upper = {'WHEELS UP': 2008, 'INVERNO': 1988, 'NITRO': 1876, 'JANTSA': 1989, 'RFR': 1181,
                           'RADIUS': 1990, 'ГАЗ': 1991, 'LF WORKS': 1992, 'REMAIN': 1993, 'RTR': 1994,
                           'BLACK RHINO': 1995, 'BEYERN': 1897, 'REDBOURNE': 1901, 'LUMARAI': 1898, 'COVENTRY': 1903,
                           'VICTOR': 1893, 'ACCURIDE': 1972, 'ASTERRO': 1974, 'LEMMERZ/MAXION': 1973, 'MAXION': 1973,
                           'TRACSTON': 1975, 'ALUTEC': 1736, 'ANTERA': 64, 'ATS': 1081, 'BBS': 1737, 'BORBET': 1738,
                           'CARWEL': 1969, 'FONDMETAL': 1084, 'IFREE': 628, 'KHOMEN': 1968, 'MAK': 1739,
                           'MANDRUS': 1887, 'NEO': 1786, 'REPLAY': 1221, 'TECH-LINE': 1735, 'VENTI': 1718, 'КИК': 1782,
                           'ЕВРОДИСК': 62, 'MOMO': 1785, 'MSW': 1885, 'OZ': 55, 'RIAL': 1777, 'RST': 1960,
                           'SPARCO': 1970, 'TECH LINE': 1735, 'K&K': 1782, 'OE': 1883, 'СКАД': 1926, 'TSW': 1083,
                           'MAGNETTO': 723, 'LS': 1139, 'LEGEARTIS': 1138, 'LEGEARTIS CONCEPT': 1140, 'TREBL': 532,
                           'FR REPLICA': 1181, 'YAMATO': 1145, 'N2O': 1720, 'PDW': 1182, 'CROSSSTREET': 1873,
                           'YOKATTA': 1143, 'NZ': 1134, 'ALCASTA': 1130, 'RACE READY': 1128, 'ARRIVO': 1939,
                           'NEXT': 1788, 'X-RACE': 1874, 'HAYES LEMMERZ': 1884, 'AERO': 1875, 'STEGER': 1879,
                           'BUFFALO': 1882, 'ТЗСК': 1996, 'HARP': 1889, 'OFF-ROAD WHEELS': 1997, 'KHOMEN WHEELS': 1968,
                           'LS FLOWFORMING': 1139, 'BETTER': 1986, 'LIZARDO': 1987, 'YST': 827, 'LS FORGED': 1998,
                           'RACE READY TECHNOLOGY': 2009, 'SRW': 2010}

categories_summer = \
    {'Tunga': 1753, 'Bridgestone': 1756, 'Toyo': 1764, 'Kumho': 1924, 'Michelin': 1755,
     'BFGOODRICH': 1162, 'NOKIAN TYRES': 1754, 'Hankook Laufenn': 1748,
     'Gislaved': 1985, 'Goodyear': 1154, 'Dunlop': 1228, 'Yokohama': 1757,
     'Sava': 1855, 
     'Continental': 1763, 'Maxxis': 1717, 'Hankook': 1748, 'Pirelli': 1156, 'Cordiant': 1719,
     'Tigar': 1166, 
     'Matador': 1161, 'Falken': 1962, 'Кама': 933, 'Viatti': 1857, 'Nitto': 1765, 'Sunfull': 1923,
     'Delinte': 1984,
     'Laufenn': 1750, 'Aosen': 1983, 'Headway': 1177, 'Kormoran': 1160, 'Nexen': 1150,
     'Marshal': 1850, 'Formula': 1167,
     'Kama': 933, 'Vredestein': 1839, 'TRIANGLE': 1856, 'Altenzo': 1859, 'Compasal': 1871,
     'GT Radial': 1766, 'Onyx': 2001, 'Sailun': 1225, 'Cachland': 1743, 'HiFly': 2002,
     'Rapid': 1742, 'Roadhiker': 2005, 'Goodride': 2003, 'Tracmax': 2004, 'Doublestar': 2006,
     'Westlake': 2012, 'Antares': 2018,  'Bars': 2017,
     'Amtel': 2016, 'General Tire': 1867, 'Nordman': 2013}

cats_summer_upper = {'TUNGA': 1753, 'BRIDGESTONE': 1756, 'TOYO': 1764, 'KUMHO': 1924, 'MICHELIN': 1755,
                     'BFGOODRICH': 1162, 'NOKIAN TYRES': 1754, 'GISLAVED': 1985, 'GOODYEAR': 1154, 'DUNLOP': 1228,
                     'YOKOHAMA': 1757, 'SAVA': 1855, 'CONTINENTAL': 1763, 'MAXXIS': 1717, 'HANKOOK': 1748,
                     'PIRELLI': 1156, 'CORDIANT': 1719, 'TIGAR': 1166, 'MATADOR': 1161, 'FALKEN': 1962, 'КАМА': 933,
                     'VIATTI': 1857, 'NITTO': 1765, 'SUNFULL': 1923, 'DELINTE': 1984, 'LAUFENN': 1750, 'AOSEN': 1983,
                     'HEADWAY': 1177, 'KORMORAN': 1160, 'NEXEN': 1150, 'MARSHAL': 1850, 'FORMULA': 1167, 'KAMA': 933,
                     'VREDESTEIN': 1839, 'TRIANGLE': 1856, 'ALTENZO': 1859, 'COMPASAL': 1871, 'GT RADIAL': 1766,
                     'ONYX': 2001, 'SAILUN': 1225, 'CACHLAND': 1743, 'HIFLY': 2002, 'RAPID': 1742, 'ROADHIKER': 2005,
                     'GOODRIDE': 2003, 'TRACMAX': 2004, 'DOUBLESTAR': 2006, 'WESTLAKE': 2012, 'ANTARES': 2018,
                     'BARS': 2017, 'AMTEL': 2016, 'GENERAL TIRE': 1867, 'NORDMAN': 2013}

categories_winter = {'Nokian Tyres (Ikon Tyres)': 1721,'Bridgestone': 1723, 'Toyo': 1770, 'Kumho': 1773, 'Michelin': 1976, 'BFGOODRICH': 1214,
                     'Nokian Tyres': 1721,
                     'Gislaved': 1192, 'Goodyear': 1977, 'Dunlop': 1188, 'Yokohama': 1208, 'Sava': 1772,
                     'Continental': 1210, 'Maxxis': 1776,
                     'Hankook': 1206, 'Pirelli': 1207, 'Cordiant': 1189, 'Tigar': 1771, 'Matador': 1732, 'Falken': 1978,
                     'Кама': 509,
                     'Viatti': 1195, 'Nitto': 1194, 'Sunfull': 1769, 'Delinte': 1980, 'Laufenn': 1913, 'Aosen': 1981,
                     'Headway': 1982,
                     'Dunlop JP': 1849, 'Kormoran': 1196, 'Marshal': 1191, 'Kama': 509, 'Nexen': 1213, 'Formula': 1197,
                     'TRIANGLE': 859,
                     'Altenzo': 1141, 'Onyx': 1999, 'GT Radial': 1200, 'Sailun': 1232, 'Cachland': 1767, 'HiFly': 2000,
                     'General Tire': 2019,
                     'Amtel': 2015, 'Westlake': 2011, 'Nordman': 2014}

cats_winter_upper = {'BRIDGESTONE': 1723, 'TOYO': 1770, 'KUMHO': 1773, 'MICHELIN': 1976, 'BFGOODRICH': 1214,
                     'NOKIAN TYRES': 1721, 'GISLAVED': 1192, 'GOODYEAR': 1977, 'DUNLOP': 1188, 'YOKOHAMA': 1208,
                     'SAVA': 1772, 'CONTINENTAL': 1210, 'MAXXIS': 1776, 'HANKOOK': 1206, 'PIRELLI': 1207,
                     'CORDIANT': 1189, 'TIGAR': 1771, 'MATADOR': 1732, 'FALKEN': 1978, 'КАМА': 509, 'VIATTI': 1195,
                     'NITTO': 1194, 'SUNFULL': 1769, 'DELINTE': 1980, 'LAUFENN': 1913, 'AOSEN': 1981, 'HEADWAY': 1982,
                     'DUNLOP JP': 1849, 'KORMORAN': 1196, 'MARSHAL': 1191, 'KAMA': 509, 'NEXEN': 1213, 'FORMULA': 1197,
                     'TRIANGLE': 859, 'ALTENZO': 1141, 'ONYX': 1999, 'GT RADIAL': 1200, 'SAILUN': 1232,
                     'CACHLAND': 1767, 'HIFLY': 2000, 'GENERAL TIRE': 2019, 'AMTEL': 2015, 'WESTLAKE': 2011,
                     'NORDMAN': 2014}

categories_allseason = {'SAILUN': 1747, 'Maxxis': 1842, 'Marshal': 1841, 'Doublestar': 1840, 'Goodyear': 1843,
                        'Compasal': 1844, 'CORDIANT': 1751, 'HANKOOK': 1749, 'TRIANGLE': 1758, 'Ovation': 1845,
                        'BFGoodrich': 1846, 'GiTi': 1847, 'GT': 1848, 'Fesite': 1851, 'Viatti': 1852, 'Pirelli': 1853,
                        'Yokohama': 1854, 'Bridgestone': 1858, 'Continental': 1860, 'Michelin': 1861, 'Nitto': 1862,
                        'Mickey': 1865, 'TopTrust': 1866, 'Nokian': 1868, 'Hankook Laufenn': 1749, 'Nexen': 1869, 'Taitong': 1870}

cats_allseason_upper = \
    {'SAILUN': 1747, 'MAXXIS': 1842, 'MARSHAL': 1841, 'DOUBLESTAR': 1840, 'GOODYEAR': 1843,
    'COMPASAL': 1844, 'CORDIANT': 1751, 'HANKOOK': 1749, 'TRIANGLE': 1758, 'OVATION': 1845,
    'BFGOODRICH': 1846, 'GITI': 1847, 'GT': 1848, 'FESITE': 1851, 'VIATTI': 1852, 'PIRELLI': 1853,
    'YOKOHAMA': 1854, 'BRIDGESTONE': 1858, 'CONTINENTAL': 1860, 'MICHELIN': 1861, 'NITTO': 1862,
    'MICKEY': 1865, 'TOPTRUST': 1866, 'NOKIAN': 1868, 'NEXEN': 1869, 'TAITONG': 1870}

cats_wheels_upper = {'WHEELS UP': 2008, 'NITRO': 1876, 'INVERNO': 1988, 'JANTSA': 1989, 'RFR': 1181, 'RADIUS': 1990, 'ГАЗ': 1991,
                     'LF WORKS': 1992, 'REMAIN': 1993, 'RTR': 1994, 'BLACK RHINO': 1995,
                     'BEYERN': 1897, 'REDBOURNE': 1901, 'LUMARAI': 1898, 'COVENTRY': 1903,
                     'VICTOR': 1893, 'ACCURIDE': 1972, 'ASTERRO': 1974, 'LEMMERZ/MAXION': 1973,
                     'MAXION': 1973, 'TRACSTON': 1975, 'ALUTEC': 1736, 'ANTERA': 64, 'ATS': 1081,
                     'BBS': 1737, 'BORBET': 1738, 'CARWEL': 1969, 'FONDMETAL': 1084, 'IFREE': 628,
                     'KHOMEN': 1968, 'MAK': 1739, 'MANDRUS': 1887, 'NEO': 1786, 'REPLAY': 1221,
                     'TECH-LINE': 1735, 'VENTI': 1718, 'КИК': 1782, 'ЕВРОДИСК': 62, 'MOMO': 1785,
                     'MSW': 1885, 'OZ': 55, 'RIAL': 1777, 'RST': 1960, 'SPARCO': 1970,
                     'TECH LINE': 1735, 'K&K': 1782, 'OE': 1883, 'СКАД': 1926, 'TSW': 1083,
                     'MAGNETTO': 723, 'LS': 1139, 'LEGEARTIS': 1138, 'LEGEARTIS CONCEPT': 1140,
                     'TREBL': 532, 'FR REPLICA': 1181, 'YAMATO': 1145, 'N2O': 1720, 'PDW': 1182,
                     'CROSSSTREET': 1873, 'YOKATTA': 1143, 'NZ': 1134, 'ALCASTA': 1130,
                     'RACE READY': 1128, 'ARRIVO': 1939, 'NEXT': 1788, 'X-RACE': 1874,
                     'HAYES LEMMERZ': 1884, 'AERO': 1875, 'STEGER': 1879, 'BUFFALO': 1882,
                     'ТЗСК': 1996, 'HARP': 1889, 'OFF-ROAD WHEELS': 1997, 'KHOMEN WHEELS': 1968,
                     'LS FLOWFORMING': 1139, 'BETTER': 1986, 'LIZARDO': 1987, 'YST': 827,
                     'LS FORGED': 1998, 'RACE READY TECHNOLOGY': 2009, 'SRW': 2010}



def rewrite_pictures_data():
    listt = {}

    with open('dict_images.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_images_read', len(data_list))
        read_file.close()

    proxy = data_list[11000:]

    with open('dict_images_rewrite.json', "w") as write_file:
        # data_list.extend(listt)
        json.dump(proxy, write_file)
        print('file_images_write_1', len(proxy))

    print('file_images_rewrite', len(data_list))


# rewrite_pictures_data()

# print({i.upper(): j for i, j in categories_allseason.items()})

# print(''.join(chr(int(j)) for j in '64 101 120 101 120 116 121 109'.split()))

def sorty(i):
    for k, v in i.items():
        return i[k]





# print(len(set(categories_wheels_upper.values())))
# print(len(categories_wheels_upper.keys()))
# print(len(cats_wheels_upper.keys()))
# print(len(special_wheels.keys()))
