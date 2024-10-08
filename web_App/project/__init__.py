# from myapp import app
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, create_engine, select, update, text
from .creds import *


# # Redis
# from rq import Worker, Queue, Connection
# from project.worker import conn

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# q = Queue(connection=conn)

TEST_MODE = 1
LOCAL_MODE = 1
if LOCAL_MODE:

    interval = 6
else:
    interval = 120
PHOTO_UPLOAD_FOLDER = 'project/templates/static/data/profile/'
DATA_PATH = '/project/data/'
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}", pool_size=20, max_overflow=30)

def create_app():
    app = Flask(__name__,
                static_folder='templates/static')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}"
    app.config['USER_ENABLE_EMAIL'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# from celery import Celery
#
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery


# if __name__ == '__main__':
#     app.run()
