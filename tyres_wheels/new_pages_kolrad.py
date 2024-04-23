import datetime
import json
import sys

from cred import *
from bs4 import BeautifulSoup as bs
from xml.etree import ElementTree as ET
import requests
import lxml
import xmltodict






def get_data_et():
    resp = requests.get(link)
    data = ET.fromstring(resp.content)
    for row in data.find('product'):
        print(row)

    print(data)


# get_data_et()

def get_smth_bs():
    '''
    <product>
    <code>00095484</code>
    <name>"Accuride 11,75x22,5 M22 10/335/281/0 (396-3101012-01) s/v 5000 кг"</name>
    <type>"Грузовые диски"</type>
    <vendor>"Accuride"</vendor>
    <model>"M22"</model>
    <width>"11,75"</width>
    <diameter>"x22,5"</diameter>
    <pcd1>"10"</pcd1>
    <pcd2>"335"</pcd2>
    <et>"0"</et>
    <dia>"281"</dia>
    <scolor>"Серебристый"</scolor>
    <color>"s/v"</color>
    <vendor_code>"396-3101012-01"</vendor_code>
    <rest>"&gt;12"</rest>
    <rest2>"0"</rest2>
    <rest3>"0"</rest3>
    <sales>"0"</sales>
    <price>"9 920.00"</price>
    <roznicaprice>"11 110.00"</roznicaprice>
    <foto>"http://images.kolrad.ru/foto/f00095484.jpg"</foto>
    </product>
    :return:
    '''
    resp = requests.get(link)
    soup = bs(resp.text, 'lxml')

    all = soup.find('product')
    print(all)

# get_smth_bs ()


def get_xml():
    resp = requests.get(link)
    data = xmltodict.parse(resp.text)
    data_product = data['data']['product']
    print(data['data']['product'][-1], sep='\n')

    print(datetime.datetime.now(), 'data_product2 - ', len(data_product))
    # post_smth(data_product, 0, '0')
    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open(DATA_PATH + "data_product.json", "w") as write_file:
        json.dump(data_product, write_file) # encode dict into JSON

    # return data['data']['product']   #list


# get_xml()