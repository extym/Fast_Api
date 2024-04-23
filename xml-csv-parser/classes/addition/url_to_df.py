import os
import requests
from lxml import etree
import pandas as pd


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


def get_df(url: str, fileformat: str, filename = ''):
    if filename == '':
        filename = f'temp/temp-file.{fileformat}'
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f'Pasring error: Status code is {resp.status_code}')
        else:
            print('Success!')
        with open(filename, 'wb') as file:
            file.write(resp.content)
        if fileformat == 'xml':
            df = pd.read_xml(filename)
        else:
            try:
                df = pd.read_csv(filename, delimiter=';', encoding='cp1251')
            except:
                df = pd.read_csv(filename, delimiter=';', encoding='utf8')
        os.remove(filename)
    else:
        if fileformat == 'xml':
            df = pd.read_xml(filename)
        else:
            try:
                df = pd.read_csv(filename, delimiter=';', encoding='cp1251')
            except:
                df = pd.read_csv(filename, delimiter=';', encoding='utf8')
    return df


def get_xml(url: str, filename: str = ''):
    if filename != '':
        return etree.parse(filename)
    filename = f'temp/temp-file.xml'
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f'Pasring error: Status code is {resp.status_code}')
    else:
        print('Success!')
    with open(filename, 'wb') as file:
        file.write(resp.content)
    doc = etree.parse(filename)
    os.remove(filename)
    return doc
