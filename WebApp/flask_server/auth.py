from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_user,logout_user, login_required, current_user
from . import db
from html import unescape
from .connect import Data_base_connect as Db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users

auth = Blueprint('auth', __name__)

@auth.route('/login-ui')
def login():
    return render_template('ui-login.html')

@auth.route('/signup')
def signup():
    return render_template('ui-register.html')

@auth.route('/login-ui', methods=['POST'])
def login_post():
    print(request.form)
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Проверте правильность ввода логина и пароля")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup',  methods=['POST'])
def signup_post():
    # if request.method == 'POST':
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in database

    if user:
        flash('Адрес почты уже существует')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))  #render_template('signup.html')

    # return redirect(url_for('auth.login'))  #render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index_main'))


@auth.route('/dashboard')
@login_required
def dashboard():
    #make smth
    pass
    return unescape(render_template('index.html'))



@auth.route('/add_mp')  #/<int:uid>')
@login_required
def add_mp():
    uid = current_user.id
    return render_template('form-validation.html', uid=uid)

@auth.route('/add_mp', methods=['POST'])  #/<int:uid>')
@login_required
def add_mp_post():
    data = request.form
    uid = current_user.id
    print(data)
    if 'select_mp' in data:
        mp = data.get('select_mp')
        shop_name = data.get('name')
        shop_id = data.get('id_mp')
        key_mp = data.get('key')
        
        if mp == 'Выбрать...':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return render_template('form-validation.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return render_template('form-validation.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, API ключ магазина на маркетплейсе', 'error')
            return render_template('form-validation.html')

        if mp != 'Выбрать...' and key_mp != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
            # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

    return render_template('form-validation.html', uid=uid)


@auth.route('/add_product')  # /<int:uid>')
@login_required
def add_product():
    uid = current_user.id
    return render_template('form-product.html', uid=uid)


@auth.route('/add_product', methods=['POST'])  # /<int:uid>')
@login_required
def add_product_post():
    data = request.form
    uid = current_user.id
    print(data)
    if 'select_mp' in data:
        mp = data.get('select_mp')
        shop_name = data.get('name')
        shop_id = data.get('id_mp')
        key_mp = data.get('key')

        if mp == 'Выбрать...':
            flash('Укажите, пожалуйста, маркетплейс', 'error')
            return render_template('form-validation.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, название магазина, желательно как на маркетплейсе', 'error')
            return render_template('form-validation.html')

        if shop_name is None:
            flash('Укажите, пожалуйста, API ключ магазина на маркетплейсе', 'error')
            return render_template('form-validation.html')

        if mp != 'Выбрать...' and key_mp != None:
            d_b = Db()
            d_b.insert_new_mp(uid, shop_id, shop_name, mp, key_mp)
            # mp_sett = (uid, shop_id, shop_name, mp, key_mp)
            # db.session.add(mp_sett)
            # db.session.commit()
            flash('Настройки удачно сохранены', 'success')

    return render_template('form-priduct.html', uid=uid)


@auth.route('/products')
@login_required
def products():
    uid = current_user.id
    rows = ''
    d_b = Db()
    raw_list_orders = d_b.select_orders()  #db.select_orders()  TODO make select orders to user id
    for row in raw_list_orders:
        print(len(raw_list_orders), row)
        order_id = row[1]
        price = ''

        rows += '<tr>' \
                f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order_id}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[7]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
                f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[8]}</td>' \
                f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{price}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[9]}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[10]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[11]}</td>' \
                f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[12]}</td>' \
                f'</tr>'

    return unescape(render_template('tables-products.html', rows=rows))



@auth.route('/main_table')
def main_table():
    uid = current_user.id
    rows = ''
    d_b = Db()
    raw_list_orders = d_b.select_orders()  #db.select_orders()  TODO make select orders to user id
    for row in raw_list_orders:
        print(len(raw_list_orders), row)
        order_id = row[1]
        price = 1200

        rows += '<tr>' \
                f'<td width = "130" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{order_id}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[7]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[2]}</td>' \
                f'<td width = "120" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[8]}</td>' \
                f'<td width = "100" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{price}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[9]}</td>' \
                f'<td width = "60" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[10]}</td>' \
                f'<td width = "140" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[11]}</td>' \
                f'<td width = "80" height = "40" align="center" style="border: 1px solid; border-color: #c4c4c4; vertical-align:middle; background-color: #f3f3f3;">{row[12]}</td>' \
                f'</tr>'

    ################################################

    return unescape(render_template('tables-responsive.html', rows=rows))