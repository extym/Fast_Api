import datetime
import requests
import json
#from cred import address, Token, contract


# GET http://vendor.shinservice.ru/regular/stock/tires.json
# GET http://vendor.shinservice.ru/regular/stock/wheels.json
# Authorization: Bearer API-ключ
# Content-Type: application/json

link = 'http://vendor.shinservice.ru/regular/stock/tires.json'
headers = {'Content-type': 'application/json', 'Authorization': 'Bearer 50264bcbecdc0356b4446bcdbeefe884'}
autority = {}
resp = requests.get(link,  headers=headers)
txt = resp.text

data_all = json.loads(txt)
data = data_all['items']
print(type(data), len(data))
time_e = datetime.datetime.now().timestamp()
#print(type(txt), len(txt), txt)
# count = 0
# # Получаем все данные по page
# def get_wheels():
#     data_product = []
#     count = 0
#     for i in range(pages):
#         links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
#         resp = requests.get(links)
#         count += 1
#         text = resp.text
#         # need_data = resp.text[983: -12]
#         after_t = text[985:-13].split('},\n        {')
#         all_data = [json.loads('{' + after_t[i] + '}') for i in range(len(after_t))] #data from one page
#
#         data_product.extend(all_data)
#
#         print(datetime.datetime.now(), '--', i, '--', len(all_data), '--', len(data_product), '--',  type(all_data))
#     print('data_product2 - ', len(data_product))
#     with open("data_product.json", "w") as write_file:
#         json.dump(data_product, write_file) # encode dict into JSON
#     resp.close()
#     return data_product
#

#print('get_whells[0]', type(get_wheels()[0]))


# tweets =[]
# for line in open('data_product.json', 'r'):
#     l = line.replace('}"" {', ',') #[1:-1]
#     our_data = json.loads(l)
#     tweets.append(json.loads(l))
#
#     print('our_data', type(our_data), len(our_data))
#     print("tweets -", type(tweets), len(tweets))
    #print(type(line))





