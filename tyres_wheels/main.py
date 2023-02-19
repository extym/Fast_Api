import datetime
import sys

import requests
import json
from cred import address, Token, contract
num = 1
page = 'page' + str(num)
vendor = 0

#for production only
requests.packages.urllib3.disable_warnings()

# link = address + page + contract + 'token=' + Token + '&vendor=' + str(vendor)# + '&category=3'
# category =5
# # get start page & pages
# resp = requests.get(link, verify=False)
# txt = resp.text
# main_data = json.loads(txt)
# pages = int(main_data['pages'])  #get how many pages
# all_data = main_data['offers']   # get data offers

def get_pages():
    link = address + page + contract + 'token=' + Token + '&vendor=' + str(vendor)# + '&category=3'
    resp = requests.get(link, verify=False)
    main_data = resp.json()
    pages = int(main_data['pages'])  #get how many pages
    return pages


#for future name image
time_e = datetime.datetime.now().timestamp()
name_img = str(round(time_e, 2)).replace('.', '-')

count = 0
# Получаем все данные по page
def get_wheels():
    pages = get_pages()
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

        # print(datetime.datetime.now(), '--', i, '--', len(page_data), '--', len(data_product), '--',  len(proxy))
    print(datetime.datetime.now(), '--', i, '--', len(page_data), '--', len(data_product), '--', len(proxy))
    print(datetime.datetime.now(), 'data_product2 - ', len(data_product))

    mems = sys.getsizeof(data_product)
    print(mems / 1000, 'Kb')

    with open("data_product.json", "w") as write_file:
        json.dump(data_product, write_file) # encode dict into JSON
    resp.close()
    #return data_product


#print('get_whells[0]', type(get_wheels()[0]))



get_wheels()

