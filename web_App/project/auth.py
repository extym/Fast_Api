import datetime
import logging
import os
import time
from html import unescape

from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from psycopg2.errors import UniqueViolation
# Pagination
# # Redis
from rq import Queue
from rq.job import Job
from sqlalchemy import func, select, update, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# from project.wb import import_product_from_wb
import project.wb as wb
from project.import_ozon import import_oson_data_prod, make_internal_import_oson_product, make_import_export_oson_price
from project.worker import conn
from project import TEST_MODE, PHOTO_UPLOAD_FOLDER, engine, ozon
from .database import Data_base_connect as Db
from .models import *
from . import db
from apscheduler.schedulers.background import BackgroundScheduler

import project.ozon as oson

import logging

LOG_DIR = os.getcwd() + './project/logs'
print('LOG_DIR', LOG_DIR)
logging.basicConfig()
# logging.basicConfig(level=logging.DEBUG, filename=LOG_DIR + '/auth_log.log',
#                     format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()

q = Queue(connection=conn)

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def back_shops_tasks():
    with Session(engine) as session:
        markets = session.query(Marketplaces) \
            .filter(or_(Marketplaces.check_send_null == True,
                        Marketplaces.send_common_stocks == True,
                        Marketplaces.enable_orders_submit == True,
                        Marketplaces.enable_sync_stocks == True,
                        Marketplaces.enable_sync_price == True)) \
            .all()
    for row in markets:
        shop_name = row.shop_name
        key = row.key_mp
        seller_id = row.seller_id

        if row.check_send_null:
            if row.name_mp == 'ozon':
                oson.send_stocks_oson_v2(key=key,
                                         seller_id=seller_id,
                                         is_stocks_null=True)
                print('Send_stocks_oson_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                      .format(len(key), seller_id, True))
                logging.DEBUG('Send_stocks_oson_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                              .format(len(key), seller_id, True))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v2(sourse='web',
                                     seller_id=seller_id,
                                     is_stocks_null=True)
                print('Send_stocks_wb_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                      .format(len(key), seller_id, True))
                logging.DEBUG('Send_stocks_wb_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                              .format(len(key), seller_id, True))

        if row.send_common_stocks:
            ii_raw = session.query(InternalImport) \
                .where(InternalImport.internal_import_store_2 == row.shop_name) \
                .where(InternalImport.internal_import_role_2 == 'recipient') \
                .first()
            store_1 = ii_raw.internal_import_store_1
            if row.name_mp == 'ozon':
                oson.send_stocks_oson_v3(key_recipient=key,
                                         donor=store_1,
                                         recipient=seller_id)
                print('Send_stocks_oson_v3 - donor {}, recipient {}'
                      .format(store_1, row.seller_id))
                logging.DEBUG('Send_stocks_oson_v3 - donor {}, recipient {}'
                              .format(store_1, row.seller_id))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v3(donor=store_1,
                                     recipient=seller_id)
                print('Send_stocks_oson_v3 - donor {}, recipient {}'
                      .format(store_1, seller_id))
                logging.DEBUG('Send_stocks_oson_v3 - donor {}, recipient {}'
                              .format(store_1, seller_id))

        if row.enable_orders_submit:
            if row.name_mp == 'ozon':
                # get_stocks_oson_v2(key=row.key_mp,
                #                     seller_id=row.seller_id,
                #                     is_stocks_null=False)
                # TODO
                pass
            elif row.name_mp == 'wb':
                wb.processing_orders_wb_v2(key=row.key_mp,
                                           shop_name=shop_name)
                print('Processing_orders_wb_v2 - len_key {}, shop_name {}'
                      .format(len(key), shop_name))
                logging.DEBUG('Processing_orders_wb_v2 - len_key {}, shop_name {}'
                              .format(len(key), shop_name))

        if row.enable_sync_stocks:
            if row.name_mp == 'ozon':
                ozon.send_stocks_oson_v2(key=key,
                                         seller_id=seller_id,
                                         is_stocks_null=False)
                print('Send_stocks_oson_v2 - seller_id {} is_stocks_null {}'
                      .format(seller_id, False))
                logging.DEBUG('Send_stocks_oson_v2 - seller_id {} is_stocks_null {}'
                              .format(seller_id, False))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v2(seller_id=seller_id,
                                     is_stocks_null=False,
                                     sourse='web')
                print('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                      .format(seller_id, False))
                logging.DEBUG('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                              .format(seller_id, False))

        if row.enable_sync_price:
            if row.name_mp == 'ozon':
                ozon.send_product_price(key_recipient=key,
                                        recipient=seller_id)
                print('Send_product_price oson - seller_id {} recipient {}'
                      .format(len(row.key_mp), row.seller_id))
                logging.DEBUG('Send_product_price oson - seller_id {} recipient {}'
                              .format(len(key), seller_id))

            if row.name_mp == 'wb':
                wb.send_price_to_wb(seller_id=seller_id, sourse='web')
                print('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                      .format(len(key), seller_id))
                logging.DEBUG('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                              .format(len(key), seller_id))

    print(777, markets)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    return redirect(url_for('main.come_in'))


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
    user_login = request.form.get('login')
    password = request.form.get('password')
    photo = ''
    user = Users.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
    name = request.form.get('name', f'{user_login}_{now_date}')
    company_id = request.form.get('cabinetID')

    if user:
        flash('Адрес почты уже существует')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email,
                     name=name,
                     login=user_login,
                     company_id=company_id,
                     roles='owner',
                     date_added=now_date,
                     date_modifed=now_date,
                     photo=photo,
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
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        pass
        return unescape(render_template('index.html'))


@auth.route('/main-page')
@login_required
def main_page():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        pass
        return render_template('base-layout.html')


def check_api(key_mp, shop_id):
    return True


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
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        need_data = db.session.execute(select(Marketplaces.shop_name)
                                       .where(Marketplaces.company_id == need_id))
        tags = ["Контент", "Цены и скидки", "Маркетплейс",
                "Статистика", "Аналитика", "Продвижение"]
        rows = []
        for row in need_data:
            rows.extend(row)
        # print(3333333, row, rows)
        return render_template('mp_settings.html', uid=uid,
                               role=role, rows=rows,
                               photo=photo,
                               tags=tags,
                               user_name=user_name)


@auth.route('/add_mp', methods=['POST'])  # /<int:uid>')
@login_required
def add_mp_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    company_id = current_user.company_id
    date_add = datetime.datetime.now()
    print(113333333111, data)
    if 'insert_new_shop' in data:
        mp = data.get('insert_new_shop')
        shop_name = data.get('name')
        shop_id = data.get('id_mp')
        key_mp = data.get('key')

        if mp == 'Выбрать':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return redirect('/add_mp')

        if shop_name is None:
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return redirect('/add_mp')

        if shop_name is None:
            flash('Укажите, пожалуйста, API ключ магазина на маркетплейсе', 'error')
            return redirect('/add_mp')

        if mp == 'ozon' and key_mp != None and shop_id != None:
            if TEST_MODE:
                result = True
            else:
                result = check_api(key_mp, shop_id)
            print('result', result)
            if result:
                # d_b = Db()
                # d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
                # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
                # db.session.add(mp_sett)
                # db.session.commit()
                # d_b = Db()
                # d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
                mp_sett = Marketplaces(
                    user_id=uid,
                    seller_id=shop_id,
                    shop_name=shop_name,
                    name_mp=mp,
                    key_mp=key_mp,
                    company_id=company_id,
                    date_added=date_add)
                db.session.add(mp_sett)
                print(2222222222222222222222222222222222222222222222)
                db.session.commit()
                flash('Настройки удачно сохранены', 'success')
            else:
                flash('Проверьте, пожалуйста, данные', 'error')
                return redirect('/add_mp')

        if mp == 'yandex' and key_mp != None and shop_id != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id)
            # mp_sett = Marketplaces(uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        if mp == 'wb':
            tags = data.get('tags')
            # print(data)
            if not tags or tags == '':
                uid = current_user.id
                role = current_user.roles
                need_id = current_user.company_id
                user_name = current_user.name
                photo = current_user.photo
                if not photo or photo is None:
                    photo = 'prof-music-2.jpg'
                need_data = db.session.execute(select(Marketplaces.shop_name,
                                                      Marketplaces.name_mp)
                                               .where(Marketplaces.company_id == need_id))
                tags = ["Контент", "Цены и скидки", "Маркетплейс",
                        "Статистика", "Аналитика", "Продвижение"]
                rows, rows_mp = [], []
                for row in need_data:
                    rows.append(row[0])
                    rows_mp.append(row[1])

                return render_template('mp_settings.html',
                                       uid=uid, shop_name=shop_name,
                                       role=role, rows=rows,
                                       rows_mp=set(rows_mp),
                                       photo=photo, id_mp=shop_id,
                                       show_wb=True, mp=mp,
                                       tags=tags, key_mp=key_mp,
                                       user_name=user_name)

            elif tags and key_mp != None and shop_id != None:
                tags_list = tags.split(",")
                d_b = Db()
                d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp, company_id, tags=tags_list)
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
        if 'edit_shop' == 'Выбрать' and 'edit_shop_settings' == 'Выбрать':
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

        if mp == 'Выбрать':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return redirect('/add_mp')

        if shop_name == 'Выбрать':
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return redirect('/add_mp')

        if shop_name != 'Выбрать' and mp != 'Выбрать' and key_mp:
            # print(1111, mp, shop_name, key_mp)
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

    if 'name_mp' in data:
        settings = dict()
        if data['shop_name'] != 'Выбрать':
            for key, value in data.items():
                if value != '':
                    settings.update({key: value})

            # del settings['settings_store']
            market = Marketplaces.query \
                .filter_by(shop_name=settings['shop_name']) \
                .update(settings)
            db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        else:
            flash('Выберите редактируемый магазин')

    return redirect('/add_mp')


@auth.route('/import_settings')
@login_required
# @roles_required('owner')
def import_settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        rows, rows_mp = [], []
        show = request.args.get('show')
        # print(1111111111111, show, request.args.get('make'))
        # if show:
        #     uid = current_user.id
        #     role = current_user.roles
        #     need_id = current_user.company_id
        #     user_name = current_user.name
        #     photo = current_user.photo
        #     if not photo or photo is None:
        #         photo = 'prof-music-2.jpg'
        #     internal_import_role_1 = request.args.get("internal_import_role_1")
        #     internal_import_markup_1 = request.args.get("internal_import_markup_1")
        #     internal_import_store_2 = request.args.get("internal_import_store_2")
        #     internal_import_discount_2 = request.args.get("internal_import_discount_2")
        #     internal_import_mp_1 = request.args.get("internal_import_mp_1")
        #     internal_import_store_1 = request.args.get("internal_import_store_1")
        #     internal_import_discount_1 = request.args.get("internal_import_discount_1")
        #     internal_import_mp_2 = request.args.get("internal_import_mp_2")
        #     internal_import_role_2 = request.args.get("internal_import_role_2")
        #     internal_import_markup_2 = request.args.get("internal_import_markup_2")
        #
        #     return render_template('/import_settings.html',
        #                            uid=uid, role=role,
        #                            internal_import_role_1=internal_import_role_1,
        #                            internal_import_markup_1=internal_import_markup_1,
        #                            internal_import_store_2=internal_import_store_2,
        #                            internal_import_discount_2=internal_import_discount_2,
        #                            internal_import_mp_1=internal_import_mp_1,
        #                            internal_import_store_1=internal_import_store_1,
        #                            internal_import_discount_1=internal_import_discount_1,
        #                            internal_import_mp_2=internal_import_mp_2,
        #                            internal_import_role_2=internal_import_role_2,
        #                            internal_import_markup_2=internal_import_markup_2,
        #                            rows=rows, rows_mp=set(rows_mp),
        #                            photo=photo,
        #                            show=True,
        #                            user_name=user_name)
        # else:
        uid = current_user.id
        role = current_user.roles
        need_id = current_user.company_id
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        need_data = db.session.execute(select(Marketplaces.shop_name,
                                              Marketplaces.name_mp)
                                       .where(Marketplaces.company_id == need_id))

        for row in need_data:
            rows.append(row[0])
            rows_mp.append(row[1])

        return render_template('/import_settings.html',
                               uid=uid, role=role,
                               rows=rows, rows_mp=set(rows_mp),
                               photo=photo,
                               user_name=user_name)


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
        change_base_price = data.get('change_base_price')
        if mp == 'ozon':
            job = q.enqueue_call(import_oson_data_prod(user_id=uid,
                                                       shop_name=shop_name,
                                                       company_id=company_id,
                                                       update_base_price=change_base_price))
            print(777777777777, job.get_id)
        elif mp == 'wb':
            job = q.enqueue_call(wb.import_product_from_wb(uid_edit_user=uid,
                                                           shop_name=shop_name,
                                                           company_id=company_id))
            print(88888888888, job.get_id)

        return redirect('/import_settings')

    elif make == 'save_internal_import':
        internal_import_mp_1 = data.get('internal_import_mp_1')
        internal_import_store_1 = data.get('internal_import_store_1')
        internal_import_role_1 = data.get('internal_import_role_1')

        if internal_import_mp_1 != 'Выбрать' and internal_import_store_1 != 'Выбрать' \
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

    elif make == 'start_internal_import_product': 
        internal_import_mp_1 = data.get('internal_import_mp_1')
        internal_import_store_1 = data.get('internal_import_store_1')
        internal_import_role_1 = data.get('internal_import_role_1')
        internal_import_mp_2 = data.get('internal_import_mp_2')
        internal_import_store_2 = data.get('internal_import_store_2')
        internal_import_role_2 = data.get('internal_import_role_2')

        if internal_import_role_1 != internal_import_role_2 and \
                internal_import_store_1 != internal_import_store_2 and \
                internal_import_mp_1 != 'Выбрать ' and \
                internal_import_mp_2 != 'Выбрать ':
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

            job = q.enqueue_call(make_internal_import_oson_product
                                 (donor=donor,
                                  recipient=recipient,
                                  source='front',
                                  donor_mp=donor_mp,
                                  recipient_mp=recipient_mp))
            print(989898989, job.get_id)
        # print(*data.items(), sep='\n')

    elif make == 'start_internal_import_price':
        print('!!!!!!_start_internal_import_price_!!!!!')
        internal_import_mp_1 = data.get('internal_import_mp_1')
        internal_import_store_1 = data.get('internal_import_store_1')
        internal_import_role_1 = data.get('internal_import_role_1')
        internal_import_mp_2 = data.get('internal_import_mp_2')
        internal_import_store_2 = data.get('internal_import_store_2')
        internal_import_role_2 = data.get('internal_import_role_2')
        internal_import_markup_2 = data.get('internal_import_markup_2')

        if internal_import_role_1 != internal_import_role_2 and \
                internal_import_store_1 != internal_import_store_2 and \
                internal_import_mp_1 != 'Выбрать ' and \
                internal_import_mp_2 != 'Выбрать ':
            if internal_import_role_2 == 'recipient' and internal_import_role_1 == 'donor':
                job = q.enqueue_call(make_import_export_oson_price(
                    donor=internal_import_role_1,
                    recipient=internal_import_role_2,
                    k=int(internal_import_markup_2),
                    send_to_mp=False)
                )
                print(4545454545, job.get_id)
        else:
            flash("Проверьте правильность ввода данных", 'error')

    elif make == 'check_settings':
        # print('!!!!!!check_settings!!!!!11')
        if data.get('internal_import_mp_1') == 'Выбрать' \
                and data.get('internal_import_store_1') == 'Выбрать' \
                and data.get('internal_import_mp_2') == 'Выбрать' \
                and data.get('internal_import_store_2') == 'Выбрать':
            flash("Укажите хотя бы один магазин для которого нужен просмотр настроек", "alert")
        else:
            result = {k: v for k, v in data.items() if (v != '0' and v != 'Выбрать')}
            port_set, mprt_setts = {}, {}
            if result.get('internal_import_store_1') is not None \
                    and result.get("internal_import_store_2") is not None:
                import_set = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.internal_import_store_1 == data.get('internal_import_store_1'))
                .where(
                    InternalImport.internal_import_store_2 == data.get('internal_import_store_2'))) \
                    .first()
                try:
                    port_set = import_set.__dict__
                    internal_import_role_1 = port_set.get("internal_import_role_1")
                    internal_import_markup_1 = port_set.get("internal_import_markup_1")
                    internal_import_store_2 = port_set.get("internal_import_store_2")
                    internal_import_discount_2 = port_set.get("internal_import_discount_2")
                    internal_import_mp_1 = port_set.get("internal_import_mp_1")
                    internal_import_store_1 = port_set.get("internal_import_store_1")
                    internal_import_discount_1 = port_set.get("internal_import_discount_1")
                    internal_import_mp_2 = port_set.get("internal_import_mp_2")
                    internal_import_role_2 = port_set.get("internal_import_role_2")
                    internal_import_markup_2 = port_set.get("internal_import_markup_2")

                    # for row in port_set.items():
                    #     # print(row + ' = ' + 'request.args.get("' + row + '")')
                    #     # print(row + '=' + row + ',')
                    #     print(row)

                    uid = current_user.id
                    role = current_user.roles
                    need_id = current_user.company_id
                    user_name = current_user.name
                    photo = current_user.photo
                    if not photo or photo is None:
                        photo = 'prof-music-2.jpg'

                    return render_template('/import_settings.html',
                                           uid=uid, role=role,
                                           photo=photo,
                                           user_name=user_name,
                                           show=True,
                                           internal_import_role_1=internal_import_role_1,
                                           internal_import_markup_1=internal_import_markup_1,
                                           internal_import_store_2=internal_import_store_2,
                                           internal_import_discount_2=internal_import_discount_2,
                                           internal_import_mp_1=internal_import_mp_1,
                                           internal_import_store_1=internal_import_store_1,
                                           internal_import_discount_1=internal_import_discount_1,
                                           internal_import_mp_2=internal_import_mp_2,
                                           internal_import_role_2=internal_import_role_2,
                                           internal_import_markup_2=internal_import_markup_2)
                except:
                    flash("Настройки для указанных магазинов не найдены. Введите требуемые настройки и сохраните их.",
                          "alert")

            elif result.get('internal_import_store_1') is not None:
                import_set = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.internal_import_store_1 == data.get('internal_import_store_1'))
                .where(
                    InternalImport.internal_import_role_1 == data.get('internal_import_role_1'))) \
                    .first()
                try:
                    port_set = import_set.__dict__
                    internal_import_role_1 = port_set.get("internal_import_role_1")
                    internal_import_markup_1 = port_set.get("internal_import_markup_1")
                    internal_import_store_2 = port_set.get("internal_import_store_2")
                    internal_import_discount_2 = port_set.get("internal_import_discount_2")
                    internal_import_mp_1 = port_set.get("internal_import_mp_1")
                    internal_import_store_1 = port_set.get("internal_import_store_1")
                    internal_import_discount_1 = port_set.get("internal_import_discount_1")
                    internal_import_mp_2 = port_set.get("internal_import_mp_2")
                    internal_import_role_2 = port_set.get("internal_import_role_2")
                    internal_import_markup_2 = port_set.get("internal_import_markup_2")

                    uid = current_user.id
                    role = current_user.roles
                    need_id = current_user.company_id
                    user_name = current_user.name
                    photo = current_user.photo
                    if not photo or photo is None:
                        photo = 'prof-music-2.jpg'

                    return render_template('/import_settings.html',
                                           uid=uid, role=role,
                                           photo=photo,
                                           user_name=user_name,
                                           show=True,
                                           internal_import_role_1=internal_import_role_1,
                                           internal_import_markup_1=internal_import_markup_1,
                                           internal_import_store_2=internal_import_store_2,
                                           internal_import_discount_2=internal_import_discount_2,
                                           internal_import_mp_1=internal_import_mp_1,
                                           internal_import_store_1=internal_import_store_1,
                                           internal_import_discount_1=internal_import_discount_1,
                                           internal_import_mp_2=internal_import_mp_2,
                                           internal_import_role_2=internal_import_role_2,
                                           internal_import_markup_2=internal_import_markup_2)
                except:
                    flash("Настройки для указанного магазина не найдены. Введите требуемые настройки и сохраните их.",
                          "alert")

            elif result.get('internal_import_store_2') is not None:
                import_settings = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.internal_import_store_2 == data.get('internal_import_store_2'))
                .where(
                    InternalImport.internal_import_role_2 == data.get('internal_import_role_2'))) \
                    .first()
                try:
                    mprt_setts = import_settings.__dict__
                    internal_import_role_1 = mprt_setts.get("internal_import_role_1")
                    internal_import_markup_1 = mprt_setts.get("internal_import_markup_1")
                    internal_import_store_2 = mprt_setts.get("internal_import_store_2")
                    internal_import_discount_2 = mprt_setts.get("internal_import_discount_2")
                    internal_import_mp_1 = mprt_setts.get("internal_import_mp_1")
                    internal_import_store_1 = mprt_setts.get("internal_import_store_1")
                    internal_import_discount_1 = mprt_setts.get("internal_import_discount_1")
                    internal_import_mp_2 = mprt_setts.get("internal_import_mp_2")
                    internal_import_role_2 = mprt_setts.get("internal_import_role_2")
                    internal_import_markup_2 = mprt_setts.get("internal_import_markup_2")

                    uid = current_user.id
                    role = current_user.roles
                    need_id = current_user.company_id
                    user_name = current_user.name
                    photo = current_user.photo
                    if not photo or photo is None:
                        photo = 'prof-music-2.jpg'

                    return render_template('/import_settings.html',
                                           uid=uid, role=role,
                                           photo=photo,
                                           user_name=user_name,
                                           show=True,
                                           internal_import_role_1=internal_import_role_1,
                                           internal_import_markup_1=internal_import_markup_1,
                                           internal_import_store_2=internal_import_store_2,
                                           internal_import_discount_2=internal_import_discount_2,
                                           internal_import_mp_1=internal_import_mp_1,
                                           internal_import_store_1=internal_import_store_1,
                                           internal_import_discount_1=internal_import_discount_1,
                                           internal_import_mp_2=internal_import_mp_2,
                                           internal_import_role_2=internal_import_role_2,
                                           internal_import_markup_2=internal_import_markup_2)
                except:
                    flash("Настройки для указанного магазина не найдены. Введите требуемые настройки и сохраните их.",
                          "alert")

    return redirect('/import_settings')


@auth.route('/user-settings')
@login_required
def user_settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        users = Users.query.filter_by(company_id=current_user.company_id).all()
        rows = [row.name for row in users if row.name not in ('admin100500', 'Admin100500')]
        # print(rows)
        return render_template('user-settings.html', uid=uid,
                               role=role, rows=rows,
                               photo=photo,
                               user_name=user_name)


@auth.route('/user-settings', methods=['POST'])
@login_required
def user_settings_post():
    data = request.form.to_dict()
    uid = current_user.id
    if 'add_user_role' in data:
        user_role = data.get('add_user_role')
        user_name = data.get('user_name')
        user_login = data.get('user_login')
        user_email = data.get('user_email')
        user_password = data.get('Password')
        photo = data.get('photo')
        now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
        company_id = current_user.company_id  # request.form.get('cabinetID')
        user = Users.query.filter_by(email=user_email).first()

        if user:
            flash('Адрес почты уже существует')
            return render_template('mp_settings.html', uid=uid,
                                   photo=photo,
                                   user_name=user_name)
        elif not user and user_email != '' and user_name != '':

            new_user = Users(email=user_email,
                             name=user_name,
                             login=user_login,
                             company_id=company_id,
                             roles=user_role,
                             date_added=now_date,
                             date_modifed=now_date,
                             photo=photo,
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
        user_login = data.get('user_login')
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
        if user_login != '':
            smth = update(Users).where(Users.name == exist_user_name) \
                .where(Users.company_id == company_id) \
                .values({'login': user_login, 'date_modifed': now_date})
            db.session.execute(smth)
            flash("Логин пользователя успешно изменен")

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
        rows_shops = db.session \
            .execute(select(Marketplaces.shop_name) \
                     .where(Marketplaces.company_id == current_user.company_id)) \
            .all()
        # print(rows_shops, type(rows_shops))
        rows = [row[0] for row in rows_shops]
        role = current_user.roles
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
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
                               rows=rows,
                               photo=photo,
                               user_name=user_name)


@auth.route('/edit_product', methods=['POST'])
@login_required
def edit_product_post():
    data = request.form.to_dict()
    role = current_user.roles
    photo = current_user.photo
    user_name = current_user.name
    if not photo or photo is None:
        photo = 'prof-music-2.jpg'
    # print('/edit_product', *data, sep='\n')
    # print('/edit_product', *data, sep=', \n')
    if 'search_product' in data:
        articul = data.get('search_product')
        shop_name = data.get('import_shop_names')
        if articul and articul != '':
            prod = db.session \
                .execute(select(Product)
                         .filter_by(shop_name=shop_name) \
                         .where(Product.articul_product == articul)) \
                .first()
            if not prod:
                flash('Артикул не найден')
                product = {}
            else:
                product = dict(prod[0].__dict__)
                # print(111111111, *product.items(), sep='\n')
            rows_shops = db.session \
                .execute(select(Marketplaces.shop_name)
                         .where(Marketplaces.company_id == current_user.company_id)) \
                .all()
            # print(rows_shops, type(rows_shops))
            rows = [row[0] for row in rows_shops]
            # prod = Product.query.filter_by(articul_product="12345").first().__dict__
            # print(22222, *product.items(), sep='\n')  # ' sep=' = prod.get(""),\n')
            # print(33333, product)

            return render_template('/product-edit-add.html', product=product,
                                   rows=rows, photo=photo, role=role,
                                   user_name=user_name)

    else:
        prod_set = Product(
            uid_edit_user=current_user.id,
            selected_mp=data.get('insert_new_shop', '0'),
            shop_name=data.get('set_shop_name', '0'),
            articul_product=data.get('articul_product', '0'),
            name_product=data.get('name_product', '0'),
            status_mp=data.get('status_mp', '0'),
            images_product=data.get('image_product', '0'),
            price_product_base=int(data.get('price_product_base', '0')),
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

    return redirect('/edit_product')


@auth.route('/add_product')  # /<int:uid>')
@login_required
def add_product():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        uid = current_user.id
        role = current_user.roles
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'

        return render_template('product-add.html', uid=uid, role=role,
                               photo=photo,
                               user_name=user_name)


@auth.route('/add_product', methods=['POST'])  # /<int:uid>')
@login_required
def add_product_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    user_name = current_user.name
    photo = current_user.photo
    if not photo or photo is None:
        photo = 'prof-music-2.jpg'
    # print('/add_product', *data, sep='\n')
    # print('/add_product', *data, sep=', \n')
    shop_k_product = data.get('shop_k_product', 1)
    shop_name = data.get('set_shop_name', '0')
    price_product_base = int(data.get('price_product_base', '0'))
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
        return render_template('form-validation.html',
                               photo=photo,
                               user_name=user_name)

    if price_product_base is None:
        flash('Укажите, пожалуйста, базовую цену товара на маркетплейсе', 'error')
        return render_template('product-add.html',
                               photo=photo,
                               user_name=user_name)

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
        user_name = current_user.name
        photo = current_user.photo
        shop = request.args.get('select_shop_name')
        # print(11111, shop)
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        rows = ''
        limit = 30
        pre_rows_shops = db.session.query(Marketplaces.shop_name) \
            .where(Marketplaces.company_id == current_user.company_id).all()
        rows_shops = [i[0] for i in pre_rows_shops]
        if shop is None or shop == 'Все Магазины':
            my_query = db.func.count(Product.id)
            all_product = db.session.execute(my_query).scalar()
            max_page = all_product // limit
            raw_list_products = db.session.query(Product) \
                .paginate(page=page, per_page=30, error_out=False)

        else:
            my_query = db.func.count(Product.id)
            all_product = db.session.execute(my_query).scalar()
            max_page = all_product // limit
            raw_list_products = db.session.query(Product).filter_by(shop_name=shop) \
                .paginate(page=page, per_page=30, error_out=False)

        for row in raw_list_products.items:
            rows += '<tr>' \
                    f'<td>{row.name_product}</td>' \
                    f'<td >{row.articul_product}</td>' \
                    f'<td >{row.shop_name}</td>' \
                    f'<td >{row.quantity}</td>' \
                    f'<td >{row.final_price}</td>' \
                    f'<td >{row.status_in_shop}</td>' \
                    f'<td >{row.date_modifed}</td>' \
                    f'</tr>'

        return unescape(render_template('tables-products.html',
                                        rows=rows, role=role,
                                        raw_list_products=raw_list_products,
                                        max_page=max_page,
                                        photo=photo,
                                        user_name=user_name,
                                        shops=rows_shops))


@auth.route('/shops', methods=['GET', 'POST'])
@login_required
def shops():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        if request.method == "POST":
            data = request.form.to_dict()
            proxy_settings = {}
            if len(data.keys()) > 0:
                for key, value in data.items():
                    need_job = key.rsplit('_', maxsplit=1)[0]
                    proxy_settings[value] = proxy_settings.get(value, []) + [need_job]

            markets = Marketplaces.query \
                .filter_by(company_id=current_user.company_id).all()
            for row in markets:
                current_work = {'check_send_null': False,
                                'send_common_stocks': False,
                                'enable_orders_submit': False,
                                'enable_sync_price': False,
                                'enable_sync_stocks': False}
                if row.shop_name in proxy_settings.keys():
                    current = {i: True for i in proxy_settings[row.shop_name]}
                    current_work.update(current)
                    db.session.execute(update(Marketplaces)
                                       .where(Marketplaces.seller_id == row.seller_id)
                                       .values(current_work))
                else:
                    db.session.execute(update(Marketplaces)
                                       .where(Marketplaces.seller_id == row.seller_id)
                                       .values(current_work))
                db.session.commit()

            if len(data.keys()) > 0:
                try:
                    scheduler.remove_job('shops_back')
                except:
                    print('Job_update_error')
                finally:
                    current_job = scheduler.add_job(back_shops_tasks, id='shops_back',
                                                    trigger='interval', minutes=60)
                    if scheduler.state == 0:
                        scheduler.start()

                    print(100000000, current_job)
                    # print(111000, len(data.keys()))
            else:
                try:
                    scheduler.remove_job('shops_back')
                except:
                    print('Job_remove_error')

            return redirect(url_for('auth.shops'))

        else:
            # print(22222, request.args.to_dict())
            uid = current_user.id
            role = current_user.roles
            user_name = current_user.name
            photo = current_user.photo
            if not photo or photo is None:
                photo = 'prof-music-2.jpg'
            rows = ''

            raw_list_shops = db.session.query(Marketplaces) \
                .filter_by(company_id=current_user.company_id) \
                .order_by(Marketplaces.seller_id.asc()) \
                .all()
            # raw_list_products = db.session.query(Product)
            # .paginate(page=30, per_page=30, error_out=False).items
            for row in raw_list_shops:
                seller_id = row.seller_id
                if row.date_modifed:
                    date_modifed = row.date_modifed
                else:
                    date_modifed = "Нет"
                if row.check_send_null:
                    check_send_null = "checked"
                else:
                    check_send_null = "unchecked"

                if row.send_common_stocks:
                    send_common_stocks = "checked"
                else:
                    send_common_stocks = "unchecked"

                if row.enable_sync_stocks:
                    enable_sync_stocks = "checked"
                else:
                    enable_sync_stocks = "unchecked"

                if row.enable_sync_price:
                    enable_sync_price = "checked"
                else:
                    enable_sync_price = "unchecked"

                if row.enable_orders_submit:
                    enable_orders_submit = "checked"
                else:
                    enable_orders_submit = "unchecked"

                rows += '<tr>' \
                        f'<td >{row.shop_name} </td>' \
                        f'<td >{row.name_mp}</td>' \
                        f'<td >{row.seller_id}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.shop_name}" name="enable_sync_stocks_{seller_id}' \
                        f'" {enable_sync_stocks} class="iswitch iswitch iswitch-primary"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.shop_name}" name="enable_sync_price_{seller_id}' \
                        f'" {enable_sync_price} class="iswitch iswitch iswitch-primary"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.shop_name}" name="send_common_stocks_{seller_id}' \
                        f'" {send_common_stocks} class="iswitch iswitch iswitch-purple"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.shop_name}" name="check_send_null_{seller_id}' \
                        f'" {check_send_null} class="iswitch iswitch iswitch-warning"></div></td>' \
                        f'<td >{str(date_modifed).rsplit(":")[0]}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.shop_name}" name="enable_orders_submit_{seller_id}' \
                        f'" {enable_orders_submit} class="iswitch iswitch iswitch-purple"></div></td>' \
                        f'</tr>'

            return unescape(render_template('tables-shops.html',
                                            rows=rows, role=role,
                                            photo=photo,
                                            user_name=user_name))


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
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
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
                    f'<td >{row.quantity}</td>' \
                    f'<td >{row.price}</td>' \
                    f'<td >{row.shop_name}</td>' \
                    f'<td >{str(row.date_added).rsplit(":")[0]}</td>' \
                    f'<td >{row.shop_status}</td>' \
                    f'<td >{row.shipment_date}</td>' \
                    f'</tr>'

        return unescape(render_template('table-sales-page.html',
                                        rows=rows, role=role,
                                        max_page=max_page,
                                        total_sales=total_sales,
                                        sales=sales,
                                        photo=photo,
                                        user_name=user_name))


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
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
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
                                        sales_today=sales_today,
                                        photo=photo,
                                        user_name=user_name))


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
        user_name = current_user.name
        user_photo = current_user.photo
        shop = request.args.get('select_shop_name')
        if not user_photo or user_photo is None:
            user_photo = 'prof-music-2.jpg'
        rows = ''
        limit = 30
        HOUR = '09:00:00'
        yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)) \
            .strftime(f"%Y-%m-%d {HOUR}")
        pre_rows_shops = db.session.query(Marketplaces.shop_name) \
            .where(Marketplaces.company_id == current_user.company_id).all()
        rows_shops = [i[0] for i in pre_rows_shops]
        # rows_shops.insert(0, 'Все Магазины')

        if shop is None or shop == 'Все Магазины':
            my_query = db.func.count(SalesToday.id)
            total_assembly_sales = db.session.execute(my_query).scalar()
            max_page = total_assembly_sales // limit

            # TODO
            assembly_orders = db.session.query(SalesToday.article_mp,
                                               SalesToday.shop_name,
                                               SalesToday.article,
                                               SalesToday.order_status,
                                               func.sum(SalesToday.quantity)
                                               .label('total_sales')) \
                .group_by(SalesToday.article_mp,
                          SalesToday.shop_name,
                          SalesToday.article,
                          SalesToday.order_status) \
                .where(SalesToday.date_added > yesterday) \
                .where(SalesToday.our_status == "NEW") \
                .order_by(SalesToday.article_mp) \
                .paginate(page=page, per_page=limit, error_out=False)

            # print(333333, assembly)
            # print(assembly)
            print(222222, shop)
        else:
            my_query = db.func.count(SalesToday.id)
            total_assembly_sales = db.session.execute(my_query).scalar()
            max_page = total_assembly_sales // limit
            # TODO
            assembly_orders = db.session.query(SalesToday.article_mp,
                                               SalesToday.shop_name,
                                               SalesToday.article,
                                               SalesToday.order_status,
                                               func.sum(SalesToday.quantity)
                                               .label('total_sales')) \
                .group_by(SalesToday.article_mp,
                          SalesToday.shop_name,
                          SalesToday.article,
                          SalesToday.order_status) \
                .where(SalesToday.date_added > yesterday) \
                .where(SalesToday.our_status == "NEW") \
                .filter(SalesToday.shop_name == shop) \
                .order_by(SalesToday.article_mp) \
                .paginate(page=page, per_page=limit, error_out=False)

        for row in assembly_orders.items:
            s_today = (select(Product.photo)
                       .where(Product.articul_product == row.article)
                       .where(Product.shop_name == row.shop_name))

            photo = db.session.execute(s_today).first()
            if photo is None:
                photo = ('нет фото',)

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
                                        assembly_sales=assembly_orders,
                                        photo=user_photo,
                                        user_name=user_name,
                                        shops=rows_shops,
                                        select_shop_name=shop))


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
        user_name = current_user.name
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
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
                                        total_users=total_users,
                                        photo=photo,
                                        user_name=user_name))


@auth.route('/profile')
@auth.route('/profile', methods=['POST'])
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        user_id = current_user.id
        role = current_user.roles
        company_id = current_user.company_id
        user_data = db.session.execute(select(Users)
                                       .where(Users.id == user_id) \
                                       .where(Users.company_id == company_id)) \
            .first()
        photo = user_data[0].photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        user_name = user_data[0].name

    if request.method == 'POST':
        proxy = dict()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(PHOTO_UPLOAD_FOLDER, filename))
            proxy['photo'] = filename

        data = request.form.to_dict()
        now_date = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M %d/%m/%Y')
        proxy['date_modifed'] = now_date
        if data.get('current_user_name') != current_user.name:
            proxy_name = data.get('current_user_name')
            proxy['name'] = proxy_name

        if data.get('change_user_password') != data.get('check_user_password') \
                and data.get('check_user_password') != '':
            flash('Введенные пароли не совпадают', 'error')

        elif data.get('change_user_password') == data.get('check_user_password') \
                and data.get('check_user_password') != '':

            proxy['password'] = generate_password_hash \
                (data.get('change_user_password'), method='scrypt')

        smth = update(Users) \
            .where(Users.id == current_user.id) \
            .values(proxy)

        db.session.execute(smth)
        db.session.commit()

        return redirect('/profile')

    return render_template('hos-profile-edit.html',
                           uid=user_id, user_role=role,
                           photo=photo,
                           user_name=user_name)


@auth.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(PHOTO_UPLOAD_FOLDER, filename))

            return redirect(url_for('auth.upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@auth.app_errorhandler(404)
def page_not_found(error):
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        photo = current_user.photo
        if not photo or photo is None:
            photo = 'prof-music-2.jpg'
        user_name = current_user.name
        role = current_user.roles
        return render_template("blank-2.html", title='404',
                               role=role,
                               user_name=user_name,
                               photo=photo), 404


@auth.app_errorhandler(500)
def page_server_error(error):
    photo = current_user.photo
    if not photo or photo is None:
        photo = 'prof-music-2.jpg'
    user_name = current_user.name
    role = current_user.roles
    return render_template("blank-500.html", title='500',
                           role=role,
                           photo=photo,
                           user_name=user_name,
                           error=error), 500
