from flask import Blueprint, render_template
from flask_login import current_user, login_required
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index_main():
    return render_template('start_page.html')  #index_2.html')

@main.route('/profile')
@login_required
def profile():
    name = current_user.name
    uid = current_user.id
    return render_template('index.html', name=name, uid=uid)