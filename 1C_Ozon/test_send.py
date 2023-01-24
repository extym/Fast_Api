import requests
import json
import datetime

data = '''
    {
    "order":
        {
     "shop": "Yandex",
     "businessId": 3675591,
     "id": "12345",
     "paymentType": "PREPAID",
     "itemsTotal": 5650,
     "delivery": false,
     "items": [{
     "sku": "150714598463"}, {
     "sku": "150714598789"
            }]
        }
    }
'''
json_data = json.loads(data)
def send_resp():
    r = requests.post('http://192.168.88.253:8800/post', data=data)
    print(datetime.datetime.now(), r)

send_resp()