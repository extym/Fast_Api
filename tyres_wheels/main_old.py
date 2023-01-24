import datetime
import requests
import json
from cred import address, Token, contract
num = 1
page = 'page' + str(num)
vendor = 0

#for production only
requests.packages.urllib3.disable_warnings()

link = address + page + contract + 'token=' + Token + '&vendor=' + str(vendor)# + '&category=3'
category = 0
# get start page & pages
resp = requests.get(link, verify=False)
txt = resp.text
main_data = json.loads(txt)
pages = int(main_data['pages'])  #get how many pages
##previous
#after_t = txt[974:-15].split('},\n        {')
#all_data = [json.loads('{' + after_t[i] + '}') for i in range(len(after_t))] -
#print(all_data[0]['name'])

# Получаем все данные по page
def get_wheels():
    data_product = []
    for i in range(pages):
        links = address + 'page'+ str(i) + contract + 'token=' + Token + '&vendor=' + str(vendor)
        resp = requests.get(links, verify=False)
        text = resp.text
        data = json.loads(text)
        page_data = data['offers']
        proxy = []
        for j in range(len(page_data)):
            if page_data[j].get('category') in [1, 4, 5, 7]:
                proxy.append(page_data[j])

        data_product.extend(proxy)

        #print(datetime.datetime.now(), '--', i, '--', len(page_data), '--', len(data_product), '--',  len(proxy))
    print('data_product2 - ', len(data_product))
    with open("data_product.json", "w") as write_file:
        json.dump(data_product, write_file) # encode dict into JSON
    resp.close()
    return data_product





