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
print(link)
resp = requests.get(link)
txt = resp.text
pages = txt[88:92]
#print(txt[950:974])
# err_after = txt[583:1078]#[983:1078]
# # number = resp.json(["pages"])

before_t = txt[:974] + "}"
main_data = json.loads(before_t)
print(main_data['pages'])
#print(txt[:1187])


#get data from response
after_t = txt[985:-13].split('},\n        {')
all_data = [json.loads('{' + after_t[i] + '}') for i in range(len(after_t))]
print(all_data[0]['name'])
print(len(all_data))
print('all_data -', type(all_data))


# Получаем все данные по page
for i in range(int(10)):
    links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
    need_data = resp.text[983: -12]
    curr_data = []
    curr_data = curr_data.append(need_data)

    with open("devvv.json", "a") as write_file:
        json.dumps(curr_data, write_file) # encode dict into JSON
        print(f'page {i}')
print(f"Done writing JSON data into .json file on {i + 1} pages")
print(need_data[:20])
print(curr_data[0][0])
#with open('devv.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
# data = [json.loads(line) for line in open('devv.json', 'r')]

tweets =[]
for line in open('devv.json', 'r'):
    l = line.replace('}"" {', ',') #[1:-1]
    our_data = json.loads(l)
    tweets.append(json.loads(l))
    print(len(our_data))
    print(type(our_data))
    #print(tweets[0:5])
    print(type(tweets[0]))
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



