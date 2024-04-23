import re
import json
import datetime
from lxml import etree
from classes.addition.url_to_df import get_df, get_xml
from classes.addition.data import dop, yandex, yam_cols, yam_param_checker, yam_params_names_for_check


with open('jsons/tires_season.json', 'r', encoding='utf8') as file:
    tires_season = json.load(file)

with open('jsons/all_arts_wheels.json', 'r', encoding='utf8') as file:
    wheels_arts: dict = json.load(file)

with open('jsons/akk.json', 'r', encoding='utf8') as file:
    akk_data = json.load(file)


out_path = '/var/www/html/feed'

class YandexTable:
    def __init__(self, file_format):
        self.file_format = file_format
        if file_format == 'csv':
            self.main_table = get_xml(yandex['xml'])
            self.dop_rims = get_df(dop[file_format]['wheels'], fileformat=file_format)
            self.dop_akk = get_df(dop[file_format]['akk'], fileformat=file_format)
            self.dop_tires = get_df(dop[file_format]['tires'], fileformat=file_format)
        else:
            self.main_table = get_xml(yandex['xml'])
            self.dop_rims = get_xml(dop[file_format]['wheels'])
            self.dop_akk = get_xml(dop[file_format]['akk'])
            self.dop_tires = get_xml(dop[file_format]['tires'])

    def get_source_xml(file):
        # Не используется, так как нельзя csv таблицу перевести в yml без уточнения категорий
        d = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset=d, name='Moscow')
        n = datetime.datetime.now(tz=tz)
        et = etree.parse('shablon.xml')
        yml = et.getroot()
        yml.attrib['date'] = n.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':00'
        return et

    def get_yml_csv(self):
        offers = self.main_table.getroot().find('shop').find('offers')
        for good_type in ['tires', 'wheels', 'akk']:
            if good_type == 'tires':
                tdf = self.dop_tires
            elif good_type == 'wheels':
                tdf = self.dop_rims
            else:
                tdf = self.dop_akk
            for _row in tdf.iterrows():
                row = _row[1]
                try:
                    info = self.get_common_info_csv(row, good_type)
                except Exception as ex:
                    with open(f'logs/yam_{good_type}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                        file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {row["Название"]}.\nArticle: {row["Код"][1:]}\n{"="*40}\n')
                    continue
                self.get_offer(offers, info, good_type)
        self.main_table.write(f'{out_path}/yandex_csv.yml', encoding='utf8', pretty_print=True)

    def get_yml_xml(self):
        offers = self.main_table.getroot().find('shop').find('offers')
        for good_type in ['tires', 'wheels', 'akk']:
            if good_type == 'tires':
                tdf = self.dop_tires
            elif good_type == 'wheels':
                tdf = self.dop_rims
            else:
                tdf = self.dop_akk
            if good_type != 'akk':
                for offer in tdf.getroot().find('shop').find('offers').findall('offer'):
                    try:
                        info = self.get_common_info_xml(offer, good_type)
                    except Exception as ex:
                        with open(f'logs/yam_{good_type}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                            file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {offer.find("name").text}.\nArticle: {offer.find("vendorCode").text}\n{"="*40}\n')
                        continue
                    self.get_offer(offers, info, good_type)
            else:
                for offer in tdf.getroot().findall('Ad'):
                    try:
                        info = self.get_common_info_xml(offer, good_type, akk=True)
                    except Exception as ex:
                        with open(f'logs/yam_{good_type}_{self.file_format}_err_log.txt', 'a', encoding='utf8') as file:
                            file.write(f'[{datetime.datetime.now()}] Error: {ex}\nBad item: {offer.find("Title").text}.\nArticle: {offer.find("OEM").text}\n{"="*40}\n')
                        continue
                    self.get_offer(offers, info, good_type)
            self.main_table.write(f'{out_path}/yandex_xml.yml', encoding='utf8', pretty_print=True)

    def get_common_info_xml(self, offer, good_type: str, akk=False):
        if akk:
            url = ''
            price = offer.find('Price').text
            picture = ''
            name = offer.find('Title').text
            vendor = self.__check_brands(offer.find('Brand').text, good_type)
            oem = offer.find('OEM').text
            description = offer.find('Description').text
        else:
            url = offer.find('url').text
            price = offer.find('price').text
            try:
                picture = offer.find('picture').text
            except:
                picture = ''
            name = offer.find('name').text
            vendor = self.__check_brands(offer.find('vendor').text, good_type)
            oem = offer.find('vendorCode').text
            description = offer.find('description').text
        info = self.get_extra_info(good_type, name, description, vendor, price, oem, picture, url)
        return info

    def get_offer(self, parent, good_info: str, good_type: str):
        offer = etree.SubElement(parent, 'offer', attrib={'id': good_info['id']})
        for elem_name in yam_cols['main']:
            elem = etree.SubElement(offer, elem_name)
            if elem_name in {'name', 'description'}:
                elem.text = etree.CDATA(good_info[elem_name])
            else:
                elem.text = str(good_info[elem_name])
        for param_name in yam_cols['dop'][good_type]:
            splited = param_name.split(', ')
            if len(splited) > 1:
                name, unit = splited
                param = etree.SubElement(
                    offer,
                    'param',
                    attrib={
                        'name': name,
                        'unit': unit
                    }
                )
            else:
                name = splited[0]
                param = etree.SubElement(
                    offer,
                    'param',
                    attrib={
                        'name': name
                    }
                )
            try:
                param.text = good_info[name]
            except Exception as ex:
                print(f'{ex}: {param_name}, {good_info}')
                exit()
        del_opts = etree.SubElement(offer, 'delivery-options')
        pick_opts = etree.SubElement(offer, 'pickup-options')
        etree.SubElement(del_opts, 'option', attrib={'cost':"", 'days':''})
        etree.SubElement(pick_opts, 'option', attrib={'cost':"", 'days':'', 'order-before': ''})

    def get_common_info_csv(self, row: str, good_type: str):
            title = row['Название']
            description = title
            price = row['Цена']
            oem = row['Код'].replace('\'', '')
            brand = self.__check_brands(row['Бренд'], good_type)
            info = self.get_extra_info(good_type, title, description, brand, price, oem)
            return info

    def get_extra_info(self, good_type, title, description, brand, price, oem, picture='', url=''):
            good_id = re.sub(r'[^\w\d]', '', brand.upper()) + oem
            if good_type == 'tires':
                h, w, d, season, spikes = self.get_tires_info(title, oem)
                info = {
                    'id': good_id,
                    'url': url,
                    'name': title,
                    'description': description,
                    'price': price,
                    'categoryId': '207',
                    'currencyId': 'RUB',
                    'picture': picture,
                    'vendor': brand,
                    'vendorCode': oem,
                    'store': 'true',
                    'pickup': 'true',
                    'delivery': 'true',
                    'Высота профиля': h,
                    'Диаметр': d,
                    'Ширина профиля': w,
                    'Сезонность': season,
                    'Шипы': spikes
                }
            elif good_type == 'wheels':
                et, d, bolts, bolts_d, dia, rimtype, w = self.get_wheels_info(title, oem)
                info = {
                    'id': good_id,
                    'url': url,
                    'name': title,
                    'description': description,
                    'price': price,
                    'categoryId': '207',
                    'currencyId': 'RUB',
                    'picture': picture,
                    'vendor': brand,
                    'vendorCode': oem,
                    'store': 'true',
                    'pickup': 'true',
                    'delivery': 'true',
                    'Вылет (ET)': et,
                    'Диаметр обода (D)': d,
                    'Диаметр расположения отверстий': bolts_d,
                    'Диаметр центрального отверстия (DIA)': dia,
                    'Количество крепежных отверстий': bolts,
                    'Вид': rimtype,
                    'Ширина обода (J)': w
                }
            else:
                voltage, dcl, capacity, polarity, l, w, h = self.get_akk_info(title, oem)
                info = {
                    'id': good_id,
                    'url': url,
                    'name': title,
                    'description': description,
                    'price': price,
                    'categoryId': '136',
                    'currencyId': 'RUB',
                    'picture': picture,
                    'vendor': brand,
                    'vendorCode': oem,
                    'store': 'true',
                    'pickup': 'true',
                    'delivery': 'true',
                    'Напряжение': voltage,
                    'Пусковой ток': dcl,
                    'Емкость': capacity,
                    'Полярность': polarity,
                    'Длина': l,
                    'Ширина': w,
                    'Высота': h,
                }
            return info

    def get_tires_info(self, title, oem):
        wh = re.findall(r'\d{2,3}\/\d{1,2}(?:,\d|\.\d|C)?Z?(?:R\d{1,2}(?:,\d|\.\d)?C?)?\b', title)
        if len(wh) == 0:
            raise Exception('Нет параметров!')
        params = re.findall(r'\d+\.?C?\d?', wh[0].replace(',', '.'))
        if len(params) > 2:
            w, h, d = params
            d = 'R' + d
        else:
            w, h = params
            d = re.findall(r'R\d{1,2}(?:,\d|\.\d)?C?', title)[0]
            d = d.replace(',', '.')
        self.check_params('tires', [h, d, w])
        if len(d) == 0:
            raise Exception('Нет диаметра!')
        try:
            season = tires_season[oem]
            if season == 'Зимние шипованные':
                season = 'зимние'
                spikes = 'Да'
            elif season == 'Зимние нешипованные':
                season = 'зимние'
                spikes = 'Нет'
            else:
                season = season.lower()
                spikes = 'Нет'
        except:
            season = 'летние'
            spikes = 'Нет'
        return w, h, d, season, spikes
    
    def get_wheels_info(self, s: str, article: str):
        full_info_pattern = r'\b\d{1,2}(?:,\d{1,2}|\.\d{1,2})?x\d{1,2}(?:,\d|\.\d)?\/\d{1,2}x\d{2,3}(?:,\d{1,2}|\.\d{1,2})?\b'
        try:
            wheel_info = wheels_arts[article]
        except:
            raise Exception(f'Article not found: {article}.')
        if type(wheel_info) is dict:
            rim_type = wheel_info['Тип']
        else:
            rim_type = wheel_info.lower()
        info = re.findall(full_info_pattern, s)
        
        if info is not None and len(info) != 0:
            r_n_w, pcd = info[0].replace(',', '.').split('/')
            width, radius = r_n_w.split('x')
            bolts, bolts_rad = pcd.split('x')
        else:
            try:
                rim_radius_n_width = re.findall(r'\bR\d{1,2}(?:,\d|\.\d)?x\d{1,2}(?:,\d{1,2}|\.\d{1,2})?\b', s)[0]
                radius, width = rim_radius_n_width.replace(',', '.').split('x')
                radius = radius.replace('R', '')
            except:
                raise Exception(f'Диаметр и ширина не найдены. Строка: {s}')
            try:
                pcd = re.findall(r'\b\d{1,2}x(?:98|\d{3}|0)(?:,\d{1,2}|\.\d{1,2})?\b', s)[0]
                bolts, bolts_rad = pcd.replace(',', '.').split('x')
            except:
                raise Exception(f'PCD не найдены. Строка: {s}')
        try:
            offset = re.findall(r'\bET-?\d{1,3}(?:\.\d|,\d)?\b', s)[0].replace('ET', '').replace(',', '.')
        except:
            raise Exception(f'Вылет не найден. Строка: {s}')
        try:
            dia = re.findall(r'\b(?:[Dd]|CB)\d{2,3}(?:\.\d{1,2}|,\d{1,2})?\b', s)[0]
            dia = re.findall(r'\d{2,3}(?:\.\d{1,2}|,\d{1,2})?', dia)[0].replace(',', '.')
        except:
            raise Exception(f'DIA не найден. Строка: {s}')
        radius, bolts_rad, bolts, width = self.check_params('wheels', [radius, bolts_rad, bolts, width])
        return offset, radius, bolts, bolts_rad, dia, rim_type, width
    
    def get_akk_info(self, s: str, article: str):
        matches = re.findall(r'\b\d{2,3}(?:x|\*)\d{2,3}(?:x|\*)\d{2,3}\b', s)
        if len(matches) == 0:
            raise Exception(f'Bad item! {s}')
        sizes = matches[0].replace('*', 'x')
        l, w, h = re.findall(r'\d+', sizes)
        try:
            data = akk_data[article][0]
            dcl = data['Пусковой ток, А']
            polarity = data['Полярность'].split()[0].replace(',', '')
            voltage = '12' if 'Напряжение' not in data else data['Напряжение']
            capacity = data['Емкость']
            self.check_params('akk', [sizes, voltage])
        except Exception as ex:
            raise Exception(f'No data: {ex}')
        return voltage, dcl, capacity, polarity, l, w, h

    def __check_brands(self, s: str, good_type: str):
        for brand in yam_param_checker[good_type]['brand']:
            if s.upper() == 'KAMA':
                s = 'КАМА'
            if s.upper() == 'NOKIAN':
                s = 'Nokian Tyres'
            if s.upper() == 'OVATION':
                s = 'Ovation Tyres'
            if s.upper() == 'HANKOOK':
                s = 'Hankook Tire'
            if s.upper() == 'MARSHALL':
                s = 'Marshal'
            if brand.upper() == s.upper():
                return brand
        raise Exception(f'Бренд не в списке: {s}')
    
    def check_params(self, goods_type: str, params: list):
        params_names = yam_params_names_for_check[goods_type]
        for i, (name, value) in enumerate(zip(params_names, params)):
            self.check_param(name, value, goods_type)
        return params
    
    def check_param(self, param_name: str, param_value: str, good_type: str):
        if param_value not in yam_param_checker[good_type][param_name]:
            raise Exception(f'{param_name} нет в словаре. Value: {param_value}')