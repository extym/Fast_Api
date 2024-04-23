import re
import json
from classes.addition.data import params_checker, params_names_for_check
# from data import params_checker, params_names_for_check, tires_models


with open('jsons/tires_models_avito.json', 'r', encoding='utf8') as file:
    models_tires_avito = json.load(file)

with open('jsons/akk.json', 'r', encoding='utf8') as file:
    akk_data = json.load(file)

with open('jsons/all_arts_wheels.json', 'r', encoding='utf8') as file:
    wheels_arts: dict = json.load(file)


def check_param(param_name: str, param_value: str):
    if param_value not in params_checker[param_name]:
        raise Exception(f'{param_name} нет в словаре. Value: {param_value}')
    

def check_params(goods_type: str, params: list):
    params_names = params_names_for_check[goods_type]
    if goods_type == 'tires':
        for i, (name, value) in enumerate(zip(params_names, params)):
            try:
                check_param(name, value)
            except:
                params[i] = 'Другое'
    else:
        for name, value in zip(params_names, params):
            if name == 'rimoffset':
                try:
                    check_param(name, value)
                except:
                    value = value.replace('.', ',')
                    params[2] = value
            elif name == 'rimdia':
                try:
                    check_param(name, value)
                except:
                    value = str(float(value))
                    params[-1] = value
            check_param(name, value)
    return params


def get_tires_params(s: str, brand: str):
    # Есть проблемы с распознованием модели шин, требует более глубокого изучения
    # // [
    # //     "Advan Sport V105W ",
    # //     "(?:\\badvan\\b|\\bsport\\b|\\bv105w\\b)",
    # //     3
    # // ],
    # Модель не проходит проверку
    wh = re.findall(r'\d{2,3}\/\d{1,2}(?:,\d|\.\d|C)?Z?(?:R\d{1,2}(?:,\d|\.\d)?C?)?\b', s)
    if len(wh) == 0:
        raise Exception('Нет параметров!')
    params = re.findall(r'\d+\.?C?\d?', wh[0].replace(',', '.'))
    if len(params) > 2:
        w, h, d = params
    else:
        w, h = params
        d = re.findall(r'R\d{1,2}(?:,\d|\.\d)?C?', s)[0]
        d = d.replace(',', '.').replace('R', '')
    w, d, h = check_params('tires', [w, d, h])
    if len(d) == 0:
        raise Exception('Нет диаметра!')
    models = models_tires_avito[brand][::-1]
    final_name = ''
    for model in models:
        model_name, pattern, word_count = model
        matches = re.findall(pattern, s.lower())
        if len(set(matches)) == word_count:
            final_name = model_name
            break
    if final_name == '':
        raise Exception('Нет модели')
    return w, h, d, final_name


def get_akk_params(s: str, article: str):
    matches = re.findall(r'\b\d{2,3}(?:x|\*)\d{2,3}(?:x|\*)\d{2,3}\b', s)
    if len(matches) == 0:
        raise Exception(f'Bad item! {s}')
    sizes = matches[0]
    l, w, h = re.findall(r'\d+', sizes)
    try:
        data = akk_data[article][0]
        dcl = data['Пусковой ток, А']
        polarity = data['Полярность'].split()[0].replace(',', '')
        voltage = '12' if 'Напряжение' not in data else data['Напряжение']
        capacity = data['Емкость']
        brand = data['Бренд']
        l, w, h, dcl, voltage, capacity = check_params('akk', [l, w, h, dcl, voltage, capacity])
    except Exception as ex:
        raise Exception(f'No data: {ex}')
    return l, w, h, dcl, polarity, voltage, capacity, brand


def get_wheels_params(s: str, article: str):
    full_info_pattern = r'\b\d{1,2}(?:,\d{1,2}|\.\d{1,2})?x\d{1,2}(?:,\d|\.\d)?\/\d{1,2}x\d{2,3}(?:,\d{1,2}|\.\d{1,2})?\b'
    try:
        wheel_info = wheels_arts[article]
    except:
        raise Exception(f'Article not found: {article}.')
    if type(wheel_info) is dict:
        rim_type = wheel_info['Тип']
    else:
        rim_type = wheel_info.title()
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
    width, radius, offset, bolts, bolts_rad, dia = check_params('wheels', [width, radius, offset, bolts, bolts_rad, dia])
    return rim_type, radius, width, bolts, bolts_rad, offset, dia


if __name__ == '__main__':
    s = 'КиК Серия Реплика КС894 (ZV17_Mazda 6) R17x7.5 5x114.3 ET50 CB67.1 Silver'
    art = '75471'
    test = 'Michelin Pilot Alpin PA4 235/50R17 100V XL'
    print(get_tires_params(test, 'Michelin'))
    # print(get_wheels_params(s, art))
    pass