import datetime

from    categories import *


xs = ['Legeartis Optima', 'Enkei', 'ALCAR HYBRIDRAD', 'K7', 'Vector', 'Vissol', 'Megami', 'Cross Street', 'OZ Racing', 'Replica H', 'AEZ', 'Kronprinz', 'Kosei', 'ASTERRO', 'Top Driver', 'X-trikeRST', 'Replica FR', 'ACCURIDE', 'HARP', 'Yamato Samurai', 'Premium Series', 'Vianor', 'Original Specification', 'Прома', 'ALCAR STAHLRAD (KFZ)', 'Dotz', 'TREBL', 'X-trike', 'RPLC-Wheels', 'Yamato Segun', 'Top Driver S-series', 'Legeartis Concept', 'RPLC', 'Kormetal', 'DOTZ 4X4 STAHLRADER', 'Dezent', 'ORW']

# print(set([i.strip("'") for i in ks]))

xsss = ['X-trikeRST', 'Top Driver S-series', 'RPLC', 'Yamato Samurai', 'ORW', 'DOTZ 4X4 STAHLRADER', 'Enkei', 'Megami', 'Прома', 'RPLC-Wheels', 'Replica H', 'Vector', 'Dezent', 'OZ Racing', 'Premium Series', 'Original Specification', 'Dotz', 'Top Driver', 'K7', 'Kosei', 'Replica FR', 'X-trike', 'Cross Street', 'ALCAR HYBRIDRAD', 'Vianor', 'Yamato Segun', 'ALCAR STAHLRAD (KFZ)', 'Kronprinz', 'Legeartis Optima', 'Kormetal', 'AEZ', 'Vissol']


data = [i for i in xs if i.upper() not in cats_wheels_upper.keys()]

from datetime import datetime

date = datetime.now().replace(minute=2, second=0, microsecond=0)
# print(date,  type(date))

pr = (['category_id', 'name', 'description', 'price', 'in_stock', 'enabled', 'product_code', 'vendor', 'meta_d', 'meta_k',
                 'params', 'koeff', 'meta_h1', 'provider', 'category'], 'image_tuple', 'options', 'rule')

print(pr[0][:-1])