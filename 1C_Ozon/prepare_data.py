import csv
# wh_ozon = {'casual':[], 'kgt': []}

# wh_ozon = {'casual': ['OWLM200201', 'OWLM200300', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN50', 'ИМRUNN40', 'OWLM200302', 'OWLM200100', 'OWLM200301', 'OWLM200202', 'OWLT190301/2', 'OWLT190303/2', 'OWLT190402/2', 'OWLT190702/2', 'OWLT200901/2', 'OWLT190901/2', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'ИМALS80', 'OWLT190305'],
#            'kgt': ['OWLT190101', 'OWLT190302', 'OWLT190403S', 'OWLT190304', 'ИМOWLT190901', 'ИМOWLT200901', 'ИМMAL80', 'ИМHELLS65', 'ИМRUNN60', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200101', 'OWLM200102', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190303', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSS100', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190303', 'OWLT190402', 'OWLT190702', 'OWLT200901', 'OWLT190901', 'TOWLT190302', 'OWLT190201']
#            }

# wh_yandex= {'fbs_ctm': ['ИМOWLT190303', 'ИМSS100'],
#             'fbs_express': ['а0026033', 'а0026027', 'а0027471', 'а0027470', 'ИМOWLT190901', 'ИМOWLT200901', 'OWLM200201', 'а0027568', 'ИМMAL80', 'ИМHELLS65', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN60', 'ИМRUNN50', 'ИМRUNN40', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200302', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200100', 'OWLM200101', 'OWLM200102', 'OWLM200301', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLM200202', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190301/2', 'OWLT190303', 'OWLT190303/2', 'OWLT190402', 'OWLT190402/2', 'OWLT190702', 'OWLT190702/2', 'OWLT200901', 'OWLT200901/2', 'OWLT190901', 'OWLT190901/2', 'TOWLT190302', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'OWLT190201'],
#             'dbs_our_delivery': ['all']
#             }

# # create warehouses ozon for product group
# def read_wh():
#     with open('wh.csv', 'r') as file:
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             if row[3] == 'Обычный' and row[0] not in wh_ozon['casual']:
#                 wh_ozon['casual'].append(row[0])
#             elif row[3] == 'КГТ' and row[0] not in wh_ozon['kgt']:
#                 wh_ozon['kgt'].append(row[0])
#
#         print(len(wh_ozon))
#         print(len(wh_ozon['casual']))
#         print(len(wh_ozon['kgt']))
#         # return wh_ozon
#
#
# read_wh()

# # create warehouses yandex for product group
# def read_wh():
#     with open('wh_yandex.csv', 'r') as file:
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             if row[3] == 'СТМ' and row[0] not in wh_yandex['fbs_ctm']:
#                 wh_yandex['fbs_ctm'].append(row[0])
#             elif row[3] == 'Экспресс+СТМ' and row[0] not in wh_yandex['fbs_express']:
#                 wh_yandex['fbs_express'].append(row[0])
#
#         print(wh_yandex)
#
#
# read_wh()

##get vendor_vode (SKU), name, barcode from price
# def read_price():
#     with open('./price.csv', 'r') as file:
#         liist = []
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             proxy = (row[2], row[3], row[4]) #get vendor_vode (SKU), name, barcode
#             liist.append(proxy)
#         # print(proxy)
#         print(len(liist))
#
#     return liist


##get sku from error list YM
# def read_shop_feed():
#     with open('./shop_feed-2.csv', 'r') as file:
#         liist = []
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             if row[0] is not None:
#                 liist.append(row[0])
# 
#         #print(liist)
# 
# read_shop_feed()


##create dict from price and response 1C - concat id_ic & other data from price
# def create_target_data():
#     target = {}
#     complete_data = read_price()  #get id_ic, vendor_vode (SKU), name, barcode from price_list.csv
#     for key, value in data.items():
#         for row in complete_data:
#             if value[0] == row[0] and value[0] != '':
#                 target[key] = row
#                 #print(target[key])
#
#     with open('target.json', 'w') as file:
#         json.dump(target, file)
#
#     #print(target)
#     print('target len  -', len(target))
#     return target


#get Ozon_proguct_id
# def get_proxy_data():
#     with open('current.csv', 'r') as file:
#         reader = csv.reader(file, delimiter=';')
#         proxy = []
#         faxy = []
#         for row in reader:
#             proxy.append(row)
#             faxy.append(row[2])
#
#     del proxy[0]
#     del faxy[0]
#
#     print(*faxy, sep='", "')
#
#     return proxy
#
# #data = get_proxy_data()


# def get_ozon_sku():
#     datas = read_file()   # data from json
#     proxy =  get_proxy_data()  #data from csv
#     l = [proxy[i][1] for i in range(len(proxy))]  #list product_id from csv
#     for i in range(len(datas)):
#         product_id = str(datas[i]['product_id'])
#         index = l.index(product_id)
#         offer_id = proxy[index][0]
#         #print(type(product_id), type(proxy[index][1]))
#         if product_id == proxy[index][1]:
#             datas[i]['offer_id'] = offer_id
#     #print(datas[2])
#     write_file(datas)
#
# #get_ozon_sku()



##get vendor_vode (SKU), name, barcode from WB
# def read_price():
#     with open('./CTM_Wildberries.csv', 'r') as file:
#         proxy = {}
#         reader = csv.reader(file, delimiter = '\t')
#         for row in reader:
#             #
#             # print(row[1])
#             r = ''.join(row)
#             row = r.split(',')
#             print(row)
#             try:
#                 if row[4] != '':
#                     proxy[row[0]] =  row[4]  # get vendor_vode (SKU), name, barcode
#             except:
#                 continue
#
#             print(proxy)
#             print(len(proxy))
#
#
#     return proxy
#
# read_price()

# from datetime import datetime, timezone
# from backports.zoneinfo import ZoneInfo
# dt = datetime.now()
# dt = dt.replace(tzinfo=ZoneInfo('Africa/Nairobi')).isoformat()
# print(dt)
# # print(dt.isoformat())