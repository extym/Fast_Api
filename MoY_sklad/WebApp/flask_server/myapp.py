"""
Flask
"""

import os
import logging
from flask import Flask, request, render_template, url_for, redirect, send_file
from html import unescape
import json
import time
from datetime import datetime

from settings import LOG_FILE, PUBLIC_DIR, MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, LOGGING, \
    LOGIN, PASSW, TEST_MODE, OZON_COMMENT_FIELDS, OZON_DATA_FIELDS, OZON_TYPES, MS_DEFAULT_PRICE, LABEL_DIR, URL, \
    ACT_DIR, MS_FIELD_SOBRAN_BOOL, MS_DEMAND_STATUS_PAYED, MS_DEMAND_STATUS_NOT_PAYED, MS_ORDER_STATUS_NOT_PAYED, \
    MS_MINUS_STATUS
from database import MsDatabase
import ozon
import ms


app = Flask(__name__,
            static_folder='templates/static')
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('index', _external=True)
    url_today = url_for('sellers_today', _external=True)
    seller_orders_url = url_for('seller_orders', _external=True)
    seller_acts_url = url_for('seller_acts', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)
    status = ''

    contragents_dict = db.get_dict('counterparty')

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        ############################ Добавление селлера #################################
        if 'add_seller' in result:
            seller_name = result['seller_name']
            seller_token = result['seller_token']
            seller_ozon_id = str(result['seller_ozon_id'])
            if not seller_token or not seller_name or not seller_ozon_id:
                status = 'Заполните все поля!'
            else:
                if not ozon.check_api(seller_token, seller_ozon_id):
                    status = 'Связка токена и client id не валидны'
                else:
                    if not db.get_seller(seller_ozon_id):
                        if not db.insert_new_seller(seller_name, seller_ozon_id, seller_token):
                            status = 'Ошибка при добавлении селлера в базу!'
                        else:
                            status = f'Селлер добавлен, отредактируйте его <a href="{edit_seller_url}?seller_id={seller_ozon_id}&login={login}&passw={passw}">настройки</a>!'
                    else:
                        status = f'Селлел с id {seller_ozon_id} уже существует в базе'

        ############################# Удаление файлов #####################################
        if 'delete_files' in result:
            status_text = 'Результаты удаления этикеток:'
            agent = result['contragent']
            date_from = result['date_from']
            date_to = result['date_to']
            date_from_obj = datetime.strptime(date_from, "%d.%m.%Y")
            date_to_obj = datetime.strptime(date_to, "%d.%m.%Y")
            orders = ms.get_contragent_orders(agent, date_from_obj, date_to_obj)
            files_count = 0
            orders_count = 0
            for order in orders:
                order_files = ms.get_order_files(order)
                if order_files:
                    orders_count += 1
                    for file in order_files:
                        res = ms.delete_order_file(order, order_files[file])
                        files_count += 1
            status += f"Контрагент {contragents_dict[agent]}. Обработано {orders_count} заказов. Удалено {files_count} файлов."

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    ######################## Отображение таблицы селлеров ###########################
    db.reconnect()
    sellers = ''
    sellers_list = db.get_all_sellers()
    # print(sellers_list)
    for seller in sellers_list:
        seller_orders_href = f"{seller_orders_url}?seller_id={seller[3]}&login={login}&passw={passw}&name={seller[2]}"
        edit_seller_href = f"{edit_seller_url}?seller_id={seller[3]}&login={login}&passw={passw}"
        button_text = f'<a href="{seller_acts_url}?seller_id={seller[3]}&login={login}&passw={passw}&name={seller[2]}">Акты</a>'
        ##### stat start
        stat_dict = {'awaiting_deliver': 0, 'delivering': 0, 'last-mile': 0, 'delivered': 0}
        seller_stat = db.get_orders_stat(seller[3], 1)
        for elem_stat in seller_stat:
            if elem_stat[0] in stat_dict:
                stat_dict[elem_stat[0]] += 1
        stat_text = f"{stat_dict['awaiting_deliver']} / {stat_dict['delivering']} / {stat_dict['last-mile']} / {stat_dict['delivered']}"
        ##### stat end
        seller_string = f'<tr>\
                        <td width="200" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle"><a href="{edit_seller_href}">{seller[2]}</a></td>\
                        <td width="100" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller[3]}</a></td>\
                        <td width = "200" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle"><a href="{seller_orders_href}">Заказы</a></td>\
                        <td width = "300" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{stat_text}</td>\
                        <td width = "150" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{button_text}</td>\
                    </tr>'
        sellers += seller_string
    #################################################################################

    ######################## Удаление доков #############################
    contragents = ''
    for key in contragents_dict:
        contragents += f"<option value='{key}'>{contragents_dict[key]}</option>"
    ######################################################################

    db.close()
    sellers_today_href = f"<a href='{url_today}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
    #not_ass_labels = f"<a href='{URL}labels_not_assembled/all_labels.pdf' target='_blank'>Все этикетки</a>"
    #not_ass_labels_day = f"<a href='{URL}labels_not_assembled_day/all_labels_day.pdf' target='_blank'>Этикетки сегодня</a>"
    return unescape(render_template("index.html", url=url, login=LOGIN, passw=PASSW, sellers=sellers, status=status, contragents=contragents, sellers_today_href=sellers_today_href))


@app.route("/sellers_today", methods=['GET', 'POST'])
def sellers_today():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url_today = url_for('sellers_today', _external=True)
    url = url_for('index', _external=True)
    seller_orders_url = url_for('seller_orders', _external=True)
    seller_acts_url = url_for('seller_acts', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)
    status = ''
    status_text = ''
    seller_id = ''

    # contragents_dict = db.get_dict('counterparty')

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        # seller_id = request.values.get('seller_id')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        # seller_id = result.get('seller_id')

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url_today))


    ######################## Отображение таблицы селлеров ###########################
    db.reconnect()
    sellers = ''
    # sellers_list = db.get_all_sellers()
    sellers_today_href = f"{url_today}?login={login}&passw={passw}"
    shipments_today = db.get_seller_id_today()
    proxy, shipments_list_today = [], []
    for cd in shipments_today:
        cd = list(cd)
        proxy.extend(cd)
        shipments_list_today = tuple(set(proxy))
    # print('shipments_list_today', shipments_list_today)
    sellers_list_today = db.get_all_sellers_today(shipments_list_today)
    sell_dict = {s[3]: (s[2], s[4]) for s in sellers_list_today}
    for seller in sellers_list_today:
        print('seller', seller)
    # logging.info('sellers_today', sell_dict)
###########################################################################
    # list_act_id = db.get_acts_today()  # TODO need its make?
    list_act_id = db.get_seller_acts_v3()  #db.get_acts_today()  #
    print('list_act_id', len(list_act_id), list_act_id)


    #################################################################################
    for act in list_act_id:
        print(type(act), act)
        seller_id = act[1]
        sell_tok = sell_dict.get(seller_id)[1]
        header = ozon.get_header(sell_tok, seller_id)
        seller_name = sell_dict.get(seller_id)[0]
        act_id = act[0]
        dt = act[2]
        status_act = act[3]
        file_path = 'not ready'
        file_path_edo = '-'
        if act[4]:
            file_path = f"<a href='{URL}{ACT_DIR}{act[4]}' target='_blank'>pdf</a>"
        if act[5]:
            file_path_edo = f"<a href='{URL}{ACT_DIR}{act[5]}' target='_blank'>pdf</a>"
        # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
        if act[6] == 1:
            demand = 'Отгружен'
        elif act[6] == 0:
            demand = 'Архив'
        elif act[6] == 2:
            orders = ozon.get_act_orders(act_id, header)
            print(act_id, '-',  header, '-',  orders)
            i = 0
            j = 0
            for order in orders:
                order_db_res = db.get_order_ms_id(seller_id, order)
                if not order_db_res:
                    continue
                order_href = order_db_res[0][1]
                order_dict = ms.get_order_params_and_attributes(order_href, [],
                                                                [MS_FIELD_SOBRAN_BOOL])
                if order_dict[MS_FIELD_SOBRAN_BOOL]:
                    db.update_oder_demand(seller_id, order_href, 1)
                    j += 1
                i += 1
            if j != i:
                demand = f"Собрано {j}/{i}"
            else:
                demand = f'<button type="submit" value={act_id} name="create_demand" class="my">Отгрузить</button> {j}/{i}'

        seller_string = f'<tr>\
                    <td width="200" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_name}</td>\
                    <td width="100" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_id}</td>\
                    <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{act_id}</td> \
                    <td width = "200" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt}</td> \
                    <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{status_act}</td> \
                    <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path}</td> \
                    <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path_edo}</td> \
                    <td width = "130" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{demand}</td> \
                </tr>'
        sellers += seller_string

    ##################################################################################
    # if request.method == 'POST':
    result = request.form
    result_status_text = ''
    if 'create_act' in result:
        for seller in sellers_list_today:
            header = ozon.get_header(seller[4], seller[3])
            # print(ozon.get_delivery_methods(header))
            sklads_dict = json.loads(seller[13])
            print('sklads_dict', sklads_dict)
            status_text = ''
            for sklad_id in sklads_dict:
                act_id = ozon.get_act(int(sklad_id), header)
                if act_id is None:
                    status_text += f"Нет Актов в API для склада {sklad_id}<br>"
                    result_status_text += status_text + '\n'
                else:
                    if not db.insert_act(act_id, seller[3]):
                        status_text += f'Ошибка записи act_id={act_id} и seller_id={seller[3]} в БД. Вероятно акт уже существуетю<br>'
                        result_status_text += status_text + '\n'
                    else:
                        status_text += f"Акт под номером {act_id} для склада {sklad_id} заказан. Ожидайте pdf.<br>"
                        result_status_text += status_text + '\n'

    elif 'create_demand' in result:
        act_id = int(result['create_demand'])
        for row in list_act_id:
            if row[0] == act_id:
                print(type(row[0]))
                seller_id = row[1]
        sell_tok = sell_dict.get(seller_id)[1]
        header = ozon.get_header(sell_tok, seller_id)
        # ms_demand: 0 - по умолчанию, 1 - не собран, 2 - не отгружен, 3 - отгружен
        orders = ozon.get_act_orders(act_id, header)
        # orders = db.get_fbs_orders_href_wo_demand(seller_id, period=3)
        status_text = f'Результаты отгрузки:'
        flag = True
        for order in orders:
            order_db_res = db.get_order_ms_id(seller_id, order)
            if not order_db_res:
                continue
            order_href = order_db_res[0][1]
            order_dict = ms.get_order_params_and_attributes(order_href, ['name', 'demands', 'payments', 'sum'],
                                                            [MS_FIELD_SOBRAN_BOOL])
            ###################### Payment ######################
            if not order_dict['payments']:
                state_href = MS_ORDER_STATUS_NOT_PAYED
            else:
                state_href = MS_MINUS_STATUS
            if not ms.update_order_status(order_href, state_href):
                status_text += f"<br>{order_dict['name']} - ошибка смены статуса"
            #####################################################
            if order_dict[MS_FIELD_SOBRAN_BOOL] and not order_dict['demands']:
                demand_dict = ms.get_demand_template(order_href)
                if demand_dict:
                    if ms.post_demand_v2(demand_dict):
                        status_text += f"<br>{order_dict['name']} - отгружен"
                        db.update_oder_demand(seller_id, order_href, 3)
                    else:
                        db.update_oder_demand(seller_id, order_href, 2)
                        status_text += f"<br>{order_dict.get('name')} - ОШИБКА ОТГРУЗКИ!"
            elif order_dict['demands']:
                demand_href = order_dict['demands'][0]['meta']['href'].split('/')[-1]
                demand_dict = ms.get_demand_params_and_attributes(demand_href, ['sum', 'applicable'], [])
                if order_dict['sum'] != demand_dict['sum']:
                    status_text += f"<br>{order_dict['name']} - не совпадает сумма в Отгрузке"
                if demand_dict['applicable']:
                    status_text += f"<br>{order_dict['name']} - был отгружен ранее"
                    db.update_oder_demand(seller_id, order_href, 3)
                else:
                    if ms.update_entity_main_param('demand', demand_href, 'applicable', True):
                        status_text += f"<br>{order_dict['name']} - проведена старая отгрузка"
                        db.update_oder_demand(seller_id, order_href, 3)
                    else:
                        db.update_oder_demand(seller_id, order_href, 2)
                        status_text += f"<br>{order_dict['name']} - ОШИБКА ПРОВЕДЕНИЯ ОТГРУЗКИ!"

            elif not order_dict[MS_FIELD_SOBRAN_BOOL]:
                db.update_oder_demand(seller_id, order_href, 1)
                status_text += f"<br>{order_dict['name']} - НЕ СКОМПЛЕКТОВАН!"
                flag = False
            else:
                db.update_oder_demand(seller_id, order_href, 2)
                status_text += f"<br>{order_dict['name']} - не отгружен"
        if flag:
            # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
            db.update_act_demand(act_id, 1)

        seller_string = f'<tr>\
                    <td width="200" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_name}</td>\
                    <td width="100" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_id}</td>\
                    <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{act_id}</td> \
                    <td width = "200" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt}</td> \
                    <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{status_act}</td> \
                    <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path}</td> \
                    <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path_edo}</td> \
                    <td width = "130" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{demand}</td> \
                </tr>'
        sellers += seller_string

    # else:
        # for act in list_act_id:
        #     seller_id = act[1]
        #     sell_tok = sell_dict.get(seller_id)[1]
        #     header = ozon.get_header(sell_tok, seller_id)
        #     seller_name = sell_dict.get(seller_id)[0]
        #     act_id = act[0]
        #     dt = act[2]
        #     status_act = act[3]
        #     file_path = 'not ready'
        #     file_path_edo = '-'
        #     if act[4]:
        #         file_path = f"<a href='{URL}{ACT_DIR}{act[4]}' target='_blank'>pdf</a>"
        #     if act[5]:
        #         file_path_edo = f"<a href='{URL}{ACT_DIR}{act[5]}' target='_blank'>pdf</a>"
        #     # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
        #     if act[6] == 1:
        #         demand = 'Отгружен'
        #     elif act[6] == 0:
        #         demand = 'Архив'
        #     elif act[6] == 2:
        #         orders = ozon.get_act_orders(act_id, header)
        #         i = 0
        #         j = 0
        #         for order in orders:
        #             order_db_res = db.get_order_ms_id(seller_id, order)
        #             if not order_db_res:
        #                 continue
        #             order_href = order_db_res[0][1]
        #             order_dict = ms.get_order_params_and_attributes(order_href, [],
        #                                                             [MS_FIELD_SOBRAN_BOOL])
        #             if order_dict[MS_FIELD_SOBRAN_BOOL]:
        #                 db.update_oder_demand(seller_id, order_href, 1)
        #                 j += 1
        #             i += 1
        #         if j != i:
        #             demand = f"Собрано {j}/{i}"
        #         else:
        #             demand = f'<button type="submit" value={act_id} name="create_demand" class="my">Отгрузить</button> {j}/{i}'
        #
        #     seller_string = f'<tr>\
        #                 <td width="200" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_name}</td>\
        #                 <td width="100" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align: middle">{seller_id}</td>\
        #                 <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{act_id}</td> \
        #                 <td width = "200" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt}</td> \
        #                 <td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{status_act}</td> \
        #                 <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path}</td> \
        #                 <td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path_edo}</td> \
        #                 <td width = "130" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{demand}</td> \
        #             </tr>'
        #     sellers += seller_string



    ######################################################################

    db.close()
    acts_today_href = f"<a href='{URL} + {PUBLIC_DIR} + 'acts_not_assembled_day/all_acts_today.pdf' target='_blank'>Акты сегодня</a>"
    # not_ass_labels = f"<a href='{URL}labels_not_assembled/all_labels.pdf' target='_blank'>Все этикетки</a>"
    not_ass_labels_day = f"<a href='{URL}labels_not_assembled_day/all_labels_day.pdf' target='_blank'>Этикетки сегодня</a>"

    return unescape(
        render_template("today.html", url_today=sellers_today_href, url=url, login=LOGIN, passw=PASSW, sellers=sellers,
                        status=status, acts_today_href=acts_today_href, not_ass_labels_day=not_ass_labels_day,
                        result_status_text=result_status_text, edit_seller_url=edit_seller_url, index_url=url,
                        status_text=status_text))  #contragents=contragents, name=name, rows=rows,

@app.route("/edit_seller", methods=['GET', 'POST'])
def edit_seller():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('edit_seller', _external=True)
    # url = "http://127.0.0.1:5000/edit_seller"
    index_url = url_for('index', _external=True)
    edit_seller_products_url = url_for('edit_seller_products', _external=True)
    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        seller_id = request.values.get('seller_id')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        seller_id = result.get('seller_id')
        ############################ Сохранение селлера #################################
        # print(result)
        if result.get('save_seller'):
            res = {}
            if result.get('active'):
                res['active'] = 1
            else:
                res['active'] = 0
            if result.get('usluga_price_ms'):
                res['usluga_price_ms'] = 1
            else:
                res['usluga_price_ms'] = 0
            if result.get('usluga_price_ms_realfbs'):
                res['usluga_price_ms_realfbs'] = 1
            else:
                res['usluga_price_ms_realfbs'] = 0

            res['client_id'] = seller_id
            res['token'] = result.get('token')
            res['name'] = result.get('name')
            res['date_ozon_field'] = result.get('date_ozon_field')
            res['status'] = result.get('status')
            res['cancell_status'] = result.get('cancell_status')
            res['contragent'] = result.get('contragent')
            res['comment'] = result.get('comment')
            # res['fb'] = result.get('fb')
            res['fb'] = result.get('fbs')
            res['sklad'] = result.get('sklad')
            res['organization'] = result.get('organization')
            res['usluga'] = result.get('usluga')
            res['status_realfbs'] = result.get('status_realfbs')
            res['contragent_realfbs'] = result.get('contragent_realfbs')
            res['comment_realfbs'] = result.get('comment_realfbs')
            res['usluga_realfbs'] = result.get('usluga_realfbs')
            res['price'] = result.get('price')
            i = 0
            # print(result)
            ozon_store_input_dict = {}
            while True:
                val = result.get(f'ozon_stores{i}')
                if val:
                    try:
                        store_id_tmp, store_type_tmp = val.split('/')
                    except:
                        continue
                    if store_type_tmp:
                        ozon_store_input_dict[store_id_tmp] = store_type_tmp
                else:
                    break
                i += 1
            res['ozon_store'] = json.dumps(ozon_store_input_dict)
            # print(res)

            if not ozon.check_api(res['token'], res['client_id']):
                status_text = 'Связка токена и client id не валидны'
            elif db.update_seller(res):
                status_text = f'Селлел сохранен'
            else:
                status_text = f'Ошибка сохранения селлера'
        elif result.get('products_seller'):
            token = result.get('token')
            header = ozon.get_header(token, seller_id)
            try:
                res = ozon.get_products_dict(header)
                # print(len(res))
                logging.info(len(res))
                for key in res:
                    product = ozon.get_product_dict(key, header)
                    # print(product)
                    db.insert_update_ozon_product(seller_id, product)
                status_text = f'Выгружено {len(res)} товаров селлера'
            except:
                status_text = f'Ошибка получения товаров селлера'

        #################################################################################

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    ######################## Отображение таблицы селлера ###########################
    if not seller_id:
        return f'Не найден seller_id<br><a href="{index_url}?login={login}&passw={passw}">Назад</a>'
    else:
        try:
            (id, date, name, seller_id, api_token, date_field, state, contragent_id, comment, active, fb, store, organization_id, ozon_store_json, usluga,
             usluga_price_ms, state_realfbs, contragent_realfbs, comment_realfbs, usluga_realfbs, usluga_price_ms_realfbs, price, cancell_state) = db.get_seller(seller_id)[0]
        except:
            return f'Не найден селлер в базе<br><a href="{index_url}?login={login}&passw={passw}">Назад</a>'

        if active:
            active = 'checked'
        else:
            active = ''
        if not price:
            price = MS_DEFAULT_PRICE

        contragents_dict = db.get_dict('counterparty')
        contragents = ''
        contragents_realfbs = ''
        for key in contragents_dict:
            if contragent_id and key == contragent_id:
                contragents += f"<option value='{key}' selected='selected'>{contragents_dict[key]}</option>"
            else:
                contragents += f"<option value='{key}'>{contragents_dict[key]}</option>"
            if contragent_realfbs and key == contragent_realfbs:
                contragents_realfbs += f"<option value='{key}' selected='selected'>{contragents_dict[key]}</option>"
            else:
                contragents_realfbs += f"<option value='{key}'>{contragents_dict[key]}</option>"

        organizations_dict = db.get_dict('organization')
        organizations = ''
        for key in organizations_dict:
            if organization_id and key == organization_id:
                organizations += f"<option value='{key}' selected='selected'>{organizations_dict[key]}</option>"
            else:
                organizations += f"<option value='{key}'>{organizations_dict[key]}</option>"

        states_dict = db.get_dict('states')
        states = ''
        states_realfbs = ''
        cancell_states = ''
        for key in states_dict:
            if state and key == state:
                states += f"<option value='{key}' selected='selected'>{states_dict[key]}</option>"
            else:
                states += f"<option value='{key}'>{states_dict[key]}</option>"
            if state_realfbs and key == state_realfbs:
                states_realfbs += f"<option value='{key}' selected='selected'>{states_dict[key]}</option>"
            else:
                states_realfbs += f"<option value='{key}'>{states_dict[key]}</option>"
            if cancell_state and key == cancell_state:
                cancell_states += f"<option value='{key}' selected='selected'>{states_dict[key]}</option>"
            else:
                cancell_states += f"<option value='{key}'>{states_dict[key]}</option>"

        stores_dict = db.get_dict('store')
        stores = ''
        for key in stores_dict:
            if store and key == store:
                stores += f"<option value='{key}' selected='selected'>{stores_dict[key]}</option>"
            else:
                stores += f"<option value='{key}'>{stores_dict[key]}</option>"

        prices_dict = db.get_dict('prices')
        prices = ''
        for key in prices_dict:
            if price and key == price:
                prices += f"<option value='{key}' selected='selected'>{prices_dict[key]}</option>"
            else:
                prices += f"<option value='{key}'>{prices_dict[key]}</option>"

        # fbs = ''
        # for key in OZON_SCHEMAS:
        #     if fb and key == fb:
        #         fbs += f"<option value='{key}' selected='selected'>{key}</option>"
        #     else:
        #         fbs += f"<option value='{key}'>{key}</option>"

        fields = ''
        for key in OZON_COMMENT_FIELDS:
            fields += f"{key}, "

        date_fields = ''
        for key in OZON_DATA_FIELDS:
            if date_field and key == date_field:
                date_fields += f"<option value='{key}' selected='selected'>{key}</option>"
            else:
                date_fields += f"<option value='{key}'>{key}</option>"

        uslugi = ''
        uslugi_realfbs = ''
        uslugi_list = ms.get_small_service_list()
        uslugi_list.append(['0', ''])
        if not usluga:
            usluga = '0'
        if not usluga_realfbs:
            usluga_realfbs = '0'
        for elem in uslugi_list:
            if usluga and elem[0] == usluga:
                uslugi += f"<option value='{elem[0]}' selected='selected'>{elem[1]}</option>"
            else:
                uslugi += f"<option value='{elem[0]}'>{elem[1]}</option>"
            if usluga_realfbs and elem[0] == usluga_realfbs:
                uslugi_realfbs += f"<option value='{elem[0]}' selected='selected'>{elem[1]}</option>"
            else:
                uslugi_realfbs += f"<option value='{elem[0]}'>{elem[1]}</option>"

        ozon_stores = ''
        ozon_header = ozon.get_header(api_token, seller_id)
        ozon_stores_dict = ozon.get_stores(ozon_header)
        try:
            seller_ozon_store_dict = json.loads(ozon_store_json)
        except:
            seller_ozon_store_dict = {}
        # # print(ozon_stores_dict)
        i = 0
        for key in ozon_stores_dict:
            form_name = f'ozon_stores{i}'
            ozon_stores += f"{ozon_stores_dict[key]}: <select name='{form_name}'>"
            for type in OZON_TYPES:
                if seller_ozon_store_dict and key in seller_ozon_store_dict and seller_ozon_store_dict[key] == type:
                    ozon_stores += f"<option value='{key}/{type}' selected='selected'>{type}</option>"
                elif not type and not seller_ozon_store_dict or key not in seller_ozon_store_dict:
                    ozon_stores += f"<option value='{key}/{type}' selected='selected'>{type}</option>"
                else:
                    ozon_stores += f"<option value='{key}/{type}'>{type}</option>"
            ozon_stores += "</select><br>"
            i += 1

        usluga_price_ms_active = ''
        usluga_price_ms_active_realfbs = ''
        if usluga_price_ms:
            usluga_price_ms_active = 'checked'
        if usluga_price_ms_realfbs:
            usluga_price_ms_active_realfbs = 'checked'

    #################################################################################

    db.close()
    # fbs = fbs,
    return unescape(render_template("seller.html", url=url, index_url=index_url, edit_seller_products_url=edit_seller_products_url,
                                    active=active, contragents=contragents, organizations=organizations, token=api_token, name=name,
                                    states=states, stores=stores, comment=comment, fields=fields, date_fields=date_fields,
                                    ozon_stores=ozon_stores, login=LOGIN, passw=PASSW, seller_id=seller_id, status_text=status_text,
                                    uslugi=uslugi, usluga_price_ms_active=usluga_price_ms_active, contragents_realfbs=contragents_realfbs,
                                    states_realfbs=states_realfbs, comment_realfbs=comment_realfbs, uslugi_realfbs=uslugi_realfbs,
                                    usluga_price_ms_active_realfbs=usluga_price_ms_active_realfbs, prices=prices, cancell_states=cancell_states))


@app.route("/edit_seller_products", methods=['GET', 'POST'])
def edit_seller_products():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller_products page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('edit_seller_products', _external=True)
    index_url = url_for('index', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)

    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        seller_id = request.values.get('seller_id')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        seller_id = result.get('seller_id')
        ############################ Сохранение селлера #################################
        # print(result)
        errors = 0
        jobs = 0
        if result.get('save_products'):
            ozon_products = db.get_products(seller_id)
            for product in ozon_products:
                product_id = product[0]
                # print(product_id)
                ms_id = str(product[4])
                delive = product[5]
                new_ms_id = result.get(str(product_id))
                try:
                    new_delive = float(result.get(str(product_id) + '_price'))
                except:
                    new_delive = 0
                # print(product_id, ms_id, '-', new_ms_id)
                if new_ms_id and new_ms_id != ms_id:
                    try:
                        if not db.update_ozon_product_link(seller_id, product_id, new_ms_id):
                            errors += 1
                        jobs += 1
                    except:
                        pass
                if new_delive and new_delive != delive:
                    try:
                        if not db.update_ozon_delive(seller_id, product_id, new_delive):
                            errors += 1
                        jobs += 1
                    except:
                        pass
                    # print(seller_id, product_id, new_ms_id)
        if errors:
            status_text = f"При обновлении связей товаров возникло {errors} ошибок"
        elif jobs:
            status_text = f"Обновлены связи {jobs} товаров"
        else:
            status_text = f"Связи товаров без изменений"

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    if not seller_id:
        return f'Не найден seller_id<br><a href="{index_url}?login={login}&passw={passw}">Назад</a>'
    else:
        pass

    rows = ''
    ozon_products = db.get_products(seller_id)
    ms_products = db.get_ms_products()
    for product in ozon_products:
        try:
            product_id = product[0]
            offer_id = product[1]
            name = product[2]
            barcode = product[3]
            ms_id = product[4]
            delive = product[5]
    
            ms_products_text = ''
            for elem in ms_products:
                if ms_id and elem[0] == ms_id:
                    ms_products_text += f"<option value='{elem[0]}' selected='selected'>{elem[1]} / code: {elem[2]} / article: {elem[3]}</option>"
                elif not elem[0]:
                    ms_products_text += f"<option value='' selected='selected'></option>"
                else:
                    ms_products_text += f"<option value='{elem[0]}'>{elem[1]} / code: {elem[2]} / article: {elem[3]}</option>"
        except:
            continue
        # if not ms_id:
        #     ms_products_text += f"<option value='' selected='selected'></option>"
        
        rows += f'<tr><td width = "450" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle">{name} / id: {product_id} / offer_id: {offer_id}</td>' \
                f'<td width = "450" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><select name={product_id}  style="max-width:450;">{ms_products_text}</select></td>' \
                f'<td width = "70" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><input type="text" name="{product_id}_price" value="{delive}" style="width: 60px;" required="required"></td></tr>'

    db.close()
    print('Закрыли БД')
    
    return unescape(
    render_template("products.html", url=url, login=LOGIN, passw=PASSW, seller_id=seller_id, status_text=status_text,
                    edit_seller_url=edit_seller_url, index_url=index_url, rows=rows))


@app.route("/seller_orders", methods=['GET', 'POST'])
def seller_orders():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller_products page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('seller_orders', _external=True)
    index_url = url_for('index', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)
    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        name = request.values.get('name')
        seller_id = request.values.get('seller_id')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        name = result['name']
        seller_id = result.get('seller_id')

        if 'delete_labels' in result:
            status_text = 'Результаты удаления этикеток:'
            date_from = result['date_from']
            date_to = result['date_to']
            orders = db.get_orders_w_labels_to_date(seller_id, date_from, date_to)
            # status_text += f"{orders}"
            for order in orders:
                order_files = ms.get_order_files(order[1])
                if order[0] in order_files:
                    res = ms.delete_order_file(order[1], order_files[order[0]])
                    status_text += f"<br>{order[0]} - {res}"

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    orders = db.get_seller_orders(seller_id)
    # print(orders)
    rows = ''
    for order in orders:
        end_dt = ''
        if order[6]:
            end_dt_obj = datetime.strptime(order[6], "%Y-%m-%dT%H:%M:%SZ")
            end_dt = end_dt_obj.strftime("%d.%m.%Y %H:%M")
        dt = order[1].strftime("%d.%m.%Y %H:%M")
        dt_add = '-'
        if order[7]:
            dt_add = order[7].strftime("%d.%m.%Y %H:%M")
        label = 'Нет'
        if order[4]:
            #print(f'{URL}{LABEL_DIR}{order[0]}.pdf')
            label = f"<a href='{LABEL_DIR}{order[0]}.pdf' target='_blank'>Да</a>"
        fbs = 'rFBS'
        if order[5]:
            fbs = 'FBS'
        # ms_demand: 0 - по умолчанию, 1 - не собран, 2 - не отгружен, 3 - отгружен
        demand = '-'
        if order[8] == 1:
            demand = 'Не собран'
        elif order[8] == 2:
            demand = 'Не Отгружен'
        elif order[8] == 3:
            demand = 'Отгружен'

        rows += '<tr>' \
               f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order[0]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt_add}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt}</td>' \
               f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order[2]}</td>' \
               f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order[3]}</td>' \
               f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{label}</td>' \
               f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{fbs}</td>' \
               f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{end_dt}</td>' \
                f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{demand}</td>' \
                f'</tr>'

    db.close()
    return unescape(
        render_template("orders.html", url=url, login=LOGIN, passw=PASSW, seller_id=seller_id,
                        status_text=status_text, rows=rows, name=name,
                        edit_seller_url=edit_seller_url, index_url=index_url))


@app.route("/seller_acts", methods=['GET', 'POST'])
def seller_acts():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller_products page Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('seller_acts', _external=True)
    index_url = url_for('index', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)
    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        name = request.values.get('name')
        seller_id = request.values.get('seller_id')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        name = result['name']
        seller_id = result.get('seller_id')

    seller = db.get_seller(seller_id)[0]
    header = ozon.get_header(seller[4], seller_id)
    # print('seller', seller, header)
    if request.method == 'POST':
        if 'create_act' in result:
            # print(ozon.get_delivery_methods(header))
            sklads_dict = json.loads(seller[13])
            print('sklads_dict', sklads_dict)
            status_text = ''
            for sklad_id in sklads_dict:
                act_id = ozon.get_act(int(sklad_id), header)
                if act_id is None:
                    status_text += f"Нет Актов в API для склада {sklad_id}<br>"
                else:
                    if not db.insert_act(act_id, seller_id):
                        status_text += f'Ошибка записи act_id={act_id} и seller_id={seller_id} в БД. Вероятно акт уже существует<br>'
                    else:
                        status_text += f"Акт под номером {act_id} для склада {sklad_id} заказан. Ожидайте pdf.<br>"
        elif 'create_demand' in result:
            # ms_demand: 0 - по умолчанию, 1 - не собран, 2 - не отгружен, 3 - отгружен
            act_id = int(result['create_demand'])
            orders = ozon.get_act_orders(act_id, header)
            # orders = db.get_fbs_orders_href_wo_demand(seller_id, period=3)
            status_text = f'Результаты отгрузки:'
            flag = True
            for order in orders:
                order_db_res = db.get_order_ms_id(seller_id, order)
                if not order_db_res:
                    continue
                order_href = order_db_res[0][1]
                order_dict = ms.get_order_params_and_attributes(order_href, ['name', 'demands', 'payments', 'sum'], [MS_FIELD_SOBRAN_BOOL])
                ###################### Payment ######################
                if not order_dict['payments']:
                    state_href = MS_ORDER_STATUS_NOT_PAYED
                else:
                    state_href = MS_MINUS_STATUS
                if not ms.update_order_status(order_href, state_href):
                    status_text += f"<br>{order_dict['name']} - ошибка смены статуса"
                #####################################################
                if order_dict[MS_FIELD_SOBRAN_BOOL] and not order_dict['demands']:
                    demand_dict = ms.get_demand_template(order_href)
                    if demand_dict:
                        if ms.post_demand_v2(demand_dict):
                            status_text += f"<br>{order_dict['name']} - отгружен"
                            db.update_oder_demand(seller_id, order_href, 3)
                        else:
                            db.update_oder_demand(seller_id, order_href, 2)
                            status_text += f"<br>{order_dict.get('name')} - ОШИБКА ОТГРУЗКИ!"
                elif order_dict['demands']:
                    demand_href = order_dict['demands'][0]['meta']['href'].split('/')[-1]
                    demand_dict = ms.get_demand_params_and_attributes(demand_href, ['sum', 'applicable'], [])
                    if order_dict['sum'] != demand_dict['sum']:
                        status_text += f"<br>{order_dict['name']} - не совпадает сумма в Отгрузке"
                    if demand_dict['applicable']:
                        status_text += f"<br>{order_dict['name']} - был отгружен ранее"
                        db.update_oder_demand(seller_id, order_href, 3)
                    else:
                        if ms.update_entity_main_param('demand', demand_href, 'applicable', True):
                            status_text += f"<br>{order_dict['name']} - проведена старая отгрузка"
                            db.update_oder_demand(seller_id, order_href, 3)
                        else:
                            db.update_oder_demand(seller_id, order_href, 2)
                            status_text += f"<br>{order_dict['name']} - ОШИБКА ПРОВЕДЕНИЯ ОТГРУЗКИ!"

                elif not order_dict[MS_FIELD_SOBRAN_BOOL]:
                    db.update_oder_demand(seller_id, order_href, 1)
                    status_text += f"<br>{order_dict['name']} - НЕ СКОМПЛЕКТОВАН!"
                    flag = False
                else:
                    db.update_oder_demand(seller_id, order_href, 2)
                    status_text += f"<br>{order_dict['name']} - не отгружен"
            if flag:
                # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
                db.update_act_demand(act_id, 1)

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    acts = db.get_seller_acts_v2(seller_id)

    # print(orders)
    rows = ''
    header = ozon.get_header(seller[4], seller_id)
    for act in acts:
        act_id = act[0]
        dt = act[1].strftime("%d.%m.%Y %H:%M")
        dt_update = act[2].strftime("%d.%m.%Y %H:%M")
        status = act[3]
        file_path = 'not ready'
        file_path_edo = '-'
        if act[4]:
            file_path = f"<a href='{URL}{ACT_DIR}{act[4]}' target='_blank'>pdf</a>"
        if act[5]:
            file_path_edo = f"<a href='{URL}{ACT_DIR}{act[5]}' target='_blank'>pdf</a>"
        # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
        if act[6] == 1:
            demand = 'Отгружен'
        elif act[6] == 0:
            demand = 'Архив'
        elif act[6] == 2:
            orders = ozon.get_act_orders(act_id, header)
            i = 0
            j = 0
            for order in orders:
                order_db_res = db.get_order_ms_id(seller_id, order)
                if not order_db_res:
                    continue
                order_href = order_db_res[0][1]
                order_dict = ms.get_order_params_and_attributes(order_href, [],
                                                                [MS_FIELD_SOBRAN_BOOL])
                if order_dict[MS_FIELD_SOBRAN_BOOL]:
                    db.update_oder_demand(seller_id, order_href, 1)
                    j += 1
                i += 1
            if j != i:
                demand = f"Собрано {j}/{i}"
            else:
                demand = f'<button type="submit" value={act_id} name="create_demand" class="my">Отгрузить</button> {j}/{i}'

        rows += '<tr>' \
               f'<td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{act_id}</td>' \
                f'<td width = "200" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt}</td>' \
                f'<td width = "200" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{dt_update}</td>' \
               f'<td width = "100" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{status}</td>' \
               f'<td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path}</td>' \
                f'<td width = "120" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{file_path_edo}</td>' \
                f'<td width = "130" height = "30" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{demand}</td>' \
                f'</tr>'

    db.close()
    return unescape(
        render_template("acts.html", url=url, login=LOGIN, passw=PASSW, seller_id=seller_id,
                        status_text=status_text, rows=rows, name=name,
                        edit_seller_url=edit_seller_url, index_url=index_url))



if __name__ == "__main__":
    from waitress import serve
    serve(app, host = '0.0.0.0', port = '4567')
    # app.run(debug=True, host = '0.0.0.0', port = '4567')