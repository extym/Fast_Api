import requests
from flask import Flask, request, app
import json
address = 'https://b2b.kolrad.ru/json/hannover/'
num = 1
page = 'page' + str(num)
contract = '/contract68/?'
Token = '$1$jjJ1M9JP$Bz5Epibcr9.Stn.ZCQCqN0'
vendor = 0

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

# for i in range(len(after_t)):
#     data = '{' + after_t[i] + '}'
#     also_data = json.loads(data)
# #
# print('also_data -', type(also_data))
# print(also_data)
# print('data -', type(data))
# print(data)


for i in range(int(10)):
    links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
    need_data = resp.text[983: -12]
    curr_data = []
    curr_data = curr_data.append(need_data)
    with open("devvv.json", "a") as write_file:
        json.dump(curr_data, write_file) # encode dict into JSON
        #print(f'page {i}')
print(f"Done writing JSON data into .json file on {i + 1} pages")


# print('! - ', txt[974:982])
# print('!! - ', txt[942:954])
#

#with open('devv.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
# data = [json.loads(line) for line in open('devv.json', 'r')]

tweets =[]
# for line in open('devv.json', 'r'):
#     tweets.append(json.loads(line))
try:
    for line in open('devv.json', 'r'):
        l = line[1:-1].split('""')
        tweets.append(json.loads(line))
except ValueError:  # includes simplejson.decoder.JSONDecodeError
    print(f'Decoding JSON has failed - {line[:500]}')



#get data to file - work
# for i in range(int(pages)):
#     links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
#     need_data = resp.text[983: -12]
#     with open("devvv.json", "a") as write_file:
#         json.dump(need_data, write_file) # encode dict into JSON
#         #print(f'page {i}')
# print(f"Done writing JSON data into .json file on {i + 1} pages")


# from requests.exceptions import HTTPError
#
# try:
#     # response = requests.get('https://httpbin.org/get')
#     resp.raise_for_status()
#
#     jsonResponse = resp.json()
#     print("Entire JSON response")
#     print(jsonResponse)
#
# except HTTPError as http_err:
#     print(f'HTTP error occurred: {http_err}')
# except Exception as err:
#     print(f'Other error occurred: {err}')


