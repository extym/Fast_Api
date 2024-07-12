import os
import json
import logging
from html import unescape
from flask import Flask, request, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pandas as pd

from logic import write_categories_logic_v2, save_categories_vendor
from maintenance import update_categories_from_site, update_categories_from_site_v2, execute_query_update
from marvel import save_categories_marvel
from merlion import write_categories_merlion, save_categories_merlion
from netlab import get_netlab_token_v2, save_categories_netlab
from creds import secret_key, vendors
from ocs import save_categories_ocs
from psql import PgDatabase
from settings import *
from conn import executemany_query
from conn_maintenance import query_update_from_file
from treolan import write_categories_treolan, save_categories_treolan

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PUBLIC_DIR = './'
else:
    PUBLIC_DIR = '/home/userbe/profit/'
    UPLOAD_FOLDER = '/var/www/html/load/'

ALLOWED = {'csv', 'xls', 'xlsx'}

from urllib.parse import urlparse


def check_allowed_filename(filename):
    result = '.' in filename and filename.rsplit('.')[1] in ALLOWED
    curr_name = filename.rsplit('.')[1]
    vendor = filename.rsplit('.')[0]
    return result, curr_name, vendor


def compare_id(tuple_data):
    return tuple_data[0]


def read_xls(file, vendor_name):
    f = pd.read_excel(file)
    dataframe = pd.DataFrame(f).values
    proxy = list()
    for row in dataframe:
        try:
            key = str(row[0]).split(' / ')[1].split(': ')[1]
            proxy.append((row[1], int(row[2]), int(key), vendor_name))
            print(22222, row)
        except Exception as error:
            print(111111111, row, ' fuck_up- {}'.format(error))
            continue

    return proxy


def get_all_site_cats():
    db = PgDatabase(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASW, database=MYSQL_DATABASE)
    cats_list = db.get_site_categories()
    print(len(cats_list), type(cats_list))


# get_all_site_cats()



app = Flask(__name__,
            template_folder='templates',
            static_folder='templates/static'
            )
app.secret_key = secret_key

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
async def index():
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
    result_status_text = ''
    sellers = ''
    # sellers_list = db.get_all_sellers()
    url_categories_href = f"{url_categories}?login={login}&passw={passw}&vendor_name={vendor_name}"
      ##################################################################################
    if request.method == 'POST':
        result = request.form

        if result.get('get_categories') and vendor_name:
            await update_categories_from_site(vendor_name)
            result_status_text = 'Some update'



    ######################################################################

    acts_today_href = f"<a href='{URL} + {PUBLIC_DIR} + 'acts_not_assembled_day/all_acts_today.pdf' target='_blank'>Акты сегодня</a>"
    # not_ass_labels = f"<a href='{URL}labels_not_assembled/all_labels.pdf' target='_blank'>Все этикетки</a>"
    not_ass_labels_day = f"<a href='{URL}labels_not_assembled_day/all_labels_day.pdf' target='_blank'>Этикетки сегодня</a>"

    return unescape(
        render_template("index.html", url_today=url_categories_href, url=url, login=LOGIN, passw=PASSW, sellers=sellers,
                        status=status,  vendor_name=vendor_name, index_url=url,  status_text=status_text, result_status_text=result_status_text))
                    #contragents=contragents, name=name, rows=rows,result_status_text=result_status_text, acts_today_href=acts_today_href,


@app.route("/edit_vendor_products", methods=['GET', 'POST'])
async def edit_vendor_products():
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
    upload_url = url_for('upload_file', _external=True)
    index_url = url_for('index', _external=True)
    result_url = url_for('resutl_edit_vendor', _external=True)

    # edit_seller_url = url_for('edit_seller', _external=True)

    status_text = ''

    if request.method == 'GET':
        login = request.values.get('login')
        passw = request.values.get('passw')
        vendor_name = request.values.get('vendor_name')


    if request.method == 'POST':
        result = request.form.to_dict()
        login = result['login']
        passw = result['passw']
        vendor_name = result.get('vendor_name')
        print('result_name', result)
        print('vendor_name_1', vendor_name)
        ############################################################

        errors = 0
        jobs = 0
        o = urlparse(request.base_url)
        host = o.hostname
        if result.get('get_categories') and vendor_name:
            await update_categories_from_site_v2(vendor_name)
            result_status_text = 'Some update'
        if result.get('get_categories_vendor') and vendor_name:
            if vendor_name == 'netlab':
                await get_netlab_token_v2()
                await save_categories_netlab()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/netlab_categories.csv">http://{host}/csv/netlab_categories.csv</a>')
            elif vendor_name == 'logic':
                await save_categories_vendor()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/logic_categories.csv">http://{host}/csv/logic_categories.csv</a>')
            elif vendor_name == 'ocs':
                await save_categories_ocs()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/ocs_categories.csv">http://{host}/csv/ocs_categories.csv</a>')
            elif vendor_name == 'marvel':
                await save_categories_marvel()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/marvel_categories.csv">http://{host}/csv/marvel_categories.csv</a>')
            elif vendor_name == 'treolan':
                await save_categories_treolan()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/treolan_categories.csv">http://{host}/csv/treolan_categories.csv</a>')
            elif vendor_name == 'merlion':
                await save_categories_merlion()
                flash(f'Данные категорий получены. Файл находится  <a href="http://{host}/csv/merlion_categories.csv">http://{host}/csv/merlion_categories.csv</a>')

            return redirect(url_for("index"))
            # return unescape(
            #     render_template("products.html", url_categories=url_categories,
            #                     login=LOGIN, passw=PASSW,
            #                     vendor_name=vendor_name,
            #                     status_text=status_text,
            #                     index_url=index_url,
            #                     result_url=result_url,
            #                     upload_url=upload_url))  # edit_seller_url=edit_seller_url, index_url=index_url,

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
    # print(site_categodies, sep="/n")
    categories = sorted(site_categodies, key=compare_id)
    vendor_categories = db.get_vendor_id_categoies(vendor_name)
    # print(7777777, vendor_categories)
    # vendor_categories = db.get_vendor_id_categoies_v2(vendor_name)
    for category in categories:
        # try:
        category_id = category[0]
        insales_id = category[3]
        offer_id = category[6]
        name = category[2]
        ms_id = category[4]
        site_category_id = category[11]
        if not site_category_id:
            site_category_id = '0'


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
        render_template("products.html", url_categories=url_categories,
                        login=LOGIN, passw=PASSW,
                        vendor_name=vendor_name,
                        status_text=status_text, index_url=index_url,
                        rows=rows, result_url=result_url, upload_url=upload_url)) #edit_seller_url=edit_seller_url, index_url=index_url,



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
        print('result_name_2', result)
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
                current_category_id = category[11]
                try:
                    new_category_id = result.get(str(line_id) + '_price')
                except:
                    new_category_id = '0'
                if new_category_id and new_category_id != current_category_id:   #site_category_id:
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
        render_template("products.html", url=url, login=LOGIN,
                        passw=PASSW, vendor_name=vendor_name,
                        status_text=status_text, index_url=index_url,
                        result_url=result_url
                        ))  # edit_seller_url=edit_seller_url, index_url=index_url,


@app.route("/upload", methods=['GET', 'POST'])
async def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Невозможно прочитать файл')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)

        vendor = file.filename.split('-')[0].strip().replace('3', '').lower()
        print(vendor)
        if vendor not in vendors:
            flash('Vendor not found')
            return redirect(request.url)

        check = check_allowed_filename(file.filename)
        if file and check[0]:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        if check[1] == 'xlsx' and vendor:
            data = read_xls(file, vendor)
            await executemany_query(query_update_from_file, data)

            flash('Файл excel загружен')
            return redirect(request.url)

    return render_template('file.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #
    # http_server = WSGIServer(('0.0.0.0', 5577), app)
    # http_server.serve_forever()

    app.run(debug=True, host="0.0.0.0", port=5577)