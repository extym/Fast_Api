import asyncio
import json
import logging
import os
import schedule
from connect import *
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
    PATH_DIR = os.getcwd()
    LOG_DIR = 'logs/'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH_DIR = '/home/userbe/bot3431'
    LOG_DIR = '/home/userbe/bot3431/logs/'

user_link = {
    # user_id: (link, name_tag, responsible_user_id, pipeline_id, field_url_id, field_promo_id amo_cred_id)
    357922774: ("https://amo3431ru.amocrm.ru", "3431 грузовые", 9983934, 7155526, 987785, 987783, '3431'),
    353207078: ("https://amo3431ru.amocrm.ru", "3431 новые запчасти", 9983934, 7155526, 987785, 987783, '3431'),
    353821742: ("https://amo3431ru.amocrm.ru", "3431ru", 9983934, 7155526, 987785, 987783, '3431'),
    363810872: ("https://amo3431ru.amocrm.ru", "JP AKB", 9983934, 7155526, 987785, 987783, '3431'),
    375810638: ("https://amo3431ru.amocrm.ru", "Запчасти за час", 9983934, 7155526, 987785, 987783, '3431'),
    375811020: ("https://amo3431ru.amocrm.ru", "Новые Запчасти", 9983934, 7155526, 987785, 987783, '3431'),
    375811448: ("https://amo3431ru.amocrm.ru", "Быстрые Запчасти", 9983934, 7155526, 987785, 987783, '3431'),
    10138154: ("https://zakazjpexpressru.amocrm.ru", "JPexpress", 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369221904: ('https://zakazjpexpressru.amocrm.ru', 'Быстрые шины', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369222251: ('https://zakazjpexpressru.amocrm.ru', 'Быстрый двигатель', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369220948: ('https://zakazjpexpressru.amocrm.ru', 'Классный салон', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369223108: ('https://zakazjpexpressru.amocrm.ru', 'Быстрая машина', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369222788: ('https://zakazjpexpressru.amocrm.ru', 'Быстрая коробка', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369721092: ('https://zakazjpexpressru.amocrm.ru', 'Быстрые мелочи', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    369219038: ('https://zakazjpexpressru.amocrm.ru', 'Быстрый кузов', 10131478, 5420530, 1335423, 1335421, 'JPexp'),
    'rota': ('https://otdelkadrovrota.amocrm.ru', 'OtdelKadrovRota', 0, 0, 0, 0, 'rota')
}


logging.basicConfig(filename=os.path.join(LOG_DIR + 'webhook.log'), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


def get_rfc_2822():
    nowdt = utils.format_datetime(datetime.datetime.now())

    return nowdt


def read_link(chat_id):
    with open(PATH_DIR + '/links.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)



async def read_link_v2(chat_id):
    with open(PATH_DIR + '/links.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)


def read_links_v2():
    with open(PATH_DIR + '/links.json', 'r') as file:
        links = json.load(file)

        return links


async def read_links_v3():
    with open(PATH_DIR + '/links.json', 'r')\
            as file:
        links = json.load(file)

        return links


async def get_creds_v3(user_id):
    token_name = user_link[user_id][-1]
    with open(PATH_DIR + f'/cred_update_{token_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


async def rewrite_contact(chat_id, user_id, phone_numbers):
    # need_data = await read_link_v2(chat_id)
    need_data = get_bid(chat_id)
    logging.info('CONTACT_ID {} {} {} {} '
                 .format(chat_id, user_id, phone_numbers, need_data))
    contact_id = 0
    if need_data:
        contact_id = need_data[14]
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

        if answer.ok:
            logging.info('ALL_RIDE_re_write_contact_id {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))

        else:
            logging.info('fuck_up_rewrite_2_contact_id {}, answer_status_code- {} answer.text {} {} {} {} {}'.
                         format(contact_id, answer.status_code, answer.text, user_id, chat_id, data, url))
    else:
        logging.info('Contact is not found in Amo {} {} {}'
                     .format(chat_id, user_id, phone_numbers))


async def rewrite_contact_v2(chat_id=None, contact_id=0, user_id=0, amo_name='', link=None, data=None):
    need_data = ''
    if chat_id:
        # need_data = await read_link_v2(chat_id)
        need_data = get_bid(chat_id)
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
    logging.info("Check_status_make_bonus {}; {}; {}; {}; {}; {}".
                 format(contact_id, chat_id, user_id, amo_name, link, data))
    if contact_id:
        path = f'/api/v4/contacts/{contact_id}'
        url = link + path
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        answer = requests.patch(url, json=data, headers=headers)
        if answer.ok:
            logging.info('ALL_RIDE_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))

        else:
            logging.info('fuck_up_re_write_contact_v2_ {}, answer- {} {} {} {} {}'.
                         format(contact_id, answer.status_code, user_id, chat_id, data, url))
    else:
        logging.info('Contact is not found in Amo {} {} {} {} '
                     .format(chat_id, user_id, data, contact_id))


async def re_write_link_v3(chat_id, leads_id, contact_id):
    links = await read_links_v3()
    with open(PATH_DIR + '/links.json', 'w') as file:
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
    with open(PATH_DIR + f'/cred_update_{amo_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


def get_creds_v2(user_id): # : int):
    token_name = user_link.get(user_id)[-1]
    with open(PATH_DIR + f'/cred_update_{token_name}.json', 'r') as file:
        creds = json.load(file)
        # fresh = creds.get('refresh_token')
        # access = creds.get('access_token')

    return creds


def get_amo_akk(user_id):
    logging.info('GET_USER_AKK_AMO {}'.format(user_id))
    with open(PATH_DIR + '/amo_akk.json', 'r') as file:
        data = json.load(file)
        return data.get(user_link.get(user_id)[-1])


def get_amo_akk_v2(amo_name):
    logging.info('GET_USER_AKK_AMO {}'.format(amo_name))
    with open(PATH_DIR + '/amo_akk.json', 'r') as file:
        data = json.load(file)
        print(111, data.get(amo_name))
        return data.get(amo_name)


async def get_amo_akk_v3(user_id):
    with open(PATH_DIR + '/amo_akk.json', 'r') as file:
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

        result = True

    except:
        logging.info('SOMETHING_WRONG_WITH_SEND_TO_AMO ' + str(path))
        # print("SOMETHING_WRONG_WITH_SEND_TO_AMO", path)
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
            print(88, answer.text)
        else:
            logging.error('ERROR_SEND_TO_AMO_2 {} {} {}'.format(answer.text, message, url))

        result = True

    except:
        logging.info('SOMETHING_WRONG_WITH_SEND_TO_AMO ' + str(path))

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

    try:
        re_avatar = chat_data.get("users")[1].get('public_user_profile').get("avatar").get("default")
    except:
        re_avatar = ''

    try:
        name = chat_data.get("users")[0].get("name")
    except:
        name = ''

    try:
        profile_link = chat_data.get("users")[0].get("public_user_profile").get("url")
    except:
        profile_link = ''

    try:
        re_profile_link = chat_data.get("users")[1].get("public_user_profile").get("url")
    except:
        re_profile_link = ''

    try:
        receiver = chat_data.get("users")[0].get('id')
        if receiver == sender_id:
            receiver = chat_data.get("users")[1].get('id')
    except:
        receiver = ''

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
        logging.info('We_make_message_for_amo_1 {} {}'.format(user_id, message))
    except:
        print('FUCKUP_make_message_for_amo_1')


async def make_message_for_amo_v2(hook_data, chat_data, sender_id, silent):
    tst = timestamp()
    try:
        avatar = chat_data.get("users")[0].get('public_user_profile').get("avatar").get("default")
    except:
        avatar = ''

    try:
        re_avatar = chat_data.get("users")[1].get('public_user_profile').get("avatar").get("default")
    except:
        re_avatar = ''

    try:
        name = chat_data.get("users")[0].get("name")
    except:
        name = ''

    try:
        profile_link = chat_data.get("users")[0].get("public_user_profile").get("url")
    except:
        profile_link = ''

    try:
        re_profile_link = chat_data.get("users")[1].get("public_user_profile").get("url")
    except:
        re_profile_link = ''

    try:
        receiver = chat_data.get("users")[0].get('id')
        if receiver == sender_id:
            receiver = chat_data.get("users")[1].get('id')
    except:
        receiver = ''

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
        # logging.info('We_make_message_for_amo_2 {}'.format(user_id))
    except:
        print('FUCKUP_make_message_for_amo_2')

    is_phone = await get_phone(message)

    if len(is_phone) > 0:
        chat_id = hook_data.get('payload').get("value").get('chat_id')
        logging.info('We_send_re_write_contact {} {} {} {} '
                     .format(user_id, message, chat_id, is_phone))

        await rewrite_contact(chat_id, user_id, is_phone)


def get_amo_account_amojo_id(amo_name):
    # name = 'rota'
    access_token = get_creds(amo_name).get("access_token")
    link = get_amo_akk_v2(amo_name).get("link") # 'https://zakazjpexpressru.amocrm.ru'
    # link = 'https://amo3431ru.amocrm.ru/'
    path = '/api/v4/account?with=amojo_id'
    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    answer = requests.get(url, headers=headers)
    print(45, answer.text)

    return answer.json().get('amojo_id')


def get_amo_account_users(user_id):
    access_token = get_creds_v2(user_id).get("access_token")
    link = user_link.get(user_id)[0]
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
    creds = get_creds(amo_name)
    refresh = creds.get('refresh_token')
    file = open(PATH_DIR + '/warning.txt', 'a')
    file.write(str(datetime.datetime.now()))
    file.write('\n')
    file.write(f'refresh_{amo_name}=' + refresh)
    file.write('\n')
    file.close()
    amo_cred = get_amo_akk_v2(amo_name)
    print(22222, amo_cred)
    # data = {
    #     "client_id": amo_cred.get("client_id"),
    #     "client_secret": amo_cred.get("client_secret"),
    #     "grant_type": "refresh_token",
    #     "refresh_token": refresh,
    #     "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    # }
    link = amo_cred.get("link")
    data = {
        "client_id": amo_cred.get("client_id"),
        "client_secret": amo_cred.get("client_secret"),
        "grant_type": "authorization_code",
        "code": 'def5020072d7f9b1c9ad8fb9ea984f9eb134cb1cb523f56c5c5aaa083e04ac1173cf156a5b3d0e386864d4e3e74d5cf6c18200aedcd33cd451752d229adfc4cb5df2fe5873c4fab5a8a5422c4a9523c057eaa66f571d65d6d645876b95cb8926965d834ca63f1245cb28c97f7e8451b24be8b02438656e30f20ebc9e6b83e525b0d86ed6c90c441b1656c872d51f99e1ada2255ec98e2c15db02096790a89270dd085bad8260dfbb39bb76645d30d4de79d54d90117c83e72dd8aa5aaab795d49869dfd522700e436a5a804ee5588cee8e8c92a9b70c4d97fa374b58bf085725036ba6e3d7efc5fc89b9cb1fee66b6d5c88648c6c35d0ac88979abf8675b19391af13876690b97f2c5ba232c95e5c4cac7518af5169a0d68e6e2a0b01f05f1c96d51e9062ce170245d1b1956a27c93394ce5f4823aca5ee7df69e2048b928deb267bd864d2eb1cd40a165cdf1c086c1501be29c1bf694260ad51ada47024868b7d1b56b0a1d5bec0e70f5244c397ed991a644b71f142676f86f512a6e24f7fa932e95422e524d9862032069460fce45bf6b47852414abb94f036643e172bcad449bff4eeca9e5ea8c38a33f88a9e3477b2d0edfa5c28b91129a1aad105357cb60eff910af86c868ec875930304ba05a1ba247b93036b367e95c4c77b2bd7a05be343ab6bd86a2609f35959feabd648c399964bd0fc2b452fcbf2',  # authorization_code,
        "redirect_uri": "https://phone-call.i-bots.ru/token-token"
    }
    headers = {'Content-Type': 'application/json'}
    metod = '/oauth2/access_token'
    url = link + metod
    answer = requests.post(url, headers=headers, json=data)
    print('refresh_access_main_amo', answer.text)
    result = update_creds_main_amo_v2(answer.text, amo_name)
    if result:
        print('ALL_RIDE_refresh_access_main_amo')

    else:
        print('ERROR_UPDATE_refresh_access_main_amo', answer.text)


def refresh_access_main_amo_v2(user_id):
    url = user_link.get(user_id)[0]
    token_name = user_link.get(user_id)[-1]
    creds = get_creds_v2(user_id)
    refresh = creds.get('refresh_token')
    file = open(PATH_DIR + '/warning.txt', 'a')
    file.write(str(datetime.datetime.now()) + token_name)
    file.write('\n')
    file.write(f'refresh_{user_id}=' + refresh)
    file.write('\n')
    file.close()
    data_client = get_amo_akk(user_id)
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
        # print(333, need_data[0])
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
    print('get_amo_current_leads ', answer.status_code)

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




async def get_amo_unsorted_list_v3(user_id):
    path = '/api/v4/leads/unsorted'
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
        # print(answer.status_code, need_data)
        return answer.status_code, need_data


def get_amo_events(avito_id=0, amo_name=None):
    path = '/api/v4/events'
    if avito_id:
        access_token = get_creds_v2(avito_id).get("access_token")
        link = user_link.get(avito_id)[0]
    elif amo_name:
        credos = get_amo_akk_v2(amo_name)
        link = credos.get('link')
        access_token = credos.get('longlife_token')
    else:
        access_token = ''
        link = ''

    url = link + path
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
        'page': 2,
        'limit': 250,  # but we can 250
        'filter': {
            'category': [],
            'order': {
                'created_at': 'desc'
            }
        }
    }
    answer = requests.get(url, headers=headers, params=params)
    print('get_amo_events ', answer.status_code)
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
        # print(333, 'status', answer.text, data)
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
        # print('rewrite_leads', answer.status_code)
        if not answer.ok:
            print('ERROR rewrite_leads ', data, chat_id, leads_id)
            logging.info('fuck_up_rewrite_leads{} {} {} {}'.
                         format(answer.status_code, data, chat_id, leads_id))
    else:
        print('Leads is not leads')


async def get_phone(string):
    extract_number = "\\+?[7-9][0-9]{9,11}"
    result = re.findall(extract_number, string.replace(' ', '').replace(',', ''))
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
    # data_link = await read_link_v2(chat_id)
    data_link = get_bid(chat_id)
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
        # print("Some_fuck_up_title {}".format(error))
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
        # logging.info('try_rewrite_lead_v2_{} {} {} {} {} {}'.
        #              format(answer.status_code, user_id, chat_id, leads_id, data, url))
        if answer.ok:
            # await re_write_link_v3(chat_id, leads_id, contact_id)
            await execute_query_v3(query_update_contact_id,(chat_id,
                                                            leads_id, contact_id))
            logging.info('ALL_RIDE_rewrite_lead_v2 {} {} {} {} {} {} {}'.
                         format(answer.status_code, user_id, chat_id,
                                leads_id, data, url, contact_id))
        else:
            logging.info('Error_rewrite_lead_v2 status_code {}, text {},'
                         ' user_id {}, chat_id {}, '
                         'leads_id {}, data {}, url {}'.
                         format(answer.status_code, answer.text, user_id,
                                chat_id, leads_id, data, url))
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
    # print('connect_channel_with_account_amo', result)
    return result


async def make_bonus(subdomain, lead_id: int):
    amo_name = ''
    if subdomain == 'zakazjpexpressru':
        amo_name = 'JPexp'
    elif subdomain == 'amo3431ru':
        amo_name = '3431'

    # links = await read_links_v3()
    bid = get_bid(leads_id=lead_id)
    bonuses, contact_id, price = 0, 0, 0
    # for key, value in links.items():
    #     if len(value) == 9 and value[7] == lead_id:
    #         price = value[0].replace('\xa0', '').replace(' ₽', '')
    #         contact_id = value[8]
    #         bonuses = int(price) * 0.05
    #         logging.info('BONUSES_price {}, contact_id {}, bonuses {}, lead_id {}'.
    #                      format( price, contact_id, bonuses, lead_id))
    #         break

    if len(bid) < 0:
        logging.info('BONUSES_TRY_price {}, contact_id {}, bonuses {}, lead_id {}'.
                     format(price, *bid, lead_id))
        price = bid[7].replace('\xa0', '').replace(' ₽', '')
        contact_id = bid[14]
        bonuses = int(price) * 0.05
        logging.info('BONUSES_price {}, contact_id {}, bonuses {}, lead_id {}'.
                     format( price, contact_id, bonuses, lead_id))

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
        if LOCAL_MODE:
            print('We are calculate_&_send_note {} user, {} bonuses, {} lead_id, and get answer - {}'
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

        await rewrite_contact_v2(data=data_bonuses,
                                 contact_id=contact_id,
                                 amo_name=amo_name, link=link)

    else:
        logging.info("Not found a candidate for bonuses {} user, {} bonuses, {} lead_id, and price - {}"
                     .format(contact_id, bonuses, lead_id, price))


def update_creds_main_amo(answer):
    token_data = json.loads(answer)
    re_access = token_data.get('access_token')
    re_refresh = token_data.get('refresh_token')
    if re_refresh and re_access:
        f = open(PATH_DIR + '/cred_update.json', 'w')
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
        f = open(PATH_DIR + f'/cred_update_{token_name}.json', 'w')
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
    name_link = [
        ('JPexp', 'https://zakazjpexpressru.amocrm.ru'),
        ("3431", 'https://amo3431ru.amocrm.ru/'),
        ("rota", 'https://otdelkadrovrota.amocrm.ru')
    ]
    for row in name_link:
        name, url = row[0], row[1]
        creds = get_creds(name)
        refresh = creds.get('refresh_token')
        file = open(PATH_DIR + '/warning.txt', 'a')
        file.write(str(datetime.datetime.now()))
        file.write('\n')
        file.write(f'refresh_{name}=' + refresh)
        file.write('\n')
        file.close()
        other_data = get_amo_akk_v2(name)
        data = {
            "client_id": other_data.get('client_id'),
            "client_secret": other_data.get('client_secret'),
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


# get_amo_account_amojo_id('rota')
# refresh_access_main_amo_v3('rota')
# get_amo_unsorted_list()
# connect_channel_with_account_amo('rota')
# refresh_access_main_amo()
# get_amo_unsorted_list()

# get_amo_account_users(10138154)
# print(asyncio.run(get_phone('Семь 9172213870')))
# print(user_link.get(10138154)[0])
# refresh_access_main_amo_v2(369222788)
# print(get_amo_akk(353821742))
# asyncio.run(get_amo_unsorted_list_v3(369222788))
# get_amo_events(369222788)
# get_contact_fields(10138154)
# get_contact_fields(353207078)
# asyncio.run(make_bonus('zakazjpexpressru', 49320771))
# asyncio.run(make_bonus('zakazjpexpressru', 49320503))
# asyncio.run(rewrite_contact_v2(chat_id='u2i-I9OIOGcbfkZKhO_uTUplCA', user_id=10138154,
#                    data={"custom_fields_values":[
#                        {"field_code":"PHONE","values":[
#                            {"value":"89202004457","enum_code": "WORK"}]}]}))

# asyncio.run(rewrite_contact('u2i-yMWc30AcgTbquI~Bi6Riig', 10138154, ["89211112357"]))
# asyncio.run(rewrite_contact('u2i-U0FJJh6V1Trxk21sYY61qQ', 10138154, ['700948278543']))

# refresh_access_main_amo_v3('rota')
# get_amo_events(amo_name='JPexp')
# print(get_amo_akk_v2('rota'))