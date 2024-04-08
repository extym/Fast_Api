import os
import json
import logging
from html import unescape
from flask import Flask, request, flash, redirect, render_template, url_for
from datetime import datetime, timedelta
from psql import PgDatabase
from settings import *

if LOCAL_MODE:
    PUBLIC_DIR = './'
else:
    PUBLIC_DIR = '/home/userbe/profit/'


def get_all_site_cats():
    db = PgDatabase(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASW, database=MYSQL_DATABASE)
    cats_list = db.get_site_categories()
    print(len(cats_list), type(cats_list))


# get_all_site_cats()



app = Flask(__name__,
            template_folder='templates',
            static_folder='templates/static'
            )

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     url_login = url_for("login", _external=True)
#     url = url_for('index', _external=True)
#
#     if request.method == 'GET':
#         login = request.values.get('login')
#         passw = request.values.get('passw')
#         # seller_id = request.values.get('seller_id')
#
#     if request.method == 'POST':
#         result = request.form
#         login = result['login']
#         passw = result['passw']
#         # seller_id = result.get('seller_id')
#
#     if login is None or login != LOGIN or passw is None or passw != PASSW:
#         return unescape(render_template('ui-login.html', url=url))
#
#     else:
#         return redirect('index', passw=passw, login=login, url=url, url_login=url_login)
#

# @app.route('/', methods=['GET', 'POST'])
# def root():
#     url = url_for('index', _external=True)
#     return redirect('index', url=url) ####unescape(render_template('ui-login.html'), url=url)



@app.route("/index", methods=['GET', 'POST'])
def index():
    headers = request.headers
    ip_addr = request.environ.get('REMOTE_ADDR')
    print('ip_addr_index', ip_addr)
    addr = request.headers.get('X-Forwarded-For')
    print('addr_index', addr)
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Index page Started' + str(addr) + '-' + str(ip_addr))
        logging.info('Headers' + str(headers))

    db = PgDatabase(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASW, database=MYSQL_DATABASE)
    url_categories = url_for('edit_vendor_products', _external=True)
    url = url_for('index', _external=True)
    # seller_orders_url = url_for('seller_orders', _external=True)

    status = ''
    status_text = ''
    # vendor_name = ''

    # contragents_dict = db.get_dict('counterparty')

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        vendor_name = request.values.get('vendor_name')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        vendor_name = result.get('vendor_name')

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))


    ######################## Отображение таблицы селлеров ###########################

    sellers = ''
    # sellers_list = db.get_all_sellers()
    url_categoies_href = f"{url_categories}?login={login}&passw={passw}&vendor_name={vendor_name}"
    # site_categories = db.get_seller_id_category()
    # #print(type(site_categories))
    # proxy, shipments_list_today = [], []
    # for cd in site_categories:
    #     cd = list(cd)
    #     proxy.extend(cd)
    #     shipments_list_today = tuple(set(proxy))
      ##################################################################################
    # if request.method == 'POST':
    result = request.form
    result_status_text = ''



    ######################################################################

    # db.close()
    acts_today_href = f"<a href='{URL} + {PUBLIC_DIR} + 'acts_not_assembled_day/all_acts_today.pdf' target='_blank'>Акты сегодня</a>"
    # not_ass_labels = f"<a href='{URL}labels_not_assembled/all_labels.pdf' target='_blank'>Все этикетки</a>"
    not_ass_labels_day = f"<a href='{URL}labels_not_assembled_day/all_labels_day.pdf' target='_blank'>Этикетки сегодня</a>"

    return unescape(
        render_template("index.html", url_today=url_categoies_href, url=url, login=LOGIN, passw=PASSW, sellers=sellers,
                        status=status, acts_today_href=acts_today_href, vendor_name=vendor_name,
                        result_status_text=result_status_text, index_url=url,
                        status_text=status_text))  #contragents=contragents, name=name, rows=rows,


@app.route("/edit_vendor_products", methods=['GET', 'POST'])
def edit_vendor_products():
    headers = request.headers
    ip_addr = request.environ.get('REMOTE_ADDR')
    print('ip_addr_edit_vendors', ip_addr)
    addr = request.headers.get('X-Forwarded-For')
    print('addr_edit_vendors', addr)
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller_products page Started' + str(addr) + '-'  + str(ip_addr))
        logging.info('Headers' + str(headers))

    db = PgDatabase(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASW, database=MYSQL_DATABASE)
    url_categories = url_for('edit_vendor_products', _external=True)
    url = url_for('index', _external=True)
    index_url = url_for('index', _external=True)
    result_url = url_for('resutl_edit_vendor', _external=True)

    # edit_seller_url = url_for('edit_seller', _external=True)

    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        vendor_name = request.values.get('vendor_name')


    if request.method == 'POST' or request.method == 'GET':
        result = request.form
        login = result['login']
        passw = result['passw']
        vendor_name = result.get('vendor_name')
        # print('result_name', result)
        print('vendor_name_1', vendor_name)
        ############################ Сохранение селлера #################################

        errors = 0
        jobs = 0
        # if result.get('get_categoies'):

        if result.get('save_products'):
            site_categories = db.get_seller_id_category_v2(vendor_name)
            for category in site_categories:
                category_id = category[0]
                site_category_id = category[3]

                # ms_id = str(category[4])
                new_vendor_id = result.get(str(category_id))


                try:
                    new_category_id = result.get(str(category_id) + '_price')  #int(result.get(str(category_id) + '_price'))
                except:
                    new_category_id = 0

                if new_category_id and new_category_id != site_category_id:
                    print('how-how', vendor_name, category_id, new_category_id)
                    try:
                        if not db.update_site_delive(vendor_name, category_id, new_category_id):
                            errors += 1
                        jobs += 1
                    except:
                        pass
                    # print(vendor_name, category_id, new_vendor_id)

                    # print('category', category)

        if errors:
            status_text = f"При обновлении связей категорий возникло {errors} ошибок"
        elif jobs:
            status_text = f"Обновлены связи {jobs} категорий"
        else:
            status_text = f"Связи категорий без изменений"

    if TEST_MODE:
        login = LOGIN
        passw = PASSW
    if login is None or login != LOGIN or passw is None or passw != PASSW:
        return unescape(render_template("ui-login.html", text="Неверный логин/пароль", url=url))

    if not vendor_name:
        return f'Не найден vendor_name<br><a href="{url_categories}?login={login}&passw={passw}">Назад</a>'
    else:
        pass

    url_categoies_href = f"{url_categories}?login={login}&passw={passw}&vendor_name={vendor_name}"

    rows = ''
    # ozon_products = db.get_products(vendor_name)
    # site_categodies = db.get_seller_id_category()
    site_categodies = db.get_seller_id_category_v2(vendor_name)
    # vendor_categories = db.get_vendor_id_categoies(vendor_name)
    vendor_categories = db.get_vendor_id_categoies_v2(vendor_name)
    for category in site_categodies:
        # try:
        category_id = category[0]
        insales_id = category[3]
        offer_id = category[6]
        name = category[2]
        ms_id = category[4]
        site_category_id = category[11]
        if not site_category_id:
            site_category_id = '0'
        # if vendor_name == 'netlab':
        #     delive = category[10]
        # elif vendor_name == '3logic':
        #     delive = category[11]
        # else:
        #     delive = ''
        # if category[6]:
        #     discount = category[6]
        # else:
        #     discount = '0'

        vendor_categories_text = ''
        for elem in vendor_categories:
            if ms_id and elem[0] == ms_id:
                vendor_categories_text += f"<option value='{elem[0]}' selected='selected'>{elem[1]} / name: {elem[2]} / category: {elem[3]} / parent: {elem[6]}</option>"
            elif not elem[0]:
                vendor_categories_text += f"<option value='' selected='selected'></option>"
            else:
                vendor_categories_text += f"<option value='{elem[0]}'>{elem[1]} / name: {elem[2]} / category: {elem[3]} / parent: {elem[6]}</option>"
        # except:
        #     continue
        # if not ms_id:
        #     vendor_categories_text += f"<option value='' selected='selected'></option>"

        rows += f'<tr><td width = "450" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle">{name} / id: {category_id} / site_id: {insales_id} / parent_id: {offer_id}</td>' \
                f'<td width = "450" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><select name={category_id}  style="max-width:450;">{vendor_categories_text}</select></td>' \
                f'<td width = "170" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><input type="text" name="{category_id}_price" value="{site_category_id}" style="width: 160px;" required="required"></td></tr>'
                #f'<td width = "170" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><input type="text" name="{category_id}_discount" value="{discount}" style="width: 160px;" required="required">' \
        # f'<td width = "70" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; background-color: #f3f3f3; vertical-align:middle"><input type="text" name="count_base" value="{count_base}" style="width: 60px;" required="required"></td>' \
    # db.close()
    print('Закрыли БД')

    return unescape(
        render_template("products.html", url_categories=url_categories,  login=LOGIN, passw=PASSW, vendor_name=vendor_name,
                        status_text=status_text, index_url=index_url, rows=rows, result_url=result_url)) #edit_seller_url=edit_seller_url, index_url=index_url,



@app.route("/result_vendor_products", methods=['GET', 'POST'])
def resutl_edit_vendor():
    headers = request.headers
    ip_addr = request.environ.get('REMOTE_ADDR')
    print('ip_addr_result_vendors', ip_addr)
    addr = request.headers.get('X-Forwarded-For')
    print('addr_result_vendors', addr)
    if LOGGING:
        logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
                            format='[%(asctime)s] [%(levelname)s] => %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info('Edit_seller_products page Started' + str(addr) + '-' + str(ip_addr))
        logging.info('Headers' + str(headers))

    db = PgDatabase(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASW, database=MYSQL_DATABASE)
    url = url_for('edit_vendor_products', _external=True)
    # url = url_for('resutl_edit_vendor', _external=True)
    index_url = url_for('index', _external=True)
    result_url = url_for('resutl_edit_vendor', _external=True)
    # edit_seller_url = url_for('edit_seller', _external=True)

    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        vendor_name = request.values.get('vendor_name')

    if request.method == 'POST':
        result = request.form
        login = result['login']
        passw = result['passw']
        vendor_name = result.get('vendor_name')
        # print('result_name_2', result)
        # print('vendor_name', vendor_name)
        ############################ Сохранение селлера #################################

        errors = 0
        jobs = 0
        # if result.get('get_categoies'):

        if result.get('save_products'):
            site_categories = db.get_seller_id_category_v2(vendor_name)
            # print('AFTER_2')
            for category in site_categories:
                # print('category', category)
                line_id = category[0]
                site_category_id = category[3]
                new_vendor_id = result.get(str(line_id))

                try:
                    new_category_id = result.get(str(line_id) + '_price')
                    # print(111111111111, new_category_id)
                except:
                    new_category_id = '0'

                if new_category_id != [0] and new_category_id != site_category_id:
                    # print(333333333333333333, new_category_id)
                    try:
                        if not db.update_site_delive_v2(vendor_name, line_id, new_category_id):
                            errors += 1
                        jobs += 1
                    except:
                        # pass
                        print('This_except_category', vendor_name, line_id, new_vendor_id)


        if errors:
            status_text = f"При обновлении связей категорий возникло {errors} ошибок"
        elif jobs:
            status_text = f"Обновлены связи {jobs} категорий"
        else:
            status_text = f"Связи категорий без изменений"

    return unescape(
        render_template("products.html", url=url, login=LOGIN, passw=PASSW, vendor_name=vendor_name,
                        status_text=status_text, index_url=index_url, result_url=result_url
                        ))  # edit_seller_url=edit_seller_url, index_url=index_url,


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #
    # http_server = WSGIServer(('0.0.0.0', 5577), app)
    # http_server.serve_forever()

    app.run(debug=True, host="0.0.0.0", port=5577)