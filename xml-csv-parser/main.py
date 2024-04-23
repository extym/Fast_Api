from sys import argv
# import pandas as pd
# from lxml import etree
from classes.avito import AvitoTable
from classes.yandex import YandexTable


def avito(ff):

    avta = AvitoTable(ff)
    if ff == 'csv':
        avta.get_csv()
    elif ff == 'xml':
        avta.get_xml()


def yandex(ff: str):
    yam = YandexTable(ff)
    yam.get_yml_csv()



def main(market, ff):
    # print('hello, guf!')
    if market == 'yandex':
        yandex(ff)
        print(f'Яндекс! market: {market}, format: {ff}')
    else:
        avito(ff)
        print(f'Авито! market: {market}, format: {ff}')


if __name__ == '__main__':
    script, market, ff = argv
    if market not in ['yandex', 'avito']:
        raise Exception(f'Неверный параметр маркетплейса: {market}')
    if ff not in ['xml', 'csv']:
        raise Exception(f'Неверный параметр формата файла: {ff}')
    main(market, ff)