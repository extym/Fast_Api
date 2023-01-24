import hashlib
import json
import datetime

import requests

# secret_key = 'qKhfiV0YzILj25CxPPoHxGmnBRCqeT'
# metod = "init_payment"
# ll = ['RUB','511291497','https://3ds.pay2.pro/payment/vAaNegrwXjR3kaMPGjYR','payment_system','5969408526','ok']
# ss = ';'.join(ll)
# s = metod + ';' +  ss + ';' + secret_key
# signat = hashlib.sha256(s.encode()).hexdigest()
# print(signat)

headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

url = 'https://api-test.contactpay.io/gateway/v1/shop_output_config/shop'
secret_key = 'd34d8d5a618640979d4165302037e1e4'
metod = "shop_output_config/shop"
shop_id = '265'
now = '2022-11-17T15:28:02.000Z'


#ll = ['RUB','511291497','https://3ds.pay2.pro/payment/vAaNegrwXjR3kaMPGjYR','payment_system','5969408526','ok']
ss = now  + ':' + shop_id
#ss = ':'.join(ll)
s = ss + secret_key
signat = hashlib.sha256(s.encode()).hexdigest()
print(signat)
string = {
    'shop_id': '265',
    'now': '2022-11-17T15:28:02.000Z',
    "sign": signat
}
data = json.dumps(string)

answer = requests.post(url, data=data, headers=headers)
#response = answer.json()
response = answer.text
print(datetime.datetime.now(), response)
#f = open('log3.txt', 'a')

#8ade572c739718806fb02914c559bfb47d8751d5d0130e34a6a32a0b4d2ca3a1

print(s)
print(ss)
print(string)
print(response)