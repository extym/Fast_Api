import re
import json
import datetime
import pandas as pd
from lxml import etree
from classes.addition.url_to_df import get_df
from classes.addition.parsers import get_tires_params, get_akk_params, get_wheels_params
from classes.addition.data import avito_cols, goods, checks

with open('jsons/tires_season.json', 'r', encoding='utf8') as file:
    tires_season = json.load(file)

out_path = '/var/www/html/feed'

class AvitoTable:
    def __init__(self, file_format: str):
        self.table_tires = get_df(
            goods[file_format]['tires'],
            fileformat=file_format,
            # filename=f'tables/avito/{good_type}.{file_format}'
        )
        self.table_wheels = get_df(
            goods[file_format]['wheels'],
            fileformat=file_format,
            # filename=f'tables/avito/{good_type}.{file_format}'
        )
        self.table_akk = get_df(
            goods[file_format]['akk'],
            fileformat=file_format,
            # filename=f'tables/avito/{good_type}.{file_format}'
        )
        self.file_format = file_format
 
    def get_csv(self):
        df = pd.DataFrame(columns=avito_cols['common'])
        for gtype in ['tires', 'wheels', 'akk']:
            if gtype == 'tires':
                tdf = self.table_tires
            elif gtype == 'wheels':
                tdf = self.table_wheels
            else:
                tdf = self.table_akk
            if gtype != 'wheels':
                fn_b = f'tables/brands_{gtype}.csv'
                brands = get_df(checks['brands'], fileformat='csv', filename=fn_b)
                brands = brands.join(brands['Brand'].apply(lambda x: x.upper()), rsuffix='_up')
                tdf = pd.merge(tdf, brands, left_on='Бренд', right_on='Brand_up')
            for row in tdf.iterrows():
                row = row[1]
                try:
                    if gtype == 'tires':
                        values = self.__collect_tires_values(row)
                    elif gtype == 'wheels':
                        values = self.__collect_wheels_values(row)
                    else:
                        values = self.__collect_akk_values(row, brands)
                except Exception as ex:
                    art = row["Код"]
                    title = row["Название"]
                    with open(f'logs/{gtype}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                        file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {title}.\nArticle: {art}\n{"="*40}\n')
                    continue
                # try:
                if values[0] not in df['Id'].unique():
                    new_row = dict(zip(avito_cols[gtype], values))
                    df = df._append(new_row, ignore_index=True)
                # except Exception as ex:
                #     print(ex)
                #     df.to_csv(f'{out_path}/avito.csv', encoding='utf8', index=False)
                #     print(values)
                #     exit()
        df.to_csv(f'{out_path}/avito.csv', encoding='utf8', index=False)

    def __collect_tires_values(self, row: dict):
        if self.file_format == 'csv':
            pre_title = row['Название']
            code = re.sub(r'[^\w\d]', '', row['Brand_up']) + row['Код'].replace('\'', '')
            oem = row['Код'].replace('\'', '')
            price = str(int(row['Цена']))
            brand = row['Brand']
        else:
            pre_title = row[9].replace('<![CDATA[', '').replace(']]>', '')
            code = row[0]
            oem = row[14]
            price = row[12]
            brand = row[17]
        title_splited = pre_title.split('http')
        title = title_splited[0]
        w, h, d, model = get_tires_params(title, brand)
        try:
            season = tires_season[oem]
        except:
            season = 'Летние'
        try:
            url = 'http' + title_splited[1].replace('.png.', '.')
        except:
            url = ''
        values = [
            code,
            'Санкт-Петербург, Лахтинский проспект дом 7',
            'Запчасти и аксессуары',
            title,
            '+78125076964',
            title,
            'Шины, диски и колёса',
            'Товар приобретен на продажу',
            'Для автомобилей',
            'Шины',
            '10-048',
            brand,
            model,
            oem,
            w,
            d,
            h,
            season,
            'за 1 шт.',
            'Новое',
            price,
            url
        ]
        return values

    def __collect_wheels_values(self, row: dict):
        if self.file_format == 'csv':
            article = row['Код'].replace("\'", '')
            pre_title = row['Название']
            price = str(int(row['Цена']))
            gid = re.sub(r'[^\w\d]', '', row['Бренд']) + article
        else:
            article = row[13]
            pre_title = row[8].replace('<![CDATA[', '').replace(']]>', '')
            price = row[11]
            gid = row[0]
        title_splited = pre_title.split('http') 
        title = title_splited[0]
        try:
            url = 'http' + title_splited[1].replace('.png.', '.')
        except:
            url = ''
        rim_type, radius, width, bolts, bolts_rad, offset, dia = get_wheels_params(title, article)
        values = [
            gid,
            'Санкт-Петербург, Пискаревский пр-кт 150 к.2',
            'Запчасти и аксессуары',
            title,
            title,
            'Шины, диски и колёса',
            'Товар приобретен на продажу',
            'Диски',
            width,
            radius,
            offset,
            bolts,
            bolts_rad,
            dia,
            rim_type,
            'Новое',
            price,
            url
        ]
        return values
    
    def __collect_akk_values(self, row: dict, brands: pd.DataFrame):
        if self.file_format == 'csv':
            article = row['Код'].replace("\'", '')
            pre_title = row['Название']
            price = str(int(row['Цена']))
        else:
            article = row[14]
            pre_title = row[9].replace('<![CDATA[', '').replace(']]>', '')
            price = row[12]
        title = pre_title
        l, w, h, dcl, polarity, voltage, capacity, brand = get_akk_params(title, article)
        if brand.upper() not in brands['Brand_up'].unique():
            raise Exception(f'Brand not in avito. Brand: {brand}. String: {title}')
        values = [
            re.sub(r'[^\w\d]', '', brand.upper()) + article,
            'Санкт-Петербург, Пискаревский пр-кт 150 к.2',
            'Запчасти и аксессуары',
            title,
            title,
            'Запчасти',
            'Товар приобретен на продажу',
            'Для автомобилей',
            'Аккумуляторы',
            voltage,
            capacity,
            dcl,
            polarity,
            l,
            w,
            h,
            'Новое',
            brand,
            article,
            price,
            ''
        ]
        return values

    def get_xml(self):
        ads = etree.Element(
            'Ads',
            attrib={
                'formatVersion': '3',
                'target': 'Avito.ru'
            }
        )
        table = etree.ElementTree(ads)
        for gtype in ['tires', 'wheels', 'akk']:
            if gtype == 'tires':
                tdf = self.table_tires
            elif gtype == 'wheels':
                tdf = self.table_wheels
            else:
                tdf = self.table_akk
            if gtype != 'wheels':
                fn_b = f'tables/brands_{gtype}.csv'
                brands = get_df(checks['brands'], fileformat='csv', filename=fn_b)
                brands = brands.join(brands['Brand'].apply(lambda x: x.upper()), rsuffix='_up')
                tdf = pd.merge(tdf, brands, left_on='Brand', right_on='Brand_up')
            # tdf.to_csv('check_wheels.csv', index=False)
            # exit()
            were = set()
            for row in tdf.itertuples(index=False):
                try:
                    if gtype == 'tires':
                        values = self.__collect_tires_values(row)
                    elif gtype == 'wheels':
                        values = self.__collect_wheels_values(row)
                    else:
                        values = self.__collect_akk_values(row, brands)
                except Exception as ex:
                    art = row[0]
                    title = row[9]
                    with open(f'logs/{gtype}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                        file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {title}.\nArticle: {art}\n{"="*40}\n')
                    continue
                ad = etree.SubElement(ads, 'Ad')
                try:
                    for name, value in zip(avito_cols[gtype], values):
                        value = str(value)
                        if name == 'ImageUrls':
                            name = 'Images'
                            imgs = etree.SubElement(ad, name)
                            img = etree.SubElement(imgs, 'Image', attrib={'url': value})
                        else:
                            if name == 'Id':
                                if value not in were:
                                    were.add(value)
                                else:
                                    raise Exception(f'Dublicate: {value}')
                            if name == 'Description' or name == 'Title':
                                value = etree.CDATA(value)
                            temp = etree.SubElement(ad, name)
                            temp.text = value
                except Exception as ex:
                    art = row[0]
                    title = row[9]
                    with open(f'logs/{gtype}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                        file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {title}.\nArticle: {art}\n{"="*40}\n')
                    continue
        table.write(f'{out_path}/avito.xml', pretty_print=True, encoding='utf8')
            






