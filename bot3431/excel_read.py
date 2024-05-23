import os

import pandas as pd
# pip install openpyxl  ## required

exist = [9705042666484, 9696749521336, 9682799885548, 9682799885548, 9674479370284, 9587004479548, 9654261977932, 9690080336404, 9596866844680, 9649782402280, 9618598716784, 9608490020608, 9561687122248, 9493654137244, 9516380456896, 9516380456896, 9494831052232, 9545648234272, 9521124610336, 9448411335496, 9444141597400, 9394236752560, 9392767889668, 9369275206768, 9358938426292, 9325920943024, 9587389421426, 9538287433322, 9530924872118, 9451469425370, 9417813306062, 9210083248994, 9203185979762, 9202301012678, 9178352161178, 9032907364754, 9896293992415, 9597430572439, 9635584514143, 9488543127619, 9448509771283, 9463928269963, 9442378865299, 9406122584971, 9384034901359, 9321603666763, 9365733417127, 9356336343967, 9324523145803, 9213053786707, 9252074448751, 9869330746596, 9926753249964, 9840902319444, 9883353369360, 9764968494288, 9708020406264, 9524950823712, 9561772753104, 9554893730616, 9599370169116, 9567693821532, 9491267334288, 9477773867100, 9437275218792, 9361250159916, 9332785239276, 9312987522036, 9217246856268, 9247244503404, 9180871972104, 9025181628924, 9074967869928, 9060315734496, 9803693526869, 9328785520781, 9213493468817, 9086505253949, 9134010651953, 9049747188161, 9044063327405, 9046690858541, 9009951039497, 9012888765281, 9979296509566, 9970291741402, 9897487232842, 9897487232842, 9831589116886, 9819382045150, 9420416987590, 9472133701899, 9472133701899]

def read_xlsx(file):
    file = pd.read_excel(file)
    df = pd.DataFrame(file).values
    proxy = {}
    maxy = []
    row = []
    shipment_date = ''
    for row in df:
        # try:
        #     if row[45] is not None:
        #         rr = int(row[45])
        #     else:
        #         continue
        #     if rr not in exist:
        #         faxy.append(rr)
        #     else:
        #         continue
        # except:
        #     continue
        # proxy[row[0]] = tuple(row[1:])
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
    print(1111111111, maxy, type(maxy[0]))
    return sorted(maxy), shipment_date


# read_xlsx('заказы-2024-02-29-отгрузка.xlsx')
# read_xlsx('order_items96.xls')
# read_xlsx('order_items-77.xls')
# read_xlsx('заказы-2024-04-10- отменен_покупателем.xlsx')
# read_xlsx('shipment_orders_2024-05-21.xlsx')