import pandas as pd
from parts-soft import *


def read_xls(files):
    file = pd.read_excel(files)
    df = pd.DataFrame(file).values
    proxy = {}
    for row in df:
        proxy[row[0]] = tuple(row[1:])
    print(proxy, sep='\n')

    return proxy  #dict


# read_xls('заказы-2024-02-29-отгрузка.xlsx')