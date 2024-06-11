
import connect as conn
import yandex as yan
import parts_soft as ps


def get_id_1c(offer_id):
    return None


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result


def counter_items(items_list):
    pr, lst = {}, []
    for item in items_list:
        proxy_offer_id = item['offerId']
        pr[proxy_offer_id] = pr.get(proxy_offer_id, 0) + 1
    for itemm in items_list:
        if itemm["offerId"] in pr.keys():
            value = pr.pop(itemm["offerId"])
            itemm["quantity"] = value
            lst.append(itemm)

    return lst


def reformat_data_order(order, mp, client_id_ps):
    result, result_items = None, []
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
        try:
            day = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
        except:
            day = order["shipments"][0]["handover"]["dateFrom"].split('T')[0]
        result = (
            order["shipments"][0]["shipmentId"],
            mp,
            day,
            order["status"],
            order["our_status"],
            "PREPAID",  # order['data'].get("paymentType"),
            order["shipments"][0]['fulfillmentMethod']
        )

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

    return result, result_items


def reformat_data_order_v2(order, mp, client_id_ps,
                           model=None, customers=True):
    result_items, result_customer = [], ()
    result = None
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
        day = order["shipment_date"].split('T')[0]
        result = (
            order['id'],
            order["our_id"],
            mp,
            day,
            order["status"],
            order["our_status"],
            "PREPAID",
            order["delivery_method"]["warehouse_id"]
        )

    elif mp == 'Sber': #and it's request from mp to shop
        list_items = order["count_items"]
        summ_order = 0
        for item in list_items:
            proxy = (
                order["shipments"][0]["shipmentId"],
                mp,
                item["offerId"],
                '', # item["id_1c"],
                item["quantity"],
                str(item["price"])
            )
            result_items.append(proxy)
            summ_order += item["price"]

        if model == 'dbs':
            day = order["shipments"][0]["handover"]["deliveryInterval"]["dateFrom"].split('T')[0]
            order_create_day = order["shipments"][0]['shipmentDate'].split('T')[0]
            delivery = order["shipments"][0]["handover"]['serviceScheme']
        else:
            day = order["shipments"][0]["shipping"]["shippingDate"].split('T')[0]
            order_create_day = order['shipmentDate'].split('T')[0]
            delivery = order["shipments"][0]['fulfillmentMethod']
        result = (
            order["shipments"][0]["shipmentId"],
            mp,
            day,
            order_create_day,
            order["status"],
            "new",  # order["substatus"],
            order["our_status"],
            "PREPAID",  #order['data'].get("paymentType"),
            delivery,
            str(summ_order),
            client_id_ps
        )

        if customers and model == 'dbs':
            result_customer = (
                order["shipments"][0]["shipmentId"],
                mp,
                order_create_day,
                str(summ_order),
                order["shipments"][0]["customer"]['phone'],
                order["shipments"][0]["customer"]['email'],
                order["shipments"][0]["customer"]["address"]["fias"]['regionId'],
                order["shipments"][0]["customer"]["address"]["fias"]['destinationId'],
                order["shipments"][0]["customer"]["address"]["geo"]['lat'],
                order["shipments"][0]["customer"]["address"]["geo"]['lon'],
                order["shipments"][0]["customer"]["address"]['regionKladrId'],
                order["shipments"][0]["customer"]["address"]['regionWithType'],
                order["shipments"][0]["customer"]["address"]['cityWithType']
            )

    return result, result_items, result_customer


def make_orders_to_ps(delta_time:int=1):
    campain_list = conn.execute_query_return_v3(conn.query_get_all_shops, "Yandex")
    if len(campain_list) > 0:
        for campain in campain_list:
            # orders_data = get_current_orders(campain[3])
            # orders = orders_data['orders']
            # orders = get_current_orders(campain[3])
            orders = yan.get_current_orders_ym_v2(campain[7], time_delta=delta_time)
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
                    check = conn.check_order_exist(conn.query_is_exist_order, order_id)

                    # sys.exit()
                    if not check[0]:
                        data_order = reformat_data_order(order, 'Yandex', campain[1])
                        write_order = conn.execute_query_return_bool(conn.query_write_order,
                                                                data_order[0])
                        write_items = conn.executemany_return_bool(conn.query_write_items,
                                                              data_order[1])
                        print("Write order {},  write order items {}".
                              format( write_order, write_items))
                        # sys.exit()
                        result = ps.create_resp_if_not_exist(order.get('items'),
                                                             campain[8], key=campain[7],
                                                             external_order_id=order.get('id'))

                        if result:
                            final_result = ps.send_current_basket_to_order(key=campain[7])
                            if final_result is not None:
                                data = ' '.join([str(i['id']) for i in final_result]).strip()
                                print(5555555555, data)
                                finish = ps.change_status_v2(data, status_id=2)
                                print(7777777777, finish)


                    else:
                        continue

            if len(list_canceled_orders) > 0:
                for canceled in list_canceled_orders:

                    check = conn.check_order_exist(conn.query_is_exist_order,
                                              str(canceled.get('id')))
                    if check[1] != 'CANCELLED':
                        conn.execute_query_return_bool(conn.update_order_and_items,
                                                  ('CANCELLED', str(canceled.get('id'))))
                        data = ' '.join([str(i['id']) for i in canceled.get['items'][0]]).strip()
                        finish = ps.change_status_v2(data, status_id=10)
                        print('check_CANCELLED', check, str(canceled.get('id')), finish)

                    else:
                        continue

                    # elif not check[2]:
                    #     change_status(canceled)