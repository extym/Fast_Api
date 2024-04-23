import datetime
import logging
import time

import flask_login
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user, UserMixin

from html import unescape

from sqlalchemy import func, select, update, join, values, text
from sqlalchemy.sql.functions import sum
from .database import Data_base_connect as Db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from . import db, TEST_MODE
from sqlalchemy.orm import Session, load_only

from project.import_ozon import import_oson_data_prod, make_internal_import_oson
from project.wb import import_product_from_wb
# Pagination
from flask_paginate import Pagination, get_page_parameter
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
                                  role=current_user.roles,
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
                     roles='owner',
                     date_added=now_date,
                     date_modifed=now_date,
                     password=generate_password_hash(password, method='scrypt'))

    db.session.add(new_user)
    db.session.commit()

    flash('Вы удачно зарегистрировались. Войдите в аккаунт')
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


def check_api(key_mp, shop_id):
    pass


@auth.route('/add_mp')  # /<int:uid>')
@login_required
# @roles_required('owner')
def add_mp():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        need_id = current_user.company_id
        need_data = db.session.execute(select(Marketplaces.shop_name)
                                       .where(Marketplaces.company_id == need_id))
        rows = []
        for row in need_data:
            rows.extend(row)
        # print(3333333, row, rows)
        return render_template('mp_settings.html', uid=uid, role=role, rows=rows)


@auth.route('/add_mp', methods=['POST'])  # /<int:uid>')
@login_required
def add_mp_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    company_id = current_user.company_id
    print(11111111111, data)
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
                d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
                # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
                # db.session.add(mp_sett)
                # db.session.commit()
                flash('Настройки удачно сохранены', 'success')
            else:
                flash('Проверьте, пожалуйста, данные', 'error')
                return render_template('mp_settings.html')

        if mp == 'yandex' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        if mp == 'wb' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            flash('Настройки удачно сохранены', 'success')

        if mp == 'leroy' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            flash('Настройки удачно сохранены', 'success')

        if mp == 'sber' and key_mp and shop_id:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

    if 'import_from' in data:
        pass
        # job = q.enqueue_call(test_time)
        # print(job.get_id)
    if 'edit_shop' in data:
        print(33333333333333333333333, data)
        if 'edit_shop' == 'Выбрать...' and 'edit_shop_settings' == 'Выбрать':
            flash('Не выбран магазин')
        if 'edit_shop_settings' != 'Выбрать' and 'key':
            mp = data.get('edit_shop')
            shop_name = data.get('edit_shop_name')
            shop_id = data.get('id_mp')
            key_mp = data.get('key')
            d_b = Db()
            d_b.update_mp(shop_name, mp, key_mp)
        print(*data.keys(), sep='\n')
    # if
    #     pass

    return redirect('/add_mp')


@auth.route('/edit_mp', methods=['POST'])  # /<int:uid>')
@login_required
def edit_mp_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    company_id = current_user.company_id
    print(11111111111, data)
    if 'edit_name_mp' in data:
        mp = data.get('edit_name_mp')
        shop_name = data.get('edit_shop_names')
        shop_id = data.get('id_mp')
        key_mp = data.get('key')

        if mp == 'Выбрать...':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return redirect('/add_mp')

        if shop_name == 'Выбрать':
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return redirect('/add_mp')

        if shop_name != 'Выбрать' and mp != 'Выбрать...' and key_mp:
            print(1111, mp, shop_name, key_mp)
            mp = data.get('edit_shop')
            shop_name = data.get('edit_shop_name')
            shop_id = data.get('id_mp')
            key_mp = data.get('key')
            d_b = Db()
            d_b.update_mp(shop_name, mp, key_mp)

            flash('Настройки удачно сохранены', 'success')
            return redirect('/add_mp')

    return redirect('/add_mp')


@auth.route('/edit_store', methods=['POST'])  # /<int:uid>')
@login_required
def edit_store_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    company_id = current_user.company_id
    print(*data.items(), sep='\n')
    # {'select_name_mp': 'Выбрать...',
    # 'extract_articul_shop': '',
    # 'mp_discount': '',
    # 'price_before': '',
    # 'add_articul_mp': '',
    # 'extract_articul_mp': '',
    # 'set_shop_settings': 'Выбрать',
    # 'extra_markup_shop': '',
    # 'formfield6': '',
    # 'shop_add_price_before': '',
    # 'formfield7': '',
    # 'formfield11': ''}
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
                d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
                # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
                # db.session.add(mp_sett)
                # db.session.commit()
                flash('Настройки удачно сохранены', 'success')
            else:
                flash('Проверьте, пожалуйста, данные', 'error')
                return render_template('mp_settings.html')

        if mp == 'yandex' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        if mp == 'wb' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            flash('Настройки удачно сохранены', 'success')

        if mp == 'leroy' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            flash('Настройки удачно сохранены', 'success')

        if mp == 'sber' and key_mp and shop_id:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

    if 'import_from' in data:
        pass
        # job = q.enqueue_call(test_time)
        # print(job.get_id)
    if 'edit_shop' in data:
        print(33333333333333333333333, data)
        if 'edit_shop' == 'Выбрать...' and 'edit_shop_settings' == 'Выбрать':
            flash('Не выбран магазин')
        if 'edit_shop_settings' != 'Выбрать' and 'key':
            mp = data.get('edit_shop')
            shop_name = data.get('edit_shop_name')
            shop_id = data.get('id_mp')
            key_mp = data.get('key')
            d_b = Db()
            d_b.update_mp(shop_name, mp, key_mp)
        print(*data.keys(), sep='\n')

    return redirect('/add_mp')


@auth.route('/import_settings')
# @roles_required('owner')
def import_settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        need_id = current_user.company_id
        need_data = db.session.execute(select(Marketplaces.shop_name,
                                              Marketplaces.name_mp)
                                       .where(Marketplaces.company_id == need_id))
        rows, rows_mp = [], []
        for row in need_data:
            rows.append(row[0])
            rows_mp.append(row[1])

        return render_template('/import_settings.html',
                               uid=uid, role=role, rows=rows, rows_mp=set(rows_mp))


@auth.route('/import_settings', methods=['POST'])
@login_required
# @roles_required('owner')
def import_settings_post():
    uid = str(current_user.id)
    role = current_user.roles
    company_id = current_user.company_id
    data = request.form.to_dict()
    make = data.get('make')
    print(111, data, current_user.name)
    if make == 'start_import':
        mp = data.get('import_mp_name')
        shop_name = data.get('import_shop_names')
        if mp == 'ozon':
            job = q.enqueue_call(import_oson_data_prod(user_id=uid,
                                                       shop_name=shop_name,
                                                       company_id=company_id))
            print(777777777777, job.get_id)
        elif mp == 'wb':
            job = q.enqueue_call(import_product_from_wb(uid_edit_user=uid,
                                                        shop_name=shop_name,
                                                        company_id=company_id))
            print(88888888888, job.get_id)

        return redirect('/import_settings')

    elif make == 'save_internal_import':
        internal_import_mp_1 = data.get('internal_import_mp_1')
        internal_import_store_1 = data.get('internal_import_store_1')
        internal_import_role_1 = data.get('internal_import_role_1')

        if internal_import_mp_1 != 'Выбрать...' and internal_import_store_1 != 'Выбрать...' \
                and internal_import_role_1 == 'donor':
            in_import = InternalImport(
                internal_import_mp_1=internal_import_mp_1,
                internal_import_store_1=internal_import_store_1,
                internal_import_role_1=internal_import_role_1,
                internal_import_markup_1=data.get('internal_import_markup_1'),
                internal_import_discount_1=data.get('internal_import_discount_1'),
                internal_import_mp_2=data.get('internal_import_mp_2'),
                internal_import_store_2=data.get('internal_import_store_2'),
                internal_import_role_2=data.get('internal_import_role_2'),
                internal_import_discount_2=data.get('internal_import_discount_2'),
                internal_import_markup_2=data.get('internal_import_markup_2'),
                company_id=current_user.company_id,
                user_id=current_user.name
            )
            db.session.add(in_import)
            db.session.commit()
            flash("Настройки удачно сохранены", 'success')
        else:
            flash("Проверьте, пожалуйста, корректность вводимых данных", 'error')
            return redirect('/import_settings')

    elif make == 'start_internal_import':
        internal_import_mp_1 = data.get('internal_import_mp_1')
        internal_import_store_1 = data.get('internal_import_store_1')
        internal_import_role_1 = data.get('internal_import_role_1')
        internal_import_mp_2 = data.get('internal_import_mp_2')
        internal_import_store_2 = data.get('internal_import_store_2')
        internal_import_role_2 = data.get('internal_import_role_2')

        if internal_import_role_1 != internal_import_role_2 and \
                internal_import_store_1 != internal_import_store_2 and \
                internal_import_mp_1 != 'Выбрать... ' and \
                internal_import_mp_2 != 'Выбрать... ':
            if internal_import_role_2 == 'donor' and internal_import_role_1 == 'recipient':
                donor = data.get('internal_import_store_2')
                recipient = data.get('internal_import_store_1')
                donor_mp = data.get('internal_import_mp_2')
                recipient_mp = data.get('internal_import_mp_1')
            else:
                donor = data.get('internal_import_store_1')
                recipient = data.get('internal_import_store_2')
                donor_mp = data.get('internal_import_mp_1')
                recipient_mp = data.get('internal_import_mp_2')

            job = q.enqueue_call(make_internal_import_oson(donor=donor,
                                                           recipient=recipient,
                                                           sourse='front',
                                                           donor_mp=donor_mp,
                                                           recipient_mp=recipient_mp))
            print(989898989, job.get_id)
        # print(*data.items(), sep='\n')

    return redirect('/import_settings')


@auth.route('/user-settings')
@login_required
def user_settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        users = Users.query.filter_by(company_id=current_user.company_id).all()
        rows = [row.name for row in users if row.name not in ('admin100500', 'Admin100500')]
        # print(rows)
        return render_template('user-settings.html', uid=uid, role=role, rows=rows)


@auth.route('/user-settings', methods=['POST'])
@login_required
def user_settings_post():
    data = request.form.to_dict()
    uid = current_user.id
    if 'add_user_role' in data:
        user_role = data.get('add_user_role')
        user_name = data.get('user_name')
        user_email = data.get('user_email')
        user_password = data.get('Password')
        now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
        company_id = current_user.company_id  # request.form.get('cabinetID')
        user = Users.query.filter_by(email=user_email).first()

        if user:
            flash('Адрес почты уже существует')
            return render_template('mp_settings.html', uid=uid)
        elif not user and user_email != '' and user_name != '':

            new_user = Users(email=user_email,
                             name=user_name,
                             company_id=company_id,
                             roles=user_role,
                             date_added=now_date,
                             date_modifed=now_date,
                             password=generate_password_hash(user_password, method='scrypt')
                             )
            db.session.add(new_user)
            db.session.commit()

            flash('Настройки удачно сохранены', 'success')
        else:
            flash('Заполните, пожалуйста, все поля')

    if 'edit_user_role' in data:
        user_role = data.get('edit_user_role')
        exist_user_name = data.get('edit_user_exist')
        user_email = data.get('user_email')
        user_password = data.get('Password')
        now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
        company_id = current_user.company_id  # request.form.get('cabinetID')
        user = Users.query.filter_by(name=exist_user_name).first()
        if user_role != '' and user.roles != user_role:
            smth = update(Users).where(Users.name == exist_user_name) \
                .where(Users.company_id == company_id) \
                .values({'roles': user_role, 'date_modifed': now_date})
            db.session.execute(smth)
            flash("Роль пользователя успешно изменена")
        if user_email != '':
            smth = update(Users).where(Users.name == exist_user_name) \
                .where(Users.company_id == company_id) \
                .values({'email': user_email, 'date_modifed': now_date})
            db.session.execute(smth)
            flash("Емайл пользователя успешно изменена")
        if user_password != '':
            smth = update(Users).where(Users.name == exist_user_name) \
                .where(Users.company_id == company_id) \
                .values({'password': generate_password_hash(user_password, method='scrypt'),
                         'date_modifed': now_date})
            db.session.execute(smth)
            flash("Пароль пользователя успешно изменен")

        db.session.commit()
        db.session.close()

    return redirect('/user-settings')


def test_time():
    count = 1
    for _ in range(10):
        count += 1
        time.sleep(1)
    return count


@auth.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        job = Job.fetch(job_key, connection=conn)

        if job.is_finished:
            return str(job.return_value), 200
        else:
            return "Nay!", 202


@auth.route('/edit_product')
@login_required
def edit_product(product=None):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        rows_shops = db.session.execute(select(Marketplaces.shop_name)
                                        .where(Marketplaces.company_id == current_user.company_id)).all()
        # print(rows_shops, type(rows_shops))
        rows = [row[0] for row in rows_shops]
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
                               price_product_base=product.get('price_product_base'),
                               rows=rows)

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
        # shop_k_product=shop_k_product,
        # discount_shop_product=discount_shop_product,
        # quantity_for_shop=quantity_for_shop,
        # description_product_add=description_product_add
        # )


@auth.route('/edit_product', methods=['POST'])
@login_required
def edit_product_post():
    data = request.form.to_dict()
    role = current_user.roles
    # print('/edit_product', *data, sep='\n')
    # print('/edit_product', *data, sep=', \n')
    if 'search_product' in data:
        articul = data.get('search_product')
        shop_name = data.get('shop_name')
        if articul and articul != '':
            try:
                product = db.session.query(Product).filter_by(articul_product=articul, shop_name=shop_name) \
                    .first().as_dict()
            except:
                flash('Артикул не найден')
                product = {}
            rows_shops = db.session.execute(select(Marketplaces.shop_name)
                                            .where(Marketplaces.company_id == current_user.company_id)).all()
            # print(rows_shops, type(rows_shops))
            rows = [row[0] for row in rows_shops]
            # prod = Product.query.filter_by(articul_product="12345").first().__dict__
            # print(22222, *product.items(), sep='\n')  # ' sep=' = prod.get(""),\n')
            # print(33333, product)

            return render_template('/product-edit-add.html', product=product, rows=rows)

    else:
        prod_set = Product(
            uid_edit_user=current_user.id,
            selected_mp=data.get('select_mp', '0'),
            shop_name=data.get('set_shop_name', '0'),
            articul_product=data.get('articul_product', '0'),
            name_product=data.get('name_product', '0'),
            status_mp=data.get('status_mp', '0'),
            images_product=data.get('image_product', '0'),
            price_product_base=int(data.get('price_product_base', '0')) * 100,
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
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
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
    price_product_base = int(data.get('price_product_base', '0')) * 100
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
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        rows = ''
        limit = 30
        my_query = db.func.count(Product.id)
        all_product = db.session.execute(my_query).scalar()
        max_page = all_product // limit
        raw_list_products = db.session.query(Product) \
            .paginate(page=page, per_page=30, error_out=False)
        for row in raw_list_products.items:
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

        return unescape(render_template('tables-products.html',
                                        rows=rows, role=role,
                                        raw_list_products=raw_list_products,
                                        max_page=max_page))


@auth.route('/shops')
@login_required
def shops():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
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
@login_required
def sales_page(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        rows = ''
        limit = 30
        sales = db.session.query(Sales) \
            .paginate(page=page, per_page=limit, error_out=False)
        my_query = db.func.count(Sales.id)
        total_sales = db.session.execute(my_query).scalar()
        max_page = total_sales // limit
        for row in sales.items:
            # print(row)
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


@auth.route('/sales_today', methods=['GET', 'POST'])
@auth.route('/sales_today/sales_today', methods=['GET', 'POST'])
@auth.route('/sales_today/sales_today/<int:page>', methods=['GET', 'POST'])
@login_required
def sales_today(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        rows = ''
        limit = 30
        # sales_today = db.session.query(SalesToday) \
        #     .paginate(page=page, per_page=limit, error_out=False)
        sales_today = db.session.query(SalesToday) \
            .paginate(page=page, per_page=limit, error_out=False)
        my_query = db.func.count(SalesToday.id)
        total_sales_today = db.session.execute(my_query).scalar()
        max_page = total_sales_today // limit
        for row in sales_today.items:
            # print(row)
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

        return unescape(render_template('table-sales-today.html',
                                        rows=rows, role=role,
                                        max_page=max_page,
                                        total_sales_today=total_sales_today,
                                        sales_today=sales_today))


@auth.route('/assembly_sales', methods=['GET', 'POST'])
@auth.route('/assembly_sales/assembly_sales', methods=['GET', 'POST'])
@auth.route('/assembly_sales/assembly_sales/<int:page>', methods=['GET', 'POST'])
@login_required
def assembly_sales(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        rows = ''
        limit = 30
        HOUR = '09:00:00'
        example = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(f"%Y-%m-%d {HOUR}")
        # print(333333333333, example, type(example))
        my_query = db.func.count(SalesToday.id)
        total_assembly_sales = db.session.execute(my_query).scalar()
        max_page = total_assembly_sales // limit

        # assembly_orders = db.session.query(SalesToday) \
        #     .where(SalesToday.date_added > example) \
        #     .order_by(SalesToday.article_mp) \
        #     .paginate(page=page, per_page=limit, error_out=False)

        assembly_orders = db.session.query(SalesToday.article_mp,
                                           SalesToday.shop_name,
                                           SalesToday.article,
                                           SalesToday.order_status,
                                           func.sum(SalesToday.quantity).label('total_sales')) \
            .group_by(SalesToday.article_mp,
                      SalesToday.shop_name,
                      SalesToday.article,
                      SalesToday.order_status) \
            .where(SalesToday.date_added > example) \
            .where(SalesToday.shop_status == "NEW") \
            .order_by(SalesToday.article_mp) \
            .paginate(page=page, per_page=limit, error_out=False)

        # print(333333, assembly)
        # print(assembly)

        for row in assembly_orders.items:
            # print(11111111111, row)

            s_today = (select(Product.photo)
                       .where(Product.articul_product == row.article)
                       .where(Product.shop_name == row.shop_name))

            photo = db.session.execute(s_today).first()
            # print(111, photo)
            if photo is None:
                photo = ('нет фото',)

            # if row.shipment_date is not None:
            #     shipment_date = str(row.shipment_date).split(" ")
            # else:
            #     shipment_date = row.shipment_date
            #
            # rows += '<tr>' \
            #         f'<td ><img class="img-fluid" src="{photo[0]}" alt="" style="max-width:50px;"></td>' \
            #         f'<td>{row.shop_order_id}</td>' \
            #         f'<td >{row.article}</td>' \
            #         f'<td >{row.shop_name}</td>' \
            #         f'<td >{row.quantity}</td>' \
            #         f'<td >{str(row.date_added).rsplit(".")[0]}</td>' \
            #         f'<td >{shipment_date}</td>' \
            #         f'<td >{row.order_status}</td>' \
            #         f'</tr>'

            rows += '<tr>' \
                    f'<td ><img class="img-fluid" src="{photo[0]}" alt="" style="max-width:50px;"></td>' \
                    f'<td>{row.article}</td>' \
                    f'<td >{row.shop_name}</td>' \
                    f'<td >{row.total_sales}</td>' \
                    f'<td >{row.order_status}</td>' \
                    f'</tr>'

        return unescape(render_template('table-assembly-sales.html',
                                        rows=rows, role=role,
                                        max_page=max_page,
                                        total_assembly_sales=total_assembly_sales,
                                        assembly_sales=assembly_orders))


@auth.route('/users-table')
@auth.route('/users-table/users-table', methods=['GET', 'POST'])
@auth.route('/users-table/users-table/<int:page>', methods=['GET', 'POST'])
@login_required
def users_table(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        company_id = current_user.company_id
        role = current_user.roles
        data = []
        rows = ''
        limit = 10
        raw_list_orders = db.session.query(Users) \
            .filter_by(company_id=company_id) \
            .paginate(page=page, per_page=30, error_out=False).items
        my_query = db.func.count(Users.id)
        total_users = db.session.execute(my_query).scalar()
        max_page = total_users // limit
        for row in raw_list_orders:
            if row.name == 'admin100500' or row.name == 'Admin100500':
                continue
            else:
                rows += '<tr>' \
                        f'<td>{row.name}</td>' \
                        f'<td >{row.email}</td>' \
                        f'<td >{row.roles}</td>' \
                        f'<td >{row.date_added}</td>' \
                        f'<td >{row.date_modifed}</td>' \
                        f'</tr>'

        return unescape(render_template('users-table.html',
                                        rows=rows, role=role,
                                        max_page=max_page,
                                        total_users=total_users))


# @auth.route('/add-product')
# @login_required
# def add_product():
#     pass
#
#     return unescape(render_template('eco-product-add.html'))


@auth.app_errorhandler(404)
def page_not_found(error):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        # role = current_user.roles
        return render_template("blank-2.html", title='404'), 404


@auth.app_errorhandler(500)
def page_server_error(error):
    role = current_user.roles
    return render_template("blank-500.html", title='500', role=role, error=error), 500

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
