import requests
from creds import basic_auth, link
import pandas as pd


headers = {'Content-Type': 'application/json', 'Authorization': 'Basic '+ basic_auth}

def make_product_to_site():
    data = ''

    metod = '/admin/products.json'
    url = link + metod
    answer = requests.post(url=url, headers=headers, data=data)


def make_bundle_to_site():
    '''{
  "product": {                                     #required
    "category_id": 1,                              #required
    "title": "Van Gogh Ruled Peach Notebook",
    "bundle": true,                                #required
    "variants_attributes": [                       #required
      {
        "price": 100
      }
    ],
    "product_bundle_components_attributes": [      #required
      {
        "variant_id": 1,
        "quantity": 2,
        "free": false
      }
    ]
  }
}'''
    data = ''

    metod = '/admin/products.json'
    url = link + metod
    answer = requests.post(url=url, headers=headers, data=data)



import csv
def read_xls(file, vendor_name):
    f = pd.read_excel(file)
    dataframe = pd.DataFrame(f).values
    proxy = list()
    for row in dataframe:
        try:
            # print(row)
            # site_id = str(row[0]).split(' / ')[1].split(': ')[2]
            # parent_id = str(row[0]).split(' / ')[1].split(': ')[3]
            key = str(row[0]).split(' / ')[1].split(': ')[1]
            proxy.update((vendor_name, int(key), row[1], int(row[2])))
        except Exception as error:
            print(111111111, row, ' fuck_up- {}'.format(error))
            continue

    print(row)
    print(proxy.get('292'))
    return proxy

# read_xls('3Logic.xlsx', 'logic')


# def write_csv(file):
#     with open(file, 'rb', encoding='windows-1251') as f:
#         reader = csv.DictReader(f)
#         proxy = []
#         for row in reader:
#             proxy.append(row)
#             print(row)
#

# write_csv('3Logic_1.xlsx')