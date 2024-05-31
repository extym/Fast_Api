import datetime
import json
import os
import sys
import pandas as pd
from connect import *
from cred import bearer_token
import parts_soft as ps
import requests


# 93445631

def get_current_orders(campaign_id: int):
    link = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    result = []
    # date_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=3), "%d-%m-%Y")
    date_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=1), "%d-%m-%Y")
    requesting = True
    page = 1
    while requesting:
        params = {
            "fromDate": date_time,
            "page": page
        }
        headers = {
            "Authorization": "Bearer " + bearer_token
        }
        answer = requests.get(link, params=params, headers=headers)
        if answer.ok:
            data = answer.json()
            print(len(data['orders']), type(data))
            print('!!!!!!!!!!!! - page', page, data['pager'])
            result.extend(data['orders'])
            if data['pager']['pagesCount'] > page:
                page += 1
            else:
                requesting = False
        else:
            print('Error_get_data {}'.format(answer.text))

    # result.extend(data['orders'])

    print(222222, len(result))
    return result


def get_current_orders_ym_v2(campaign_id: int, time_delta: int=1):
    link = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    result = []
    date_time = datetime.datetime.strftime(datetime.datetime.now()
                                           - datetime.timedelta(days=time_delta),
                                           "%d-%m-%Y")
    requesting = True
    page = 1
    while requesting:
        params = {
            "fromDate": date_time,
            "page": page
        }
        headers = {
            "Authorization": "Bearer " + bearer_token
        }
        answer = requests.get(link, params=params, headers=headers)
        if answer.ok:
            data = answer.json()
            print(len(data['orders']), type(data))
            print('!!!!!!!!!!!! - page', page, data['pager'])
            result.extend(data['orders'])
            if data['pager']['pagesCount'] > page:
                page += 1
            else:
                requesting = False
        else:
            print('Error_get_data {}'.format(answer.text))

    # result.extend(data['orders'])

    print(222222, len(result))
    return result


def get_vendor_code(number_sber, offer_id):
    link = get_sber_link(number_sber)  #upload_price
    brand, vendor_code, price = '', '', ''
    data = pd.read_xml(link, xpath='//offer')
    count = 0
    for row in data:
        if row[0] == offer_id:
            print(len(row))
            brand = row[6]
            vendor_code = row[7]
            price = row[8]
        if len(row) != 14:
            print(*row, sep='\n')
            count += 1
    print(count)
    return brand, vendor_code, price

def get_id_1c(offer_id):

    return None


def reformat_data_order(order, mp, client_id_ps):
    result, result_items = None, None
    if mp == 'Yandex':
        try:
            day = order["delivery"]["shipments"][0]["shipmentDate"]
        except:
            day = order['delivery']['dates']['fromDate']
        result = (
            order["id"],
            mp,
            day,
            order["status"],
            order["substatus"],
            order["paymentType"],
            order["delivery"]["type"],
            order["buyerTotalBeforeDiscount"],
            client_id_ps
        )

        result_items = []
        list_items = order['items']
        for item in list_items:
            id_1c = get_id_1c(order.get('offerId'))
            proxy = (
                str(order["id"]),
                mp,
                item["offerId"],
                id_1c,
                item["count"],
                str(item["price"] + item.get("subsidy")).split(".")[0]  # TODO is make it int ?
            )
            result_items.append(proxy)

    elif mp == 'Ozon':
        time = order["shipment_date"].split('T')[0]

        result = (
            order['id'],
            order["our_id"],
            # shop,
            # day_for_stm(time),  # reverse_time()
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif mp == 'Sber':
        time = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            order['our_id'],
            # shop,  # order["shop"],
            # day_for_stm(time),  # reverse_time(time),
            order["status"],
            order["our_status"],
            "PREPAID",  # order['data'].get("paymentType"),
            order["shipments"][0]['fulfillmentMethod']
        )

    return result, result_items

    # def reformat_data_items(order, shop):
    #     result = []
    #     elif shop == 'Ozon':
    #         result = []
    #         list_items = order['products']
    #         items_ids = read_json_ids()  # ids 1C
    #         for item in list_items:
    #             sku = str(item["sku"])
    #             vendor_code = item["offer_id"]
    #             id_1c = items_ids[vendor_code][0]
    #             # print('product_info_price', sku[0], vendor_code)
    #             # price = product_info_price(items_skus[sku][0], vendor_code)
    #             proxy = (
    #                 order["id"],
    #                 order["our_id"],
    #                 shop,
    #                 order["our_status"],
    #                 vendor_code,
    #                 id_1c,  # 1c
    #                 item["quantity"],
    #                 item["price"][:-2]  # price
    #             )
    #             result.append(proxy)
    #
    #     elif shop == 'Sber':
    #         list_items = order["count_items"]
    #         result = []
    #         for item in list_items:
    #             proxy = (
    #                 order["shipments"][0]["shipmentId"],
    #                 order["our_id"],
    #                 shop,
    #                 order["our_status"],
    #                 item["offerId"],
    #                 item["id_1c"],
    #                 item["quantity"],
    #                 item["price"]
    #             )
    #             result.append(proxy)



# def get_vendor_code_from_xlm(offer_id, link):
#     # sber4 = 'https://3431.ru/system/unload_prices/21/sbermegamarket.xml'
#     # akk_ym = 'https://3431.ru/system/unload_prices/17/yandex_market1.xml'
#     data = pd.read_xml(link, xpath='//offer')
#     count = 0
#     for row in data:
#         if row[0] == offer_id:
#             print(len(row))
#         if len(row) != 14:
#             print(*row, sep='\n')
#             count += 1
#         print(*row.xmltodict, sep='\n')
#     print(count)


def make_orders_to_ps(delta_time:int=1):
    campain_list = execute_query_return_v3(query_get_all_shops, "Yandex")
    if len(campain_list) > 0:
        for campain in campain_list:
            # orders_data = get_current_orders(campain[3])
            # orders = orders_data['orders']
            # orders = get_current_orders(campain[3])
            orders = get_current_orders_ym_v2(campain[3], time_delta=delta_time)
            list_fresh_orders = [i for i in orders if i['status'] == 'PROCESSING']
            list_canceled_orders = [i for i in orders if (i['status'] == 'CANCELLED'
                                                          and i['substatus'] != 'USER_NOT_PAID')]
            # print(*list_fresh_orders, sep='\n')
            # print('!' * 100)
            # print(*list_canceled_orders, sep='\n')
            # sys.exit()
            if len(list_fresh_orders) > 0:
                for order in list_fresh_orders:
                    order_id = str(order.get('id'))
                    print("$$$$$$$$4444", order_id)
                    check = check_order_exist(query_is_exist_order, order_id)

                    # sys.exit()
                    if not check[0]:
                        data_order = reformat_data_order(order, 'Yandex', campain[1])
                        # print(order, 'Yandex', campain[1])
                        write_order = execute_query_return_bool(query_write_order,
                                                                data_order[0])
                        write_items = executemany_return_bool(query_write_items,
                                                              data_order[1])
                        print("Write order {},  write order items {}".
                              format( write_order, write_items))
                        # sys.exit()
                        result = ps.create_resp_if_not_exist(order.get('items'), campain[8],
                                                             external_order_id=order.get('id'))

                        if result:
                            final_result = ps.send_current_basket_to_order()
                            if final_result:
                                data = ' '.join([i['id'] for i in final_result]).strip()
                                print(5555555555, data)
                                finish = ps.change_status_v2(data)
                                print(7777777777, finish)


                    else:
                        continue

            # sys.exit()

            if len(list_canceled_orders) > 0:
                for canceled in list_canceled_orders:

                    check = check_order_exist(query_is_exist_order,
                                              str(canceled.get('id')))
                    if check[1] != 'CANCELLED':
                        execute_query_return_bool(update_order_and_items,
                                                  ('CANCELLED', str(canceled.get('id'))))
                        # ps.change_status()
                        print('check_CANCELLED', check, str(canceled.get('id')))

                    else:
                        continue

                    # elif not check[2]:
                    #     change_status(canceled)


# print(datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=3), "%d-%m-%Y"))


# make_orders_to_ps(delta_time=4)
# make_orders_to_ps()
# We need - get vendor code with offer_id
# check price ?

# print(get_current_orders(93445631))

from io import StringIO
#  pip install lxml

# articul = "ZIC162658"

#
# get_vendor_code_from_xls(articul)