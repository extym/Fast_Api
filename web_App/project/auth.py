import datetime
import logging
import time

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user

from html import unescape

from sqlalchemy import func

from .connect import Data_base_connect as Db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users, ConsultUsers, Sales, Product, Marketplaces
from . import db, TEST_MODE
from sqlalchemy.orm import Session, load_only
from sqlalchemy import update
# Pagination
from flask_paginate import Pagination, get_page_parameter
from contextlib import closing
# # Redis
from rq import Worker, Queue, Connection
from project.worker import conn
from rq.job import Job

q = Queue(connection=conn)

auth = Blueprint('auth', __name__)


@auth.route('/login-ui')
def login():
    return render_template('ui-login.html')


@auth.route('/login-ui', methods=['POST'])
def login_post():
    print(request.form)
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('login')
    company_id = request.form.get('company_id')
    remember = True if request.form.get('remember') else False

    # user = Users.query.filter_by(email=email).first()
    user = Users.query.filter_by(name=name, company_id=company_id).first()

    if not user or not check_password_hash(user.password, password):
        flash("Проверте правильность ввода логина и пароля")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/form-consult', methods=['post'])
def form_consult():
    name = request.form.get('inlineFormName2')
    mail = request.form.get('inlineFormUserEmail2')
    phone = request.form.get('inlineFormUserPhone2')
    now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
    foreigin_id = current_user.id
    company_id = current_user.company_id

    new_consulting = ConsultUsers(name=name,
                                  email=mail,
                                  phone=phone,
                                  company_id=company_id,
                                  current_user_id=foreigin_id,
                                  role=current_user.role,
                                  date_added=now_date,
                                  date_modifed=now_date)

    db.session.add(new_consulting)
    db.session.commit()

    role = current_user.roles
    return redirect('blank-2.html', role=role)


@auth.route('/signup')
def signup():
    return render_template('ui-register.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # ('cabinetID', '1'), ('login', '1'), ('email', '1'), ('password', '1234'), ('remember', 'forever'), ('wp-submit', 'Зарегистрироваться')
    email = request.form.get('email')
    name = request.form.get('login')
    password = request.form.get('password')
    user = Users.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
    company_id = request.form.get('cabinetID')

    if user:
        flash('Адрес почты уже существует')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email,
                     name=name,
                     company_id=company_id,
                     role='owner',
                     date_added=now_date,
                     date_modifed=now_date,
                     password=generate_password_hash(password, method='scrypt'))

    db.session.add(new_user)
    db.session.commit()

    role = current_user.roles
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index_main'))


@auth.route('/dashboard')
@login_required
def dashboard():
    # make smth
    pass
    return unescape(render_template('index.html'))


@auth.route('/main-page')
@login_required
def main_page():
    pass
    return render_template('base-layout.html')


@auth.route('/add_mp')  # /<int:uid>')
@login_required
# @roles_required('owner')
def add_mp():
    session = Session()
    uid = current_user.id
    role = current_user.roles
    need_id = current_user.company_id
    dt_bs = Db()
    need_data = dt_bs.select_shop_name(need_id)
    rows = []
    for row in need_data:
        rows.extend(list(row))
    # rows = [list(i) for i in need_data]
    print(type(need_data[0]))
    return render_template('mp_settings.html', uid=uid, role=role, rows=rows)


def check_api(key_mp, shop_id):
    pass


@auth.route('/user-settings')
@login_required
def user_settings():
    uid = current_user.id
    role = current_user.roles
    return render_template('user-settings.html', uid=uid, role=role)


@auth.route('/add_mp', methods=['POST'])  # /<int:uid>')
@login_required
def add_mp_post():
    data = request.form
    uid = current_user.id
    role = current_user.roles
    print(data)
    if 'select_mp' in data:
        mp = data.get('select_mp')
        shop_name = data.get('name')
        shop_id = data.get('id_mp')
        key_mp = data.get('key')

        if mp == 'Выбрать...':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return render_template('mp_settings.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return render_template('mp_settings.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, API ключ магазина на маркетплейсе', 'error')
            return render_template('mp_settings.html')

        if mp == 'ozon' and key_mp != None and shop_id != None:
            if TEST_MODE:
                result = True
            else:
                result = check_api(key_mp, shop_id)
            # print('result', result)
            if result:
                d_b = Db()
                d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
                # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
                # db.session.add(mp_sett)
                # db.session.commit()
                flash('Настройки удачно сохранены', 'success')
            else:
                flash('Проверьте, пожалуйста, данные', 'error')
                return render_template('mp_settings.html')

        if mp == 'yandex' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        if mp == 'wb' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
            flash('Настройки удачно сохранены', 'success')

        if mp == 'leroy' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
            flash('Настройки удачно сохранены', 'success')

    if 'add_user_role' in data:
        user_role = data.get('add_user_role')
        user_name = data.get('user_name')
        user_email = data.get('user_email')
        user_password = data.get('Password')
        now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
        company_id = request.form.get('cabinetID')
        user = Users.query.filter_by(email=user_email).first()

        if user:
            flash('Адрес почты уже существует')
            return render_template('mp_settings.html', uid=uid)
        elif not user and user_email != '' and user_name != '':

            new_user = Users(email=user_email,
                             name=user_name,
                             company_id=company_id,
                             role=user_role,
                             date_added=now_date,
                             date_modifed=now_date,
                             password=generate_password_hash(user_password, method='scrypt')
                             )
            db.session.add(new_user)
            db.session.commit()

            flash('Настройки удачно сохранены', 'success')
        else:
            flash('Заполните, пожалуйста, все поля')

    if 'import_from' in data:
        pass
        # job = q.enqueue_call(test_time)
        # print(job.get_id)
    if 'select_name_mp' in data:
        pass

    return redirect('/add_mp')


@auth.route('/edit_product')
@login_required
def edit_product(product=None):
    role = current_user.roles
    if product is None:
        product = {
            'selected_mp': '',
            'articul_product': '',
            'name_product': '',
            'status_mp': '',
            'images_product': '',
            'price_product_base': '0',
            'price_add_k': '1',
            'discount_mp_product': '1.0',
            'quantity': '0',
            'description_product': '',
            'set_shop_name': '',
            'external_sku': '',
            'alias_prod_name': '',
            'status_in_shop': '',
            'shop_k_product': '1.0',
            'discount_shop_product': '1.0',
            'quantity_for_shop': '0',
            'description_product_add': ''
        }

    # return render_template('product-edit.html', role=role)
    return render_template('product-edit-add.html',
                           TEST_MODE=TEST_MODE,
                           role=role,
                           product=product,
                           price_product_base=product.get('price_product_base'))

    # selected_mp=selected_mp,
    # articul_product=articul_product,
    # name_product=name_product,
    # status_mp=status_mp,
    # images_product=image_product,
    # price_product_base=price_product_base,
    # price_add_k=price_add_k,
    # discount_mp_product=discount_mp_product,
    # quantity=quantity,
    # description_product=description_product,
    # set_shop_name=set_shop_name,
    # external_sku=external_sku,
    # alias_prod_name=alias_prod_name,
    # status_in_shop=alias_prod_name,
    # photo_line=photo_line,
    # shop_k_product=shop_k_product,
    # discount_shop_product=discount_shop_product,
    # quantity_for_shop=quantity_for_shop,
    # description_product_add=description_product_add
    # )


# def test_time():
#     count = 1
#     for _ in range(10):
#         count += 1
#         time.sleep(1)
#     return count


@auth.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.return_value), 200
    else:
        return "Nay!", 202


@auth.route('/edit_product', methods=['POST'])
@login_required
def edit_product_post():
    data = request.form.to_dict()
    role = current_user.roles
    # print('/edit_product', *data, sep='\n')
    # print('/edit_product', *data, sep=', \n')
    if 'search_product' in data:
        articul = data.get('search_product')
        if articul and articul != '':
            product = db.session.query(Product).filter_by(articul_product=articul) \
                .first().as_dict()
            # prod = Product.query.filter_by(articul_product="12345").first().__dict__
            print(22222, *product.items(), sep='\n') #' sep=' = prod.get(""),\n')
            print(33333, product)

            # job = q.enqueue_call(test_time

            # print(job.get_id)

            return render_template('/product-edit-add.html', product=product)

    else:
        prod_set = Product(
            uid_edit_user=current_user.id,
            selected_mp=data.get('select_mp', '0'),
            shop_name=data.get('set_shop_name', '0'),
            articul_product=data.get('articul_product', '0'),
            name_product=data.get('name_product', '0'),
            status_mp=data.get('status_mp', '0'),
            images_product=data.get('image_product', '0'),
            price_product_base=data.get('price_product_base', '0'),
            price_add_k=data.get('price_add_k', '1'),
            discount_mp_product=data.get('discount_mp_product', '0'),
            quantity=data.get('quantity', '0'),
            description_product=data.get('id_mp', '0'),
            set_shop_name=data.get('set_shop_name', '0'),
            external_sku=data.get('external_sku', '0'),
            alias_prod_name=data.get('alias_prod_name', '0'),
            status_in_shop=data.get('status_in_shop', '0'),
            shop_k_product=data.get('shop_k_product', 1.0),
            discount_shop_product=data.get('discount_shop_product', '0'),
            quantity_for_shop=data.get('quantity_for_shop', '0'),
            description_product_add=data.get('description_product_add', ' '),
            final_price=0.0
        )

        try:
            db.session.add(prod_set)
            db.session.commit()
            flash('Товар удачно сохранен', 'success')

        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!', data)
                db.session.rollback()
                articul_product = data.get('articul_product')
                product = Product.query.filter_by(articul_product=articul_product).update(data)
                # # print('!!!!!!!!!!!!!!!!!!!!!!!!!!', data, product)
                db.session.commit()
                flash(f'Товар с артикулом {articul_product} удачно обновлен', 'success')
        except Exception as error:
            db.session.rollback()
            logging.error('Ошибка сохранения отредактированного товара {} {}'
                          .format(current_user.id, error))
            flash('Уже существует продукт с таким Артикулом (ID)', 'error')

        finally:
            db.session.close()

        # print(123, session)
        # return render_template('product-edit.html', role=role)
    return redirect('/edit_product')


@auth.route('/add_product')  # /<int:uid>')
@login_required
def add_product():
    uid = current_user.id
    role = current_user.roles
    # return render_template('form-product.html', uid=uid, role=role)
    return render_template('product-add.html', uid=uid, role=role)


@auth.route('/add_product', methods=['POST'])  # /<int:uid>')
@login_required
def add_product_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    print('/add_product', *data, sep='\n')
    print('/add_product', *data, sep=', \n')
    shop_k_product = data.get('shop_k_product', 1)
    shop_name = data.get('set_shop_name', '0')
    price_product_base = data.get('price_product_base', '0')
    prod_set = Product(
        uid_edit_user=current_user.id,
        selected_mp=data.get('select_mp', '0'),
        shop_name=shop_name,
        articul_product=data.get('articul_product', '0'),
        name_product=data.get('name_product', '0'),
        status_mp=data.get('status_mp', '0'),
        images_product=data.get('image_product', '0'),
        price_product_base=price_product_base,
        price_add_k=data.get('price_add_k', '1'),
        discount_mp_product=data.get('discount_mp_product', '0'),
        quantity=data.get('quantity', '0'),
        description_product=data.get('id_mp', '0'),
        set_shop_name=data.get('set_shop_name', '0'),
        external_sku=data.get('external_sku', '0'),
        alias_prod_name=data.get('alias_prod_name', '0'),
        status_in_shop=data.get('status_in_shop', '0'),
        photo_line=data.get('photo_line', '0'),
        shop_k_product=float(shop_k_product),
        discount_shop_product=data.get('discount_shop_product', '0'),
        quantity_for_shop=data.get('quantity_for_shop', '0'),
        description_product_add=data.get('description_product_add', ' '),
        final_price=0.0
    )

    if shop_name is None:
        flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
        return render_template('form-validation.html')

    if price_product_base is None:
        flash('Укажите, пожалуйста, базовую цену товара на маркетплейсе', 'error')
        return render_template('product-add.html')

    try:
        db.session.add(prod_set)
        db.session.commit()
        flash('Настройки удачно сохранены', 'success')
    except Exception as error:
        db.session.rollback()
        logging.error('Ошибка сохранения товара {} {}'
                      .format(current_user.id, error))
        flash('Уже существует продукт с таким Артикулом (ID)', 'error')
    finally:
        db.session.close()
        return redirect(url_for('auth.add_product'))

    # return render_template('form-product.html', uid=uid, role=role)


@auth.route('/products')
@auth.route('/products/products_page', methods=['GET', 'POST'])
@auth.route('/products/products_page/<int:page>', methods=['GET', 'POST'])
@login_required
def products_page(page=1):
    uid = current_user.id
    role = current_user.roles
    rows = ''
    limit = 30
    my_query = db.func.count(Product.id)
    all_product = db.session.execute(my_query).scalar()
    max_page = all_product // limit
    raw_list_products = db.session.query(Product).paginate(page=page, per_page=30, error_out=False)
    for row in raw_list_products.items:
        print(8888888, row)

        rows += '<tr>' \
                f'<td>{row.name_product}</td>' \
                f'<td >{row.articul_product}</td>' \
                f'<td >{row.external_sku}</td>' \
                f'<td >{row.quantity}</td>' \
                f'<td >{row.discount}</td>' \
                f'<td >{row.final_price}</td>' \
                f'<td >{row.date_added}</td>' \
                f'<td >{row.date_modifed}</td>' \
                f'<td >{row.discount_shop_product}</td>' \
                f'<td >{row.status_in_shop}</td>' \
                f'</tr>'

    return unescape(render_template('tables-products.html', rows=rows, role=role,
                                    raw_list_products=raw_list_products, max_page=max_page))


@auth.route('/shops')
@login_required
def shops():
    uid = current_user.id
    role = current_user.roles
    rows = ''
    # d_b = Db()
    # raw_list_orders = d_b.select_orders()  # TODO make select orders to user id
    # raw_list_products = db.session.query(Product).all()
    # raw_list_products = db.session.query(Product).paginate(page=30, per_page=30, error_out=False).items
    # for row in raw_list_products:
    #     print(8888888, len(raw_list_products), row)
    #     order_id = row[1]
    #     price = ''
    #
    #     rows += '<tr>' \
    #             f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order_id}</td>' \
    #             f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
    #             f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[7]}</td>' \
    #             f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
    #             f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[8]}</td>' \
    #             f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{price}</td>' \
    #             f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[9]}</td>' \
    #             f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[10]}</td>' \
    #             f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[11]}</td>' \
    #             f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[12]}</td>' \
    #             f'</tr>'

    return unescape(render_template('tables-shops.html', rows=rows, role=role))




@auth.route('/sales', methods=['GET', 'POST'])
@auth.route('/sales/sales_page', methods=['GET', 'POST'])
@auth.route('/sales/sales_page/<int:page>', methods=['GET', 'POST'])
def sales_page(page=1):
    uid = current_user.id
    role = current_user.roles
    rows = ''
    limit = 30
    sales = db.session.query(Sales)\
        .paginate(page=page, per_page=limit, error_out=False)
    my_query = db.func.count(Sales.id)
    total_sales = db.session.execute(my_query).scalar()
    max_page = total_sales // limit
    for row in sales.items:
        print(row)
        rows += '<tr>' \
                f'<td>{row.shop_order_id}</td>' \
                f'<td >{row.article}</td>' \
                f'<td >{row.article_mp}</td>' \
                f'<td >{row.quantity}</td>' \
                f'<td >{row.price}</td>' \
                f'<td >{row.shop_name}</td>' \
                f'<td >{row.date_added}</td>' \
                f'<td >{row.shipment_date}</td>' \
                f'<td >{row.order_status}</td>' \
                f'<td >{row.category}</td>' \
                f'</tr>'

    return unescape(render_template('table-paginate.html', rows=rows, role=role,
                                    max_page=max_page, total_sales=total_sales,
                                    sales=sales))


@auth.route('/users-table')
@login_required
def users_table():
    role = current_user.roles
    data = []
    rows = ''

    # raw_list_orders = db.session.query(Sales).paginate(page=page, per_page=30, error_out=False).items
    for row in data:
        user_id = ''

        rows += '<tr>' \
                f'<td>{user_id}</td>' \
                f'<td >{row.article}</td>' \
                f'<td >{row.shop_order_id}</td>' \
                f'<td >{row.quantity}</td>' \
                f'<td >{row.price}</td>' \
                f'<td >{row.shop_name}</td>' \
                f'<td >{row.date_added}</td>' \
                f'<td >{row.shipment_date}</td>' \
                f'<td >{row.order_status}</td>' \
                f'<td >{row.category}</td>' \
                f'</tr>'

    return unescape(render_template('users-table.html', rows=rows, role=role))


# @auth.route('/add-product')
# @login_required
# def add_product():
#     pass
#
#     return unescape(render_template('eco-product-add.html'))


@auth.app_errorhandler(404)
def page_not_found(error):
    role = current_user.roles
    return render_template("blank-2.html", title='404', role=role), 404


# @auth.route('/main_table')
# @auth.route('/main_table/<int:page>', methods=['GET', 'POST'])
# def main_table():
#     uid = current_user.id
#     role = current_user.roles
#     rows = ''
#
#     if current_user.roles in ['admin', 'owner']:
#         content = {}
#         company_id = current_user.company_id
#         # открываем соединение с БД
#         db = Db().conn
#         # определяем текущую страницу пагинации
#         page = request.args.get(get_page_parameter(), type=int, default=1)
#         limit = 3
#         # определяем `offset` записей для основного запроса
#         offset = 0 if page == 1 else (page - 1) * limit
#         # with closing(db.cursor()) as cursor:
#         cursor = db.cursor()
#         cursor.execute("SELECT id FROM sales WHERE company_id=%s", (company_id,))
#         total = cursor.rowcount
#         print(222222222222, total, company_id)
#
#         pagination = Pagination(page=page, total=total, search=True,
#                                 per_page=limit, css_framework='bootstrap3')  # bs_version=4)
#         # `page` это номер текущей страницы, параметр URL (по умолчанию page') из которого
#         #  он будет извлекаться. Его можно настроить, например Pagination(page_parameter='p', ...)
#         # или установить `PAGE_PARAMETER` в файле конфигурации.
#         # Также можно настроить параметр URL, который будет передавать количество выводимых
#         # записей на одной странице, например Pagination(per_page_parameter='pp') или установить
#         # параметр `PER_PAGE` в файле конфигурации
#
#         if total:
#
#             with closing(db.cursor()) as cursor:
#                 # try:
#                 cursor.execute("SELECT * FROM sales "
#                                "WHERE company_id = %s LIMIT %s OFFSET %s ",
#                                (current_user.company_id, limit, offset))
#                 # except Exception as e:
#                 #     print(f'{e.args} ==> {e.args}')
#                 #     # abort(404)
#                 dsata = cursor.fetchall()
#                 for row in dsata:
#                     print(row)
#                     rows += '<tr>' \
#                             f'<td>{row[1]}</td>' \
#                             f'<td >{row[3]}</td>' \
#                             f'<td >{row[2]}</td>' \
#                             f'<td >{row[4]}</td>' \
#                             f'<td >{row[6]}</td>' \
#                             f'<td >{row[7]}</td>' \
#                             f'<td >{row[8]}</td>' \
#                             f'<td >{row[9]}</td>' \
#                             f'<td >{row[21]}</td>' \
#                             f'<td >{row[20]}</td>' \
#                             f'</tr>'
#         else:
#             # abort(404)
#             print(1111, 'fuckup')
#
#         if db:
#             # закрываем соединение с БД
#             db.close()
#
#         return unescape(render_template('tables-responsive.html',
#                                         rows=rows, role=role, pagination=pagination))
#
#     # raw_list_orders = d_b.select_orders()  #db.select_orders()  TODO make select orders to user id
#     # raw_list_orders = db.session.query(Sales).all()
#     # raw_list_orders = db.session.query(Sales).paginate(page=page, per_page=30, error_out=False).items
#
#     # for row in raw_list_orders:
#     #     print(7777888, row.mp_order_id)
#     #     order_id = row.shop_order_id
#     #     price = 1200
#     #
#     #     rows += '<tr>' \
#     #             f'<td>{order_id}</td>' \
#     #             f'<td >{row.article}</td>' \
#     #             f'<td >{row.shop_order_id}</td>' \
#     #             f'<td >{row.quantity}</td>' \
#     #             f'<td >{row.price}</td>' \
#     #             f'<td >{row.shop_name}</td>' \
#     #             f'<td >{row.date_added}</td>' \
#     #             f'<td >{row.shipment_date}</td>' \
#     #             f'<td >{row.order_status}</td>' \
#     #             f'<td >{row.category}</td>' \
#     #             f'</tr>'
#
#     # rows += '<tr>' \
#     #         f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order_id}</td>' \
#     #         f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
#     #         f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[7]}</td>' \
#     #         f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
#     #         f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[8]}</td>' \
#     #         f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{price}</td>' \
#     #         f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[9]}</td>' \
#     #         f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[10]}</td>' \
#     #         f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[11]}</td>' \
#     #         f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[12]}</td>' \
#     #         f'</tr>'
#
#     ################################################
#
#     return unescape(render_template('tables-responsive.html', rows=rows, role=role))
