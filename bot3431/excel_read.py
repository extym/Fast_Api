import os

import pandas as pd
# pip install openpyxl  ## required

import parts_soft as ps

def read_xlsx(file):
    file = pd.read_excel(file, sheet_name='Товары, доступные для поставки')
    df = pd.DataFrame(file).values
    proxy = {}
    maxy = []
    row = []
    shipment_date = ''
    for row in df:
        print(row)
        try:
            maxy.append(int(row[0]))
        except:
            continue
        shipment_date = row[13][:-5]

    print(*row, sep='\n')
    print(11221111, shipment_date, maxy)
    return sorted(maxy), shipment_date

def read_xlsx_v2(file, market):
    file = pd.read_excel(file)
    df = pd.DataFrame(file).values
    proxy = {}
    maxy = []
    row = []
    shipment_date = ''
    # print('market', market, type(market))
    if market == '2063' or market == '235':
        for row in df:
            try:
                maxy.append(int(row[0]))

            except:
                continue
            shipment_date = row[11]
    elif market == "710" or market == "715":
        for row in df:
            maxy.append(int(row[0]))
            shipment_date = row[13][:-5]

    # print(*row, sep='\n')
    # print(1111111111, maxy, type(maxy[0]))
    return sorted(maxy), shipment_date


def rewrite_xlsx(file1, file2):
    global row2, row, cow
    file = pd.read_excel(file1, sheet_name='Товары, доступные для поставки')
    sber = pd.DataFrame(file)
    our_file = pd.read_excel(file2)
    df2 = pd.DataFrame(our_file).values
    proxy = []
    maxy = []
    for cow in df2:
        articul  = str(cow[2]) + str(cow[3])
        for i in sber.index:
            sber_articul = sber.values[i][0]
            if articul.upper() == sber_articul.upper():
                maxy = list(sber.values[i])
                sber_max = sber.values[i][5]
                availible_stock = cow[6]
                # if availible_stock <= sber_max:
                #     maxy[4] = availible_stock
                #     proxy.append(maxy)
                # else:
                #     sber.values[i][4] = sber_max
                #     proxy.append(sber.values[i])
                if availible_stock <= sber_max:
                    maxy[4] = availible_stock
                else:
                    maxy[4] = sber_max

                sber_barkode = sber.values[i][2]
                if str(sber_barkode) == 'nan':
                    barcode = ps.get_barcode_from_xml_v2(vendor=str(cow[2]),
                                                         vendor_code=str(cow[3]),
                                                         link='https://3431.ru/system/unload_prices/46/yandex_market.xml')
                    maxy[2] = barcode
                proxy.append(maxy)

    pr = pd.DataFrame(proxy)
    pr.to_excel('output-2.xlsx', sheet_name='Товары, доступные для поставки')   #,
                # columns=['number', 'Артикул товара продавца', 'Наименование товара', 'Штрихкод',
                #          'Необходимость маркировки', 'План поставки (шт.)',
                #          'Максимальный план поставки (шт.)', 'Комментарии'])


    print("ALL RIDE")
    # print(*cow, sep='\n')



# read_xlsx('заказы-2024-02-29-отгрузка.xlsx')
# read_xlsx('order_items96.xls')
# read_xlsx('order_items-77.xls')
# read_xlsx('заказы-2024-04-10- отменен_покупателем.xlsx')
# read_xlsx('shipment_orders_2024-05-21.xlsx')
# rewrite_xlsx('02-07-2024.xlsx', 'fbo-0207.xlsx')