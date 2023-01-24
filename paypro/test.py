import hashlib
import json
import datetime
import requests

secret_key = 'qKhfiV0YzILj25CxPPoHxGmnBRCqeT'

metod = "init_payment"
url_init = 'https://api.pay2.pro/' + metod
headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}
#parametrs
sp_order_id = '123'
sp_payment_id = ''  #response_result_url
sp_currency = 'RUB'   #'643'    #ISO 4217 ?
sp_net_amount = ''  #response_result_url
sp_lifetime = 3600
sp_user_name = 'Eagle'
sp_user_phone = '79797979797'
sp_recurring_start = 0
#sp_result_url = 'test-bt.hotra.ru'

#bold parametrs
sp_user_contact_email = 'example@localhost.com'
sp_outlet_id = 281604
sp_user_ip = '192.168.1.1'
sp_payment_system = 'CARD'
sp_amount = 1.1
sp_description = 'laptop'   #1024 chars
sp_salt  = '1234322'
listt = ['sp_outlet_id', 'sp_payment_system', 'sp_user_phone', 'sp_description', 'sp_salt', 'sp_user_contact_email',
         'sp_user_name', 'sp_result_url', 'sp_currency', 'sp_user_ip', 'sp_amount']

listt.sort()
# target_string = metod  + ';' + str(sp_amount) + ';' + sp_currency + ';' + sp_description + ';' + str(sp_outlet_id) + ';' \
#                 + sp_result_url + ';' + sp_salt + ';' + secret_key + ';' + sp_user_ip
target_string = metod  + ';' + str(sp_amount) + ';' + sp_currency + ';' + sp_description + ';' + str(sp_outlet_id) + ';' \
                + sp_payment_system + ';' + sp_salt + ';' + sp_user_contact_email + ';' + sp_user_ip + ';' \
                + sp_user_name + ';' + sp_user_phone + ';' + secret_key

sp_sig = hashlib.sha256(target_string.encode()).hexdigest()  #SHA256

all_string = {
    "sp_amount": sp_amount,
    "sp_currency": sp_currency,
    "sp_description": sp_description,
    "sp_outlet_id": sp_outlet_id,
    "sp_payment_system": sp_payment_system,
#    "sp_result_url": sp_result_url,
    "sp_salt": sp_salt,
    "sp_user_contact_email": sp_user_contact_email,
    "sp_user_ip": sp_user_ip,
    "sp_user_name": sp_user_name,
    "sp_user_phone": sp_user_phone,
    "sp_sig": sp_sig
}
data = json.dumps(all_string)

answer = requests.post(url_init, data=data, headers=headers)
response = answer.json()
print(datetime.datetime.now(), response)
f = open('log3.txt', 'a')

#8ade572c739718806fb02914c559bfb47d8751d5d0130e34a6a32a0b4d2ca3a1
print(listt)
print(target_string)
print(all_string)
print(sp_sig)