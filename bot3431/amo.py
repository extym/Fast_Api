import asyncio
import json
import logging
import os
import schedule
import time
from cred import *
import requests
import datetime
import urllib.parse
import hashlib
from email import utils
import hmac
import logging
import os
import re

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH_DIR = './'
    LOG_DIR = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH_DIR = '/home/userbe/phone/'
    LOG_DIR = 'home/userbe/phone/logs/'

user_link = {
    # user_id: (link, name_tag, responsible_user_id, pipeline_id, field_url_id, field_promo_id amo_cred_id)
    357922774: ("https://amo3431ru.amocrm.ru", "3431 грузовые", 9983934, 7155526, 987785, 987783, '3431'),
    353207078: ("https://amo3431ru.amocrm.ru", "3431 новые запчасти", 9983934, 7155526, 987785, 987783, '3431'),
    353821742: ("https://amo3431ru.amocrm.ru", "3431ru", 9983934, 7155526, 987785, 987783, '3431'),
    363810872: ("https://amo3431ru.amocrm.ru", "JP AKB", 9983934, 7155526, 987785, 987783, '3431'),
    10138154: ("https://zakazjpexpressru.amocrm.ru", "JPexpress", 0, 5420530, 1335423, 1335421, 'JPexp'),
    369221904: ('https://zakazjpexpressru.amocrm.ru', 'Быстрые шины', 0, 5420530, 1335423, 1335421, 'JPexp'),
    369222251: ('https://zakazjpexpressru.amocrm.ru', 'Быстрый двигатель', 0, 5420530, 1335423, 1335421, 'JPexp'),
    369220948: ('https://zakazjpexpressru.amocrm.ru', 'Классный салон', 0, 5420530, 1335423, 1335421, 'JPexp'),
    369223108: ('https://zakazjpexpressru.amocrm.ru', 'Быстрая машина', 0, 5420530, 1335423, 1335421, 'JPexp'),
    369222788: ('https://zakazjpexpressru.amocrm.ru', 'Быстрая коробка', 0, 5420530, 1335423, 1335421, 'JPexp'),
    369721092: ('https://zakazjpexpressru.amocrm.ru', 'Быстрые мелочи', 0, 5420530, 1335423, 1335421, 'JPexp')
}
# 363810872: ("https://zakazjpexpressru.amocrm.ru", "JPexpress", 9983934, 7155526)
# 357922774 = "3431 грузовые"
# 353207078 = "3431 новые запчасти"
# 353821742 = "3431ru"
# 363810872 = "JP AKB"


logging.basicConfig(filename=os.path.join(LOG_DIR + 'webhook.log'), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


def get_rfc_2822():
    nowdt = utils.format_datetime(datetime.datetime.now())

    return nowdt


# amo_connnect_answer = {"account_id":"d2914d60-a44a-4625-881b-d9e237592dce",
#                        "scope_id":"8bf871d6-fc08-49e0-aac7-d5241c3542ea_d2914d60-a44a-4625-881b-d9e237592dce",
#                        "title":"ChatIntegration","hook_api_version":"v2","is_time_window_disabled":false}
#
channel_key = 'c77c73cb95dae182f221fc8786866875c968a2c2'


# scope_id = "8bf871d6-fc08-49e0-aac7-d5241c3542ea_d2914d60-a44a-4625-881b-d9e237592dce"


#
#  POST https://amojo.amocrm.ru/v2/origin/custom/8bf871d6-fc08-49e0-aac7-d5241c3542ea_d2914d60-a44a-4625-881b-d9e237592dce
# Date: Fri, 08 Sep 2023 16:36:19 +0200
# Content-Type: application/json
# Content-MD5: a5e8ae04332a6d0aac15f01ad05d40e3
# X-Signature: 0b7eb4f0a5be5111a074e68476042c1ad127ffe6
# def json_default(thing):
#     try:
#         return dataclasses.asdict(thing)
#     except TypeError:
#         pass
#     if isinstance(thing, datetime.datetime):
#         return thing.isoformat(timespec='microseconds')
#     raise TypeError(f"object of type {type(thing).__name__} not serializable")
#
#
# def json_dumps(thing):
#     return json.dumps(
#         thing,
#         default=json_default,
#         ensure_ascii=False,
#         sort_keys=True,
#         indent=None,
#         separators=(',', ':'),
#     )
#
#
# def get_hash(thing):
#     return hashlib.md5(json_dumps(thing).encode('utf-8')).digest()
#


def read_link(chat_id):
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)


async def read_link_v2(chat_id):
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)


def read_links_v2():
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links


async def read_links_v3():
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links


async def get_creds_v3(user_id):
    token_name = user_link[user_id][-1]
    with open(PATH_DIR + f'cred_update_{token_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


async def rewrite_contact(chat_id, user_id, phone_numbers):
    need_data = await read_link_v2(chat_id)
    logging.info('CONTACT_ID {} {} {} {} '
                 .format(chat_id, user_id, phone_numbers, need_data))
    contact_id = 0
    if need_data:
        contact_id = need_data[8]
    creds = await get_creds_v3(user_id)
    access_token = creds.get('access_token')

    data = {
        "custom_fields_values": [
            {
                "field_code": "PHONE",  # IS this need?
                "values": [
                    {
                        "value": phone_numbers[0],
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }

    if contact_id:
        path = f'/api/v4/contacts/{contact_id}'
        link = user_link.get(user_id)[0]
        url = link + path
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        logging.info('TRY_write_contact_id {} {} {} {} {}'
                     .format(contact_id, user_id, chat_id, data, url))
        answer = requests.patch(url, json=data, headers=headers)
        print(answer.text)
        if answer.ok:
            logging.info('ALL_RIDE_re_write_contact_id {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))

        else:
            logging.info('fuck_up_rewrite_2_contact_id {}, answer_status_code- {} answer.text {} {} {} {} {}'.
                         format(contact_id, answer.status_code, answer.text, user_id, chat_id, data, url))
    else:
        logging.info('Contact is not found in Amo {} {} {}'
                     .format(chat_id, user_id, phone_numbers))




async def rewrite_contact_v2(chat_id=0, contact_id=0, user_id=0, amo_name='', link=None, data=None):
    need_data = ''
    if chat_id:
        need_data = await read_link_v2(chat_id)
        logging.info('CONTACT_ID {} {} {} {} '
                 .format(chat_id, user_id, need_data, data))
    if need_data and contact_id == 0:
        contact_id = need_data[8]
    access_token = ''
    if user_id:
        creds = await get_creds_v3(user_id)
        access_token = creds.get('access_token')
        link = user_link.get(user_id)[0]
    elif amo_name:
        access_token = get_creds(amo_name).get("access_token")

    if contact_id and access_token:
        path = f'/api/v4/contacts/{contact_id}'
        url = link + path
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        answer = requests.patch(url, json=data, headers=headers)
        if answer.ok:
            logging.info('ALL_RIDE_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))
            # print('ALL_RIDE_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
            #              format(contact_id, answer.status_code, user_id, chat_id, data, url))

        else:
            logging.info('fuck_up_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))
            # print('fuck_up_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
            #              format(contact_id, answer.status_code, user_id, chat_id, data, url))
    else:
        logging.info('Contact is not found in Amo {} {} {}'
                     .format(chat_id, user_id, data))


async def re_write_link_v3(chat_id, leads_id, contact_id):
    links = await read_links_v3()
    with open(PATH_DIR + f'links.json', 'w') as file:
        proxy = links.get(chat_id)
        #############
        # {chat_id: (
        # price,
        # target_link,
        # msg_id,
        # user_id,
        # title,
        # first_answer,
        # rewrite_leads,
        # leads_id,
        # contact_id)} [8]
        links.update(
            {
                chat_id: (
                    proxy[0],
                    proxy[1],
                    proxy[2],
                    proxy[3],
                    proxy[4],
                    proxy[5],
                    True,
                    leads_id,
                    contact_id
                )
            }
        )
        logging.info('!!!!!!!!!!!!_re_write_link_for_contact_id {} {} {}'
                     .format(chat_id, leads_id, contact_id))
        json.dump(links, file)


def get_creds(amo_name):
    with open(PATH_DIR + f'cred_update_{amo_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


def get_creds_v2(user_id: int):
    token_name = user_link.get(user_id)[-1]
    with open(PATH_DIR + f'cred_update_{token_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


def get_amo_akk(user_id):
    logging.info('GET_USER_AKK_AMO {}'.format(user_id))
    with open(PATH_DIR + 'amo_akk.json', 'r') as file:
        data = json.load(file)
        return data.get(user_link.get(user_id)[-1])


def get_amo_akk_v2(amo_name):
    logging.info('GET_USER_AKK_AMO {}'.format(amo_name))
    with open(PATH_DIR + 'amo_akk.json', 'r') as file:
        data = json.load(file)
        return data.get(amo_name)


async def get_amo_akk_v3(user_id):
    with open(PATH_DIR + 'amo_akk.json', 'r') as file:
        data = json.load(file)
        return data.get(user_link.get(user_id)[-1])


async def send_to_amo_message(message, path):
    try:
        metod = 'POST'
        link = 'http://amojo.amocrm.ru'
        url = link + path
        content_type = 'application/json'
        data = json.dumps(message, sort_keys=False).encode()
        data_hash = hashlib.md5(data).hexdigest()
        date_now = get_rfc_2822()
        target_string = "\n".join([metod.upper(), data_hash, content_type, date_now, path])
        signatura = hmac.new(channel_key.encode(), target_string.encode(), hashlib.sha1).digest()
        headers = {
            "Date": date_now,
            "Content-Type": content_type,
            "Content-MD5": data_hash,
            "X-Signature": signatura.hex().lower()
        }
        answer = requests.post(url, headers=headers, data=data)
        if answer.ok:
            logging.info('ALL_RIDE_SEND_TO_AMO {} {} {}'.format(answer.text, message, url))
        else:
            logging.error('ERROR_SEND_TO_AMO {} {} {}'.format(answer.text, message, url))
        # print('SEND_TO_AMO', answer.text)
        result = True

    except:
        logging.info('SOMETHING_WRONG_WITH_SEND_TO_AMO ' + str(path))
        print("SOMETHING_WRONG_WITH_SEND_TO_AMO", path)
        result = False

    # return result


def send_to_amo_message_v2(message, path):
    try:
        metod = 'POST'
        link = 'http://amojo.amocrm.ru'
        url = link + path
        content_type = 'application/json'
        data = json.dumps(message, sort_keys=False).encode()
        data_hash = hashlib.md5(data).hexdigest()
        date_now = get_rfc_2822()
        target_string = "\n".join([metod.upper(), data_hash, content_type, date_now, path])
        signatura = hmac.new(channel_key.encode(), target_string.encode(), hashlib.sha1).digest()
        headers = {
            "Date": date_now,
            "Content-Type": content_type,
            "Content-MD5": data_hash,
            "X-Signature": signatura.hex().lower()
        }
        answer = requests.post(url, headers=headers, data=data)
        if answer.ok:
            logging.info('ALL_RIDE_SEND_TO_AMO_2 {} {} {}'.format(answer.text, message, url))
        else:
            logging.error('ERROR_SEND_TO_AMO_2 {} {} {}'.format(answer.text, message, url))
        # print('SEND_TO_AMO', answer.text)
        result = True

    except:
        logging.info('SOMETHING_WRONG_WITH_SEND_TO_AMO ' + str(path))
        print("SOMETHING_WRONG_WITH_SEND_TO_AMO", path)
        result = False

    return result


def timestamp():
    tn = datetime.datetime.now()
    ts = int(tn.timestamp())
    t = int(tn.timestamp() * 1000)

    return ts, t


# asyncio.run(send_to_amo_message(test, f'/v2/origin/custom/{scope_id}'))

def timestamp_2():
    tn = datetime.datetime.now()
    ts = int(tn.timestamp())
    tms = int(tn.timestamp() * 1000)

    return ts, tms


# GET_DATA_FROM_AVITO_CHAT = {'result': {'status': False, 'message': 'access token expired'}}

async def make_message_for_amo(hook_data, chat_data, sender_id):
    tst = timestamp()
    try:
        avatar = chat_data.get("users")[0].get('public_user_profile').get("avatar").get("default")
    except:
        avatar = ''
        print('trouble avatar', chat_data)

    try:
        re_avatar = chat_data.get("users")[1].get('public_user_profile').get("avatar").get("default")
    except:
        re_avatar = ''
        print('trouble re_avatar', chat_data)

    try:
        name = chat_data.get("users")[0].get("name")
    except:
        name = ''

    try:
        profile_link = chat_data.get("users")[0].get("public_user_profile").get("url")
    except:
        profile_link = ''
        print('trouble_profile_link', chat_data)

    try:
        re_profile_link = chat_data.get("users")[1].get("public_user_profile").get("url")
    except:
        re_profile_link = ''
        print('trouble_profile_link', chat_data)

    try:
        receiver = chat_data.get("users")[0].get('id')
        if receiver == sender_id:
            receiver = chat_data.get("users")[1].get('id')
    except:
        receiver = ''
        print('trouble avatar', chat_data)

    message_type = hook_data.get('payload').get("value").get('type')

    if message_type == "text":
        message = hook_data.get('payload').get("value").get('content').get('text')
    elif message_type == "image":
        message_type = 'text'
        message = hook_data.get('payload').get("value").get('content'). \
            get('image').get('sizes').get('1280x960')
    elif message_type is None:
        message_type = 'text'
        try:
            message = hook_data.get('payload').get("value").get('text')
        except:
            message = 'UNKNOW_CONTENT'
    else:
        message = f'UNKNOW_CONTENT_FOUND_{message_type}'
        message_type = 'text'

    try:
        if sender_id not in sender_ids:
            message = {
                "event_type": "new_message",
                "payload": {
                    "timestamp": tst[0],
                    "msec_timestamp": tst[1],
                    "msgid": hook_data.get('payload').get("value").get('id'),
                    "conversation_id": hook_data.get('payload').get("value").get('chat_id'),
                    "sender": {
                        "id": str(sender_id),  # str(data.get('payload').get("value").get('author_id')),
                        "avatar": avatar,
                        "profile": {
                            "phone": '',
                            "email": ''
                        },
                        "profile_link": profile_link,
                        "name": name
                    },
                    "message": {
                        "type": message_type,
                        "text": str(message)
                    },
                    "silent": True  # False
                }
            }
        else:
            message = {
                "event_type": "new_message",
                "payload": {
                    "timestamp": tst[0],
                    "msec_timestamp": tst[1],
                    "msgid": hook_data.get('payload').get("value").get('id'),
                    "conversation_id": hook_data.get('payload').get("value").get('chat_id'),
                    "sender": {
                        "id": str(sender_id),  # '353207078',  # str(data.get('payload').get("value").get('author_id')),
                        "avatar": re_avatar,
                        "profile": {
                            "phone": '',
                            "email": ''
                        },
                        "profile_link": profile_link,
                        "name": name
                    },
                    "receiver": {
                        "id": str(receiver),  # str(data.get('payload').get("value").get('author_id')),
                        "avatar": avatar,
                        "name": name,
                        "profile": {
                            "phone": "",
                            "email": ""
                        },
                        "profile_link": re_profile_link
                    },
                    "message": {
                        "type": message_type,
                        "text": str(message),
                    },
                    "silent": True
                }
            }

        user_id = hook_data.get('payload').get("value").get('user_id')
        scope_id = get_amo_akk(user_id).get('scope_id')
        await send_to_amo_message(message, f'/v2/origin/custom/{scope_id}')
        logging.info('We_make_message_for_amo_1 {} {}'.format(user_id, send_message))
    except:
        print('FUCKUP_make_message_for_amo_1')


# print(2451341, get_amo_akk(369222788))


async def make_message_for_amo_v2(hook_data, chat_data, sender_id, silent):
    tst = timestamp()
    try:
        avatar = chat_data.get("users")[0].get('public_user_profile').get("avatar").get("default")
    except:
        avatar = ''
        print('trouble avatar', chat_data)

    try:
        re_avatar = chat_data.get("users")[1].get('public_user_profile').get("avatar").get("default")
    except:
        re_avatar = ''
        print('trouble re_avatar', chat_data)

    try:
        name = chat_data.get("users")[0].get("name")
    except:
        name = ''

    try:
        profile_link = chat_data.get("users")[0].get("public_user_profile").get("url")
    except:
        profile_link = ''
        print('trouble_profile_link', chat_data)

    try:
        re_profile_link = chat_data.get("users")[1].get("public_user_profile").get("url")
    except:
        re_profile_link = ''
        print('trouble_profile_link', chat_data)

    try:
        receiver = chat_data.get("users")[0].get('id')
        if receiver == sender_id:
            receiver = chat_data.get("users")[1].get('id')
    except:
        receiver = ''
        print('trouble avatar', chat_data)

    message_type = hook_data.get('payload').get("value").get('type')
    if message_type == "text":
        message = hook_data.get('payload').get("value").get('content').get('text')
    elif message_type == "image":
        message_type = 'text'
        message = hook_data.get('payload').get("value").get('content'). \
            get('image').get('sizes').get('1280x960')
    elif message_type == "link":
        message = hook_data.get('payload').get("value").get('content').get('link')
        message_type = 'text'
    elif message_type is None:
        message_type = 'text'
        try:
            message = hook_data.get('payload').get("value").get('text')
        except:
            message = 'UNKNOW_CONTENT'
    elif message_type == "system":
        message = 'Системное сообщение Avito'
        message_type = 'text'
    else:
        message = f'UNKNOW_CONTENT_FOUND_2 {message_type}'
        message_type = 'text'

    user_id = hook_data.get('payload').get("value").get('user_id')
    try:
        if int(sender_id) not in sender_ids:
            send_message = {
                "event_type": "new_message",
                "payload": {
                    "timestamp": tst[0],
                    "msec_timestamp": tst[1],
                    "msgid": hook_data.get('payload').get("value").get('id'),
                    "conversation_id": hook_data.get('payload').get("value").get('chat_id'),
                    "sender": {
                        "id": str(sender_id),
                        "avatar": avatar,
                        "profile": {
                            "phone": '',
                            "email": ''
                        },
                        "profile_link": profile_link,
                        "name": name
                    },
                    "message": {
                        "type": message_type,
                        "text": str(message)
                    },
                    "silent": silent  # False
                }
            }
        else:
            if silent is False:
                message = 'Мы уже запросили имя, номер телефона, артикул / вин.'
                message_type = 'text'
            send_message = {
                "event_type": "new_message",
                "payload": {
                    "timestamp": tst[0],
                    "msec_timestamp": tst[1],
                    "msgid": hook_data.get('payload').get("value").get('id'),
                    "conversation_id": hook_data.get('payload').get("value").get('chat_id'),
                    "sender": {
                        "id": str(sender_id),
                        "avatar": re_avatar,
                        "profile": {
                            "phone": '',
                            "email": ''
                        },
                        "profile_link": profile_link,
                        "name": name
                    },
                    "receiver": {
                        "id": str(receiver),
                        "avatar": avatar,
                        "name": name,
                        "profile": {
                            "phone": "",
                            "email": ""
                        },
                        "profile_link": re_profile_link
                    },
                    "message": {
                        "type": message_type,
                        "text": str(message),
                    },
                    "silent": True
                }
            }

        # user_id = hook_data.get('payload').get("value").get('user_id')
        # scope_id = get_amo_akk(user_id).get('scope_id')
        scope_data = await get_amo_akk_v3(user_id)
        scope_id = scope_data.get('scope_id')
        await send_to_amo_message(send_message, f'/v2/origin/custom/{scope_id}')
        logging.info('We_make_message_for_amo_2 {} {}'.format(user_id, send_message))
    except:
        print('FUCKUP_make_message_for_amo_2')

    is_phone = await get_phone(message)

    if len(is_phone) > 0:
        chat_id = hook_data.get('payload').get("value").get('chat_id')
        logging.info('We_send_re_write_contact {} {} {} {} '
                     .format(user_id, message, chat_id, is_phone))

        await rewrite_contact(chat_id, user_id, is_phone)


def get_amo_account_amojo_id():
    name = 'JPexp'
    access_token = get_creds(name).get("access_token")
    link = 'https://zakazjpexpressru.amocrm.ru'
    # link = 'https://amo3431ru.amocrm.ru/'
    path = '/api/v4/account?with=amojo_id'
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    answer = requests.get(url, headers=headers)
    print(45, answer.text)

    return answer.json().get('amojo_id')


def get_amo_account_users():
    access_token = get_creds(user_id).get("access_token")
    # link = 'https://amo3431ru.amocrm.ru'
    path = '/api/v4/users'
    url = link + path
    params = {
        'with': 'role',
        'page': 1,
        'limit': 50
    }
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    answer = requests.get(url, headers=headers, params=params)
    print(url, headers, params, answer.text, sep='\n')


def refresh_access_main_amo_v3(amo_name):
    url = 'https://amo3431ru.amocrm.ru/'
    # url = 'https://zakazjpexpressru.amocrm.ru'
    creds = get_creds(amo_name)
    refresh = creds.get('refresh_token')
    file = open(PATH_DIR + 'warning.txt', 'a')
    file.write(str(datetime.datetime.now()))
    file.write('\n')
    file.write(f'refresh_{amo_name}=' + refresh)
    file.write('\n')
    file.close()
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    }
    headers = {'Content-Type': 'application/json'}
    # data = {
    #     "client_id": 'c172969a-1445-4443-90da-2842aede97b2',
    #     "client_secret": 'KVuLImC2QsUmXkXOZjtuya55Wf5kHgDQ17nlRl1UpjOLxQG5fvbVwzzMWF665ySx',
    #     "grant_type": "authorization_code",
    #     "code": '', # authorization_code,
    #     "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    # }

    metod = '/oauth2/access_token'
    link = url + metod
    answer = requests.post(link, headers=headers, json=data)
    print('refresh_access_main_amo', answer.text)
    result = update_creds_main_amo(answer.text)
    if result:
        print('ALL_RIDE_refresh_access_main_amo')

    else:
        print('ERROR_UPDATE_refresh_access_main_amo', answer.text)


def refresh_access_main_amo_v2(user_id):
    url = user_link.get(user_id)[0]
    token_name = user_link.get(user_id)[-1]
    creds = get_creds_v2(user_id)
    refresh = creds.get('refresh_token')
    file = open(PATH_DIR + 'warning.txt', 'a')
    file.write(str(datetime.datetime.now()) + token_name)
    file.write('\n')
    file.write(f'refresh_{user_id}=' + refresh)
    file.write('\n')
    file.close()
    data_client = get_amo_akk(user_id)
    print(data_client)
    data = {
        "client_id": data_client.get("client_id"),
        "client_secret": data_client.get("client_secret"),
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    }
    headers = {'Content-Type': 'application/json'}
    # data = {  #3431
    #    "client_id": '1e601ad5-b0fe-468f-8dd7-e4ee08e94ba4',
    #    "client_secret": 'jrRRKIvCPtEkLnl9iHv1Qacley63CCJc256nRqq6Ahua62ILuISn5tGozmVBiGnH',
    #    "grant_type": "authorization_code",
    #    "code": '',  #authorization_code,
    #    "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    # }

    metod = '/oauth2/access_token'
    link = url + metod
    answer = requests.post(link, headers=headers, json=data)
    print('refresh_access_main_amo_v2 {} {}'.format(answer.status_code, user_id))
    # result = update_creds_main_amo(answer.text)
    print(data, data_client, link, token_name)
    result = update_creds_main_amo_v2(answer.text, token_name)
    if result:
        print('ALL_RIDE_refresh_access_main_amo_v2')

    else:
        print('ERROR_UPDATE_refresh_access_main_amo_v2', answer.text)


def get_amo_unsorted_list():
    path = '/api/v4/leads/unsorted'
    access_token = get_creds().get("access_token")
    link = 'https://amo3431ru.amocrm.ru/'
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
        'filter': {
            'category': [],
            'order': {
                'created_at': 'desc'
            }
        }
    }
    answer = requests.get(url, headers=headers, params=params)
    print('get_amo_unsorted_list ', answer.status_code)
    if answer.status_code == 401:
        refresh_access_main_amo()
        answer = requests.get(url, headers=headers, params=params)
        if not answer.ok:
            print('EROOR_RESP_get_amo_unsorted_list', headers, params, answer.text)
        else:
            data = answer.json()
            need_data = data.get('_embedded').get('unsorted')
            return answer.status_code, need_data
    else:
        data = answer.json()
        need_data = data.get('_embedded').get('unsorted')
        print(333, need_data[0])
        return answer.status_code, need_data


def get_amo_current_leads(leads_id, amo_name):
    path = f'/api/v4/leads/{leads_id}'
    access_token = get_creds(amo_name).get("access_token")
    link = f'https://{amo_name}.amocrm.ru'
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
    }
    answer = requests.get(url, headers=headers, params=params)
    print('get_amo_unsorted_list ', answer.status_code)

    if not answer.ok:
        print('EROOR_RESP_get_amo_current_leads', headers, params, answer.text)

    else:
        data = answer.json()
        # need_data = data.get('_embedded').get('unsorted')
        print(333, data)
        return answer.status_code, data



def get_amo_unsorted_list_v2(user_id):
    path = '/api/v4/leads/unsorted'
    access_token = get_creds_v2(user_id).get("access_token")
    # link = 'https://amo3431ru.amocrm.ru/'
    link = user_link.get(user_id)[0]
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
        'filter': {
            'category': [],
            'order': {
                'created_at': 'desc'
            }
        }
    }
    answer = requests.get(url, headers=headers, params=params)
    logging.info('get_amo_unsorted_list_v2_ {} {} {}'.format(answer.status_code, user_id, link))
    if answer.status_code == 401:
        # refresh_access_main_amo()
        refresh_access_main_amo_v2(user_id)
        answer = requests.get(url, headers=headers, params=params)
        if not answer.ok:
            print('EROOR_RESP_get_amo_unsorted_list', headers, params, answer.text)
        else:
            data = answer.json()
            need_data = data.get('_embedded').get('unsorted')
            return answer.status_code, need_data
    else:
        data = answer.json()
        need_data = data.get('_embedded').get('unsorted')
        return answer.status_code, need_data


def make_pipeline(order_data):
    order_id = order_data.get('clientId')
    order = get_amo_list_leads('3431', order_id)



async def get_amo_unsorted_list_v3(user_id):
    path = '/api/v4/leads/unsorted'
    # access_token = get_creds_v2(user_id).get("access_token")
    creds = await get_creds_v3(user_id)
    access_token = creds.get('access_token')
    # link = 'https://amo3431ru.amocrm.ru/'
    link = user_link.get(user_id)[0]
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
        'filter': {
            'category': [],
            'order': {
                'created_at': 'desc'
            }
        }
    }
    answer = requests.get(url, headers=headers, params=params)
    logging.info('get_amo_unsorted_list_v3_ {} {} {}'.format(answer.status_code, user_id, url))
    if answer.status_code == 401:
        refresh_access_main_amo_v2(user_id)
        answer = requests.get(url, headers=headers, params=params)
        if not answer.ok:
            print('EROOR_RESP_get_amo_unsorted_list', headers, params, answer.text)
        else:
            data = answer.json()
            need_data = data.get('_embedded').get('unsorted')
            return answer.status_code, need_data
    else:
        data = answer.json()
        need_data = data.get('_embedded').get('unsorted')
        print(answer.status_code, need_data)
        return answer.status_code, need_data


def get_amo_events(avito_id):
    path = '/api/v4/events'
    access_token = get_creds_v2(avito_id).get("access_token")
    link = user_link.get(avito_id)[0]
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
        'filter': {
            'category': [],
            'order': {
                'created_at': 'desc'
            }
        }
    }
    answer = requests.get(url, headers=headers, params=params)
    print('get_amo_unsorted_list ', answer.status_code)
    if answer.ok:
        data = answer.json()
        # need_data = data.get('_embedded').get('unsorted')
        print(333, data)
    else:
        logging.error('fuck_up {} {} '.format(answer.status_code, answer.text))

    return answer.status_code


def get_contact_fields(avito_id):
    path = '/api/v4/contacts/custom_fields'
    access_token = get_creds_v2(avito_id).get("access_token")
    link = user_link.get(avito_id)[0]
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 0,
        'limit': 250,  # but we can 250
    }
    answer = requests.get(url, headers=headers, params=params)
    print('get_amo_contact_fields ', answer.status_code)
    if answer.ok:
        data = answer.json()
        # need_data = data.get('_embedded').get('unsorted')
        print(333, 'status', answer.text, data)
    else:
        logging.error('fuck_up {} {} '.format(answer.status_code, answer.text))

    # return answer.status_code


async def rewrite_leads(chat_id):  # (leads_id, price, string):
    raw_data = get_amo_unsorted_list()
    if raw_data[0] == 401:
        refresh_access_main_amo()
        raw_data = get_amo_unsorted_list()
    leads_id = ''
    for row in raw_data[1]:
        target = ''
        try:
            target = row.get('metadata').get('to')
        except Exception as err:
            print('Some_fuck_up_get_metadata_to {} {}'.format(err, row))
        if target == chat_id:
            leads_id = row.get('_embedded').get('leads')[0].get('id')
        else:
            continue
    data_link = read_link(chat_id)
    print('try_rewrite_lead', leads_id, data_link)
    access_token = get_creds().get('access_token')
    try:
        price = int(data_link[0].replace('\xa0', '').replace(' ₽', ''))
    except:
        price = 0
    try:
        title = data_link[4]
    except IndexError:
        title = 'See in Avito'
    except Exception as error:
        title = ''
        print("Some_fuck_up_title {}".format(error))
    data = {
        'price': price,
        'custom_fields_values': [
            {
                "field_id": 987785,  # url
                "values": [
                    {
                        "value": data_link[1]
                    }
                ]
            },
            {
                "field_id": 987783,  # url
                "values": [
                    {
                        "value": title
                    }
                ]
            }
        ]
    }
    path = f'/api/v4/leads/{leads_id}'
    link = 'https://amo3431ru.amocrm.ru/'
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    if leads_id:
        answer = requests.patch(url, json=data, headers=headers)
        logging.info('rewrite_leads {} {} {}'.format
                     (answer.status_code, data, chat_id))
        print('rewrite_leads', answer.status_code)
        if not answer.ok:
            print('ERROR rewrite_leads ', data, chat_id, leads_id)
            logging.info('fuck_up_rewrite_leads{} {} {} {}'.
                         format(answer.status_code, data, chat_id, leads_id))
    else:
        print('Leads is not leads')


async def get_phone(string):
    extract_number = "\\+?[7-9][0-9]{9,11}"
    result = re.findall(extract_number, string.replace(' ', ''))
    if len(result) > 0 and len(result[0]) == 10:
        result[0] = '8' + result[0]
    return result


async def rewrite_leads_v2(chat_id, user_id):  # (leads_id, price, string):
    raw_data = await get_amo_unsorted_list_v3(user_id)
    # time.sleep(1)
    logging.info('message from rewrite leads, we get some {} {} {} '.format(raw_data[0], chat_id, user_id))
    if raw_data[0] == 401:
        # refresh_access_main_amo()
        refresh_access_main_amo_v2(user_id)
        # raw_data = get_amo_unsorted_list_v2(user_id)
        raw_data = await get_amo_unsorted_list_v3(user_id)
        logging.info('message from rewrite leads, we get error {} {} {}'.format(raw_data[0], chat_id, user_id))
        time.sleep(1)
    leads_id, contact_id = '', 0
    for row in raw_data[1]:
        target = ''
        try:
            target = row.get('metadata').get('to')
        except Exception as err:
            print('Some_fuck_up_get_metadata_to {} {}'
                  .format(err, row))
        if target == chat_id:
            leads_id = row.get('_embedded').get('leads')[0].get('id')
            contact_id = row.get('_embedded').get('contacts')[0].get('id')
        else:
            continue
    data_link = await read_link_v2(chat_id)
    logging.info('Some_get from rewrite lead, we get {}'
                 .format(data_link))
    creds = await get_creds_v3(user_id)
    access_token = creds.get('access_token')
    try:
        price = int(data_link[0].replace('\xa0', '').replace(' ₽', ''))
    except:
        price = 0
    try:
        title = data_link[4]
    except IndexError:
        title = 'See in Avito'
    except Exception as error:
        title = ''
        print("Some_fuck_up_title {}".format(error))
    data = {
        'name': title,
        'price': price,
        'pipeline_id': user_link.get(user_id, (0, 0, 0, 0, 0, 0))[3],
        'responsible_user_id': user_link.get(user_id, (0, 0, 0, 0, 0, 0))[2],  # менеджер 1
        'custom_fields_values': [
            {
                "field_id": user_link.get(user_id, (0, 0, 0, 0, 0, 0))[4],  # 987785,  # url_id
                "values": [
                    {
                        "value": data_link[1]
                    }
                ]
            },
            {
                "field_id": user_link.get(user_id, (0, 0, 0, 0, 0, 0))[5],  # field_promo_id
                "values": [
                    {
                        "value": title
                    }
                ]
            }
        ],
        '_embedded': {
            'tags': [
                {
                    'name': user_link.get(user_id)[1]  # name_tag
                }
            ]
        }
    }

    path = f'/api/v4/leads/{leads_id}'
    # link = 'https://amo3431ru.amocrm.ru/'
    link = user_link.get(user_id)[0]
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    if leads_id:
        answer = requests.patch(url, json=data, headers=headers)
        logging.info('try_rewrite_lead_v2_ {} {} {} {} {} {}'.
                     format(answer.status_code, user_id, chat_id, leads_id, data, url))
        if answer.ok:
            await re_write_link_v3(chat_id, leads_id, contact_id)
            logging.info('ALL_RIDE_rewrite_lead_v2 {} {} {} {} {} {} {}'.
                         format(answer.status_code, user_id, chat_id, leads_id, data, url, contact_id))
        else:
            logging.info('fuck_up_rewrite_lead_v2 {} {} {} {} {} {}'.
                         format(answer.status_code, user_id, chat_id, leads_id, data, url))
    else:
        print('Leads is not found in Amo leads V2')


def connect_channel_with_account_amo(amo_name):
    channel_id = '8bf871d6-fc08-49e0-aac7-d5241c3542ea'
    amojo_id = get_amo_akk_v2(amo_name).get('amojo_id')  # "d2914d60-a44a-4625-881b-d9e237592dce"
    data = {
        "account_id": amojo_id,
        "title": "ChatIntegration",
        "hook_api_version": "v2"
    }
    result = send_to_amo_message_v2(data, f'/v2/origin/custom/{channel_id}/connect')
    print('connect_channel_with_account_amo', result)
    return result


async def make_bonus(subdomain, lead_id):
    amo_name = ''
    if subdomain == 'zakazjpexpressru':
        amo_name = 'JPexp'
    elif subdomain == 'amo3431ru':
        amo_name = '3431'

    links = await read_links_v3()
    bonuses, contact_id, price = 0, 0, 0
    for key, value in links.items():
        # print(len(value), value)
        if len(value) == 9 and value[7] == lead_id:
            price = value[0].replace('\xa0', '').replace(' ₽', '')
            contact_id = value[8]
            bonuses = int(price) * 0.05
            break

    if contact_id and bonuses:
        data_note = [{
            "created_by": 8200807,
            "note_type": "common",
            "params": {
                "text": f"Начислено {bonuses} бонусов."
            }
        }]

        access_token = get_creds(amo_name).get("access_token")
        link = f'https://{subdomain}.amocrm.ru'
        entity_type = 'contacts'
        path = f'/api/v4/{entity_type}/{contact_id}/notes'
        # path = f'/api/v4/{entity_type}/notes'
        url = link + path
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        answer_note = requests.post(url, headers=headers, json=data_note)
        logging.info('We are calculate_&_send_note {} user, {} bonuses, {} lead_id, and get answer - {}'
                     .format(contact_id, bonuses, lead_id, answer_note))

        data_bonuses = {
            "custom_fields_values": [
                {
                    "field_id": 1338551,  # TODO FIXIT
                    "field_name": "Бонусы",
                    "values": [
                        {
                            "value": str(bonuses),

                        }
                    ]
                }
            ]
        }

        await rewrite_contact_v2(data=data_bonuses, contact_id=contact_id, amo_name=amo_name, link=link)

    else:
        logging.info("Not found a candidate for bonuses {} user, {} bonuses, {} lead_id, and get answer - {}"
                     .format(contact_id, bonuses, lead_id, price))



def update_creds_main_amo(answer):
    token_data = json.loads(answer)
    re_access = token_data.get('access_token')
    re_refresh = token_data.get('refresh_token')
    if re_refresh and re_access:
        f = open(PATH_DIR + 'cred_update.json', 'w')
        cred = {
            "access_token": re_access,
            "refresh_token": re_refresh
        }
        creds = json.dumps(cred)
        f.write(creds)
        f.close()
        print('Creds update successfully')
        result = True
    else:
        result = False
        print('EROOR get token data')

    return result


def update_creds_main_amo_v2(answer, token_name):
    token_data = json.loads(answer)
    re_access = token_data.get('access_token')
    re_refresh = token_data.get('refresh_token')
    # token_name = user_link.get(user_id)[-1]
    if re_refresh and re_access:
        f = open(PATH_DIR + f'cred_update_{token_name}.json', 'w')
        cred = {
            "access_token": re_access,
            "refresh_token": re_refresh
        }
        creds = json.dumps(cred)
        f.write(creds)
        f.close()
        print('Creds update successfully')
        result = True
    else:
        result = False
        print('EROOR get token data')

    return result


def refresh_access_main_amo():
    # url = 'https://amo3431ru.amocrm.ru/'
    # url = 'https://zakazjpexpressru.amocrm.ru'
    # name = 'JPexp'  # "3431"  #
    name_link = [
        ('JPexp', 'https://zakazjpexpressru.amocrm.ru'),
        ("3431", 'https://amo3431ru.amocrm.ru/')
    ]
    for row in name_link:
        name, url = row[0], row[1]
        creds = get_creds(name)
        refresh = creds.get('refresh_token')
        file = open(PATH_DIR + 'warning.txt', 'a')
        file.write(str(datetime.datetime.now()))
        file.write('\n')
        file.write(f'refresh_{name}=' + refresh)
        file.write('\n')
        file.close()
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "redirect_uri": "https://phone-call.i-bots.ru/token-token"
        }
        headers = {'Content-Type': 'application/json'}
        # data = {
        #     "client_id": '25a9117a-3fce-4a5f-9015-9d7779e97ef7',
        #     "client_secret": 'rBVi8bNWNBSHssLvQq8lhZqZpJ93CvLNXNHZ7DjsMFVxMqnQ7kdszZ6cXQF43CAc',
        #     "grant_type": "authorization_code",
        #     "code": '',
        #     # authorization_code,
        #     "redirect_uri": "https://phone-call.i-bots.ru/token-token"
        # }

        metod = '/oauth2/access_token'
        link = url + metod
        answer = requests.post(link, headers=headers, json=data)
        print('refresh_access_main_amo  {}'.format(name), answer.text)
        result = update_creds_main_amo_v2(answer.text, name)
        if result:
            print('ALL_RIDE_refresh_access_main_amo {}'.format(name))

        else:
            print('ERROR_UPDATE_refresh_access_main_amo_3 {}'.
                  format(name), answer.text)


# get_amo_unsorted_list()
# connect_channel_with_account_amo()
# refresh_access_main_amo()
# get_amo_unsorted_list()

# get_amo_account_users()
# print(asyncio.run(get_phone('Семь 9172213870')))
# print(user_link.get(10138154)[0])
# refresh_access_main_amo_v2(369222788)
# print(get_amo_akk(353821742))
# asyncio.run(get_amo_unsorted_list_v3(369222788))
# get_amo_events(369222788)
# get_contact_fields(10138154)
# get_contact_fields(353207078)
# asyncio.run(make_bonus('zakazjpexpressru', 48993631))
# asyncio.run(rewrite_contact_v2(chat_id='u2i-I9OIOGcbfkZKhO_uTUplCA', user_id=10138154,
#                    data={"custom_fields_values":[
#                        {"field_code":"PHONE","values":[
#                            {"value":"89202004457","enum_code": "WORK"}]}]}))

# asyncio.run(rewrite_contact('u2i-yMWc30AcgTbquI~Bi6Riig', 10138154, ["89211112357"]))
# asyncio.run(rewrite_contact('u2i-U0FJJh6V1Trxk21sYY61qQ', 10138154, ['700948278543']))