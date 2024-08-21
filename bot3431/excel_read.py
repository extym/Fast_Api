import os

import pandas as pd
# pip install openpyxl  ## required

import parts_soft as ps

def read_xlsx(file):
    file = pd.read_excel(file, sheet_name='Монтажный комплект тормозных ко')
    df = pd.DataFrame(file)
    row = {}
    maxy = []
    faxy = []
    category_name = ''
    prod = {
        "Код товара продавца*": row.get('@id'),
        "Название товара согласно формуле Тип товара + Бренд + Модель/Артикул": row.get("name"),
        "Бренд*": row.get("vendor"),
        "Артикул товара*": row.get("vendorCode"),
        "Описание товара": row.get("description"),
        "URL ОСНОВНОГО ФОТО*": row.get("picture"),
        "Вес упаковки (кг)": 1.2,
        "Высота упаковки (см)*": 12,
        "Ширина упаковки (см)*": 15,
        "Длина упаковки (см)*": 28,
        "Артикул производителя": row.get("vendorCode"),
        "Тип": category_name
    }
    for row in df.items():
        name = row[1][1]
        maxy.append(row[1][1])
        if name not in prod.keys():
            print(f'"{name}": row.get("{name}"),')
            faxy.append(row[1][1])
        else:
            print(f'"{name}": {prod.get(name)}.')
    print(faxy)
    print(maxy)


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
    elif market == "710" or market == "715" or market == "1972" or market == "1973":
        for row in df:
            maxy.append(int(row[0]))
            shipment_date = row[13][:-5]

    # print(*row, sep='\n')
    # print(1111111111, maxy, type(maxy))
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
    pr.to_excel('output-0907.xlsx', sheet_name='Товары, доступные для поставки')   #,
                # columns=['number', 'Артикул товара продавца', 'Наименование товара', 'Штрихкод',
                #          'Необходимость маркировки', 'План поставки (шт.)',
                #          'Максимальный план поставки (шт.)', 'Комментарии'])


    print("ALL RIDE")
    # print(*cow, sep='\n')


def rewrite_xlsx_v2(file1, file2): # for uploading if file2 has form uploading
    file = pd.read_excel(file1, sheet_name='Товары, доступные для поставки')
    sber = pd.DataFrame(file)
    our_file = pd.read_excel(file2)
    df2 = pd.DataFrame(our_file).values
    proxy = []
    count = 0
    for i in sber.index:
        sber_articul = sber.values[i][0]
        for row in df2:
            articul = str(row[0])

            if articul.upper() == sber_articul.upper():
                print(55555555555, articul, sber_articul)
                maxy = list(sber.values[i])
                sber_max = sber.values[i][5]
                availible_stock = int(row[4])
                if availible_stock <= sber_max:
                    maxy[4] = availible_stock
                else:
                    maxy[4] = sber_max

                sber_barkode = sber.values[i][2]
                our_barcode = row[2]
                # print(222, our_barcode, sber_barkode)
                if str(sber_barkode) == 'nan' and our_barcode is not None:
                    maxy[2] = our_barcode

                proxy.append(maxy)

            # elif articul.upper() != sber_articul.upper() and count == 0:
            #     faxy.append(row)

        count += 1

    example = {i[0].upper(): i for i in proxy}
    so_example = {i[0].upper(): i for i in df2}
    print(5555, len(example.keys()), len(so_example.keys()))
    faxy = so_example.copy()
    for key in so_example.keys():
        if key in example:
            del faxy[key]
    print(7777, len(faxy.keys()))
    baxy = [i for i in faxy.values()]
    pr = pd.DataFrame(proxy)
    pr.to_excel('output-11-07-new.xlsx', sheet_name='Товары, доступные для поставки')   #,
                # columns=['number', 'Артикул товара продавца', 'Наименование товара', 'Штрихкод',
                #          'Необходимость маркировки', 'План поставки (шт.)',
                #          'Максимальный план поставки (шт.)', 'Комментарии'])
    print("ALL RIDE")

    pr = pd.DataFrame(baxy)
    pr.to_excel('delta-11-07-new.xlsx', sheet_name='Товары, доступные для поставки')


def read_csv(link=None):
    data = pd.read_csv(link, encoding="windows-1251",
                        delimiter=';', skiprows=1)
    for row in data:
        print(type(row), row)


# read_xlsx('заказы-2024-02-29-отгрузка.xlsx')
# read_xlsx('order_items96.xls')
# read_xlsx('order_items-77.xls')
# read_xlsx('заказы-2024-04-10- отменен_покупателем.xlsx')
# read_xlsx('shipment_orders_2024-05-21.xlsx')
# rewrite_xlsx('02-07-2024.xlsx', 'fbo-0207.xlsx')
# rewrite_xlsx_v2("source-11-07.xlsx", "111111111111.xlsx")
# read_csv(link='https://3431.ru/system/unload_prices/45/sbermegamarket3431rucc.csv')

# read_xlsx('1234.xlsx')  #its uploading file