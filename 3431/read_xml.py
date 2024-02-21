# import zeep
from cred import *
import xmltodict
import csv
import urllib

data =  urllib.request.urlopen('https://b2b.asia-tires.ru/export_data/tires.xml')
print(11)
xml = xmltodict.parse(data.read())
print(22)

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
          'load_index', 'thorn', 'price_spb_rozn', 'rest_spb', 'width', 'diameter',  'height', 'runflat',
          'price_krd_rozn', 'price_nvt', '@internal-id', 'price_krd', 'rest_nvt', 'rest_krd',
          'rest_rnd', 'price_rnd_rozn', 'price_nvt_rozn', 'rest_msk', 'price_msk', 'price_msk_rozn']
with open(CSV_PATH + 'asia-tyres.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()
    csv_writer.writerows(xml['data']['tires'])