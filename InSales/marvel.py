import asyncio
import datetime
import json
from creds import marvel_login, marvel_password, CSV_PATH
import requests
import csv
from conn import executemany_query, execute_query_return, execute_query_return_v2
from conn_maintenance import *
import urllib.parse

link = 'https://b2b.marvel.ru/Api/'
params_marvel = {
    'user': marvel_login,
    'password': marvel_password,
    'secretKey': '',
    'responseFormat': '1',
    'inStock': '1'
}


def write_json(data):
    with open('marvel_json.txt', 'w') as file:
        json.dump(data, file)
        print('we dumped json successfully')


def read_json():
    with open('marvel_json.txt', 'r') as f:
        data = json.load(f)

        return data


def write_excel(data):
    fieldnames = ['category_treeId', 'name',  'vendor', 'category', 'sub_orderId', 'parentId']
    proxy = []
    for category in data:
        maxy = {
            'vendor': 'marvel',
            'name': category.get('CategoryName'),
            'category': category.get('CategoryID'),
            'parentId': category.get('CategoryName'),
            'sub_orderId': category.get('CategoryOrder'),
            'category_treeId': category.get('CategoryTreeId')
        }
        proxy.append(maxy)
    with open('marvel_cats_3', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(proxy)
        print('ALL_RIDE', proxy)


def write_excel_2(data):
    fieldnames = ['marvel', 'name', 'category', 'parentId', 'children']
    with open('ocs.xls', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print('ALL_RIDE_marvel')


def create_csv_for_category_from_marvel():
    list_cats = execute_query_return(query_get_actual_cats_v3, ('marvel',))
    category_ids = {}
    category_groups = {}
    list_data_categories = execute_query_return(query_rewrite_id_marwel, ('marvel',))
    dict_categories = {i[0]: i[1] for i in list_data_categories}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    base_fields = ['category_id', 'brand', 'id', 'quantity', 'price', 'published',
                   'name', 'currency']
    for key in category_groups.keys():
        result_list = []
        rewrite_properties = {}
        for pre_category_id in category_groups.get(key):
            category_id = dict_categories.get(str(pre_category_id))
            if category_id:
                # try:
                pre_data = get_stock(category_id)
                for prod in pre_data:
                    proxy = dict()
                    # print(11, type(prod), prod)
                    proxy['quantity'] = prod.get('AvailableForB2BOrderQty')
                    proxy['category_id'] = category_id
                    proxy['id'] = prod.get('WareArticle')
                    proxy['price'] = int(prod.get('WarePriceRUB').split(',')[0]) * 1.05
                    proxy['brand'] = prod.get('WareVendor')
                    proxy['published'] = category_ids[pre_category_id][2]
                    proxy['name'] = prod.get('WareFullName')
                    proxy['currency'] = 'RUB'

                    proxy.update(prod)
                    rewrite_properties.update(prod)
                    result_list.append(proxy.copy())

                    # print(22, proxy)
                # except Exception as error:
                #     print('some_FUck_Up_marvel {}'.format(error))
                #     continue
            # break

        fields = base_fields.copy()
        pr = set(rewrite_properties.keys())
        fields.extend(pr)
        print(f'fields_marvel_{key}', fields)

        with open(CSV_PATH + f'marvel_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=fields)
            writer.writeheader()
            writer.writerows(result_list)


def create_csv_for_category_from_marvel_v2():
    list_cats = execute_query_return(query_get_actual_cats_v3, ('marvel',))
    category_ids = {}
    category_groups = {}
    list_data_categories = execute_query_return(query_rewrite_id_marwel, ('marvel',))
    dict_categories = {i[0]: i[1] for i in list_data_categories if i[1]}
    for cats in list_cats:
        category_ids.update({i: cats for i in cats[0].split(', ')})
        category_groups[cats[4]] = category_groups.get(cats[4], []) + cats[0].split(', ')
    base_fields = ['category_id', 'brand', 'id', 'quantity', 'price', 'published',
                   'name', 'currency', 'photos']
    for key in category_groups.keys():
        result_list = []
        rewrite_properties = {}
        photo_ids = []
        for pre_category_id in category_groups.get(key):

            category_id = dict_categories.get(str(pre_category_id))
            if category_id:
                # try:
                pre_data = get_stock(category_id)
                # pre_data = get_stock('Ноут_Ноутбуки 13-14')
                for prod in pre_data:
                    proxy = dict()
                    prod_id = prod.get('WareArticle')
                    proxy['quantity'] = prod.get('AvailableForB2BOrderQty')
                    proxy['category_id'] = category_id
                    proxy['id'] = prod_id
                    proxy['price'] = int(prod.get('WarePriceRUB').split(',')[0]) * 1.05
                    proxy['brand'] = prod.get('WareVendor')
                    proxy['published'] = category_ids[pre_category_id][2]
                    proxy['name'] = prod.get('WareFullName')
                    proxy['currency'] = 'RUR'
                    proxy['photos'] = ''

                    proxy.update(prod)
                    rewrite_properties.update(prod)
                    result_list.append(proxy.copy())

                    photo_ids.append(prod_id)

                    # print(22, proxy)
                # except Exception as error:
                #     print('some_FUck_Up_marvel {}'.format(error))
                #     continue

        fields = base_fields.copy()
        pr = sorted(set(rewrite_properties.keys()))
        fields.extend(pr)
        print(f'fields_marvel_{key}', fields)
        # print(22222222222, len(result_list))

        photos = get_photos(photo_ids)
        pro_result_list = []
        for row in result_list:
            row.update({'photos': photos.get(row.get('id'))})
            pro_result_list.append(row)
        # print(3333333, len(pro_result_list), pro_result_list)

        with open(CSV_PATH + f'marvel_{key}.csv', 'w') as file:
            writer = csv.DictWriter(file, delimiter=';', dialect='excel',
                                    restval='', fieldnames=fields)
            writer.writeheader()
            writer.writerows(pro_result_list)

        # break

def make_data_cats():
    try:
        data = get_catalog()[1].get('Body').get('Categories')
    except:
        data = read_json()
    categories = []
    if data:
        for cats in data:
            sub_object = cats.get('SubCategories')
            if len(sub_object) > 0:
                for category in sub_object:
                    if len(category.get('SubCategories')) > 0:
                        for caties in category.get('SubCategories'):
                            if len(caties.get('SubCategories')) > 0:
                                for catty in caties.get('SubCategories'):
                                    if len(catty.get('SubCategories')) > 0:
                                        categories.extend(catty.get('SubCategories'))
                                    else:
                                        categories.append(catty)
                            else:
                                categories.append(caties)
                    else:
                        categories.append(category)
            else:
                categories.append(cats)

    datas = [i for i in categories if i.get('SubCategories') == []]
    if len(datas) == len(categories):
        write_excel(datas)
        # print(*datas, sep='\n')
        return True, datas
    else:
        return False, categories


def make_data_cats_v2(datas):
    data = datas.get('Body').get('Categories')
    categories = list()
    if data:
        for cats in data:
            sub_object = cats.get('SubCategories')
            if len(sub_object) > 0:
                for category in sub_object:
                    if len(category.get('SubCategories')) > 0:
                        for caties in category.get('SubCategories'):
                            if len(caties.get('SubCategories')) > 0:
                                for catty in caties.get('SubCategories'):
                                    if len(catty.get('SubCategories')) > 0:
                                        categories.extend(catty.get('SubCategories'))
                                    else:
                                        categories.append(catty)
                            else:
                                categories.append(caties)
                    else:
                        categories.append(category)
            else:
                categories.append(cats)

    data = [i for i in categories if i.get('SubCategories') == []]
    if len(data) == len(categories):
        write_excel(data)
        print(*data, sep='\n')
        print(type(data))
        return True, data
    else:
        return False, categories


def get_catalog():
    metod = 'GetCatalogCategories'
    url = link + metod
    answer = requests.post(url, params=params_marvel)
    try:
        data = answer.json()
        if data.get('Header').get('Code') == 0:
            write_json(data.get('Body').get('Categories'))
            make_data_cats_v2(data)
            # print('data', len(data.get('Body').get('Categories')))
        else:
            print('S0me_fuck_up_server_marvel_1 - ' + data.get('Header').get('Message'))

    except Exception as err:
        print("Some_fuck_up {}".format(err))


def get_full_stock():
    metod = 'GetFullStock'
    url = link + metod
    params = {
        'user': marvel_login,
        'password': marvel_password,
        'secretKey': '',
        'responseFormat': '1',
        'packStatus': '1',
        'inStock': '0'
    }
    answer = requests.post(url, params=params)
    if answer.ok:
        print('marvel ', answer.status_code)
    else:
        print('marvel_error ', answer.text)
    try:
        data = answer.json()
        if data.get('Header').get('Code') == 0:
            # print('data', type(data))
            print('WE get fullStock', len(data.get('Body')))
        else:
            print('S0me_fuck_up_server_marvel_2 category {}'.format(data.get('Header').get('Message')))

    except Exception as err:
        print("S0me_fuck_up_marvel {}".format(err))


def get_stock(category):
    sub_params = {
        'categoryId': category,
        'includeSubCategories': '1',
        'packStatus': '0'
    }
    params_marvel.update(sub_params)
    metod = 'GetStock'
    answer = requests.post(url=link + metod, params=params_marvel)
    print('get_stock_marvel', answer.status_code, category)
    try:
        data = answer.json()
        if data.get('Header').get('Code') == 0:
            # print('data', type(data))
            # print(len(data.get('Body')), type(data.get('Body')))
            return data.get('Body').get('CategoryItem')
        else:
            date = datetime.datetime.now()
            print('S0me_fuck_up_server_marvel_3 - category {} {} {}'.format(category, date, data.get('Header').get('Message')))
            return []
    except Exception as err:
        print("Some_fuck_up {} ".format(err))


def get_photos(list_ids):
    ids = [{"ItemId": id_s} for id_s in list_ids]
    proxy  = {}
    while len(ids) >= 500:
        sub_params = {
            'user': marvel_login,
            'password': marvel_password,
            'responseFormat': '1',
            "items":
                {
                    "WareItem": ids[:500]
                }
            }

        metod = 'GetItemPhotos'
        answer = requests.post(url=link + metod, params=urllib.parse.urlencode(sub_params))
        print('get_photos_marvel_status_code {} len_ids {}'.format( answer.status_code, len(ids)))
        if answer.ok:
            data = answer.json()
            if data.get('Header').get('Code') == 0:
                # print('data_photos', len(data.get('Body').get('Photo')))
                result = dict()
                for row in data.get('Body').get('Photo'):
                    articule = row.get('BigImage').get('WareArticle')
                    result[articule] = result.get(articule, []) + [row.get('BigImage').get('URL')]
                proxy.update({key: ', '.join(value) for key, value in result.items()})

            else:
                print('S0me_fuck_up_server_marvel_photos - {} {}'
                    .format(
                        ids,
                        answer.text
                    )
                )

        else:
            print("Some_fuck_up_photos_marvel status_{} {} {}".
                format(
                    answer.status_code,
                    answer.text,
                    len(list_ids)
                )
            )

        del ids[:500]

    return proxy


async def save_categories_vendors():
    data = make_data_cats()[1]
    proxy = []
    for category in data:
        maxy = {
            'vendor': 'marvel',
            'name': category.get('CategoryName'),
            'category': category.get('CategoryID'),
            'parentId': category.get('CategoryName'),
            'sub_orderId': category.get('CategoryOrder'),
            'category_treeId': category.get('CategoryTreeId')
        }
        proxy.append(maxy)
    write_data = [(i.get('vendor'), i.get('name'), i.get('category_treeId'), i.get('parentId', '0'), i.get('category')) for i in proxy]

    # write_excel(write_data)
    # print('write_data', write_data)
    if await executemany_query(query_write_vendors_v2, write_data):
        print('Categories tried saved')
    else:
        print("XS")


# #
# test_ids = ['1.445-330.0', '1.637-500.0', '1.673-000.0', 'DV16VSSNSZ', 'HCD12A', 'HCD18BL', 'CDLI12208', 'CDLI1222', 'CDLI12325', 'CDLI20028_PRM', 'CIRLI2002', 'CIWLI2001', 'ED2808', 'ED50028', 'ID211002', 'ID8108', 'IW10508', '600841850', 'QWCJY001', 'SPG5008', 'GS-A/800W/SBC', 'GS-A/800W/SBC', 'GS-A/800W/SBC', 'HJS18C', 'HJS600A', 'CJSLI8501', 'JS400285', 'JS400285', 'JS57028', 'JS6508', 'JS6508', 'MX11008', 'MX214008', 'MXLI2001', 'MXLI2001', 'PDB13008', 'PDB17008', 'DH24PH2NSZ', 'CRHLI1601', 'CRHLI1601', 'RGH6528', 'RGH6528_PRM', 'DS-A/185-1200W/SBS', 'DS-A/185-1200W/SBS', 'HCS18C', 'HCS800A', 'BMS14007', 'CMS2001', 'COS223589', 'CS18538', 'CS2358', 'CS2358', 'MC14008', 'MC14008', 'CRSLI1151', 'RS8008', 'G18STNSZ', 'AG1500182', 'AG200018', 'AG200018', 'AG220018', 'AG24008', 'AG24008', 'WLC15008', '42.1.0.00', 'WX741.9', 'AP14008', 'CDSLI2051', 'CROSLI2001', 'PBS12001', 'PBS12001', 'HES350/2A', 'X36247', 'BSP-B/3.6-1300/BPS', 'BSP-B/3.6-1300/BPS', 'QWLSD007', 'CSDLI0402', 'CWLI1223', 'DMD011254', 'FBLI12151', 'FBLI12151', 'FCLI2001', 'PTWT215002', 'TSB116511', '626700000', 'WA3601', 'CH-48V-100W', 'CH-48V-200W', 'CH-48V-200W', 'QBKG04LM', 'WS-EUK01', 'WS-EUK03', 'MSS510HK(EU)', 'MSS510HK(EU)-TOUCH', 'MS-101', 'MS-104']
# get_photos(test_ids)
#
# get_catalog()
# write_json(marvel_cats)
# make_data_cats()
# get_stock("ПК_Монобл_до_22")
# asyncio.run(save_categories_vendors())
# create_csv_for_category_from_marvel()
# create_csv_for_category_from_marvel_v2()
# asyncio.run(save_categories_vendors())

photo = ['31730007404', '31730007404', 'HKCITA100MKIIGRYRU', 'JBLCLIP4WHT', 'JBLFLIP5ECOBLU', 'JBLFLIP5ECOGRN', 'JBLFLIP5SAND', 'JBLFLIP5TEAL', 'JBLFLIP6BLU', 'JBLXTREME3CAMOEU', 'JBLXTREME3CAMOUK', '1005543', '1005544', '1005696', 'TCN-S1-BK', '365144', '365144', '366158', '371652', '448105', '723928', '746327', '746328', '795824', '854630', '859946', '862339', '862356', '864311', '868673', 'DG Ares Smartwatch_Green', 'WT2001 Black', 'WT2001 Black', 'WT2001 Black GPS', 'WT2001 Blue', 'WT2001 Blue GPS', 'WT2001 Gold', 'WT2001 Gold GPS', 'WT2105 Black', 'WT2105 Black', 'WT2105 Black+Strap 1', 'WT2105 Rose Gold+Strap 1', 'B020', 'B210', 'V206', 'X15303', 'X15304', 'X15871', 'X15871', 'X16084', 'X16188', 'X16189', 'X17982', 'X18713', 'X23123', 'X23123', 'X24792', 'X24792', 'X25855', 'X26111', 'X26112', 'X26552', 'X26552', 'X28505', 'X28975', 'X29188', 'X30436', 'X31063', 'X31569', 'X32427', 'X34167', 'X35115', 'X35500', 'X35890', 'X36247', 'X37007', 'X38946', 'X40526', 'X40547', 'X40588', 'X40798', 'X41838', 'X41981', 'X43377', 'FLC901', 'FLC930 BLUE', 'FLF923', 'FLQ952 BLUE', 'FLQ952 PINK', 'FLS931 WHITE', 'FLT931 BLUE', 'FLT931 WHITE', 'FMH931/10', 'FSL961', 'FSM931', 'FSM971 BLUE', 'FSM971 PINK', 'FSM971 WHITE', 'FSP951', 'Haylou-LS05-1', 'Haylou-LS05-1', 'LS09A', 'LS09A', 'LS09B', 'LS11-Silver', 'LS11-Silver', 'RS3', 'RS4', 'RS4', 'RT2', '23306', '40461', '60144', '61151', '61165', '85130', '88921', '88930', '88935', '88937', '88970', 'WOD001-Black', 'WOD001-Gray', 'WOD003-Black', 'WOD003-Black', 'WOD003-Black', 'X39873', 'X44488', 'X44491', 'X48363', 'MD818FE/A', 'MD818FE/A', 'MD822ZM/A', 'SM4-GRY-FB-INT', 'H166 TPU cover', 'H166 TPU cover', '1A21RSQ00VA', '1A21T5W00VA', '8P00000001', '8P00000107', '8P00000126', 'GP-FPA217KDATR', 'Pero_Glass_Vivo V17 V17Neo', 'Pero_Glass_Vivo Y15 Y11 Y12', 'F-MFDP112KCL', 'AC30-F100M Black', 'AC30-F100M Black-Blue', 'AC30-F100M Black-Blue', 'AC30-F100M Black-Gray', 'AC30-F100M Red-Black', 'AC30-F200M Black', 'AC30-F200M Red', 'AC30-F200M Red', 'AC30-S100 Yellow', 'AC30-TF30 White', 'AL24-F100LED Black', 'AL24-F100LED Black-Gray', 'AL24-F100LED Red-Black', 'AL24-F100M Black', 'AL24-F100M Black-Gray', 'AL24-F100M Red+Black', 'AL24-F200M Black', 'AL24-F200M Red', 'AL24-T100 White', 'AL24-TF30 Black', 'AL24-TF30 White', 'AM24-F100M Red+black', 'CC30-F100M Black', 'CC30-F100M Black-Blue', 'CC30-F100M Black-Gray', 'CC30-F100M Red-Back', 'CC30-F100MA Black-Gray', 'CC30-F200M Black', 'CC30-F200M Red', 'CC30-S100 Blue', 'CC30-S100 Violet', 'CC30-S100 White', 'CC30-S100 White', 'CC30-TF30 Black', 'CC30-TF30 White', 'CC50-F100LED Red', 'CC50-F30M Black', 'CC50-F30M White', 'CC50-T100 Black', 'CC50-T100 White', 'CC50-T200 Black', 'CC50-T200 White', 'CL30-F100M Black', 'CL30-F100M Black-Gray', 'CL30-F100M Red-Black', 'CL30-F200SS Black', 'CL30-F200SS Red', 'CL30-T100 White', 'CL30-TF30 Black', 'CL30-TF30 White', 'F01-AL White', '72259', 'TCW-E20D Black', 'TCW-E30D Black', 'Bermuda 15W Black', 'OPAL 15W Grey', 'Agate 40W2C Black', 'Agate 40W2C White', 'Amethyst 33WCA White', 'Copper 10WU White', 'Crocus GaN 65WCA Black', 'Crystal 20WUT White', 'Grape 20WC Black Grey', 'Grape 20WC White Silver', 'Quartz 20WT White', 'Sunset 18WU White', 'Topaz 30W3A Black', 'Topaz 30W3A White', 'HJ-FC016K7-EU', 'HJ-PD33W-EU', 'TA8553', 'TA8553', 'TA9552', 'TA9652', 'TA9652', 'Fitness tracker_NAL-WB00_White', '914-000034', '920-009619', '920-009619', '920-009988', '920-009994', '920-010122', 'NPV', '43893', '43894', 'X41838', 'X25702', 'X30806', 'X35792', 'X35802', 'X35802', 'X46443', 'CL1 Orange', 'CL1 Orange', 'CS1 Blue', 'CS1 Blue', 'CS1 Orange', 'CS1 Orange', 'GM2-02', 'GM2-02', 'GS1 Blue', 'GS1 Blue', 'GS1 Brown', 'GS1 Brown', 'GS1 Brown', 'PS2', 'PS2', 'PS2', 'FSM931 Stand', 'VRGT782_Black', 'XRGT78_Black', 'XRGT78_Black', 'OSWC-FVR-OJD-L03-W', 'JRA0405', 'JRA0602', 'JRA0602', 'JRKL211', 'JRKL211', 'JRKL212', 'JRKL213', '90BOTNT21112U-BL01', '90BOTNT21113U-BL01', '90BOTNT21113U-BL01', '90COTNT1807U-BLCK', '90COTNT1807U-BLCK', '90COTNT1807U-BLCK', '90COTNT1807U-GR', '90COTNT2008U-BLCK', '90COTNT2008U-BLCK', '90COTNT2009U-BLCK', '90COTNT2009U-GR', 'A400 Ivory', 'A500S', 'A500S', 'Midrive D06', 'Midrive D08', 'Midrive RC09', 'Midrive TP01', 'Midrive TP03', 'AP-20B/DF', 'AP-20CB/DUO', 'AP-30C/FM', 'WINBOT W1 PRO_demo', 'VR30R01DW', 'VR32G02MW', 'VR32V02MW', 'DEM-A10W', 'DEM-A10W', 'Kyvol D10', 'Kyvol S32', 'Kyvol S32', 'Kyvol S60', 'Robot VC Kyvol D3', 'Robot VC Kyvol D3', 'Robot VC Kyvol D6', 'Robot VC Kyvol D6', 'Robot VC Kyvol E20', 'Robot VC Kyvol E25S', 'Robot VC Kyvol E30', 'Robot VC Kyvol E30', 'Robot VC Kyvol E31', 'Robot VC Kyvol S31', 'Robot VC Kyvol S31', 'Robot VC Kyvol S31', 'Robot VC Kyvol S31', 'YM-G1-B01', 'YM-G1-B01', 'YM-G1-W01', 'YM-R5D-W03', 'YM-R5D-W03', 'YM-S1-W03', 'YM-S1-W03', 'PVCR 3000 Cyclonic PRO', 'Q702-02', 'Q752-02', 'Q7M52-02', 'Q7MP02-00', 'Q7MP02-02', 'Q7MP52-02', 'Q7P02-02', 'Q7P52-02', 'Q7P52-02', 'S5E02-02', 'S5E52-02', 'S6V52-02', 'S6V52-02', 'S7MU52-02', 'S7P02-02', 'S7P02-02', 'ZNXDJQR01ZM', 'ZNXDJQR01ZM', 'ZNXDJQR01ZM', 'B600B', 'V-RVCLM24B', 'V-RVCLM27B', 'V-RVCLM40B', 'V-RVCLMC28A', 'V-RVCLMC28A', 'V-RVCLMD40B', 'V-RVCLMD40B', '2C601EUW', '2C601RUW', 'X25012', 'X25012', 'X26199', 'X26200', 'X26200', 'X27103', 'X33663', 'X39692', 'X41722', 'X41777', 'Cube', 'Floor 3', 'Floor 3+', 'Floor 3+', 'K651G', 'K651G', 'K760', 'K850+', 'K950', 'K950', '201-1918-2407', '201-1918-3900', '201-1921-0200', '201-2102-0400', '201-2102-3000', '201-2102-3100', '201-2102-4200', '201-2115-0000', '201-2115-0400', '201-2116-0500', '201-2231-0400', '201-2241-0500', '201-2241-0500', '201-2241-1100', 'C21Y-8E0006-GBWH0A', 'C21Y-8E0006-GBWH0A', 'C21Y-8E0006-GBWH0A', 'C32Y-8E0006-GBWH0B', 'C32Y-8E0006-GBWH0B', '8.02.0052', '8.02.0052', '8.02.0053', '8.02.0056', '8.02.0064', '8.02.0079', '8.02.0081', '8.02.0082', '8.02.0092', '8.02.0101', '8.02.0101', '8.02.0134', 'SA5004BUEU', '40.02.10.00.0232', '40.02.10.00.0392', '40.02.10.00.0392', '40.02.10.00.0393', '40.02.10.00.0394', '40.02.10.00.0395', '40.02.10.00.0395', '40.02.10.00.0403', '40.02.10.00.0404', '40.02.10.00.0405', '40.02.10.00.0405', '40.02.10.00.0406', 'Midrive PV01', 'Midrive PV01', 'VH120N02DW', 'CM1300W', 'CM1300W', 'CM800', 'CM800', 'CM800', 'DEM-DX1100W', 'DEM-DX1100W', 'DEM-TB880', 'DEM-TJ300W', 'DEM-TJ300W', 'DEM-TJ300W', 'DEM-TJ300W', 'DEM-VC80', 'DEM-VC80', 'DEM-VX20W', 'DEM-VX20W', 'DX1000W', 'DX1000W', 'DX1000W', 'DX1000W', 'DX118C', 'DX118C', 'DX600', 'DX600', 'DX600 White', 'DX700S', 'DX700S', 'DX900 Green', 'DX900 Green', 'DX900 Green', 'VC01 Max', 'VC01 Max', 'VC01 Max', 'VC01 Max', 'VC03S', 'VC03S', 'VC20 Pro', 'VC20 Pro', 'VC20 Pro', 'VC20 Pro', 'VC55', 'VC55', '443072-01', 'S10', 'S20 White', 'S31', 'YM-H4-W03', 'YM-SCXCH302', 'YM-SCXCH302', 'YM-V11H-W03', 'YM-V11H-W03', 'YM-V11H-W03', '1C291RUW', '1C3802RUG', '1C382RUB', '1C5001RUG', '1C7001RUB', '1C7001RUB', '1C7001RUB', '3C5501RUW', 'VXXD05', '1A502CNW', '2C501EUS', 'X28671', 'X28829', 'X40762', 'Amaranth II 10MDQ Blue', 'Atlant 30MQD Grey', 'Battleship II 20MPQ', 'Bison 30PQD Black', 'Bison 30PQD White', 'Seashell 10PD', 'Winter 20PD', 'EF AC', 'EF MC4 to XT60', 'EF3 Pro', 'EF4', 'EF4 Pro', 'EFD320', 'EFR610', 'MIRROR-4000 BLACK', 'MIRROR-4000 RED', 'RP15000 BLACK', 'SL10000 WHITE', 'SL6000 BLACK', 'SN10000 WHITE', 'TRAVEL10K GRAY', 'ZOO OWL', 'X24269', 'X24270', 'X24270', 'X24984', 'X26557', 'X26922', 'X26923', 'X26923', 'X26923', 'X28965', 'X35969', 'A2634_128Gb_Pink', 'A2892_128Gb_Gold', 'A2892_128Gb_Silver', 'A2892_256Gb_Purple', 'A2893_512Gb_Deep_Purple', 'A3090_256Gb_Black', 'A3090_256Gb_Pink', 'A3108_256Gb_Black', 'BL5000_Black', 'S40 Pro_Army Green', 'S40 Pro_Fire Orange', 'S40 Pro_Mineral Black', 'S41_Classic Black', 'S51_Classic Black', 'S58 Pro_Mineral Black', 'S59 Pro_Fire Orange', 'S59_Fire Orange', 'S59_Fire Orange', 'S59_Mineral Black', 'S61 Pro_8+128_Wood Grain', 'S61 Pro_8+128_Wood Grain', 'S68 Pro_Fire Orange', 'S68 Pro_Mineral Black', 'S86_Fire Orange', 'S88 Pro_Fre Orange', 'S88 Pro_Fre Orange', 'S88 Pro_Mineral Black', 'S88 Pro_Mineral Black', 'S88Plus_Fire Orange', 'S88Plus_Mineral Black', 'S89 Pro_Volcano Orange', 'S96 Pro_Army Green', 'S96 Pro_Army Green', 'S96 Pro_Fire Orange', 'S97 Pro_Orange Tiger', 'S97 Pro_Orange Tiger', 'S97 Pro_Silver Black', 'S98_Wine Red', 'X95_Emerald Green', 'X95_Starry Black', 'X96 Pro_Army Green', 'X96 Pro_Brick Red', 'X98 Pro_Emerald Green', 'H166 Black', 'H166 Black', 'R570 Black', 'R570E', 'R570E', 'R570E', 'R570E', 'SA50 2GB/16GB 2000mAh GMS Blac', 'SA50 2GB/16GB 2000mAh GMS Blac', 'SA55 2GB/16GB 2400mAh GMS Blue', 'SA55 2GB/16GB 2400mAh GMS Blue', 'SH60 2GB/32GB 3000mAh GMS Silv', 'SH60 2GB/32GB 3000mAh HMS Blac', 'SH65 2GB/32GB 4800mAh GMS Blac', 'A17 W5006X 16+1 Dark blue', 'A70 A665L 256+4 Starlish Black', '10Pro_RMX3661_Dark Mat 8+128', '9 5G_RMX3474_White 4+64', '9_RMX3521_Gold', 'C21-Y_RMX3263_Blue 3+32', 'C25S_RMX3195_Grey 4+64', 'C25S_RMX3195_Grey 4+64', 'C30_RMX3581_Blue 2+32', 'C33_RMX3624_Night Sea 4+64', 'C33_RMX3624_Sandy Gold 4+128', 'C51_RMX3830_Black 4+128', 'C51_RMX3830_Green 4+128', 'C53_RMX3760_Gold 6+128', 'C55_RMX3710_Black 8+256', 'C55_RMX3710_Sunshower 8+256', 'SIM+C51_RMX3830_Green 4+128', 'SM-A057FZKUCAU', 'SM-A135FZKKSKZ', 'SM-A245FLGVSKZ', 'SM-A346EZKASKZ', 'SM-A346EZSESKZ', 'SM-A546ELGASKZ', '5164D_Black 2+32', '5164D_Black 2+32', '5164D_Black 2+64', '6102D_Space gray', '6102H_Space gray', '6102H_Space gray', '6127I_Atlantic Blue', '6165H_Atlantic Blue 4+128', '6165H_Glacial Blue 4+128', '6165H_Space gray 4+128', '6165H_Space gray 4+64', 'T506D_Lavender Purple', 'T671F_Aurora Green', 'T676H_Blue', 'AD8 256+8 Stardust Grey', 'BF6 POP 7 64+2 Black', 'BF6 POP 7 64+2 Blue', 'BG6 SPARK Go 2024 64 White', 'CI8n CAMON 19 Pro 8+128 Blue', 'CI8n CAMON 19 Pro 8+128 Mondri', 'CK7n CAMON 20 Pro 8+256 Blue', 'CK7n CAMON 20 Pro 8+256 White2', 'KD7h SPARK 5 Spark Orange', 'KG5m SPARK Go 32 Atlantic Blue', 'KG5m SPARK Go 32 Atlantic Blue', 'KG5m SPARK Go 32 Atlantic Blue', 'KG5m SPARK Go 32 Ice Silver', 'KG5n SPARK 8C 64 Diamond Grey', 'KG5n SPARK 8C 64 Magnet Black', 'KG5n SPARK 8C 64 Turq Cyan', 'KI5m SPARK 10C 128+4 Black', 'KI5m SPARK 10C 128+4 Blue', 'KI5m SPARK 10C 64+4 Black', 'KI7 SPARK 10 Pro 256+8 White', 'LH6n 128+4 Hurricane Blue', 'Impress Eagle Graphite', 'Impress Energy 4G Graphite', 'Impress Lion  Graphite', 'V23 5G_Gold_Vivo V2130 8+128', 'V23e_Moonlight Shadow_V2116', 'V27e_Black_Vivo V2237 8+256', 'Y21_Diamond Glow_Vivo V2111', 'Y27s_BurgundyBlack_V2322 8+256', 'Y53S_Deep Sea Blue_Vivo V2058', '27980', '28411', '28412', '28412', '28414', '28414', '28415', '28415', '29236', '29237', '29237', '29238', '29801', '31117', '31185', '33192', '33193', '33445', '34489', '34490', '35256', '35644', '36511', '36543', '36554', '36595', '36596', '36602', '37035', '37035', '37774', '38088', '38088', '38234', '38234', '38235', '38236', '38431', '38438', '38487', '38512', '38604', '38608', '38858', '39567', '39567', '39607', '40317', '41300', '42480', '42494', '42495', '42495', '42506', '42542', '43107', '43197', '43204', '43239', '43243', '43973', '43983', '43986', '44004', '44005', '44009', '44009', '44013', '44210', '44227', '44227', '44768', '45035', '45038', '45040', '45043', '45043', '45049', '45577', '45717', '45754', '45887', '46804', '46815', '47226', '47226', '47230', '47606', '47609', '47636', '47638', '47661', '47952', '47977', '48763', '49095', '49108', '49113', '49113', '49137', '49141', '49640', '49957', 'F30720', 'F30722', 'R33191', 'R36498', 'R38257', 'X22717', 'X30704', 'X36683', 'X38636', 'X38665', 'X38888', 'X42552', 'X43214', 'X43400', 'X43400', 'X43404', 'X45640', '01-00512B', 'Blade A7 ice blue', 'Blade L8 black 1+32', 'Nubia Red Magic 5S Серебряный', 'ZTE Blade A31 Plus Серый', 'ZTE Blade A51 Синий 2+64', 'B170 Black', 'B170 Black', 'B170 Black', 'B170 Black', 'B241 Dark Grey', 'B241 Dark Grey', 'B241 Dark Grey', 'B241 Silver', 'B241 Silver', 'B280 Dark Grey', 'B280 Dark Grey', 'B280 Dark Grey', 'B280 Silver', 'B280 Silver', 'B280 Silver', 'B280 Silver', 'Ezzy Trendy 1 Grey', 'Ezzy Trendy 1 Grey', 'Ezzy Trendy 1 Red', 'Ezzy Trendy 1 Red', 'Ezzy4 Black', 'Ezzy4 White', 'Ezzy4 White', 'Ezzy5 Black', 'Ezzy5 Black', 'Ezzy5 Black', 'Ezzy5C Black', 'Ezzy5C Black', 'Ezzy5C Black', 'F170L Light Blue', 'F170L Light Blue', 'F170L Light Blue', 'F197 Black', 'F197 Black', 'F197 Black+SIM', 'F197 Dark Blue', 'F197 Dark Blue', 'F240L Light Blue', 'F240L Light Blue', 'F240L Light Blue', 'F257 Black', 'F280 Black', 'F280 Black', 'F280 Black', 'Flip 240 Black', 'Flip 240 Black', 'Flip 240 Black', 'Flip 240 Red', 'Flip 240 Red', 'Flip 280 Black', 'Flip 280 Blue', 'Flip 280 Blue', 'Flip 280 Blue', 'Flip2 Black', 'Flip2 Red', 'Flip2 Red', 'Flip3 Black', 'PR170 black-yellow', 'PR240 black-yellow', 'PR240 black-yellow', 'R240 Black-orange', 'R280 Black-orange', 'R280 Black-orange', 'R280C Black-orange', 'R280C Black-orange', 'S240 Dark Grey', 'S240 Dark Grey', 'S240 Dark Grey', 'S240 Dark Grey', 'S240 Silver', 'S240 Silver', 'S240 Silver', 'S286 Dark Grey', 'S286 Silver', 'S286 Silver', 'S286 Silver', 'S286 Silver', 'S350 Dark Grey', 'S350 Dark Grey', 'S350 Dark Grey', 'S350 Light Grey', 'S350 Light Grey', 'S350 Light Grey', 'it6350 Black', 'it663 Black', 'it663 Green', '16LIOB01A17', 'R341_рубиновый']


# print(len(get_photos(photo)))