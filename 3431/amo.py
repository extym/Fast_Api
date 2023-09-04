import json
import schedule
import time
from cred import *
import requests
import datetime
import urllib.parse
import hashlib
from email import utils
import hmac

amo_connnect_answer = {"account_id":"d2914d60-a44a-4625-881b-d9e237592dce",
                       "scope_id":"8bf871d6-fc08-49e0-aac7-d5241c3542ea_d2914d60-a44a-4625-881b-d9e237592dce",
                       "title":"ChatIntegration","hook_api_version":"v2","is_time_window_disabled":false}

channel_key = 'c77c73cb95dae182f221fc8786866875c968a2c2'
scope_id = "8bf871d6-fc08-49e0-aac7-d5241c3542ea_d2914d60-a44a-4625-881b-d9e237592dce"

def send_to_amo_message(message, path):
    metod = 'POST'
    link = 'http://amojo.amocrm.ru'
    url = link + path
    content_type = 'application/json'
    data = json.dumps(message)
    data_hash = hashlib.m5(data.encode('utf-8')).hexdigest()
    date_now = get_rfc_2822()
    target_string = '\n'.join([metod.upper(), str(data_hash), content_type, date_now, path])
    signatura = hmac.new(channel_key.encode('utf-8'), target_string.encode('utf-8'), hashlib.sha1).hexdigest()
    headers = {
    "Date": date_now,
    "Content-Type": content_type,
    "Content-MD5": str(data_hash),
    "X-Signature": signatura
    }
    answer = requests.post(url, headers=headers, data=data)
    print(answer.text, str(signatura))

    return answer.text


def timestamp():
   tn = datetime.datetime.now()
   ts = int(tn.timestamp())
   t = int(tn.timestamp() * 1000)

   return ts, t


def make_message_for_amo(data):
   '''
   {
      "event_type": "new_message",
      "payload": {
            "timestamp": 1639660529,
            "msec_timestamp": 1639660529379,
            "msgid": "my_int-5f2836a8ca481",
            "conversation_id": "my_int-d5a421f7f218",
            "sender": {
                  "id": "my_int-1376265f-86df-4c49-a0c3-a4816df41af8",
                  "avatar": "https://images.pexels.com/photos/10050979/pexels-photo-10050979.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500",
                  "profile": {
                    "phone": "+79151112233",
                    "email": "example.client@example.com"
                  },
                  "profile_link": "https://example.com/profile/example.client",
                  "name": "Вася клиент"
            },
            "message": {
                  "type": "text",
                  "text": "Сообщение от клиента"
            },
            "silent": false
      }
   }
   :param data:
   :return:
   '''
   ts, t = timestamp()
   result = {
      "event_type": "new_message",
      "payload": {
         "timestamp": ts,
         "msec_timestamp": t,
         "msgid": data.get('payload').get("value").get('id'),
         "conversation_id": data.get('payload').get("value").get('chat_id'),
         "sender": {
            "id": data.get('payload').get("value").get('author_id'),
            "avatar": avatar,
            "profile": {
               "phone": '',
               "email": ''
            },
            "profile_link": profile_link,
            "name": name_user
         },
         "message": {
            "type": data.get('payload').get("value").get('type'),
            "text": data.get('payload').get("value").get('content').get('text'),
         },
         "silent": false
      }
   }

   return result



def get_rfc_2822():
   nowdt = utils.format_datetime(datetime.datetime.now())

   return nowdt



def connect_channel_with_account_amo():
   channel_id = '8bf871d6-fc08-49e0-aac7-d5241c3542ea'
   amojo_id = "d2914d60-a44a-4625-881b-d9e237592dce"
   data = {
   "account_id": amojo_id,
   "title": "ChatIntegration",
   "hook_api_version": "v2"
   }
   answer = send_to_amo_message(data, f'/v2/origin/custom/{channel_id}/connect')

   # print(answer)


connect_channel_with_account_amo()