# -- coding: utf-8 --
import threading
import datetime
import os
import sys
import logging
import copy
import pdfplumber

import ms
import ozon
import json
import time
from database import MsDatabase

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, DB_DICTS, PUBLIC_DIR, LOG_FILE, \
    OZON_ORDERS_HOURS, MS_DEFAULT_ORGANIZATION, MS_DEFAULT_STORE, OZON_COMMENT_FIELDS, ORDERS_LOG_FILE, \
    MS_DEFAULT_STATUS, LABEL_DIR, SLEEP_TIME, MS_DEFAULT_PRICE, OZON_HOURS_BEFOR_DELIVERED, MS_CANCELED_STATUS, \
    MS_FIELD_SOBRAN_BOOL, MS_FIELD_SOBRAN_INT, OZON_SLEEP_TIME


def check_divide_orders(list_postings, stores, divide_count): #check seller ordderress list
    print('#' * 49)
    print('11111', type(list_postings), len(list_postings))
    count_quan = []
    result = False
    # position_count = len(posting['products'])

    for posting in list_postings:   #posting is dict
        count = 0
        if posting.get('status') != 'awaiting_packaging':
            continue
        else:
            store = posting.get('delivery_method')['warehouse_id']
            # print("STORE_FROM_POSTING", store, type(store))
            type_store = stores.get(str(store))
            if type_store != 'fbs':
                continue
            else:
                index = (0,)
                for prods in posting['products']:
                    quantity = prods['quantity']
                    if quantity == divide_count: ##check need divide
                        continue
                    else:
                        count += quantity       #count quantity all positions

                if count > divide_count:  # and type_store == 'fbs':
                    print('!' * 100)
                    print('1_check_divide_orders', datetime.datetime.now(), 'products', len(posting['products']), 'quantity',
                          posting['products'][0]['quantity'], posting['products'], posting.get('posting_number'))
                    # posting_number = posting['posting_number']
                    index = (list_postings.index(posting), count)
                    count_quan.append(index)
                    result = True

                print('CHEcked_position_index_&_count', index)
    return result, count_quan,


def divide_order(posting_enum, header, divide_slice, total_count):
    shipments = posting_enum['financial_data']['products']
    total_proxy, prev_position = [], []
    for position in shipments:
        print('POSITION_FOR_DIVIDE', position)
        count_product = position['quantity']
        product_id = position['product_id']  #positon['financial_data']['products'][0]['product_id']

        while total_count >= divide_slice:
            if count_product >= divide_slice:  # division without remainder
                proxy_pac = {
                    'products': [
                        {
                            "product_id": product_id,
                            "quantity": divide_slice
                        }
                    ]
                }
                total_proxy.append(proxy_pac)
                count_product -= divide_slice
                total_count -= divide_slice
                if total_count == 0:
                    break
                print('count_prod--1', count_product, 'total_count--1', total_count, total_proxy)

            elif count_product < divide_slice and len(prev_position) == 0 and count_product != 0:
                prev_position = position.copy() #create and save remainder
                prev_position['quantity'] = count_product
                print('remainder---1111', count_product, 'total_count---1111', total_count)
                continue

            elif  count_product < divide_slice and len(prev_position) > 0 and count_product != 0:  #check remainder -> it's second and other division
                prev_reminder = prev_position['quantity']
                if prev_reminder + count_product >= divide_slice  and count_product != 0:
                    proxy_pac = {
                    'products': [
                            {
                                "product_id": prev_position['product_id'],
                                "quantity": prev_reminder
                            },
                            {
                                "product_id": product_id,
                                "quantity": divide_slice - prev_reminder #if
                            }
                        ]
                    }
                    total_proxy.append(proxy_pac)
                    count_product -= divide_slice - prev_reminder
                    total_count -= divide_slice
                    if total_count == 0:
                        break
                    prev_position.clear()
                    prev_position = position.copy()  # REcreate and save remainder
                    prev_position['quantity'] = count_product
                    print('count_prod---333', count_product, 'total_count--333', total_count)

                elif prev_reminder + count_product <= divide_slice  and count_product != 0:
                    proxy_pac = {
                        'products': [
                            {
                                "product_id": prev_position['product_id'],
                                "quantity": prev_reminder
                            },
                            {
                                "product_id": product_id,
                                "quantity": count_product
                            }
                        ]
                    }
                    total_proxy.append(proxy_pac)
                    count_product = 0
                    total_count -= count_product - prev_reminder
                    print('count_prod---444', count_product, 'total_count--444', total_count)

        else:
            proxy_pac = {
                'products': [
                    {
                        "product_id": product_id,
                        "quantity": count_product
                    }
                ]
            }
            total_proxy.append(proxy_pac)  #

    data = {
            "packages": total_proxy,
                # {
                #     "products": total_proxy
                # }
          # ],
          "posting_number": posting_enum['posting_number'],
          "with": {
              "additional_data": True
                }
          }
    print('DATA_DIVIDE', data)

    re_data = ozon.divide_orders_v4(data, header)
    if re_data[0]:
        print('RESULT_DATA_DIVIDE', datetime.datetime.now(), data, 're_data', type(re_data), re_data)
        return re_data[1]
    else:
        return 'INCORRECT_STATUS'


# def send_discount(header, seller, products):
#     list_target = [tpl for tpl in products if tpl[-1]]  ##TODO
#     if len(list_target) > 0:
#         for prods in list_target:
#             data = {
#                 "discount": prods[-1],
#                 "product_id": prods[0]
#                 }
#             result = ozon.send_discount(data, header)
#             if result:
#                 print("All ride", prods[0])
#             else:
#                 print("ERRoorr ", prods[0], prods[5])


# if __name__ == '__main__':

def start_orders():
    ################ TESTS #################
    # with open('tmp', 'rb') as f:
    #     data = f.read()
    #     t = bytes(data)
    #     # t2 = binascii.hexlify(t)
    #     print(t.decode('cp1251', errors='ignore'))
    #
    #     data2 = psycopg2.Binary(data)
    #
    #     bdata = io.BytesIO(data)
    #     print(bdata)
    #
    #     t = bytes(data)
    #
    #     print(data)
    #
    #     x = binascii.unhexlify(t)
    #     print(x)
    #
    #     t2 = binascii.hexlify(t)
    #
    #     print(psycopg2.Binary(data))
    #     # print(t2)
    #     enc = chardet.detect(t2)
    #     print(enc)
    #
    #     print(t2.decode('utf-8-sig'))
    #     # print(t.decode('utf-8-sig'))
    #     # t = t.decode('latin-1').encode("utf-8")
    #     # print(t.decode('utf-8-sig'))
    #
    #
    # order_href = 'eefa780a-f79f-11ec-0a80-0581000fd4e7'
    # file_path = os.path.join(PUBLIC_DIR + LABEL_DIR, f'17519790-0058-2.pdf')
    # print(ms.post_order_file(order_href, file_path))
    # print(ms.get_entity_meta('customerorder/2a401ffb-f7a3-11ec-0a80-0eb10010641e'))
    # print(ms.get_last_orders_w_demand())
    # ms.get_prices_id_name()
    # sys.exit(0)

    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    # sellers = db.get_active_sellers_all()
    # for seller in sellers:
    #     seller_id = seller[3]
    #     token = seller[4]
    #     header = ozon.get_header(token, seller_id)
    #     orders = ozon.get_orders_v2(48, header)
    #     for order in orders:
    #         # print(order)
    #         posting_number = order['posting_number']
    #         order_res = ozon.get_fbs_order_barcode(posting_number, header)
    #         # print(order_res)
    #         for product in order['products']:
    #             raw_tmp = db.get_product_href_delive(seller_id, product['offer_id'])
    #             print(raw_tmp[0][1], int(raw_tmp[0][1]) * 100)
    # exit(0)

    # seller_id = '118614'
    # token = '7660a38f-a39b-4a9a-99a4-32c5ffb44edf'
    # header = ozon.get_header(token, seller_id)
    # # orders = ozon.get_orders_v2(OZON_ORDERS_HOURS, header)
    # # print(orders)
    # posting_number = '42526611-0040-1'
    # print(ozon.get_fbs_order_v3('42526611-0040-1'))
    # label_file_path = os.path.join(PUBLIC_DIR + LABEL_DIR, f'{posting_number}.pdf')
    # with pdfplumber.open(label_file_path) as pdf_file:
    #     pdf_page = pdf_file.pages[0]
    #     pdf_text = pdf_page.extract_text()
    # label_up_code = pdf_text.split('\n')[0]
    # print(label_up_code)
    # exit(0)

    ########################################
    logging.basicConfig(filename=os.path.join(PUBLIC_DIR, ORDERS_LOG_FILE),
                        format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info('=' * 50)
    logging.info('Cron orders Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)

    sellers = db.get_active_sellers_all()
    # print(sellers)
    # exit(0)
    for seller in sellers:
        seller_id = seller[3]
        token = seller[4]
        name = seller[2]
        contragent_fbs = seller[7]
        organization = seller[12]
        store = seller[11]
        comment_fbs = seller[8]
        usluga_fbs = seller[14]
        status_fbs = seller[6]
        date_field = seller[5]
        usluga_price_ms_fbs = seller[15]

        status_realfbs = seller[16]
        contragent_realfbs = seller[17]
        comment_realfbs = seller[18]
        usluga_realfbs = seller[19]
        usluga_price_ms_realfbs = seller[20]
        price_id = seller[21]
        cancell_status = seller[22]
        divide = seller[23]
        divide_count = seller[24]
        if not price_id:
            price_id = MS_DEFAULT_PRICE

        logging.info(f'Seller {seller_id} orders')
        header = ozon.get_header(token, seller_id)

        ###################### realFBS delivery #########################
        proces_status_dict = dict()
        #### STATUS last-mile
        raw_ozon_current_orders = db.get_last_orders_href(seller_id, status='delivering')
        ozon_current_orders_set = {i[0] for i in raw_ozon_current_orders}

        ms_last_demand_orders = ms.get_last_orders_w_demand()

        last_mile_orders = ozon_current_orders_set & ms_last_demand_orders
        for ms_href in last_mile_orders:
            raw_posting_number = db.get_order_posting_number_by_href(seller_id, ms_href)
            try:
                posting_number = raw_posting_number[0]
            except:
                continue
            cur_status = ozon.get_fbs_order_status(posting_number, header)
            logging.info(f"Order {posting_number} cur status - {cur_status}")
            if ozon.order_status_last_mile(posting_number, header):
                logging.info(f"OK changing status to last-mile in order {posting_number} in Ozon")
                db.update_oder_status(seller_id, posting_number, 'last-mile')
                proces_status_dict[posting_number] = 'last-mile'
                # logging.info(f"posting_number: {posting_number}, proces_status_dict: {proces_status_dict}")
                # time.sleep(OZON_SLEEP_TIME)
                # db.reconnect()
            else:
                logging.warning(f"KO changing status to last-mile in order {posting_number} in Ozon")
        #### STATUS delivered
        raw_last_mile_orders = db.get_orders_date_by_status(seller_id, 'last-mile')
        for elem in raw_last_mile_orders:
            posting_number = elem[0]
            shipment_date_str = elem[1]
            try:
                shipment_date = datetime.datetime.strptime(shipment_date_str, "%Y-%m-%dT%H:%M:%SZ")
            except:
                continue
            now_date = datetime.datetime.now()
            diff_date = shipment_date - now_date
            if diff_date.total_seconds() < OZON_HOURS_BEFOR_DELIVERED * 60 * 60:
                if ozon.order_status_delivered(posting_number, header):
                    logging.info(f"OK changing status to delivered in order {posting_number} in Ozon")
                    db.update_oder_status(seller_id, posting_number, 'delivered')
                    proces_status_dict[posting_number] = 'delivered'
                    # time.sleep(OZON_SLEEP_TIME)
                    # db.reconnect()
                # else:
                #     logging.warning(f"KO changing status to delivered in order {posting_number} in Ozon")
            # logging.info(f"{posting_number} {shipment_date_str}")
            # print(posting_number, shipment_date_str)

        #################################################################

        if not organization:
            organization = MS_DEFAULT_ORGANIZATION
        if not store:
            store = MS_DEFAULT_STORE
        if not status_fbs:
            status_fbs = MS_DEFAULT_STATUS
        if not status_realfbs:
            status_realfbs = MS_DEFAULT_STATUS
        if not contragent_fbs and not contragent_realfbs:
            continue

        organization_meta = {
            "href": f"https://online.moysklad.ru/api/remap/1.2/entity/organization/{organization}",
            "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/organization/metadata",
            "type": "organization",
            "mediaType": "application/json",
            "uuidHref": f"https://online.moysklad.ru/app/#mycompany/edit?id={organization}"
        }

        store = {
            "meta": {
                "href": f"https://online.moysklad.ru/api/remap/1.2/entity/store/{store}",
                "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/store/metadata",
                "type": "store",
                "mediaType": "application/json",
                "uuidHref": f"https://online.moysklad.ru/app/#warehouse/edit?id={store}"
            }
        }

        seller_stores = seller[13]
        try:
            seller_stores = json.loads(seller_stores)
        except:
            seller_stores = {}

        orders = ozon.get_orders_v2(OZON_ORDERS_HOURS, header)
        # orders = ozon.get_orders_v3(OZON_ORDERS_HOURS, header)
        logging.info(f"Summary {len(orders)} orders in {OZON_ORDERS_HOURS} hours")

        for orde in orders:
            print('ORRDERRS_BEFORE_CHECK_DIVIDE', name, divide, divide_count,
                  orde.get('posting_number'), orde.get('status'))

        # continue
        #
        ##################CUSTOM DIVIDE###############
        o_stores = seller[13]

        if divide == 1:
            # print('divide', seller_stores)
            check = check_divide_orders(orders, seller_stores, divide_count)
            if check[0]:
                # raw_divide_orders = []
                divide_posting_number, divided_post = [], []
                print('check_len_orders', len(orders))
                for i in check[1]: #we get [1]  list of typles index & count all positions
                    oreder = orders.pop(i[0])
                    raw_posting_list = divide_order(oreder, header, divide_count, i[1])
                    print('CHECK!!!!', i, len(orders), oreder)
                    if raw_posting_list != 'INCORRECT_STATUS':
                        # raw_divide_orders.append(raw_posting_list)
                        # raw_divide_orders.extend(raw_posting_list)
                        print('RAW_divide_orders', raw_posting_list)
                        logging.info(f'divide order  {oreder} to_list_divided {raw_posting_list}')
                        if raw_posting_list is not None:
                            for post in raw_posting_list:
                                post_num = post.get('posting_number')
                                divided_post = ozon.get_fbs_order_v4(post_num, header)
                                divide_posting_number.append(divided_post)
                print('FIN_CHECK', len(orders), len(divide_posting_number))
                orders.extend(divide_posting_number)
                # orders.append(divided_post)
                print('LEN_ORDERS_&_DIVIDE_ORDERS', len(orders), len(divide_posting_number))

        ##################CUSTOM DIVIDE###############

        for order in orders:
            # logging.info(f'order__ {order.get("posting_number"), order.get("status")}')
            # print('order__type', type(order))
            if isinstance(order, str):
                print('ORDER_STRING', type(order), order)
            # print(ozon.get_fbs_order(order['posting_number'], header))
            # continue
            if not order:
                continue

            posting_number = order['posting_number']

            logging.info("-" * 50)
            logging.info(f"Oder {posting_number} processing")

            if posting_number in proces_status_dict: #FIXME 15/09 - for Delivered status form last-mile
                logging.info(f"API order['status']: {order['status']}")
                order['status'] = proces_status_dict[posting_number]
                logging.info(f"Set order['status'] param to {order['status']}")
            moment_date = order.get(date_field)

            # label_file_path = os.path.join(PUBLIC_DIR + LABEL_DIR, f'{posting_number}.pdf')
            # label_res = ozon.order_label(posting_number, label_file_path)
            # logging.info(f"Label {posting_number} is {label_res}")
            # continue
            # order_id = order['order_id']
            # order_number = order['order_number']
            # status = order['status']
            try:
                warehouse_id = str(order['delivery_method']['warehouse_id'])
            except:
                logging.info(f"Warehouse_id error, Continue")
                continue
            if warehouse_id not in seller_stores or not seller_stores[warehouse_id]:
                logging.info(f"Not our Warehouse, Continue")
                continue

            raw_ms_order_id = db.get_order_id_href_label(seller_id, posting_number)
            try:
                order_id = raw_ms_order_id[0][0]
                order_href = raw_ms_order_id[0][1]
                label = raw_ms_order_id[0][2]
            except:
                order_id = ''
                order_href = ''
                label = 0

            ############ Если отмененный заказ ############
            if order['status'] == 'cancelled' and order_href:
                db_href_status = db.get_order_href_status(seller_id, posting_number)
                if db_href_status and db_href_status[1] == 'cancelled':
                    ########################### Зашиваем новую логику проверки "снял ли галку Собрано Мендежру у отмененного заказа" ########################
                    atrs_dict = ms.get_order_attributes(db_href_status[0], [MS_FIELD_SOBRAN_BOOL, MS_FIELD_SOBRAN_INT])
                    atrs_flag = 0
                    for key in atrs_dict:
                        if atrs_dict[key]:
                            atrs_flag = 1
                            break
                    if not atrs_flag:
                        logging.info(f"Canceled order already properly marked in MS. Continue.")
                        continue
                if not cancell_status:
                    cancell_status = MS_CANCELED_STATUS
                raw_old_comment = db.get_order_comment(seller_id, posting_number)
                if raw_old_comment:
                    comment_text = raw_old_comment[0] + '\n' + 'ОТМЕНА'
                else:
                    comment_text = 'ОТМЕНА'
                ms.update_order_comment(order_href, comment_text)
                ms.update_order_status(order_href, cancell_status)
                db.update_oder_status(seller_id, posting_number, 'cancelled')
                logging.info(f"Order Canceled in Ozon. Only updating Status and Comment in MS.")
                continue

            if seller_stores[warehouse_id] == 'realfbs':
                fbs = 0
                logging.info("realfbs")
                contragent_meta = {
                    "href": f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{contragent_realfbs}",
                    "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
                    "type": "counterparty",
                    "mediaType": "application/json",
                    "uuidHref": f"https://online.moysklad.ru/app/#company/edit?id={contragent_realfbs}"
                }
                status_meta = {
                    "meta": {
                        "href": f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/{status_realfbs}",
                        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
                        "type": "state",
                        "mediaType": "application/json"
                    }
                }
                comment = comment_realfbs
                usluga = usluga_realfbs
                usluga_price_ms = usluga_price_ms_realfbs
                try:
                    address = order['customer']['address']['address_tail']
                    # customer_comment = order['customer']['address']['comment']
                    # print(address)
                except:
                    address = None
                if address:
                    ######## Очищаю адрес ########
                    try:
                        city = order['customer']['address']['city'] + ', '
                        address = address.replace(city, '')
                    except:
                        pass
                    try:
                        country = order['customer']['address']['country'] + ', '
                        address = address.replace(country, '')
                    except:
                        pass
                    try:
                        region = order['customer']['address']['region'] + ', '
                        address = address.replace(region, '')
                    except:
                        pass
                    try:
                        zip_code = order['customer']['address']['zip_code'] + ', '
                        address = address.replace(zip_code, '')
                    except:
                        pass
                    ###############################
            else:
                fbs = 1
                logging.info("fbs")
                status_meta = {
                    "meta": {
                        "href": f"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/{status_fbs}",
                        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
                        "type": "state",
                        "mediaType": "application/json"
                    }
                }
                contragent_meta = {
                    "href": f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{contragent_fbs}",
                    "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
                    "type": "counterparty",
                    "mediaType": "application/json",
                    "uuidHref": f"https://online.moysklad.ru/app/#company/edit?id={contragent_fbs}"
                }
                comment = comment_fbs
                usluga = usluga_fbs
                usluga_price_ms = usluga_price_ms_fbs
                address = None

            # print(address)
            # continue
            res_products = []
            products = []
            delive = 0
            setted_discount = 0

            for product in order['products']:
                elem_dict = {}
                elem_dict['offer_id'] = product['offer_id']

                # raw_tmp = db.get_product_href_delive(seller_id, elem_dict['offer_id'])
                raw_tmp = db.get_product_href_delive_v2(seller_id, elem_dict['offer_id'])
                try:
                    elem_dict['href'] = raw_tmp[0][0]
                except:
                    continue
                if not elem_dict['href'] or elem_dict['href'] == '0':
                    continue

                try:
                    elem_dict['delive'] = int(raw_tmp[0][1])
                except:
                    elem_dict['delive'] = 0
                if elem_dict['delive'] > delive:
                    delive = elem_dict['delive']

                try:
                    elem_dict['set_discount'] = int(raw_tmp[0][2])
                except:
                    continue

                elem_dict['sku'] = product['sku']
                elem_dict['name'] = product['name']
                elem_dict['quantity'] = product['quantity']
                # elem_dict['price'] = ms.get_opt_product_price(elem_dict['href'])
                elem_dict['price'] = ms.get_product_price(elem_dict['href'], price_id)

                # elem_dict['mark'] = #TODO маркировка

                # print(elem_dict)
                res_products.append(elem_dict) #res_products - меняется в процессе
                products.append(elem_dict)
            if not res_products:
                logging.info(f"Products 0, Continue")
                continue

            # print(1, delive)
            if usluga_price_ms:
                delive = ms.get_usluga_price(usluga)

            # print(2, delive)
            # continue

            # res_products.append({'quantity': 1, 'price': elem_dict['delive'], 'href': usluga})
            products_meta = ms.make_products_meta_v2(res_products, reserve=True)
            # products_meta = ms.make_products_meta(res_products, reserve=True)
            if usluga and usluga != '0': #FIXME del and delive
                usluga_meta = ms.make_service_meta({'quantity': 1, 'price': delive, 'href': usluga, 'vat': 0})
                products_meta.append(usluga_meta)
            print('products_meta', products_meta)

            # order_name = f"{name}_{str(posting_number)}"
            if moment_date:
                moment = moment_date.replace('T', ' ').replace('Z', '')
            else:
                moment = None

            ################# Верхний код ##################
            order['label_up_code'] = ''
            order['label_down_code'] = ''
            if fbs:
                barcodes = ozon.get_fbs_order_barcode(posting_number, header)
                # logging.info(f"Barcodes {barcodes}")
                if barcodes:
                    order['label_up_code'] = barcodes[0]
                    order['label_down_code'] = barcodes[1]

            # if label:
            #     label_file_path = os.path.join(PUBLIC_DIR + LABEL_DIR, f'{posting_number}.pdf')
            #     try:
            #         with pdfplumber.open(label_file_path) as pdf_file:
            #             pdf_page = pdf_file.pages[0]
            #             pdf_text = pdf_page.extract_text()
            #         order['label_up_code'] = '%101%' + pdf_text.split('\n')[0]
            #     except:
            #         order['label_up_code'] = ''

            ###################### Comments ########################
            comment_copy = '%s' % comment
            for field in OZON_COMMENT_FIELDS:
                if field in comment:
                    ######## PHONE #########
                    if field == 'PHONE':
                        phone = ozon.get_fbs_order_phone(posting_number, header)
                        comment_copy = comment_copy.replace(field, phone)
                        continue
                    ########################
                    path = OZON_COMMENT_FIELDS[field].split('/')
                    value = copy.deepcopy(order)
                    # print(path)
                    for pt in path:
                        try:
                            value = value.get(pt)
                            if pt.find('_date') != -1:
                                dt_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                                value = dt_obj.strftime("%d.%m.%Y %H:%M")
                            # print(value)
                        except:
                            break
                    if not isinstance(value, str):
                        value = ''
                    comment_copy = comment_copy.replace(field, value)

            # logging.info('cron_orders comment_copy', comment_copy)
            ###########################################################

            if not order_id:
                if address:
                    order_id, order_href = ms.post_order(contragent_meta, products_meta, organization_meta,
                                                         comment_copy, address, store=store, moment=moment,
                                                         status=status_meta)
                else:
                    order_id, order_href = ms.post_order(contragent_meta, products_meta, organization_meta,
                                                         comment_copy, posting_number, store=store, moment=moment,
                                                         status=status_meta)
                logging.info(f"Order {posting_number} was add to MS as {order_id}")
            elif fbs: # Обвноляем сделку только у FBS
                raw_old_comment = db.get_order_comment(seller_id, posting_number)
                if raw_old_comment and comment_copy != raw_old_comment[0]:
                    if not ms.update_order_comment(order_href, comment_copy):
                        logging.warning(f"Error updating comment {comment_copy} in MS order {order_href}")
                    else:
                        logging.info(f"OK updating comment {comment_copy} in MS order {order_href}")
                # else:
                #     logging.warning(f"No reason to update comment - raw_old_comment {raw_old_comment}, comment_copy {comment_copy}")
                # logging.info(f"Order {order_id} allready in DB, just updating")

            if not order_id:
                logging.warning(f"Error creating order {posting_number} in MS")
                # print(f"Error creating order {posting_number} in MS")
                order_id = ''
            else:
                order_id = str(order_id)
            # print(order_id)

            ############ Статусы ##########
            logging.info(f"Order state {order['status']}")
            # if seller_stores[warehouse_id] == 'realfbs':
            if not fbs:
                ################### realFBS ######################
                # if order['status'] == 'awaiting_packaging':
                #     if ozon.order_status_awaiting_delivery(posting_number, header):
                #         logging.info(f"OK changing status to awaiting_deliver in order {posting_number} in MS")
                #         order['status'] = 'awaiting_delivery'
                #     else:
                #         logging.warning(f"KO changing status to awaiting_deliver in order {posting_number} in MS")
                if order['status'] in ('awaiting_approve', 'awaiting_packaging'):
                    package_products = ozon.prepare_products_for_ship(products)
                    if ozon.order_status_ship(posting_number, package_products, header):
                        logging.info(f"OK changing status to awaiting_deliver in order {posting_number} in MS")
                        order['status'] = 'awaiting_deliver'
                        time.sleep(SLEEP_TIME)
                    else:
                        logging.warning(f"KO changing status to awaiting_deliver in order {posting_number} in MS")
                if order['status'] == 'awaiting_deliver':
                    if ozon.order_status_delivery(posting_number, header):
                        logging.info(f"OK changing status to delivering in order {posting_number} in MS")
                        order['status'] = 'delivering'
                    else:
                        logging.warning(f"KO changing status to delivering in order {posting_number} in MS")

            else:
                ################### FBS ######################
                # if order['status'] == 'awaiting_approve':
                #     package_products = ozon.prepare_products_for_ship(products)
                #     if ozon.order_status_ship(posting_number, package_products, header):
                #         logging.info(f"OK changing status to awaiting_packaging in order {posting_number} in MS")
                #         order['status'] = 'awaiting_packaging'
                #     else:
                #         logging.warning(f"KO changing status to awaiting_packaging in order {posting_number} in MS")
                # elif order['status'] == 'awaiting_packaging':
                #     if ozon.order_status_awaiting_delivery(posting_number, header):
                #         logging.info(f"OK changing status to awaiting_deliver in order {posting_number} in MS")
                #         order['status'] = 'awaiting_delivery'
                #     else:
                #         logging.warning(f"KO changing status to awaiting_deliver in order {posting_number} in MS")

                if order['status'] in ('awaiting_approve', 'awaiting_packaging'):
                    # print('fbs')
                    package_products = ozon.prepare_products_for_ship(products)
                    if ozon.order_status_ship(posting_number, package_products, header):
                        logging.info(f"OK changing status to awaiting_deliver in order {posting_number} in MS")
                        order['status'] = 'awaiting_deliver'
                        time.sleep(SLEEP_TIME)
                    else:
                        logging.warning(f"KO changing status to awaiting_deliver in order {posting_number} in MS")

                if not label:
                    label_file_path = os.path.join(PUBLIC_DIR + LABEL_DIR, f'{posting_number}.pdf')
                    label_res = ozon.order_label(posting_number, label_file_path, header)
                    logging.info(f"Label {posting_number} is {label_res}")
                    if label_res:
                        label = 1
                        if not ms.post_order_file(order_href, label_file_path):
                            label = 0
            ########################### Try get customer comment from order ######################
            try:
                customer_comment = order['customer']['address']['comment'] ## test
            except:
                customer_comment = ''
            ########## Обновление БД #########
            for product in products:
                print('product_from_xs', product)
                result = db.insert_update_oder(seller_id, order_id, order, product, comment, order_href, label, fbs)
                if result:
                    logging.info(f"Order {order_id} / {posting_number} insert/update in BD")
                    print(f"Order {order_id} / {posting_number} insert/update in BD")
                else:
                    logging.error(f"ERROR Order {order_id} / {posting_number} insert/update in BD")
                    print(f"ERROR Order {order_id} / {posting_number} insert/update in BD")

    db.close()
    # sys.exit(0)
    print(datetime.datetime.now(), 'ONE_CIRCLE_MADE')


start_orders()
    