"""
Flask
"""
from gevent import monkey
monkey.patch_all()


from gevent.pywsgi import WSGIServer
import os
import logging
from flask import Flask, request, render_template, url_for, redirect, send_file
from html import unescape
import json
import time
from datetime import datetime
from connect import Data_base_connect
from settings import LOG_FILE, PUBLIC_DIR, MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, LOGGING, \
    LOGIN, PASSW, TEST_MODE, OZON_COMMENT_FIELDS, OZON_DATA_FIELDS, OZON_TYPES, MS_DEFAULT_PRICE, LABEL_DIR, URL, \
    ACT_DIR, MS_FIELD_SOBRAN_BOOL, MS_DEMAND_STATUS_PAYED, MS_DEMAND_STATUS_NOT_PAYED, MS_ORDER_STATUS_NOT_PAYED, \
    MS_MINUS_STATUS
# from database import MsDatabase
import ozon
import ms

app = Flask(__name__,
            static_folder='templates/static')  #,
           # template_folder='templates/')


@app.route("/", methods=['GET', 'POST'])
def index():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('index', _external=True)
    # url_today = url_for('sellers_today', _external=True)
    dashboard_url = url_for("dashboard", _external=True)


    # contragents_dict = db.get_dict('counterparty')

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        ############################ Добавление селлера #################################

        ############################# Удаление файлов #####################################

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    ######################## Отображение таблицы селлеров ###########################

    # sellers_today_href = f"<a href='{url_today}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
    dashboard_href = f"<a href='{dashboard_url}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
    #not_ass_labels = f"<a href='{URL}labels_not_assembled/all_labels.pdf' target='_blank'>Все этикетки</a>"
    #not_ass_labels_day = f"<a href='{URL}labels_not_assembled_day/all_labels_day.pdf' target='_blank'>Этикетки сегодня</a>"
    return unescape(render_template("index.html", url=url, login=LOGIN, passw=PASSW,
                                    dashboard_href=dashboard_href))  #sellers_today_href=sellers_today_href, sellers=sellers, contragents=contragents,




@app.route("/blank", methods=['GET', 'POST'])
def blank():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('index', _external=True)
    # url_today = url_for('sellers_today', _external=True)
    dashboard_url = url_for("dashboard", _external=True)
    seller_orders_url = url_for('seller_orders', _external=True)
    seller_acts_url = url_for('seller_acts', _external=True)
    edit_seller_url = url_for('edit_seller', _external=True)
    status = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        ############################ Добавление селлера #################################


    if TEST_MODE:
        login = LOGIN
        passw = PASSW
        if login is None or login != LOGIN or passw is None or passw != PASSW:
            return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

        ######################## Отображение таблицы селлеров ###########################

        # sellers_today_href = f"<a href='{url_today}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
        dashboard_href = f"<a href='{dashboard_url}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
        return unescape(render_template("blank.html", url=url, login=LOGIN, passw=PASSW, status=status,
                                    dashboard_href=dashboard_href))  #sellers_today_href=sellers_today_href, sellers=sellers, contragents=contragents,


@app.route("/add_mp", methods=['GET', 'POST'])
def add_mp():
    if request.method == 'POST':
        result = request.form
        seller_id = result['sellerId']
        name_mp = result['name']
        id_mp = result['id']
        key_mp = result['key']

@app.route("/main_table", methods=['GET', 'POST'])
def main_table():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    #db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('index', _external=True)
    main_table_url = url_for('main_table', _external=True)
    dashboard_url = url_for("dashboard", _external=True)
    # seller_orders_url = url_for('seller_orders', _external=True)
    # seller_acts_url = url_for('seller_acts', _external=True)
    # edit_seller_url = url_for('edit_seller', _external=True)
    status = ''
    end_block = 'Сводная таблица заказов'

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']


    if TEST_MODE:
        login = LOGIN
        passw = PASSW
        if login is None or login != LOGIN or passw is None or passw != PASSW:
            return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    ###################################################
    rows = ''
    db = Data_base_connect()
    raw_list_orders = db.select_orders()
    for row in raw_list_orders:
        print(len(raw_list_orders), row)
        order_id = row[1]

        rows += '<tr>' \
                f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order_id}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[3]}</td>' \
                f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[7]}</td>' \
                f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[8]}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[9]}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[10]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[11]}</td>' \
                f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[12]}</td>' \
                f'</tr>'

    ################################################

    main_table_href = f"<a href='{main_table_url}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
    dashboard_href = f"<a href='{dashboard_url}?login={login}&passw={passw}' target='_blank'>Сегодня</a>"
    return unescape(render_template("tables-responsive.html", url=url, login=LOGIN, passw=PASSW, status=status,
                                    main_table_href=main_table_href, end_block=end_block, rows=rows,
                                    dashboard_href=dashboard_href))  #sellers=sellers, contragents=contragents,



@app.errorhandler(404)
def page_not_found(error):
    url = url_for('index', _external=True)
    return render_template("blank.html", title='404', url=url, login=LOGIN, passw=PASSW), 404


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started')

    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('index', _external=True)
    dashboard_url = url_for("dashboard", _external=True)


    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    else:
        dashboard_href = f"{dashboard_url}?login={login}&passw={passw}"
        return unescape(render_template("dashboard.html", login=LOGIN, passw=PASSW, dashboard_href=dashboard_href))





if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host = '0.0.0.0', port = '7654')
    # #Debug/Development
    ##run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=7654)
    # Production
    # http_server = WSGIServer(('', 7654), app)
    # http_server.serve_forever()