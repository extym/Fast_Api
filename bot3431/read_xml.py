# import zeep
import pandas as pd

from cred import *
import xmltodict
import csv
import urllib
from urllib.request import urlopen


def rewrite_asia_tires():
    data = urlopen('https://b2b.asia-tires.ru/export_data/tires.xml')
    xml = xmltodict.parse(data.read())

    # with open('https://b2b.asia-tires.ru/export_data/tires.xml', 'f') as file:
    #     xml = xmltodict.parse(file.read())

    # answer =  urllib.request.urlopen('https://b2b.asia-tires.ru/export_data/tires.xml')
    # print(11)
    # data = answer.read()
    # print(22)
    # xml = xmltodict.parse(data)

    print(type(xml['data']['tires']))
    print(xml.keys())
    print(len(xml['data']['tires']))
    fields = ['price_rnd', 'price_spb', 'name', 'model', 'articul', 'season', 'speed_index', 'img', 'brand',
              'load_index', 'thorn', 'price_spb_rozn', 'rest_spb', 'width', 'diameter', 'height', 'runflat',
              'price_krd_rozn', 'price_nvt', '@internal-id', 'price_krd', 'rest_nvt', 'rest_krd',
              'rest_rnd', 'price_rnd_rozn', 'price_nvt_rozn', 'rest_msk', 'price_msk', 'price_msk_rozn']
    with open(CSV_PATH + 'asia-tyres.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()
        csv_writer.writerows(xml['data']['tires'])


def get_data_for_cards_from_xml(category_name: str = None,
                                offer_id=None, link=None):
    proxy = []
    with urlopen(link) as xml:
        doc = xmltodict.parse(xml)
        category_pool = doc['yml_catalog']['shop']['categories']['category']
        categories = {i['@id']: i for i in category_pool}
        categories_text = {i['#text']: i for i in category_pool}

        for row in doc['yml_catalog']['shop']['offers']['offer']:
            name = row["name"]
            if name and category_name in name:
                print(*row.items(), sep='\n')

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
                prod_add = {
                    "Основной штрихкод (GTIN)": row.get("Основной штрихкод (GTIN)"),
                    "Штрихкод 2": row.get("Штрихкод 2"),
                    "Штрихкод 3": row.get("Штрихкод 3"),
                    "Штрихкод 4": row.get("Штрихкод 4"),
                    "Штрихкод 5": row.get("Штрихкод 5"),
                    "Модель": row.get("Модель"),
                    "Серия": row.get("Серия"),
                    "URL ФОТО 2": row.get("URL ФОТО 2"),
                    "URL ФОТО 3": row.get("URL ФОТО 3"),
                    "URL ФОТО 4": row.get("URL ФОТО 4"),
                    "URL ФОТО 5": row.get("URL ФОТО 5"),
                    "URL ФОТО 6": row.get("URL ФОТО 6"),
                    "URL ФОТО 7": row.get("URL ФОТО 7"),
                    "URL ФОТО 8": row.get("URL ФОТО 8"),
                    "URL ФОТО 9": row.get("URL ФОТО 9"),
                    "URL ФОТО 10": row.get("URL ФОТО 10"),
                    "URL ФОТО 11": row.get("URL ФОТО 11"),
                    "URL ФОТО 12": row.get("URL ФОТО 12"),
                    "URL ФОТО 13": row.get("URL ФОТО 13"),
                    "URL ФОТО 14": row.get("URL ФОТО 14"),
                    "URL ФОТО 15": row.get("URL ФОТО 15"),
                }
                prod.update(prod_add)
                proxy.append(prod)

    pr = pd.DataFrame(proxy)
    with pd.ExcelWriter('cart-12345.xlsx', mode='a', if_sheet_exists='replace') as writer:
        pr.to_excel(writer, sheet_name='Монтажный комплект тормозных ко', index=False,
                    # header=['Код товара продавца*',
                    #         "Название товара согласно формуле Тип товара + Бренд + Модель/Артикул",
                    #         'Бренд*', 'Артикул товара*', 'Описание товара',
                    #         'URL ОСНОВНОГО ФОТО*', 'Вес упаковки (кг)*', 'Высота упаковки (см)*',
                    #         'Ширина упаковки (см)*', 'Длина упаковки (см)*', 'Артикул производителя', 'Тип'])
                    header=['Код товара продавца*', 'Основной штрихкод (GTIN)', 'Штрихкод 2', 'Штрихкод 3',
                            'Штрихкод 4', 'Штрихкод 5', 'Название товара согласно формуле Тип товара + Бренд + Модель/Артикул',
                            'Бренд*', 'Модель', 'Артикул товара*', 'Серия', 'Описание товара',
                            'URL ОСНОВНОГО ФОТО*', 'URL ФОТО 2', 'URL ФОТО 3', 'URL ФОТО 4', 'URL ФОТО 5',
                            'URL ФОТО 6', 'URL ФОТО 7', 'URL ФОТО 8', 'URL ФОТО 9', 'URL ФОТО 10', 'URL ФОТО 11',
                            'URL ФОТО 12', 'URL ФОТО 13', 'URL ФОТО 14', 'URL ФОТО 15', 'Ссылка на pdf-инструкцию',
                            'Ссылка на сертификат', 'Вес упаковки (кг)*', 'Высота упаковки (см)*',
                            'Ширина упаковки (см)*', 'Длина упаковки (см)*', 'OEM', 'Маркетинговый цвет', 'Примечание',
                            'Цена за', 'CROSS VENDOR', 'CROSS VENDOR COD', 'Количество в упаковке, в штуках',
                            'Страна производства', 'Артикул производителя', 'Тип'])

    # return brand, oem


# get_data_for_cards_from_xml(category_name="Тормозные колодки",
#                             link='https://3431.ru/system/unload_prices/45/sbermegamarket.xml')

get_data_for_cards_from_xml(category_name="Колодки тормозные",
                            link='https://3431.ru/system/unload_prices/45/yandex_market.xml')
