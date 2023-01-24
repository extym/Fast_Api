secret_key = 'd34d8d5a618640979d4165302037e1e4'
import hashlib

time_data = "2022-11-21T15:39:20"
request_body_json = '''
{"status": "success", "payment_id": 32672917, "shop_order_id": "190", "shop_id": 265, "ps_data": {\"ps_payer_account\": \"490699XXXXXX9975\", \"required_3ds\": true}, "ps_currency": 643, "payway": "card_core_payin_rub[mock_server,success_with_callback]", "description": "order \u2116190", "created": "2022-11-21T16:11:58", "updated": "2022-11-21T16:13:49", "processed": "2022-11-21T16:13:49", "shop_currency": 643, "shop_amount": 6.0, "shop_refund": 5.7, "client_price": 6.0, "error_code": 0, "addons": {\"callback_url\": \"https://promobot.ml/contact_callback\", \"client_ip\": \"91.185.78.16\", \"description\": \"order \u2116190\", \"failed_url\": \"https://promobot.ml/index.php?route=extension/payment/contact/fail\", \"hold_required\": false, \"success_url\": \"https://promobot.ml/index.php?route=extension/payment/contact/success\"}}
'''


#"{"callback_rejected_url": "https://some-shop.com/callback-rejected-url", "callback_url": "https://some-shop.com/callback-url", "description": "Some payment", "failed_url": "https://some-shop.com/fail", "phone": "79111111111", "success_url": "https://some-shop.com/success"}",



import json
parsed_request =  json.loads(request_body_json)

keys = sorted(parsed_request)

print(keys)

values_to_sign = []
for k in keys:
    kk = dict
    if  parsed_request[k] != '' and parsed_request[k] is not None:
        values_to_sign.append(str(parsed_request[k]))



sig = "d663c7ae0e7a03f8b7409389399e29b79ba5e6e77caef90ba18a5beb3986dce1"
print('from payment system', sig)

# Формируем финальную подпись и проверяем ее значение со значением, полученным в ответе
string_to_sign = ':'.join(values_to_sign) + secret_key

new_string = string_to_sign.replace("'", '"')
kkk = new_string.replace('True', 'true')
k = kkk.replace('False', 'false')

sign = hashlib.sha256(k.encode()).hexdigest()
print('from manual code', sign)
print(new_string)
tt = '{"callback_url": "https://promobot.ml/contact_callback", "client_ip": "91.185.78.16", "description": "order №190", "failed_url": "https://promobot.ml/index.php?route=extension/payment/contact/fail", "hold_required": false, "success_url": "https://promobot.ml/index.php?route=extension/payment/contact/success"}:6.0:2022-11-21T16:11:58:order №190:0:32672917:card_core_payin_rub[mock_server,success_with_callback]:2022-11-21T16:13:49:643:{"ps_payer_account": "490699XXXXXX9975", "required_3ds": true}:6.0:643:265:190:5.7:success:2022-11-21T16:13:49' + secret_key
#assert sign == parsed_request['sign']
print(tt)
print( k == tt)
signn = hashlib.sha256(tt.encode()).hexdigest()
print('from support strint', signn)