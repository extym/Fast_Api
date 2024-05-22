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
                str(item["price"] + item.get("subsidy")).split(".")[0]
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


def make_orders_to_ps(source=None):
    campain_list = execute_query_return_v3(query_get_all_shops, "Yandex")
    if len(campain_list) > 0:
        for campain in campain_list:
            # orders_data = get_current_orders(campain[3])
            # orders = orders_data['orders']
            orders = get_current_orders(campain[3])
            list_fresh_orders = [i for i in orders if i['status'] == 'PROCESSING']
            list_canceled_orders = [i for i in orders if (i['status'] == 'CANCELLED'
                                                          and i['substatus'] != 'USER_NOT_PAID')]
            print(*list_fresh_orders, sep='\n')
            print('!' * 100)
            print(*list_canceled_orders, sep='\n')
            # sys.exit()
            if len(list_fresh_orders) > 0:
                for order in list_fresh_orders:
                    order_id = str(order.get('id'))
                    print("$$$$$$$$4444", type(order_id))
                    check = check_order_exist(query_is_exist_order, order_id)

                    # sys.exit()
                    if not check[0]:
                        data_order = reformat_data_order(order, 'Yandex', campain[1])
                        print(order, 'Yandex', campain[1])
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
                            ps.send_current_basket_to_order()

                    else:
                        continue

            # sys.exit()

            if len(list_canceled_orders) > 0:
                for canceled in list_canceled_orders:

                    check = check_order_exist(query_is_exist_order,
                                              str(canceled.get('id')))
                    if check[1] != 'CANCELLED':
                        # execute_query_return_bool(update_order_and_items,
                        #                           (str(canceled.get('id')), 'CANCELLED'))
                        # ps.change_status()
                        print('check_CANCELLED', check, str(canceled.get('id')))
                    # if not check[1]:
                    #     update(canceled)
                    # elif not check[2]:
                    #     change_status(canceled)


# print(datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=3), "%d-%m-%Y"))


make_orders_to_ps()

# We need - get vendor code with offer_id
# check price ?

# print(get_current_orders(93445631))

# resp = {'pager': {'total': 7, 'from': 1, 'to': 7, 'currentPage': 1, 'pagesCount': 1, 'pageSize': 50}, 'orders': [{'id': 451642783, 'status': 'PROCESSING', 'substatus': 'STARTED', 'creationDate': '02-05-2024 11:37:27', 'currency': 'RUR', 'itemsTotal': 6772.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 6772.0, 'buyerTotal': 6772.0, 'buyerItemsTotalBeforeDiscount': 7524.0, 'buyerTotalBeforeDiscount': 7524.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591932346, 'offerId': 'STELLOX42140459SX', 'offerName': 'STELLOX 42140459SX 4214-0459-SX_амортизатор передний газовый!\\ BMW E39 2.0-3.0/2.5TD/3.0D 95', 'price': 3386.0, 'buyerPrice': 3386.0, 'buyerPriceBeforeDiscount': 3762.0, 'priceBeforeDiscount': 3762.0, 'count': 2, 'vat': 'NO_VAT', 'shopSku': 'STELLOX42140459SX', 'subsidy': 376.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'promos': [{'type': 'MARKET_PROMOCODE', 'subsidy': 376.0}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 376.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 752.0}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '16-05-2024', 'toDate': '18-05-2024', 'fromTime': '09:00:00', 'toTime': '18:00:00'}, 'region': {'id': 11314, 'name': 'Бердск', 'type': 'CITY', 'parent': {'id': 121038, 'name': 'Городской округ Бердск', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11316, 'name': 'Новосибирская область', 'type': 'REPUBLIC', 'parent': {'id': 59, 'name': 'Сибирский федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'postcode': '633009', 'city': 'Бердск', 'street': 'улица Красная Сибирь', 'gps': {'latitude': 54.746995, 'longitude': 83.058739}}, 'deliveryServiceId': 632848, 'liftPrice': 0.0, 'outletCode': '28568', 'shipments': [{'id': 446332169, 'shipmentDate': '08-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567463109, 'fulfilmentId': '451642783-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': False}, {'id': 451638056, 'status': 'CANCELLED', 'substatus': 'CUSTOM', 'creationDate': '02-05-2024 11:27:13', 'currency': 'RUR', 'itemsTotal': 4643.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 4643.0, 'buyerTotal': 4643.0, 'buyerItemsTotalBeforeDiscount': 4690.0, 'buyerTotalBeforeDiscount': 4690.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591927025, 'offerId': 'TRIALLIGT990', 'offerName': 'TRIALLI GT990 Ремкомплект ГРМ для а/м Лада Granta (10-) 8V (помпаLuzar/ремень/1 ролик) (GT 990)', 'price': 4643.0, 'buyerPrice': 4643.0, 'buyerPriceBeforeDiscount': 4690.0, 'priceBeforeDiscount': 4690.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'TRIALLIGT990', 'subsidy': 47.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'subsidies': [{'type': 'SUBSIDY', 'amount': 47.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 47.0}], 'delivery': {'type': 'DELIVERY', 'serviceName': 'Доставка', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '13-05-2024', 'toDate': '13-05-2024', 'fromTime': '10:00:00', 'toTime': '23:00:00'}, 'region': {'id': 54, 'name': 'Екатеринбург', 'type': 'CITY', 'parent': {'id': 121110, 'name': 'Муниципальное образование Екатеринбург', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11162, 'name': 'Свердловская область', 'type': 'REPUBLIC', 'parent': {'id': 52, 'name': 'Уральский федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'city': 'Екатеринбург', 'street': 'улица Культуры', 'house': '25', 'gps': {'latitude': 56.890663, 'longitude': 60.574873}}, 'deliveryServiceId': 78080, 'liftPrice': 0.0, 'shipments': [{'id': 446327442, 'shipmentDate': '08-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567459587, 'fulfilmentId': '451638056-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': True}, {'id': 451603539, 'status': 'PROCESSING', 'substatus': 'STARTED', 'creationDate': '02-05-2024 10:08:02', 'currency': 'RUR', 'itemsTotal': 2689.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 2689.0, 'buyerTotal': 2689.0, 'buyerItemsTotalBeforeDiscount': 2716.0, 'buyerTotalBeforeDiscount': 2716.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591888087, 'offerId': 'DEPO5512004LUE', 'offerName': 'DEPO 551-2004L-UE Фара противотуманная L', 'price': 2689.0, 'buyerPrice': 2689.0, 'buyerPriceBeforeDiscount': 2716.0, 'priceBeforeDiscount': 2716.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'DEPO5512004LUE', 'subsidy': 27.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'subsidies': [{'type': 'SUBSIDY', 'amount': 27.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 27.0}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '10-05-2024', 'toDate': '10-05-2024', 'fromTime': '09:00:00', 'toTime': '18:00:00'}, 'region': {'id': 10747, 'name': 'Подольск', 'type': 'CITY', 'parent': {'id': 98603, 'name': 'Городской округ Подольск', 'type': 'REPUBLIC_AREA', 'parent': {'id': 1, 'name': 'Москва и Московская область', 'type': 'REPUBLIC', 'parent': {'id': 3, 'name': 'Центральный федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'postcode': '142118', 'city': 'Подольск', 'street': 'Юбилейная улица', 'gps': {'latitude': 55.418823, 'longitude': 37.501736}}, 'deliveryServiceId': 1005561, 'liftPrice': 0.0, 'outletCode': '864', 'shipments': [{'id': 446292925, 'shipmentDate': '08-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567438612, 'fulfilmentId': '451603539-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': False}, {'id': 451590078, 'status': 'PROCESSING', 'substatus': 'STARTED', 'creationDate': '02-05-2024 09:34:18', 'currency': 'RUR', 'itemsTotal': 3505.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 3505.0, 'buyerTotal': 3505.0, 'buyerItemsTotalBeforeDiscount': 3651.0, 'buyerTotalBeforeDiscount': 3651.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591872888, 'offerId': 'ROSSVIK1282PRO', 'offerName': 'ROSSVIK 1282PRO 12-8-2 PRO_шип ремонтный! 12-8-2 серия pro (коробка 500шт)\\', 'price': 3505.0, 'buyerPrice': 3505.0, 'buyerPriceBeforeDiscount': 3651.0, 'priceBeforeDiscount': 3651.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'ROSSVIK1282PRO', 'subsidy': 146.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'subsidies': [{'type': 'SUBSIDY', 'amount': 146.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 146.0}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '12-05-2024', 'toDate': '12-05-2024', 'fromTime': '09:00:00', 'toTime': '18:00:00'}, 'region': {'id': 54, 'name': 'Екатеринбург', 'type': 'CITY', 'parent': {'id': 121110, 'name': 'Муниципальное образование Екатеринбург', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11162, 'name': 'Свердловская область', 'type': 'REPUBLIC', 'parent': {'id': 52, 'name': 'Уральский федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'postcode': '620000', 'city': 'Екатеринбург', 'street': 'улица Спутников', 'apartment': '5', 'gps': {'latitude': 56.758704, 'longitude': 60.808187}}, 'deliveryServiceId': 420399, 'liftPrice': 0.0, 'outletCode': '17614', 'shipments': [{'id': 446279464, 'shipmentDate': '07-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567429039, 'fulfilmentId': '451590078-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': False}, {'id': 451559269, 'status': 'CANCELLED', 'substatus': 'CUSTOM', 'creationDate': '02-05-2024 07:46:54', 'currency': 'RUR', 'itemsTotal': 6294.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 6294.0, 'buyerTotal': 6294.0, 'buyerItemsTotalBeforeDiscount': 6358.0, 'buyerTotalBeforeDiscount': 6358.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591838099, 'offerId': 'LUZARLRC0192B', 'offerName': 'LUZAR LRC0192B Радиатор охл.алюм.несборный Гранта A/C LRc0192b', 'price': 6294.0, 'buyerPrice': 6294.0, 'buyerPriceBeforeDiscount': 6358.0, 'priceBeforeDiscount': 6358.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'LUZARLRC0192B', 'subsidy': 64.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'subsidies': [{'type': 'SUBSIDY', 'amount': 64.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 64.0}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '11-05-2024', 'toDate': '11-05-2024', 'fromTime': '09:00:00', 'toTime': '18:00:00'}, 'region': {'id': 195, 'name': 'Ульяновск', 'type': 'CITY', 'parent': {'id': 120966, 'name': 'Городской округ Ульяновск', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11153, 'name': 'Ульяновская область', 'type': 'REPUBLIC', 'parent': {'id': 40, 'name': 'Приволжский федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'postcode': '432030', 'city': 'Ульяновск', 'street': 'улица Толбухина', 'gps': {'latitude': 54.34214, 'longitude': 48.364944}}, 'deliveryServiceId': 686811, 'liftPrice': 0.0, 'outletCode': '28532', 'shipments': [{'id': 446248658, 'shipmentDate': '07-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567406975, 'fulfilmentId': '451559269-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': True}, {'id': 451549169, 'status': 'PROCESSING', 'substatus': 'STARTED', 'creationDate': '02-05-2024 06:48:54', 'currency': 'RUR', 'itemsTotal': 7020.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 7020.0, 'buyerTotal': 7020.0, 'buyerItemsTotalBeforeDiscount': 7020.0, 'buyerTotalBeforeDiscount': 7020.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591826800, 'offerId': 'TREILER6012', 'offerName': 'Трейлер 6012 Фаркоп трейлер Ford Focus II sedan 2004-2011', 'price': 7020.0, 'buyerPrice': 7020.0, 'buyerPriceBeforeDiscount': 7020.0, 'priceBeforeDiscount': 7020.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'TREILER6012', 'subsidy': 0.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0'}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '15-05-2024', 'toDate': '15-05-2024', 'fromTime': '10:00:00', 'toTime': '18:00:00'}, 'region': {'id': 117646, 'name': 'Гамово', 'type': 'VILLAGE', 'parent': {'id': 172872, 'name': 'Гамовское сельское поселение', 'type': 'OTHER', 'parent': {'id': 99658, 'name': 'Пермский район', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11108, 'name': 'Пермский край', 'type': 'REPUBLIC', 'parent': {'id': 40, 'name': 'Приволжский федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}}, 'address': {'country': 'Россия', 'postcode': '614512', 'city': 'село Гамово', 'street': 'улица 50 лет Октября', 'gps': {'latitude': 57.870131, 'longitude': 56.098541}}, 'deliveryServiceId': 124261, 'liftPrice': 0.0, 'outletCode': '7617', 'shipments': [{'id': 446238558, 'shipmentDate': '08-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567401205, 'fulfilmentId': '451549169-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': False}, {'id': 451530744, 'status': 'CANCELLED', 'substatus': 'USER_REFUSED_DELIVERY', 'creationDate': '02-05-2024 01:43:43', 'currency': 'RUR', 'itemsTotal': 2934.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 2934.0, 'buyerTotal': 2934.0, 'buyerItemsTotalBeforeDiscount': 3280.0, 'buyerTotalBeforeDiscount': 3280.0, 'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False, 'items': [{'id': 591805581, 'offerId': 'MILESDG2147201', 'offerName': 'MILES DG21472-01 Амортизатор передний правый OPEL CORSA D 06- (KYB 339714) DG21472-01', 'price': 2934.0, 'buyerPrice': 2934.0, 'buyerPriceBeforeDiscount': 3280.0, 'priceBeforeDiscount': 3280.0, 'count': 1, 'vat': 'NO_VAT', 'shopSku': 'MILESDG2147201', 'subsidy': 346.0, 'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0', 'subsidies': [{'type': 'SUBSIDY', 'amount': 346.0}]}], 'subsidies': [{'type': 'SUBSIDY', 'amount': 346.0}], 'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0, 'deliveryPartnerType': 'YANDEX_MARKET', 'dates': {'fromDate': '11-05-2024', 'toDate': '11-05-2024', 'fromTime': '09:00:00', 'toTime': '18:00:00'}, 'region': {'id': 11053, 'name': 'Шахты', 'type': 'CITY', 'parent': {'id': 121151, 'name': 'Городской округ Шахты', 'type': 'REPUBLIC_AREA', 'parent': {'id': 11029, 'name': 'Ростовская область', 'type': 'REPUBLIC', 'parent': {'id': 26, 'name': 'Южный федеральный округ', 'type': 'COUNTRY_DISTRICT', 'parent': {'id': 225, 'name': 'Россия', 'type': 'COUNTRY'}}}}}, 'address': {'country': 'Россия', 'postcode': '346503', 'city': 'Шахты', 'street': 'улица Ионова', 'gps': {'latitude': 47.724897, 'longitude': 40.209932}}, 'deliveryServiceId': 606235, 'liftPrice': 0.0, 'outletCode': '25919', 'shipments': [{'id': 446220133, 'shipmentDate': '07-05-2024', 'shipmentTime': '11:30', 'boxes': [{'id': 567390693, 'fulfilmentId': '451530744-1'}]}]}, 'buyer': {'type': 'PERSON'}, 'taxSystem': 'USN', 'cancelRequested': True}]}
# orders = json.dumps(resp)
# print(orders)


from io import StringIO
#  pip install lxml

articul = "ZIC162658"

#
# get_vendor_code_from_xls(articul)