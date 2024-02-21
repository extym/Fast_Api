import asyncio
import json
import re

import schedule
import time
from cred import *
import requests
import datetime
from cred import *
from amo import make_message_for_amo_v2, rewrite_leads_v2, user_link
from worker import worker, async_worker
import urllib.parse
import hashlib
from email import utils
import hmac
import logging
import os


# 357922774 = "3431 грузовые"
# 353207078 = "3431 новые запчасти"
# 353821742 = "3431ru"
# 363810872 = "JP AKB"

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH_DIR = './'
    LOG_DIR = './'
    CSV_PATH = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH_DIR = '/home/userbe/phone/'
    LOG_DIR = 'home/userbe/phone/logs/'
    CSV_PATH = '/var/www/html/csv/'

logging.basicConfig(filename=os.path.join(LOG_DIR + 'webhook.log'), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
#
# bot_answer = 'Добрый день.\n Благодарим за Ваше обращение в нашу компанию. ' \
#              'Ваша заявка получена и наш специалист скоро свяжется с Вами. ' \
#              'Если Вы хотите ускорить процесс - отправьте нам: \n ' \
#              'Как к Вам можно обращаться (фио) \n ' \
#              'Номер телефона \n ' \
#              'VIN или артикул или название детали\n ' \
#              'и Ваша заявка сразу попадёт в работу.'

sub_user_id = {}


def read_links():
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links


async def re_write_link_v2(chat_id, msg_id):
    links = read_links()
    with open(PATH_DIR + 'links.json', 'w') as file:
        proxy = links.get(chat_id)
        #############{chat_id: (
        # price,
        # target_link,
        # msg_id,
        # user_id,
        # title,
        # first_answer,
        # rewrite_lead,
        # leads_id,
        # contact_id)}
        if len(proxy) == 9:
            links.update(
                {
                    chat_id: (
                        proxy[0],
                        proxy[1],
                        msg_id,
                        proxy[3],
                        proxy[4],
                        proxy[5],
                        proxy[6],
                        proxy[7],
                        proxy[8]
                    )
                }
            )
        if len(proxy) == 7:
            leads_id = 0
            contact_id = 0
            links.update(
                {
                    chat_id: (
                        proxy[0],
                        proxy[1],
                        msg_id,
                        proxy[3],
                        proxy[4],
                        proxy[5],
                        proxy[6],
                        leads_id,
                        contact_id
                    )
                }
            )
        # logging.info('LINKS {}'.format(proxy))
        json.dump(links, file)



# def rewrite_links():
#     with open(PATH_DIR + 'links.json', 'r') as file:
#         links = json.load(file)
#         data = {key: (value[0], value[1], value[2], 353207078) for key, value in links.items()}
#         write_link(data)


def write_link(data):
    links = read_links()
    with open(PATH_DIR + f'links.json', 'w') as file:
        links.update(data)
        # print('links', links)
        json.dump(links, file)


async def wrote_link_v2(data):
    links = read_links()
    with open(PATH_DIR + f'links.json', 'w') as file:
        links.update(data)
        # print('links', links)
        json.dump(links, file)



def re_write_link(chat_id, msg_id):
    links = read_links()
    with open(PATH_DIR + 'links.json', 'w') as file:
        proxy = links.get(chat_id)
        #############{chat_id: (price, target_link, msg_id, user_id, title, first_answer)}
        links.update(
            {
                chat_id: (
                    proxy[0],
                    proxy[1],
                    msg_id,
                    proxy[3],
                    proxy[4],
                    proxy[5]
                )
            }
        )
        # print('links', links)
        json.dump(links, file)


def read_links_v2(chat_id):
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)


async def read_links_v4(chat_id):
    with open(PATH_DIR + 'links.json', 'r') as file:
        links = json.load(file)
        print(links.get(chat_id))
        return links.get(chat_id)

# asyncio.run(read_links_v4('u2i-oQfUJXqCG1jPGgXR8Kx6wQ'))


def read_links_v3(user_id, chat_id):
    name = user_link.get(user_id)[-1]
    with open(PATH_DIR + f'links_{name}.json', 'r') as file:
        links = json.load(file)

        return links.get(chat_id)


# def write_link_v(data, user_id):
#     links = read_links()
#     name = user_link.get(user_id)[-1]
#     with open(PATH_DIR + f'links_{name}.json', 'w') as file:
#         links.update(data)
#         print('links', user_id, links)
#         json.dump(links, file)


def get_creds():
    with open(PATH_DIR + 'cred_update.json', 'r') as file:
        creds = json.load(file)
    # fresh = creds.get('refresh_token')
    # access = creds.get('access_token')

    return creds


def get_creds_avito(user_id):
    with open(PATH_DIR + f'cred_update_avito_{user_id}.json', 'r') as file:
        creds = json.load(file)
        access = creds.get('access_token')

    return access


async def get_creds_avito_v2(user_id):
    with open(PATH_DIR + f'cred_update_avito_{user_id}.json', 'r') as file:
        creds = json.load(file)
        access = creds.get('access_token')

    return access


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


def test_lead_complex():  # (data):
    access_token = creds.get('access_token')
    data = test_compex_data(test)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    metod = '/api/v4/leads/complex'
    link = url + metod
    answer = requests.post(link, headers=headers, json=data)

    return answer.text

# import re
# validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
# re.match(validate_phone_number_pattern, "+12223334444") # Returns Match object

# extract_phone_number_pattern = "\\+?[7-9][0-9]{7,14}"
# re.findall(extract_phone_number_pattern, 'You can reach me out at +12223334444 and +56667778888')


def check_is_phone_number(hook):
    result, target = False, ''
    if hook.get('payload').get('value').get('content') == 'text':
        string = hook.get('payload').get('value').get('content').get('text').strip()
        target = ''.join([i for i in string if i.isdigit()])
    if len(target) == 11 and target[0] == '8':
        result = True
        target = '+7' + target[1:]
    elif len(target) == 10 and target[0] == '9':
        result = True
        target = '+7' + target
    elif len(target) == 11 and target[0] == '7':
        result = True
        target = '+' + target

    return result, target


def update_creds_avito(answer, user_id):
    token_data = json.loads(answer)
    re_access = token_data.get('access_token')
    if re_access:
        f = open(PATH_DIR + f'cred_update_avito_{user_id}.json', 'w')
        cred = {
            "access_token": re_access
        }
        creds = json.dumps(cred)
        f.write(creds)
        f.close()
        print('Creds avito update successfully', user_id)
        result = True
    else:
        result = False
        print('ERPOOR get avito token data', user_id)

    return result


async def update_creds_avito_v2(answer, user_id):
    token_data = json.loads(answer)
    re_access = token_data.get('access_token')
    if re_access:
        f = open(PATH_DIR + f'cred_update_avito_{user_id}.json', 'w')
        cred = {
            "access_token": re_access
        }
        creds = json.dumps(cred)
        f.write(creds)
        f.close()
        print('Creds avito update successfully', user_id)
        result = True
    else:
        result = False
        print('ERPOOR get avito token data', user_id)

    # return result


def read_avito_akk(user_id):
    with open(PATH_DIR + 'avito_akk.json', 'r') as file:
        data = json.load(file)

        return data.get(str(user_id))


async def read_avito_akk_v2(user_id):
    with open(PATH_DIR + 'avito_akk.json', 'r') as file:
        data = json.load(file)

        return data.get(str(user_id))


def all_avito_akk():
    with open(PATH_DIR + 'avito_akk.json', 'r') as file:

        return json.load(file)



def get_avito_token(user_id):
    url = 'https://api.avito.ru/token/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = read_avito_akk(user_id)
    data = {
        "client_id": data.get('avito_key'),
        "client_secret": data.get('avito_secret'),
        "grant_type": "client_credentials"
    }
    answer = requests.post(url=url, headers=headers, data=data)
    print(answer.text)
    update_creds_avito(answer.text, user_id)
    # data = answer.json()
    # print(data)


def get_avito_token_v2():
    for user_id in sender_ids:
        url = 'https://api.avito.ru/token/'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        time.sleep(1)
        data = read_avito_akk(user_id)
        data = {
            "client_id": data.get('avito_key'),
            "client_secret": data.get('avito_secret'),
            "grant_type": "client_credentials"
        }
        answer = requests.post(url=url, headers=headers, data=data)
        print(answer.text)
        update_creds_avito(answer.text, user_id)
        # data = answer.json()
        # print(data)


async def get_avito_token_v3(user_id):
    url = 'https://api.avito.ru/token/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = await read_avito_akk_v2(user_id)
    data = {
        "client_id": data.get('avito_key'),
        "client_secret": data.get('avito_secret'),
        "grant_type": "client_credentials"
    }
    answer = requests.post(url=url, headers=headers, data=data)
    # print('get_avito_token_v3', user_id, answer.text)
    await update_creds_avito(answer.text, user_id)
    # data = answer.json()
    # print(data)


async def make_data_for_avito_v2(data):
    user_id = 0
    logging.info('111444444111 {} '.format(data))
    try:
        chat_id = data.get('message').get('conversation').get('client_id')
    except:
        chat_id = None
        print('FUCK_UP_with_get_chatId_for_avito', data)
    # pre_user_id = read_links_v2(chat_id)
    pre_user_id = await read_links_v4(chat_id)
    if pre_user_id:
        user_id = pre_user_id[3]
        # logging.info('2223333 {} {}'.format(chat_id, user_id))

        # avito_token = get_creds_avito(user_id)
        avito_token = await get_creds_avito_v2(user_id)
        header_avito = {'Authorization': f'Bearer {avito_token}'}
        # user_id = 353207078
        url = f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages'

        try:
            data_text = data.get('message').get('message').get('text')
        except:
            data_text = 'Менеджер уже занят Вашим вопросом. Если Вы торопитесь, то лучше об этом сообщить'
            logging.info('FUCK_UP_with_get_text_for_avito {}'.format(data))

        message = {
            "message": {
                "text": data_text
            },
            "type": "text"
        }
    else:
        logging.info('FUCK_UP_with_chatId_from_amo_1 {} {}'.format(data, pre_user_id))

    if chat_id and user_id:
        answer = requests.post(url, headers=header_avito, json=message)
        response = answer.json()
        if response.get('created'):
            logging.info('ALL_RIDE_make_data_for_avito')
            return True
        else:
            logging.error('FUCK_UP_with_get_answer_json_from_avito {} {}'
                          .format(answer.text))
            return False

    logging.info('FUCK_UP_with_chatId_from_amo_2 {} {}'.format(data, pre_user_id))

# print(read_links_v2('u2i-kIW6LSkhsX~wAx6AKAQfeQ'))


def make_first_answer_avito(chat_id, user_id):
    avito_token = get_creds_avito(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    url = f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages'
    message = {
        "message": {
            "text": bot_answer
        },
        "type": "text"
    }

    if chat_id:
        # time.sleep(1.50)
        answer = requests.post(url, headers=header_avito, json=message)
        response = answer.json()
        if response.get('created'):
            logging.info('ALL_RIDE_make_data_for_avito {} {} {}'
                         .format(chat_id, user_id, answer.text))
            return True
        else:
            print('FUCK_UP_with_get_first_answer_json_from_avito {} {} {}'
                  .format(chat_id, user_id, answer.text))
            return False

        # except:
        #     print('FUCK_UP_with_get&send_chatId_from_amo', answer.text)
        #     return False

    # print('FUCK_UP_with_chatId_from_amo')


async def make_first_answer_avito_v2(chat_id, user_id):
    # avito_token = get_creds_avito(user_id)
    avito_token = await get_creds_avito_v2(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}

    if chat_id:
        url = f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages'
        message = {
            "message": {
                "text": bot_answer
            },
            "type": "text"
        }
        answer = requests.post(url, headers=header_avito, json=message)
        response = answer.json()
        try:
            if response['created']:
                print('ALL_RIDE_make_data_for_avito')
                return True
        except Exception as e:
            print('FUCK_UP_with_get_first_answer_json_from_avito_v2 {} {} {}'.
                  format(answer.text, chat_id, user_id))
            return False

    # proxy = {chat_id: (price, target_link, msg_id, user_id, title, first_answer)}
    # write_link(proxy)

    # print('FUCK_UP_with_chatId_from_amo')


def get_avito_chats_info(user_id):
    avito_token = get_creds_avito(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    # user_id = 353207078
    url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats'
    # params = {
    #    'unread_only': True   ##for unread message only
    # }
    answer = requests.get(url=url, headers=header_avito)
    # print(answer.text)
    raw_data = answer.json()
    # print(len(raw_data['chats']), raw_data['meta'])
    # print(*raw_data['chats'], sep='\n')

    return raw_data


async def get_avito_current_chat_v2(hook, check):
    chat_id = hook.get('payload').get('value').get('chat_id')
    user_id = hook.get('payload').get('value').get('user_id')  # 353207078
    # avito_token = get_creds_avito(user_id)
    avito_token = await get_creds_avito_v2(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    msg_id = hook.get('payload').get('value').get('id')

    title, price, target_link, first_answer, rewrite_lead, leads_id, contact_id \
        = \
        '', '', 'http', False, False, 0, 0
    if not check[1]:  # if is a first message or not
        ## try read current chat
        url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
        answer = requests.get(url=url, headers=header_avito)
        logging.info("GET_AVITO_CURRENT_CHAT_1 {} {} {}"
                     .format(answer.status_code, chat_id, answer.text))
        try:
            raw_data = answer.json()
        except Exception as error:
            raw_data = json.loads(answer.text)
            logging.error('Some_fuck_up_load_json_from avito_chat {} {} {}'
                          .format(answer.text, chat_id, user_id))
        author_id = hook.get('payload').get('value').get('author_id')
        # await make_message_for_amo(hook, raw_data, author_id)
        await make_message_for_amo_v2(hook, raw_data, author_id, False)
        logging.info('SEND_DATA_FOR_MESSAGE_TO_AMO_2_ {} {}'
                     .format(chat_id, user_id))
        # resp = make_first_answer_avito(chat_id, user_id)
        resp = await make_first_answer_avito_v2(chat_id, user_id)
        logging.info('SEND_DATA_FOR__AMO_2_  {}'.format(resp))
        # We await response, but this is so long and we get another hook
        if resp:
            first_answer = True
        ### if avito token expired
        try:
            expired = raw_data.get('result').get('message')
        except:
            expired = 'not access token expired'
        if expired == 'access token expired':
            get_avito_token(user_id)
            # avito_token = get_creds_avito(user_id)
            avito_token = await get_creds_avito_v2(user_id)
            header_avito = {'Authorization': f'Bearer {avito_token}'}
            url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
            answer = requests.get(url=url, headers=header_avito)
            logging.info("reTRY_GET_AVITO_CHAT {} {}"
                         .format(answer.status_code, chat_id))
            raw_data = answer.json()
            logging.info("reTRY_GET_AVITO_CHAT"
                         .format(answer.status_code))
            # resp = make_first_answer_avito(chat_id, user_id)
            resp = await make_first_answer_avito_v2(chat_id, user_id)
            if resp:
                first_answer = True
        try:
            price = raw_data.get('context').get('value').get('price_string')
            target_link = raw_data.get('context').get('value').get('url')
            title = raw_data.get('context').get('value').get('title')
        except Exception as err:
            print("FUCK UP get_avito_price_string_chat {}".format(err))

        proxy = {chat_id: 
                     (price, 
                      target_link,
                      msg_id, 
                      user_id,
                      title, 
                      first_answer, 
                      rewrite_lead,
                      leads_id,
                      contact_id )
                 }
        await wrote_link_v2(proxy)
        # await rewrite_leads(chat_id)
        logging.info('WROTE_DATA_FOR___33 {}'.format(proxy))
        await rewrite_leads_v2(chat_id, user_id)
        logging.info('TRY_REWRITE_DATA_TO_AMO_1 {} {} {} {} '.
                     format(chat_id, user_id, title, target_link))

    ### Now in there no send
    elif not check[0]:  # if it's a message exist  or not
        url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
        answer = requests.get(url=url, headers=header_avito)
        logging.info("GET_AVITO_CURRENT_CHAT_2 {} {} {}"
                     .format(answer.status_code, chat_id, user_id))
        raw_data = answer.json()
        try:
            expired = raw_data.get('result').get('message')
        except:
            expired = 'not access token expired'
        if expired == 'access token expired':
            get_avito_token(user_id)
            avito_token = get_creds_avito(user_id)
            header_avito = {'Authorization': f'Bearer {avito_token}'}
            url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
            answer = requests.get(url=url, headers=header_avito)
            logging.info("reTRY_GET_AVITO_CURRENT_CHAT4 {} {} {}"
                         .format(answer.status_code, chat_id, user_id))
            raw_data = answer.json()
            logging.info("reTRY_GET_AVITO_CURRENT_CHAT5 {} {}"
                         .format(answer.status_code, user_id))

        # re_write_link(chat_id, msg_id)
        await re_write_link_v2(chat_id, msg_id)

        author_id = hook.get('payload').get('value').get('author_id')
        await make_message_for_amo_v2(hook, raw_data, author_id, False) # True)
        logging.info('SEND_DATA_FOR_MESSAGE_TO_AMO_3_ {} {} {}'
                     .format(chat_id, user_id, check))

        if not check[2]:
            try:
                await rewrite_leads_v2(chat_id, user_id)
                logging.info('TRY_REWRITE_DATA_TO_AMO_11_ {} {} {} {} '.
                             format(chat_id, user_id, title, target_link))
            except:
                logging.info('FuckUp_TRY_REWRITE_DATA_TO_AMO_ {} {} {} {} '.
                         format(chat_id, user_id, title, target_link))

    elif not check[2]:
        # try:
        await rewrite_leads_v2(chat_id, user_id)
        logging.info('TRY_REWRITE_DATA_TO_AMO_111_{} {} {} {} '.
                     format(chat_id, user_id, title, target_link))

    else:
        print("WE ALREADY HAVE THIS MESSAGE", chat_id)

    # return raw_data


async def get_avito_current_chat(chat_id, hook):
    user_id = hook.get('payload').get('value').get('user_id')  # 353207078
    avito_token = get_creds_avito(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    msg_id = hook.get('payload').get('value').get('id')
    author_id = hook.get('payload').get('value').get('author_id')
    check = check_is_exist(msg_id, chat_id)
    if not check:
        url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
        answer = requests.get(url=url, headers=header_avito)
        logging.info("GET_AVITO_CURRENT_CHAT_3 {} {}".format
                     (answer.status_code, chat_id))
        raw_data = answer.json()
        print(1111111111, raw_data)
        try:
            expired = raw_data.get('result').get('message')
        except:
            expired = 'not access token expired'
        if expired == 'access token expired':
            get_avito_token(user_id)
            url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/{chat_id}'
            answer = requests.get(url=url, headers=header_avito)
            logging.info("reTRY_GET_AVITO_CURRENT_CHAT6 {} {}".format
                         (answer.status_code, chat_id))
            raw_data = answer.json()
            print(1112222111, raw_data)
            logging.info("reTRY_GET_AVITO_CURRENT_CHAT7 {} {}".format
                         (answer.status_code, chat_id))
        price, target_link, title = '', '', ''
        try:
            price = raw_data.get('context').get('value').get('price_string')
            target_link = raw_data.get('context').get('value').get('url')
            title = raw_data.get('context').get('value').get('title')
        except Exception as err:
            print("FUCK UP get_avito_price_string_chat {}".format(err))

        proxy = {chat_id: (price, target_link, msg_id, user_id, title, False, 0, 0)}
        write_link(proxy)

        try:
            sender_id = str(raw_data.get('last_message').get('author_id'))
        except:
            sender_id = ''
            print('WE GET TROUBLE for get sender_id')
        if author_id in sender_ids:  # and sender_id != '353207078':  #str(add_data.get('context').get('value').get('user_id'))
            await rewrite_leads(chat_id)
            logging.info('TRY_REWRITE_DATA_TO_AMO ' + str(chat_id))
        elif raw_data and author_id not in sender_ids:
            # await make_message_for_amo(hook, raw_data, sender_id)
            logging.info('SEND_DATA_FOR_MESSAGE_TO_AMO_4_ ' + str(chat_id))
    else:
        print('WE ALREADY HAS it the MESSAGE', chat_id)

        # return raw_data


def enable_avito_webhook(user_id):
    avito_token = get_creds_avito(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    data = {
        'url': 'https://phone-call.i-bots.ru/webhook'
    }
    url = 'https://api.avito.ru/messenger/v3/webhook'
    answer = requests.post(url=url, headers=header_avito, json=data)
    print('enable_avito_webhook', answer.text)


def  disable_avito_webhook(user_id):
    avito_token = get_creds_avito(user_id)
    header_avito = {'Authorization': f'Bearer {avito_token}'}
    data = {
        'url': 'https://phone-call.i-bots.ru/webhook'
    }
    url = 'https://api.avito.ru/messenger/v1/webhook/unsubscribe'
    answer = requests.post(url=url, headers=header_avito, json=data)
    print('enable_avito_webhook', answer.text)


def get_current_hook():
    url = 'https://api.avito.ru/messenger/v1/subscriptions'
    for user_id in sender_ids:
        time.sleep(1)
        avito_token = get_creds_avito(user_id)
        header_avito = {'Authorization': f'Bearer {avito_token}'}
        answer = requests.post(url, headers=header_avito)

        print(user_id, answer.text)


heck = {'id': 'd8e51513-9229-4497-94c6-69dc65ffedab', 'version': 'v3.0.0', 
        'timestamp': 1706865998, 
        'payload': {
            'type': 'message', 
            'value': {
                'id': 'c1348bb968650a00e693d87e0e5e7e92', 
                'chat_id': 'u2i-YvRiaEtf8Qn~N4sh3mMKkA', 
                'user_id': 369223108, 'author_id': 459734245, 'created': 1706865998, 'type': 'text', 'chat_type': 'u2i', 'content': {'text': 'планируется поставка?'}, 'item_id': 4098549657}}}


# import asyncio
# asyncio.run(get_avito_current_chat('u2i-YvRiaEtf8Qn~N4sh3mMKkA', heck))
#
# #
# get_avito_token(369221904)

# get_avito_token(369222788)
# get_avito_token(369721092)

# get_avito_token(369721092)
# get_avito_token(10138154)
# # # get_vito_current_chat('u2i-plZ1VOkef3W2z8rMnrNHDg')
# enable_avito_webhook(353207078)
# enable_avito_webhook(369721092)
# write_link({'u2i-sjJYEdKG89VKhGV6SDQIEw': ('5\xa0691 ₽', 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/standart_3396397474')})
# hook = {'id': '97d14aac-97ac-40de-9220-4e6bdea78c5d', 'version': 'v3.0.0', 'timestamp': 1693842617, 'payload': {'type': 'message', 'value': {'id': '72ab5028eb846209e22f1c132e44a29e', 'chat_id': 'u2i-TOYzRVLyb9Hw_l7u2aBTVg', 'user_id': 353207078, 'author_id': 259749082, 'created': 1693842617, 'type': 'text', 'chat_type': 'u2i', 'content': {'text': 'Покупку произвести у вас непосредственно там, на месте можно при осмотре.'}, 'item_id': 3364311913}}}
# result = hook.get('payload').get('value').get('chat_id')
# rewrite_links()
# print(read_avito_akk(357922774))
# get_avito_token(369721092)


# get_avito_token_v2()
# get_current_hook()
# disable_avito_webhook(10138154)

