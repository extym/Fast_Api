import datetime
#from connect import
import requests
from flask import Flask, request, app
import json
address = 'https://b2b.kolrad.ru/json/hannover/'
num = 1
page = 'page' + str(num)
contract = '/contract944/?'
Token = '$1$jjJ1M9JP$Bz5Epibcr9.Stn.ZCQCqN0'
vendor = 0

#Получить данные
#--------# Промежуточный файл?
# Привести их к виду на сайте
# Записать в бд

link = address + page + contract + 'token=' + Token + '&vendor=' + str(vendor)# + '&category=3'
category = 0
# get start page & pages
resp = requests.get(link)
txt = resp.text
# pages = txt[88:92]
# print('pages 1 -', pages)

before_t = txt[:974] + "}"
main_data = json.loads(before_t)
pages = int(main_data['pages'])  #get how many pages
print('pages 2 -', pages)


#get data from response - one page?
after_t = txt[985:-13].split('},\n        {')
all_data = [json.loads('{' + after_t[i] + '}') for i in range(len(after_t))]
print(all_data[0]['name'])

#for future name image
time_e = datetime.datetime.now().timestamp()
name_img = str(round(time_e, 2)).replace('.', '-')

count = 0
# Получаем все данные по page
def get_wheels():
    data_product = []
    count = 0
    for i in range(pages):
        links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
        resp = requests.get(links)
        count += 1
        text = resp.text
        # need_data = resp.text[983: -12]
        after_t = text[985:-13].split('},\n        {')
        all_data = [json.loads('{' + after_t[i] + '}') for i in range(len(after_t))] #data from one page

        data_product.extend(all_data)
        #data_product.extend(all_data)
        # with open("devvv.json", "w") as write_file:
        #     json.dump(data_product, write_file) # encode dict into JSON
        print(datetime.datetime.now(), '--', i, '--', len(all_data), '--', len(data_product), '--',  type(all_data))
    print('data_product2 - ', len(data_product))

    return data_product

#print('get_whells[0]', type(get_whell()[0]))
print('get_whells[0]', type(get_wheels()[0]))
#     print(f'page {i}')
# print(f"Done writing JSON data into .json file on {i + 1} pages")
# print(len(need_data))
# print(len(data_product))
#with open('devv.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
# data = [json.loads(line) for line in open('devv.json', 'r')]

tweets =[]
for line in open('devv.json', 'r'):
    l = line.replace('}"" {', ',') #[1:-1]
    our_data = json.loads(l)
    tweets.append(json.loads(l))

    print('our_data', type(our_data))
    #print(tweets[0:5])
    #print(type(line))
# try:
#     for line in open('devv.json', 'r'):
#         l = line[1:-1].split('""')
#         tweets.append(json.loads(line))
# except ValueError:  # includes simplejson.decoder.JSONDecodeError
#     print(f'Decoding JSON has failed - {line[:500]}')



#get data to file - work
# for i in range(int(pages)):
#     links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
#     need_data = resp.text[983: -12]
#     with open("devvv.json", "a") as write_file:
#         json.dump(need_data, write_file) # encode dict into JSON
#         #print(f'page {i}')
# print(f"Done writing JSON data into .json file on {i + 1} pages")



