import json
import schedule
import time
from cred import *
import requests
import datetime
from cred import client_secret, client_id, avito_key, avito_secret
# from cred_update import creds
# from maintenance import read_gmotors_link
import urllib.parse
import hashlib
from email import utils
import hmac

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH = '/home/userbe/phone/'


proxy = [
   {
      "name": "Название сделки",
      "price": 3422,
      "_embedded":{
         "contacts": [
            {
               "first_name":"Екатерина",
               "created_at":1608905348,
               "responsible_user_id":2004184,
               "updated_by":0,
               "custom_fields_values": [
                  {
                     "field_id":66186,
                     "values":[
                        {
                           "enum_id":193200,
                           "value":"example@example.com"
                        }
                     ]
                  },
                  {
                     "field_id":66192,
                     "values":[
                        {
                           "enum_id":193226,
                           "value":"+79123456789"
                        }
                     ]
                  }
               ]
            }
         ],
         "companies":[
            {
               "name":"ООО Рога и Копыта"
            }
         ]
      },
      "created_at":1608905348,
      "responsible_user_id":2004184,
      "custom_fields_values":[
         {
            "field_id":1286573,
            "values":[
               {
                  "value":"Поле текст"
               }
            ]
         },
         {
            "field_id":1286575,
            "values":[
               {
                  "enum_id":2957741
               },
               {
                  "enum_id":2957743
               }
            ]
         }
      ],
      "status_id":33929752,
      "pipeline_id":3383152,
      "request_id": "qweasd"
   },
   {
      "name": "Название сделки",
      "price": 3422,
      "_embedded":{
         "metadata":{
            "category": "forms",
            "form_id": 123,
            "form_name": "Форма на сайте",
            "form_page": "https://example.com",
            "form_sent_at": 1608905348,
            "ip": "8.8.8.8",
            "referer": "https://example.com/form.html"
         },
         "contacts":[
            {
               "first_name":"Евгений",
               "custom_fields_values":[
                  {
                     "field_code":"EMAIL",
                     "values":[
                        {
                           "enum_code":"WORK",
                           "value":"unsorted_example@example.com"
                        }
                     ]
                  },
                  {
                     "field_code":"PHONE",
                     "values":[
                        {
                           "enum_code":"WORK",
                           "value":"+79129876543"
                        }
                     ]
                  }
               ]
            }
         ]
      },
      "status_id":33929749,
      "pipeline_id":3383152,
      "request_id": "uns_qweasd"
   }
]

# test = ('Москва', 'тест', '9251166091', 'тестовый источник', 'запорожец', '', 'Другое (записать в комментариях)', 'тест', 'тест')
#
# tt_token = {"token_type":"Bearer","expires_in":85977,
#             "access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImM3ZmVmYThiZTA4OWQ2ZTVkZjMwMWE1N2MxZTc2NDMxYTZiZjI1NTkxZTQ0ZGU4ODU2N2E3ZjU4Y2M1YmJkMDg2YTBlMjEyYTVkNTQzZWEyIn0.eyJhdWQiOiIyMWM0ZmEwYS03MzhjLTRjYjAtYThiNS03OTY4YjFjMjI4OGMiLCJqdGkiOiJjN2ZlZmE4YmUwODlkNmU1ZGYzMDFhNTdjMWU3NjQzMWE2YmYyNTU5MWU0NGRlODg1NjdhN2Y1OGNjNWJiZDA4NmEwZTIxMmE1ZDU0M2VhMiIsImlhdCI6MTY4OTUzNjg0OCwibmJmIjoxNjg5NTM2ODQ4LCJleHAiOjE2ODk2MjI4MjUsInN1YiI6IjgyMDA4MDciLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzAxNzYwOTgsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6InYxIiwic2NvcGVzIjpbInB1c2hfbm90aWZpY2F0aW9ucyIsImZpbGVzIiwiY3JtIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyJdfQ.QwynZhaW92maAaHgvxquwKpIq5PMDFD9jRCCCBYHcjYLSh_CVTmRrtsS_5i-KNpTHcCKl4YW9gkdP4YoAzPX6_Di1tOpAgZrv7EhOwwRFqDOgsjdLDeT6oHAqJ8Hv8hIksLAohDgUfRPOmoP7pGkY9q4MPVtFkarqYJ7REghNaydpXblmsoyTCXdCfG0UROnb3LTvLu-K1SYqosy7VsMIW3NwZa1osRqnE25BqVYS_vcAwHxu1E6LcYvyK5Z_WlFeAmd89e3Fc65Bg2e3tu3SiUTwtQ3cBRbHFNtkoIXJVad1iDkp_pGFwxSSn_GtWiYcfqaCk-aaYKyTrDkhu-Rag",
#             "refresh_token":"def5020010619d2c236fb05ea8dd730087098b1f8ac537868b94c6d2efff1223d0b87244810ae923b613e9b17f079d47f31a80f6f79a912032db9b43b60240dc47aa003d11fd3ee8b9009a9deaed1ca99818d62d9565e76acce112e4e00952e69b2ce3f5e779868c055eb610801d6ebe7dbf3ecdafde5b2831d076c50b461f30342342ef845283b765eb82beb95108b5336d20327a8554336553a7b223de833dee0b506441707e290404ad00b37df57567895c29dfadb029b47dd20ef605872e33b434c8149c1f114498e16e32709e6826b9557d597bc3ee426fedfc48a1b572953aa67640987b4d73936436be7360f8c633713eddad617544fa27032f3ce079132bf0262461cda9927f29960e6e051f56a81e3faf2238d40d3fd930c87d752c8e65ea723572979c83f91cd8bf9d0e302a8cb7609a157202ec40a27b5bd78ad28ce7e6da808b068e3a124d6abd1a000b35c94ed635d6d3d051fb08a6a105878cb437f2a7b9ffcec6ba47da4f12aaa11062169772d7770e44b713b511a611b6509553b3d706d3ec99a856a0a039d83bcf85f5f8134754f7f31abcb7fefe5338d7ba0d74d796aec825ea4213258e5b3d56bcdc1487dc5e526b3d5a17402086da4d2c48cf17b70d24e6ba4485159fa5725c9b3ebdf4f9b7f5e4a3cbabd7e9d6593f72a4412d86e640bb139065e025c0ee8d"}
#
# test_token = json.dumps(tt_token)
# test2 = {"token_type":"Bearer","expires_in":86400,
#               "access_token":"eyPrAGQ",
#               "refresh_token":"def50200f4a96c"}
#


def get_creds():
   with open(PATH + 'cred_update.json', 'r') as file:
      creds = json.load(file)
      fresh = creds.get('refresh_token')
      access = creds.get('access_token')
   print(creds, fresh, access)

   return creds


def test_compex_data(test_data):
   data = [  # (sity, name, phone, source, mark, first_name, call_result, comment, target)
      {
         "name": test_data[8],
         "_embedded": {
            "contacts": [
               {
                  "first_name": test_data[5],
                  'custom_fields_values': [
                     {
                        "field_id": 1277277,  # sity - now make on field address
                        "values": [
                           {
                              "value": test_data[0]
                           }
                        ]
                     },
                     {
                        "field_id": 952417,  # phone number
                        "values": [
                           {
                              "value": test_data[2]
                           }
                        ]
                     }
                  ]
               }
            ]
         },
         'pipeline_id': 5420530,
         'custom_fields_values': [
            {
               "field_id": 1253779,  # auto mark
               "values": [
                  {
                     "value": test_data[4]
                  }
               ]
            },
            {
               "field_id": 1315595,  # advertising source TODO
               "values": [
                  {
                     "value": test_data[3]
                  }
               ]
            },
            {
               "field_id": 1315601,  # call result TODO
               "values": [
                  {
                     "value": test_data[6]
                  }
               ]
            },
            {
               "field_id": 1277265,  # comment
               "values": [
                  {
                     "value": test_data[7]
                  }
               ]
            }
         ]
      }
   ]

   return data


def test_lead_complex():  #(data):
   access_token = creds.get('access_token')
   data = test_compex_data(test)
   headers = {
      'Authorization': 'Bearer ' + access_token
   }
   metod = '/api/v4/leads/complex'
   print(headers)
   link = url + metod
   print(link)
   answer = requests.post(link, headers=headers, json=data)

   print(answer.text)

   return answer.text


# test_lead_complex()
avito_token = 'fwXn3FlbRlOKuE9ZqB3nbAO8K3pxnS-i_GTURURX'
def get_avito_token():
   url = 'https://api.avito.ru/token/'
   headers = {'Content-Type': 'application/x-www-form-urlencoded'}
   data = {
      "client_id": avito_key,
      "client_secret": avito_secret,
      "grant_type": "client_credentials"  #"authorization_code"
   }
   encode_data = urllib.parse.urlencode(data)
   answer = requests.post(url=url, headers=headers, json=encode_data)
   print(answer.text)
   data = answer.json()
   print(data)

get_avito_token()

header = {'Authorization': f'Bearer {avito_token}'}

def get_avito_chats_info():
   user_id = 353207078
   url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats'
   # params = {
   #    'unread_only': True   ##for unread message only
   # }
   answer = requests.get(url=url, headers=header)
   # print(answer.text)
   raw_data = answer.json()
   print(len(raw_data['chats']), raw_data['meta'])
   print(*raw_data['chats'], sep='\n')
   
   return raw_data

# get_avito_chats_info()


def make_data_for_amo_from_avito(data):
   chats = data.get('chats')
   for chat in chats:
       chat_id = chat.get('id')
       msg_id = chat.get()
       sender = {
          'id': ''
       }


# def enable_avito_webhook():
#    data = {
#       'url': 'https://phone-call.i-bots.ru/webhook'
#    }
#    url = 'https://api.avito.ru/messenger/v3/webhook'
#    answer = requests.post(url=url, headers=header, json=data)
#    print(answer.text)


# enable_avito_webhook()



def get_amo_account_amojo_id():
   access_token = get_creds().get("access_token")
   link = 'https://amo3431ru.amocrm.ru/'
   path = '/api/v4/account?with=amojo_id'
   url = link + path
   headers = {
      'Authorization': 'Bearer ' + access_token
   }
   answer = requests.get(url, headers=headers)
   print(answer.text)

   return answer.json().get('amojo_id')






def update_creds_main_amo(answer):
   token_data = json.loads(answer)
   re_access = token_data.get('access_token')
   re_refresh = token_data.get('refresh_token')
   if re_refresh and re_access:
      f = open(PATH + 'cred_update.json', 'w')
      cred = {
         "access_token": re_access,
         "refresh_token": re_refresh
      }
      creds = json.dumps(cred)
      # print(creds)
      f.write(creds)
      f.close()
      print('Creds update successfully')
      result = True
   else:
      result = False
      print('EROOR get token data')

   return result



def refresh_access_main_amo():
   url = 'https://amo3431ru.amocrm.ru/'
   creds = get_creds()
   refresh = creds.get('refresh_token')
   file = open(PATH + 'warning.txt', 'a')
   file.write(str(datetime.datetime.now()))
   file.write('\n')
   file.write('refresh=' + refresh)
   file.write('\n')
   file.close()
   data = {
      "client_id": client_id,
      "client_secret": client_secret,
      "grant_type": "refresh_token",
      "refresh_token": refresh,
      "redirect_uri": "http://phone-call.i-bots.ru/token"
   }
   headers = {'Content-Type':'application/json'}
   # data = {
   #    "client_id": '8d3cb4e4-b414-4917-9ae4-180b99c99ae5',  #client_id,
   #    "client_secret": '1WHdXclAfVyYqeV3ZZXPSJ0cssZMkxZdFegEdqOFk08FAXcQPJYQGaJqbngs2tWI',  #client_secret,
   #    "grant_type": "authorization_code",
   #    "code": 'def5020065594703c2d2fd949acfa9c0dba8fbd1e52546d680a826d646c461a42cc9dbce204997084c20e39ceceaf051ea917ffe1b9f10d560af4666ef868b1b9cb73eacb088500ba96b6fb96d8ff09ba6a2ae4eaf47d37a3051832bd35b7bf31f2e26850dfba9fabb112324cf9846230739170cd41d96a5c9ed3a08d631f36bad823ea0a53bf983c4098f496a1a79968ce9b3b0fcbab017656b7f21cb3a54300643cdc42109c352bd8a235368a05d23397337550a553afe8a599fdf3069005df659566a22f061d00ffe7c200294bf290dad376deaef7ef3fbab8a5d4c54c20201bec94738a1f68dc5cdd07e53aa77ffe395229651b30330954caf2e7dd4e75f3385276a468d34c2c8efa2eed2cfac080c329a9c537555148f734db4306677eaa0a3edc014d91b2254127163f7a94e147e7406b12c897e34cdb28ad1f270ed7eeb9bf9157e49691e9f879aca20860dc8affbe5d30902385ef22fd25d13389c14a9d5ce2cb427701230687432cb030b7359e0d52af2163eaa4458ea0684a815c98ff95f10c63c00acb91779e737c0e27602869d90bf252819f8d5d72589b3b6e21845b9e9271906fa35260c2e4ab66d6d254e427665c32a55b72f3f4e3055e9e183e7c595c8cd5ed74e67c55e76abe4b81bc571f4ef53722b2851b6e5',  #authorization_code,
   #    "redirect_uri": "https://phone-call.i-bots.ru/token"
   # }

   metod = '/oauth2/access_token'
   link = url + metod
   answer = requests.post(link, headers=headers, json=data)
   result = update_creds_main_amo(answer.text)
   # print(answer.text)
   if result:
      print('ALL RIDE')

   else:
      print('ERROR_UPDATE', answer.text)






