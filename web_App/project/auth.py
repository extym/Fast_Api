import datetime
import logging
import os
import time
from html import unescape
from .creds import LOCAL_MODE, WHEELS
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

import project.sber as sber
import project.ozon as oson
import project.yandex as yan
import project.addons.kolrad as kolrad
import project.addons.shins as shins
import project.addons.four_tochki as tochki

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

                logging.info('Send_stocks_oson_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                             .format(len(key), seller_id, True))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v2(sourse='web',
                                     seller_id=seller_id,
                                     is_stocks_null=True)
                print('Send_stocks_wb_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                      .format(len(key), seller_id, True))

                logging.info('Send_stocks_wb_v2 - len_key {}, seller_id {}, is_stocks_null {}'
                             .format(len(key), seller_id, True))

        if row.send_common_stocks:
            ii_raw = session.query(InternalImport) \
                .where(InternalImport.i_import_acceptor_store == row.shop_name) \
                .first()
            store_1 = ii_raw.i_import_donor_store
            # seller_id = row.seller_id
            if row.name_mp == 'ozon':
                oson.send_stocks_oson_v3(key_acceptor=key,
                                         donor_name=store_1,
                                         acceptor=seller_id)
                print('Send_stocks_oson_v3 - donor_name {}, acceptor_id {}, key_acceptor {}'
                      .format(store_1, seller_id, key))
                logging.info('Send_stocks_oson_v3 - donor {}, acceptor {}'
                             .format(store_1, seller_id))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v3(donor=store_1,
                                     acceptor=seller_id)
                print('send_stocks_wb_v3 - donor {}, acceptor {}'
                      .format(store_1, seller_id))
                logging.info('send_stocks_wb_v3 - donor {}, acceptor {}'
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
                print('Processing_orders_wb_v2 - len_key {}, shop_name {}' \
                      .format(len(key), shop_name))

                logging.info('Processing_orders_wb_v2 - len_key {}, shop_name {}'
                             .format(len(key), shop_name))

        if row.enable_sync_stocks:
            if row.name_mp == 'ozon':
                ozon.send_stocks_oson_v2(key=key,
                                         seller_id=seller_id,
                                         is_stocks_null=False)
                print('Send_stocks_oson_v2 - seller_id {} is_stocks_null {}'
                      .format(seller_id, False))

                logging.info('Send_stocks_oson_v2 - seller_id {} is_stocks_null {}'
                             .format(seller_id, False))
            if row.name_mp == 'wb':
                wb.send_stocks_wb_v2(seller_id=seller_id,
                                     is_stocks_null=False,
                                     sourse='web')
                print('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                      .format(seller_id, False))

                logging.info('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                             .format(seller_id, False))

        if row.enable_sync_price:
            if row.name_mp == 'ozon':
                ozon.send_product_price(key_acceptor=key,
                                        acceptor=seller_id)
                print('Send_product_price oson - len key {},  seller_id {}'
                      .format(len(key), row.seller_id))
                logging.info('Send_product_price oson - key {}, acceptor_id {}'
                             .format(key, seller_id))

            if row.name_mp == 'wb':
                wb.send_price_to_wb(seller_id=seller_id, sourse='web')
                print('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                      .format(len(key), seller_id))
                logging.info('Send_stocks_wb_v2 - seller_id {} is_stocks_null {}'
                             .format(key, seller_id))

    # print(777, markets)


def back_distibutors_tasks():
    with Session(engine) as session:
        distibutors_job = session.query(Distributor) \
            .filter(or_(Distributor.is_scheduler == True,
                        Distributor.enable_orders_submit == True)) \
            .all()
        for row in distibutors_job:
            enabled = row.is_scheduler
            if enabled:
                if row.distributor == '3logic':
                    pass


def back_dist_prices_tasks():
    with Session(engine) as session:
        distr_prices = session.query(DistributorPrice) \
            .filter(or_(DistributorPrice.is_scheduler == True)) \
            .all()
        for row in distr_prices:
            if row.distributor == 'shins' and row.type_downloads == 'csv':
                shins.get_data_csv(url=row.price_link)


def back_upload_prices():
    with Session(engine) as session:
        upload_prices = session.query(UploadPrice) \
            .filter(or_(UploadPrice.is_scheduler == True,
                        UploadPrice.is_null_stocks == True)) \
            .all()

        for row in upload_prices:
            if row.upload_price_mp == 'sber' and row.type_downloads == 'xml':
                sber.create_sber_xml(stocks_is_null=row.is_null_stocks,
                                     without_db=row.enable_sync_bd,
                                     legal_name=row.upload_price_legal_name,
                                     short_shop_name=row.upload_prices_short_shop,
                                     markup=row.upload_prices_markup,
                                     discount=row.upload_price_discount,
                                     wh_id=row.warehouses_id)
            if row.upload_price_mp == 'yandex' and row.type_downloads == 'xml':
                yan.create_ym_xml(stocks_is_null=row.is_null_stocks,
                                  without_db=row.enable_sync_bd,
                                  legal_name=row.upload_price_legal_name,
                                  short_shop_name=row.upload_prices_short_shop,
                                  markup=row.upload_prices_markup,
                                  discount=row.upload_price_discount)


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

    return redirect('/add_mp')


@auth.route('/edit_mp', methods=['POST'])  # /<int:uid>')
@login_required
def edit_mp_post():
    data = request.form.to_dict()
    uid = current_user.id
    role = current_user.roles
    company_id = current_user.company_id
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
    user_name = current_user.name
    company_id = current_user.company_id
    photo = current_user.photo
    if not photo or photo is None:
        photo = 'prof-music-2.jpg'
    print(*data.items(), sep='\n')

    if 'save_edited_shop' in data:
        settings = dict()
        if data['shop_name'] != 'Выбрать':
            for key, value in data.items():
                if value != '':
                    settings.update({key: value})
                else:
                    value = 0
                    settings.update({key: value})

            del settings['save_edited_shop']
            market = Marketplaces.query \
                .filter_by(shop_name=settings['shop_name']) \
                .update(settings)
            db.session.commit()
            flash('Настройки удачно сохранены', 'success')

        else:
            flash('Выберите редактируемый магазин', 'alert')

    if 'check_mp_shop' in data:
        print('!!!!!!!!!!!!!!!!!!!!!-check_mp_shop')
        if data['shop_name'] != 'Выбрать':
            shop_name = data.get('shop_name')
            shop_data = Marketplaces.query \
                .filter_by(shop_name=shop_name) \
                .first()

            if data.get('name_mp') == 'wb':
                name_mp = shop_data.name_mp
                mp_markup = shop_data.mp_markup
                mp_discount = shop_data.mp_discount
                shop_name = shop_data.shop_name
                store_markup = shop_data.store_markup
                store_discount = shop_data.store_discount
                # warehouses = shop_data.warehouses

                return render_template('mp_settings.html', uid=uid,
                                       role=role,
                                       photo=photo,
                                       name_mp=name_mp,
                                       mp_markup=mp_markup,
                                       mp_discount=mp_discount,
                                       shop_name=shop_name,
                                       store_markup=store_markup,
                                       store_discount=store_discount,
                                       warehouses=warehouses,
                                       show_wb_sett=True,
                                       show_sett=True,
                                       user_name=user_name)

            else:
                name_mp = shop_data.name_mp
                mp_markup = shop_data.mp_markup
                mp_discount = shop_data.mp_discount
                shop_name = shop_data.shop_name
                store_markup = shop_data.store_markup
                store_discount = shop_data.store_discount

                return render_template('mp_settings.html', uid=uid,
                                       role=role,
                                       photo=photo,
                                       name_mp=name_mp,
                                       mp_markup=mp_markup,
                                       mp_discount=mp_discount,
                                       shop_name=shop_name,
                                       store_markup=store_markup,
                                       store_discount=store_discount,
                                       show_sett=True,
                                       user_name=user_name)

        else:
            flash('Выберите редактируемый магазин', 'alert')

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
        # if show:
        #     uid = current_user.id
        #     role = current_user.roles
        #     need_id = current_user.company_id
        #     user_name = current_user.name
        #     photo = current_user.photo
        #     if not photo or photo is None:
        #         photo = 'prof-music-2.jpg'
        #     i_import_donor_role = request.args.get("i_import_donor_role")
        #     i_import_donor_markup = request.args.get("i_import_donor_markup")
        #     i_import_acceptor_store = request.args.get("i_import_acceptor_store")
        #     i_import_acceptor_discount = request.args.get("i_import_acceptor_discount")
        #     i_import_donor_mp = request.args.get("i_import_donor_mp")
        #     i_import_donor_store = request.args.get("i_import_donor_store")
        #     i_import_donor_discount = request.args.get("i_import_donor_discount")
        #     i_import_acceptor_mp = request.args.get("i_import_acceptor_mp")
        #     i_import_acceptor_role = request.args.get("i_import_acceptor_role")
        #     i_import_acceptor_markup = request.args.get("i_import_acceptor_markup")
        #
        #     return render_template('/import_settings.html',
        #                            uid=uid, role=role,
        #                            i_import_donor_role=i_import_donor_role,
        #                            i_import_donor_markup=i_import_donor_markup,
        #                            i_import_acceptor_store=i_import_acceptor_store,
        #                            i_import_acceptor_discount=i_import_acceptor_discount,
        #                            i_import_donor_mp=i_import_donor_mp,
        #                            i_import_donor_store=i_import_donor_store,
        #                            i_import_donor_discount=i_import_donor_discount,
        #                            i_import_acceptor_mp=i_import_acceptor_mp,
        #                            i_import_acceptor_role=i_import_acceptor_role,
        #                            i_import_acceptor_markup=i_import_acceptor_markup,
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
    print(57575, data)
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
        i_import_donor_mp = data.get('i_import_donor_mp')
        i_import_donor_store = data.get('i_import_donor_store')

        if i_import_donor_mp != 'Выбрать' and i_import_donor_store != 'Выбрать':
            in_import = InternalImport(
                i_import_donor_mp=i_import_donor_mp,
                i_import_donor_store=i_import_donor_store,
                i_import_donor_markup=data.get('i_import_donor_markup'),
                i_import_donor_discount=data.get('i_import_donor_discount'),
                i_import_acceptor_mp=data.get('i_import_acceptor_mp'),
                i_import_acceptor_store=data.get('i_import_acceptor_store'),
                i_import_acceptor_discount=data.get('i_import_acceptor_discount'),
                i_import_acceptor_markup=data.get('i_import_acceptor_markup'),
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
        i_import_donor_mp = data.get('i_import_donor_mp')
        i_import_donor_store = data.get('i_import_donor_store')
        i_import_acceptor_mp = data.get('i_import_acceptor_mp')
        i_import_acceptor_store = data.get('i_import_acceptor_store')

        if i_import_donor_store != i_import_acceptor_store and \
                i_import_donor_mp != 'Выбрать ' and \
                i_import_acceptor_mp != 'Выбрать ':
            job = q.enqueue_call(make_internal_import_oson_product
                                 (donor=i_import_donor_store,
                                  acceptor=i_import_acceptor_store,
                                  source='front',
                                  donor_mp=i_import_donor_mp,
                                  acceptor_mp=i_import_acceptor_mp))
            print(989898989, job.get_id)
        # print(*data.items(), sep='\n')

    elif make == 'start_internal_import_price':
        print('!!!!!!_start_internal_import_price_!!!!!')
        i_import_donor_mp = data.get('i_import_donor_mp')
        i_import_donor_store = data.get('i_import_donor_store')
        i_import_donor_role = 'donor'
        i_import_acceptor_mp = data.get('i_import_acceptor_mp')
        i_import_acceptor_store = data.get('i_import_acceptor_store')
        i_import_acceptor_role = 'acceptor'
        i_import_acceptor_markup = data.get('i_import_acceptor_markup')

        if i_import_donor_store != i_import_acceptor_store and \
                i_import_donor_mp != 'Выбрать ' and \
                i_import_acceptor_mp != 'Выбрать ':

            job = q.enqueue_call(make_import_export_oson_price(
                donor=i_import_donor_role,
                acceptor=i_import_acceptor_role,
                k=int(i_import_acceptor_markup),
                send_to_mp=False)
            )
            print(4545454545, job.get_id)
        else:
            flash("Проверьте правильность ввода данных", 'error')

    elif make == 'check_settings':
        # print('!!!!!!check_settings!!!!!11')
        if data.get('i_import_donor_mp') == 'Выбрать' \
                and data.get('i_import_donor_store') == 'Выбрать' \
                and data.get('i_import_acceptor_mp') == 'Выбрать' \
                and data.get('i_import_acceptor_store') == 'Выбрать':
            flash("Укажите хотя бы один магазин для которого нужен просмотр настроек", "alert")
        else:
            result = {k: v for k, v in data.items() if (v != '0' and v != 'Выбрать')}
            port_set, mprt_setts = {}, {}
            if result.get('i_import_donor_store') is not None \
                    and result.get("i_import_acceptor_store") is not None:
                import_set = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.i_import_donor_store == data.get('i_import_donor_store'))
                .where(
                    InternalImport.i_import_acceptor_store == data.get('i_import_acceptor_store'))) \
                    .first()
                try:
                    port_set = import_set.__dict__
                    i_import_donor_role = port_set.get("i_import_donor_role")
                    i_import_donor_markup = port_set.get("i_import_donor_markup")
                    i_import_acceptor_store = port_set.get("i_import_acceptor_store")
                    i_import_acceptor_discount = port_set.get("i_import_acceptor_discount")
                    i_import_donor_role = 'donor'
                    i_import_donor_store = port_set.get("i_import_donor_store")
                    i_import_donor_discount = port_set.get("i_import_donor_discount")
                    i_import_acceptor_mp = port_set.get("i_import_acceptor_mp")
                    i_import_acceptor_role = 'acceptor'
                    i_import_acceptor_markup = port_set.get("i_import_acceptor_markup")

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
                                           i_import_donor_role=i_import_donor_role,
                                           i_import_donor_markup=i_import_donor_markup,
                                           i_import_acceptor_store=i_import_acceptor_store,
                                           i_import_acceptor_discount=i_import_acceptor_discount,
                                           i_import_donor_mp='donor',
                                           i_import_donor_store=i_import_donor_store,
                                           i_import_donor_discount=i_import_donor_discount,
                                           i_import_acceptor_mp=i_import_acceptor_mp,
                                           i_import_acceptor_role='acceptor',
                                           i_import_acceptor_markup=i_import_acceptor_markup)
                except:
                    flash("Настройки для указанных магазинов не найдены. Введите требуемые настройки и сохраните их.",
                          "alert")

            elif result.get('i_import_donor_store') is not None:
                import_set = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.i_import_donor_store == data.get('i_import_donor_store'))) \
                    .first()
                try:
                    port_set = import_set.__dict__
                    i_import_donor_role = 'donor'
                    i_import_donor_markup = port_set.get("i_import_donor_markup")
                    i_import_acceptor_store = port_set.get("i_import_acceptor_store")
                    i_import_acceptor_discount = port_set.get("i_import_acceptor_discount")
                    i_import_donor_mp = port_set.get("i_import_donor_mp")
                    i_import_donor_store = port_set.get("i_import_donor_store")
                    i_import_donor_discount = port_set.get("i_import_donor_discount")
                    i_import_acceptor_mp = port_set.get("i_import_acceptor_mp")
                    i_import_acceptor_role = 'acceptor'
                    i_import_acceptor_markup = port_set.get("i_import_acceptor_markup")

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
                                           i_import_donor_role='donor',
                                           i_import_donor_markup=i_import_donor_markup,
                                           i_import_acceptor_store=i_import_acceptor_store,
                                           i_import_acceptor_discount=i_import_acceptor_discount,
                                           i_import_donor_mp=i_import_donor_mp,
                                           i_import_donor_store=i_import_donor_store,
                                           i_import_donor_discount=i_import_donor_discount,
                                           i_import_acceptor_mp=i_import_acceptor_mp,
                                           i_import_acceptor_role='acceptor',
                                           i_import_acceptor_markup=i_import_acceptor_markup)
                except:
                    flash("Настройки для указанного магазина не найдены. Введите требуемые настройки и сохраните их.",
                          "alert")

            elif result.get('i_import_acceptor_store') is not None:
                import_settings = db.session.scalars(select(InternalImport)
                .where(
                    InternalImport.i_import_acceptor_store == data.get('i_import_acceptor_store'))) \
                    .first()
                try:
                    mprt_setts = import_settings.__dict__
                    i_import_donor_role = 'donor'
                    i_import_donor_markup = mprt_setts.get("i_import_donor_markup")
                    i_import_acceptor_store = mprt_setts.get("i_import_acceptor_store")
                    i_import_acceptor_discount = mprt_setts.get("i_import_acceptor_discount")
                    i_import_donor_mp = mprt_setts.get("i_import_donor_mp")
                    i_import_donor_store = mprt_setts.get("i_import_donor_store")
                    i_import_donor_discount = mprt_setts.get("i_import_donor_discount")
                    i_import_acceptor_mp = mprt_setts.get("i_import_acceptor_mp")
                    i_import_acceptor_role = 'acceptor'
                    i_import_acceptor_markup = mprt_setts.get("i_import_acceptor_markup")

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
                                           i_import_donor_role=i_import_donor_role,
                                           i_import_donor_markup=i_import_donor_markup,
                                           i_import_acceptor_store=i_import_acceptor_store,
                                           i_import_acceptor_discount=i_import_acceptor_discount,
                                           i_import_donor_mp=i_import_donor_mp,
                                           i_import_donor_store=i_import_donor_store,
                                           i_import_donor_discount=i_import_donor_discount,
                                           i_import_acceptor_mp=i_import_acceptor_mp,
                                           i_import_acceptor_role=i_import_acceptor_role,
                                           i_import_acceptor_markup=i_import_acceptor_markup)
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
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!', data)
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
            # print(232323, proxy_settings)
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
            else:
                try:
                    scheduler.remove_job('shops_back')
                except:
                    print('Job_shops_back_remove_error')

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
@login_required
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


@auth.route('/upload_prices_table', methods=['GET', 'POST'])
@login_required
def upload_prices_table():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        if request.method == "POST":
            data = request.form.to_dict()
            print(34343434, data)

            proxy_settings = {}
            if len(data.keys()) > 0:
                for key, value in data.items():
                    need_job = key.rsplit('_', maxsplit=1)[0]
                    proxy_settings[value] = proxy_settings.get(value, []) + [need_job]
            print(232323, proxy_settings)
            uploads = UploadPrice.query.all()
            for row in uploads:
                current_work = {'is_null_stocks': False,
                                'is_scheduler': False}
                curr_id = str(row.id)
                if curr_id in proxy_settings.keys():
                    current = {i: True for i in proxy_settings[curr_id]}
                    print(345345, current)
                    current_work.update(current)
                    db.session.execute(update(UploadPrice)
                                       .where(UploadPrice.id == row.id)
                                       .values(current_work))
                else:
                    db.session.execute(update(UploadPrice)
                                       .where(UploadPrice.id == row.id)
                                       .values(current_work))
                db.session.commit()

            if len(data.keys()) > 0:
                try:
                    scheduler.remove_job('upload_prices')
                except:
                    print('Job_upload_prices_update_error')
                finally:
                    current_job = scheduler.add_job(back_upload_prices,
                                                    id='upload_prices',
                                                    trigger='interval',
                                                    minutes=60)
                    if scheduler.state == 0:
                        scheduler.start()

                    print(100000000, current_job)
            else:
                try:
                    scheduler.remove_job('upload_prices')
                except:
                    print('Job_upload_prices_remove_error')

            return redirect(url_for('auth.upload_prices_table'))

        else:
            # print(22222, request.args.to_dict())
            uid = current_user.id
            role = current_user.roles
            user_name = current_user.name
            photo = current_user.photo
            if not photo or photo is None:
                photo = 'prof-music-2.jpg'
            rows = ''

            raw_list_uploads = db.session.query(UploadPrice) \
                .order_by(UploadPrice.id.asc()) \
                .all()

            print(raw_list_uploads)

            for row in raw_list_uploads:
                id = row.id
                if row.is_null_stocks:
                    is_null_stocks = "checked"
                else:
                    is_null_stocks = "unchecked"

                if row.is_scheduler:
                    is_scheduler = "checked"
                else:
                    is_scheduler = "unchecked"

                rows += '<tr>' \
                        f'<td >{row.id} </td>' \
                        f'<td >{row.name}</td>' \
                        f'<td >{row.upload_prices_markup}</td>' \
                        f'<td >{row.upload_price_discount}</td>' \
                        f'<td >{row.upload_prices_url}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.id}" name="is_scheduler_{id}' \
                        f'" {is_scheduler} class="iswitch iswitch iswitch-purple"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.id}" name="is_null_stocks_{id}' \
                        f'" {is_null_stocks} class="iswitch iswitch iswitch-warning"></div></td>' \
                        f'<td >{row.upload_option}</td>' \
                        f'</tr>'

            return unescape(render_template('upload_price_table.html',
                                            rows=rows, role=role,
                                            photo=photo,
                                            user_name=user_name,
                                            distributors=WHEELS))


@auth.route('/upload-prices-settings', methods=['GET', 'POST'])
@login_required
def upload_prices_settings():
    if request.method == "POST":
        uid = str(current_user.id)
        role = current_user.roles
        company_id = current_user.company_id
        data = request.form.to_dict()
        make = data.get('make')
        print(11122, *data.items(), sep='\n')
        # for key in data.keys():
        #     print(key, f"= data.get('{key}'),")
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # for key in data.keys():
        #     print(key, f"={key}")

        if make == 'save_upload_price':
            upload_prices_mp = data.get('upload_prices_mp')
            upload_prices_id = data.get('upload_prices_id')
            upload_option = data.get('option')

            if upload_prices_mp != 'Выбрать' \
                    and upload_option \
                    and upload_prices_id == '0':
                upload_price = UploadPrice(
                    is_null_stocks=data.get('is_null_stocks', 'off'),
                    is_scheduler=data.get('enabled_upload_price', 'off'),
                    name=data.get('upload_price_name', 'default'),
                    upload_option=data.get('option'),
                    upload_prices_mp=data.get('upload_prices_mp'),
                    upload_prices_markup=data.get('upload_prices_markup'),
                    upload_prices_store=data.get('upload_prices_store'),
                    upload_price_discount=data.get('upload_price_discount'),
                    upload_prices_short_shop=data.get('upload_prices_short_shop'),
                    upload_prices_legal_name=data.get('upload_prices_legal_name'),
                    upload_prices_url=data.get('upload_prices_url'),
                    upload_price_category=data.get('upload_price_category'),
                    date_modifed=datetime.datetime.now(),
                    user_id=current_user.id
                )

                db.session.add(upload_price)
                db.session.commit()
                flash("Настройки удачно сохранены", 'success')
            elif upload_prices_mp != 'Выбрать' \
                    and upload_option \
                    and upload_prices_id != '0':
                upload_price = UploadPrice(
                    id=upload_prices_id,
                    is_null_stocks=data.get('is_null_stocks', 'off'),
                    is_scheduler=data.get('enabled_upload_price', 'off'),
                    name=data.get('upload_price_name', 'default'),
                    upload_option=data.get('option'),
                    upload_prices_mp=data.get('upload_prices_mp'),
                    upload_prices_markup=data.get('upload_prices_markup'),
                    upload_prices_store=data.get('upload_prices_store'),
                    upload_price_discount=data.get('upload_price_discount'),
                    upload_prices_short_shop=data.get('upload_prices_short_shop'),
                    upload_prices_legal_name=data.get('upload_prices_legal_name'),
                    upload_prices_url=data.get('upload_prices_url'),
                    upload_price_category=data.get('upload_price_category'),
                    date_modifed=datetime.datetime.now(),
                    user_modifed=current_user.id
                )

                db.session.merge(upload_price)
                db.session.commit()
            else:
                flash("Проверьте, пожалуйста, корректность вводимых данных", 'error')
                return redirect('/upload-prices-settings')

        elif make == 'make_product_feed':
            upload_price_name = data.get('upload_price_name')
            is_scheduler = data.get('enabled_upload_price', 'off')
            upload_prices_mp = data.get('upload_prices_mp')
            is_null_stocks = data.get('is_null_stocks', False)
            upload_option = data.get('option')
            upload_prices_markup = data.get('upload_prices_markup')
            upload_prices_store = data.get('upload_prices_store')
            upload_price_discount = data.get('upload_price_discount')
            upload_prices_short_shop = data.get('upload_prices_short_shop')
            upload_prices_legal_name = data.get('upload_prices_legal_name')
            upload_prices_url = data.get('upload_prices_url')
            upload_price_category = data.get('upload_price_category')

            if upload_prices_short_shop == '':
                flash("Укажите на вкладке Профиль - Краткое название магазина")
            if upload_prices_legal_name == '':
                flash("Укажите на вкладке Профиль - Краткое название организации")

            if upload_prices_store != 'Выбрать' and \
                    upload_prices_short_shop != '' and \
                    upload_prices_legal_name != '' and \
                    upload_prices_mp != 'Выбрать ':
                if upload_prices_mp == 'sber' and upload_option == 'xml':
                    job = q.enqueue_call(sber.create_sber_xml
                                         (stocks_is_null=is_null_stocks,
                                          site_url=upload_prices_url,
                                          legal_name=upload_prices_legal_name,
                                          short_shop_name=upload_prices_short_shop,
                                          category=upload_price_category,
                                          markup=upload_prices_markup,
                                          discount=upload_price_discount,
                                          shop_name=upload_prices_store))
                    print(97777789, job.get_id)
                elif upload_prices_mp == 'yandex' and upload_option == 'xml':
                    job = q.enqueue_call(yan.create_ym_xml
                                         (stocks_is_null=is_null_stocks,
                                          site_url=upload_prices_url,
                                          legal_name=upload_prices_legal_name,
                                          short_shop_name=upload_prices_short_shop,
                                          category=upload_price_category,
                                          markup=upload_prices_markup,
                                          discount=upload_price_discount))
                    print(97777789, job.get_id)

            print(989898989, *data.items(), sep='\n')

        elif make == 'make_price_feed':
            print('!!!!!!_start_internal_import_price_!!!!!')
            upload_price_name = data.get('upload_price_name')
            is_scheduler = data.get('enabled_upload_price', 'off')
            upload_prices_mp = data.get('upload_prices_mp')
            is_null_stocks = data.get('is_null_stocks', False)
            upload_option = data.get('option')
            upload_prices_markup = data.get('upload_prices_markup')
            upload_prices_store = data.get('upload_prices_store')
            upload_price_discount = data.get('upload_price_discount')
            upload_prices_short_shop = data.get('upload_prices_short_shop')
            upload_prices_legal_name = data.get('upload_prices_legal_name')
            upload_prices_url = data.get('upload_prices_url')
            upload_price_category = data.get('upload_price_category')

            if upload_prices_store != 'Выбрать' and \
                    upload_prices_short_shop != '' and \
                    upload_prices_legal_name != '' and \
                    upload_prices_mp != 'Выбрать ':
                if upload_prices_mp == 'sber' and upload_option == 'xml':
                    job = q.enqueue_call(sber.create_sber_xml
                                         (stocks_is_null=is_null_stocks,
                                          site_url=upload_prices_url,
                                          legal_name=upload_prices_legal_name,
                                          short_shop_name=upload_prices_short_shop,
                                          category=upload_price_category,
                                          markup=upload_prices_markup,
                                          discount=upload_price_discount))
                elif upload_prices_mp == 'yandex' and upload_option == 'xml':
                    job = q.enqueue_call(yan.create_ym_xml
                                         (stocks_is_null=is_null_stocks,
                                          site_url=upload_prices_url,
                                          legal_name=upload_prices_legal_name,
                                          short_shop_name=upload_prices_short_shop,
                                          category=upload_price_category,
                                          markup=upload_prices_markup,
                                          discount=upload_price_discount))
                print(989898989, job.get_id)
                print(989898989, *data.items(), sep='\n')

            else:
                flash("Проверьте правильность ввода данных", 'error')

        elif make == 'check_settings_uploads':
            print('!!!!!!check_settings!!!!!11')
            if data.get('upload_prices_mp') == 'Выбрать' \
                    and data.get('upload_prices_store') == 'Выбрать':
                flash("Укажите хотя бы один магазин для которого нужен просмотр настроек", "alert")
            else:
                result = {k: v for k, v in data.items() if (v != '0' and v != 'Выбрать')}
                if result.get('upload_prices_store') is not None \
                        and result.get("upload_prices_mp") is not None:
                    upload_settings = db.session.scalars(select(UploadPrice)
                    .where(
                        UploadPrice.upload_prices_mp == data.get('upload_prices_mp'))
                    .where(
                        UploadPrice.upload_prices_store == data.get('upload_prices_store'))) \
                        .first()
                    try:
                        upl_price_setts = upload_settings.__dict__
                        uid = current_user.id
                        role = current_user.roles
                        need_id = current_user.company_id
                        user_name = current_user.name
                        photo = current_user.photo
                        if not photo or photo is None:
                            photo = 'prof-music-2.jpg'

                        return render_template('/upload_price_settings.html',
                                               uid=uid, role=role,
                                               photo=photo,
                                               user_name=user_name,
                                               show=True,
                                               upload_data=upl_price_setts)
                    except:
                        flash(
                            "Настройки для указанных магазинов не найдены. "
                            "Введите требуемые настройки и сохраните их.",
                            "alert")

                elif result.get('upload_prices_store') is not None:
                    upload_settings = db.session.scalars(select(UploadPrice)
                    .where(
                        UploadPrice.upload_prices_store == data.get('upload_prices_store'))) \
                        .first()

                    try:
                        upload_data = upload_settings.__dict__
                        # print(232323, type(upload_data), upload_data)

                        uid = current_user.id
                        role = current_user.roles
                        need_id = current_user.company_id
                        user_name = current_user.name
                        photo = current_user.photo
                        if not photo or photo is None:
                            photo = 'prof-music-2.jpg'

                        return render_template('/upload_price_settings.html',
                                               upload_data=upload_data,
                                               uid=uid, role=role,
                                               photo=photo,
                                               user_name=user_name,
                                               show=True
                                               )
                    except:
                        flash("Настройки для указанного магазина не найдены. "
                              "Введите требуемые настройки и сохраните их.",
                              "alert")

                elif result.get('upload_prices_mp') is not None:
                    upload_settings = db.session.scalars(select(UploadPrice)
                    .where(
                        UploadPrice.upload_prices_mp == data.get('upload_prices_mp'))) \
                        .first()
                    try:
                        upload_data = upload_settings.__dict__
                        uid = current_user.id
                        role = current_user.roles
                        need_id = current_user.company_id
                        user_name = current_user.name
                        photo = current_user.photo
                        if not photo or photo is None:
                            photo = 'prof-music-2.jpg'

                        return render_template('/upload_price_settings.html',
                                               uid=uid, role=role,
                                               photo=photo,
                                               user_name=user_name,
                                               show=True,
                                               upload_data=upload_data
                                               )
                    except:
                        flash(
                            "Настройки для указанного магазина не найдены. "
                            "Введите требуемые настройки и сохраните их.",
                            "alert")

        return redirect('/upload-prices-settings')

    show = request.args.get('show')
    #######################################################
    # print(1111111111111, show, request.args.get('make'))
    # for key in request.args.keys():
    #     print(key, f"= request.args.get('{key}')")
    #######################################################
    rows, rows_mp = [], []
    # if show:
    #     uid = current_user.id
    #     role = current_user.roles
    #     need_id = current_user.company_id
    #     user_name = current_user.name
    #     photo = current_user.photo
    #     if not photo or photo is None:
    #         photo = 'prof-music-2.jpg'
    #     upload_price_name = request.args.get('upload_price_name')
    #     is_null_stocks = request.args.get('is_null_stocks')
    #     upload_prices_mp = request.args.get('upload_prices_mp')
    #     upload_option = request.args.get('option')
    #     upload_prices_markup = request.args.get('upload_prices_markup')
    #     upload_prices_store = request.args.get('upload_prices_store')
    #     upload_price_discount = request.args.get('upload_price_discount')
    #     upload_prices_short_shop = request.args.get('upload_prices_short_shop')
    #     upload_prices_legal_name = request.args.get('upload_prices_legal_name')
    #     upload_prices_url = request.args.get('upload_prices_url')
    #     upload_price_category = request.args.get('upload_price_category')
    #
    #     return render_template('/upload_price_settings.html',
    #                            uid=uid, role=role,
    #                            upload_price_name=upload_price_name,
    #                            upload_prices_mp=upload_prices_mp,
    #                            upload_option=upload_option,
    #                            is_null_stocks=is_null_stocks,
    #                            upload_prices_markup=upload_prices_markup,
    #                            upload_prices_store=upload_prices_store,
    #                            upload_price_discount=upload_price_discount,
    #                            upload_prices_short_shop=upload_prices_short_shop,
    #                            upload_prices_legal_name=upload_prices_legal_name,
    #                            upload_prices_url=upload_prices_url,
    #                            upload_price_category=upload_price_category,
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

    return render_template('/upload_price_settings.html',
                           uid=uid, role=role,
                           rows=rows, rows_mp=set(rows_mp),
                           photo=photo,
                           distributors=WHEELS,
                           user_name=user_name)


@auth.route('/distributor-settings', methods=['GET', 'POST'])
@login_required
def distributor_settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index_main'))
    else:
        rows = []
        rows_mp = []
        role = current_user.roles
        photo = current_user.photo
        user_name = current_user.name
        if request.method == 'POST':
            data = request.form.to_dict()
            # print(*data.items(), sep='\n')
            print(55555, data)

            if data.get('check_settings') is not None:
                if data.get('edit_name_dist') == 'Выбрать':
                    flash('Не выбран поставщик. Укажите поставщика.')
                # return current settings that distributor
                distributor = Distributor.query \
                    .filter_by(distributor=data.get('edit_name_dist')).first()
                # dist_data = distributor.__dict__
                # print(3333333, dist_data)

                dist_name = distributor.distributor
                key_api_dist = distributor.key_api_dist
                login_api_dist = distributor.login_api_dist
                api_link = distributor.api_link
                return render_template('distributor-settings.html',
                                       role=role, rows=rows,
                                       key_api_dist=key_api_dist,
                                       login_api_dist=login_api_dist,
                                       distributor=dist_name,
                                       api_link=api_link,
                                       show_dist=True,
                                       distributors=WHEELS,
                                       photo=photo,
                                       user_name=user_name)

            elif data.get('distributor') == 'save':
                if data.get('add_distributor') == 'Выбрать':
                    flash('Выберите поставщика')
                disributor = Distributor(
                    distributor=data.get('add_distributor'),
                    login_api_dist=data.get('add_login_api_dist'),
                    key_api_dist=data.get('add_key_api_dist'),
                    api_link=data.get('add_api_link')
                )
                db.session.add(disributor)
                db.session.commit()
                flash('Настройки поставщика удачно сохранены')

            elif data.get('distributor_price') == 'save':
                print(88888, data)
                if data.get('settings_name_dist') == '':
                    flash('Выберите поставщика')
                if data.get('dist_price_name') == '':
                    flash('Укажите название прайса')
                upload_prices_id = data.get('upload_prices_id')
                if upload_prices_id == '0':
                    dist_price = DistributorPrice(
                        price_name=data.get('dist_price_name'),
                        distributor=data.get('settings_name_dist'),
                        login_dist_price=data.get('login_dist_price'),
                        dist_price_markup=data.get('dist_price_markup'),
                        key_dist_price=data.get('key_dist_price'),
                        price_link=data.get('price_link'),
                        is_scheduler=data.get('is_scheduler'),
                        type_downloads=data.get('type_downloads'),
                        user_modifed=current_user.id
                    )
                    db.session.add(dist_price)
                    db.session.commit()

                    flash('Настройки прайса поставщика удачно сохранены')
                else:
                    keypass = data.get('key_dist_price')
                    loginpass = data.get('login_dist_price')
                    if loginpass == '0' and keypass != '0':
                        dist_price = DistributorPrice(
                            id=upload_prices_id,
                            price_name=data.get('dist_price_name'),
                            distributor=data.get('settings_name_dist'),
                            key_dist_price=data.get('key_dist_price'),
                            dist_price_markup=data.get('dist_price_markup'),
                            price_link=data.get('price_link'),
                            is_scheduler=data.get('is_scheduler'),
                            type_downloads=data.get('type_downloads'),
                            user_modifed=current_user.id
                        )
                        db.session.merge(dist_price)
                        db.session.commit()

                    elif keypass == '0' and loginpass != '0':
                        dist_price = DistributorPrice(
                            id=upload_prices_id,
                            price_name=data.get('dist_price_name'),
                            distributor=data.get('settings_name_dist'),
                            login_dist_price=data.get('login_dist_price'),
                            dist_price_markup=data.get('dist_price_markup'),
                            price_link=data.get('price_link'),
                            is_scheduler=data.get('is_scheduler'),
                            type_downloads=data.get('type_downloads'),
                            user_modifed=current_user.id
                        )
                        db.session.merge(dist_price)
                        db.session.commit()

                    elif keypass == '0' and loginpass == '':
                        dist_price = DistributorPrice(
                            id=upload_prices_id,
                            price_name=data.get('dist_price_name'),
                            distributor=data.get('settings_name_dist'),
                            dist_price_markup=data.get('dist_price_markup'),
                            price_link=data.get('price_link'),
                            is_scheduler=data.get('is_scheduler'),
                            type_downloads=data.get('type_downloads'),
                            user_modifed=current_user.id
                        )
                        db.session.merge(dist_price)
                        db.session.commit()

                    else:
                        dist_price = DistributorPrice(
                            id=upload_prices_id,
                            price_name=data.get('dist_price_name'),
                            distributor=data.get('settings_name_dist'),
                            login_dist_price=data.get('login_dist_price'),
                            dist_price_markup=data.get('dist_price_markup'),
                            key_dist_price=data.get('key_dist_price'),
                            price_link=data.get('price_link'),
                            is_scheduler=data.get('is_scheduler'),
                            type_downloads=data.get('type_downloads'),
                            user_modifed=current_user.id
                        )
                        db.session.merge(dist_price)
                        db.session.commit()

                    flash('Настройки прайса поставщика удачно обновлены', 'success')

            elif data.get('check_dist_price') == 'check':
                if data.get('settings_name_dist') == 'Выбрать':
                    flash('Не выбран поставщик. Укажите поставщика.')
                else:
                    # return current settings that distributor_price
                    dist_price = DistributorPrice.query \
                        .filter_by(distributor=data.get('settings_name_dist')).first()
                    # print(333555553333, dist_price)
                    dist_price_data = dist_price.__dict__
                    key_api_dist = dist_price_data.get('key_dist_price', '0')
                    login_api_dist = dist_price_data.get('login_dist_price')
                    if not login_api_dist:
                        login_api_dist = '0'
                    store = dist_price_data.get('upload_prices_store', 'Выбрать')
                    print(111111111111111111111111111111111111111111111111111111111111111111, login_api_dist)
                    return render_template('distributor-settings.html',
                                           role=role, rows=rows,
                                           dist_price_data=dist_price_data,
                                           login_api_dist=login_api_dist,
                                           key_api_dist=key_api_dist,
                                           store=store,
                                           distributors=WHEELS,
                                           show=True,
                                           photo=photo,
                                           user_name=user_name)

            return redirect(url_for('auth.distributor_settings'))

        shops_list = Marketplaces.query. \
            filter_by(company_id=current_user.company_id) \
            .all()

        for shop in shops_list:
            rows.append(shop.shop_name)

        return render_template('distributor-settings.html',
                               role=role,
                               rows=rows, rows_mp=set(rows_mp),
                               photo=photo,
                               user_name=user_name,
                               distributors=WHEELS)


@auth.route('/distributors-table', methods=['GET', 'POST'])
@login_required
def distributors_table():
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
                # print(3242344314, proxy_settings)

            disributors_data = Distributor.query.all()
            for row in disributors_data:
                current_work = {'is_scheduler': False,
                                'enable_orders_submit': False,
                                'enable_sync_bd': False,
                                'send_tg_notice': False}
                if row.distributor in proxy_settings.keys():
                    current = {i: True for i in proxy_settings[row.distributor]}
                    current_work.update(current)
                    db.session.execute(update(Distributor)
                                       .where(Distributor.id == row.id)
                                       .values(current_work))
                else:
                    db.session.execute(update(Distributor)
                                       .where(Distributor.id == row.id)
                                       .values(current_work))
                db.session.commit()

            if len(data.keys()) > 0:
                try:
                    scheduler.remove_job('distibutors')
                except:
                    print('Job_distibutors_update_error')
                finally:
                    current_job = scheduler.add_job(back_distibutors_tasks,
                                                    id='distibutors',
                                                    trigger='interval',
                                                    minutes=600)
                    if scheduler.state == 0:
                        scheduler.start()

                    print(100000000, current_job)
            else:
                try:
                    scheduler.remove_job('distibutors')
                except:
                    print('Job_distibutors_remove_error')

            return redirect(url_for('auth.distributors_table'))

        else:
            # print(22222, request.args.to_dict())
            uid = current_user.id
            role = current_user.roles
            user_name = current_user.name
            photo = current_user.photo
            if not photo or photo is None:
                photo = 'prof-music-2.jpg'
            rows = ''

            raw_list_shops = db.session.query(Distributor) \
                .order_by(Distributor.id.asc()) \
                .all()
            # raw_list_products = db.session.query(Product)
            # .paginate(page=30, per_page=30, error_out=False).items
            for row in raw_list_shops:
                id = row.id
                # if row.date_modifed:
                #     date_modifed = row.date_modifed
                # else:
                #     date_modifed = "Нет"
                # if row.check_send_null:
                #     check_send_null = "checked"
                # else:
                #     check_send_null = "unchecked"
                #
                # if row.send_common_stocks:
                #     send_common_stocks = "checked"
                # else:
                #     send_common_stocks = "unchecked"

                if row.is_scheduler:
                    is_scheduler = "checked"
                else:
                    is_scheduler = "unchecked"

                if row.enable_sync_bd:
                    enable_sync_bd = "checked"
                else:
                    enable_sync_bd = "unchecked"

                if row.enable_orders_submit:
                    enable_orders_submit = "checked"
                else:
                    enable_orders_submit = "unchecked"

                if row.send_tg_notice:
                    send_tg_notice = "checked"
                else:
                    send_tg_notice = "unchecked"

                rows += '<tr>' \
                        f'<td >{row.id} </td>' \
                        f'<td >{row.distributor}</td>' \
                        f'<td >{row.api_link}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="is_scheduler_{id}' \
                        f'" {is_scheduler} class="iswitch iswitch iswitch-purple"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="enable_sync_bd_{id}' \
                        f'" {enable_sync_bd} class="iswitch iswitch iswitch-warning"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="enable_orders_submit_{id}' \
                        f'" {enable_orders_submit} class="iswitch iswitch iswitch-warning"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="send_tg_notice_{id}' \
                        f'" {send_tg_notice} class="iswitch iswitch iswitch-primary"></div></td>' \
                        f'</tr>'

            return unescape(render_template('distributors-table.html',
                                            rows=rows, role=role,
                                            photo=photo,
                                            user_name=user_name,
                                            distributors=WHEELS))


@auth.route('/distributors-prices', methods=['GET', 'POST'])
@login_required
def distributors_prices():
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
                # print(3242344314, proxy_settings)

            disr_prices_data = DistributorPrice.query.all()
            for row in disr_prices_data:
                current_work = {'is_scheduler': False,
                                'enable_sync_bd': False,
                                'send_tg_notice': False}
                if row.distributor in proxy_settings.keys():
                    current = {i: True for i in proxy_settings[row.distributor]}
                    current_work.update(current)
                    db.session.execute(update(DistributorPrice)
                                       .where(DistributorPrice.id == row.id)
                                       .values(current_work))
                else:
                    db.session.execute(update(DistributorPrice)
                                       .where(DistributorPrice.id == row.id)
                                       .values(current_work))
                db.session.commit()

            if len(data.keys()) > 0:
                try:
                    scheduler.remove_job('distibutors_prices')
                except:
                    print('Job_update_error')
                finally:
                    current_job = scheduler.add_job(back_dist_prices_tasks,
                                                    id='distibutors_prices',
                                                    trigger='interval',
                                                    minutes=600)
                    if scheduler.state == 0:
                        scheduler.start()

                    print(100000000, current_job)
            else:
                try:
                    scheduler.remove_job('distibutors')
                except:
                    print('Job_remove_error')

            return redirect(url_for('auth.distributors_prices'))

        else:
            uid = current_user.id
            role = current_user.roles
            user_name = current_user.name
            photo = current_user.photo
            if not photo or photo is None:
                photo = 'prof-music-2.jpg'
            rows = ''

            raw_list_prices = db.session.query(DistributorPrice) \
                .order_by(DistributorPrice.id.asc()) \
                .all()

            for row in raw_list_prices:
                id = row.id

                if row.is_scheduler:
                    is_scheduler = "checked"
                else:
                    is_scheduler = "unchecked"

                if row.enable_sync_bd:
                    enable_sync_bd = "checked"
                else:
                    enable_sync_bd = "unchecked"

                if row.send_tg_notice:
                    send_tg_notice = "checked"
                else:
                    send_tg_notice = "unchecked"

                shop_name = row.shop_name
                if shop_name == 'all':
                    shop_name = 'Все магазины'

                rows += '<tr>' \
                        f'<td >{row.id} </td>' \
                        f'<td >{row.price_name}</td>' \
                        f'<td >{row.distributor}</td>' \
                        f'<td >{shop_name}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="is_scheduler_{id}' \
                        f'" {is_scheduler} class="iswitch iswitch iswitch-purple"></div></td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="enable_sync_bd_{id}' \
                        f'" {enable_sync_bd} class="iswitch iswitch iswitch-warning"></div></td>' \
                        f'<td >{row.type_downloads}</td>' \
                        f'<td ><div class="form-block"><input type="checkbox" value="{row.distributor}" name="send_tg_notice_{id}' \
                        f'" {send_tg_notice} class="iswitch iswitch iswitch-primary"></div></td>' \
                        f'</tr>'

            return unescape(render_template('distributors-prices.html',
                                            rows=rows, role=role,
                                            photo=photo,
                                            user_name=user_name,
                                            distributors=WHEELS))


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
