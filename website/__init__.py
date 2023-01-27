import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()
mail = Mail()
admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '4Nff5wg93dvf7hrbgn'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    mail.init_app(app)
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    admin.init_app(app)

    from .views import views
    from .auth import auth
    from .posts import posts
    from .work_order import work_order
    from .products import prod
    from .vehicles import vehi

    app.register_blueprint(views, url_prifix='/')
    app.register_blueprint(auth, url_prifix='/')
    app.register_blueprint(posts, url_prifix='/')
    app.register_blueprint(work_order, url_prifix='/')
    app.register_blueprint(prod, url_prifix='/')
    app.register_blueprint(vehi, url_prifix='/')

    # from .models import User, Post

    create_database(app)

    return app


def create_database(app):
    if not path.exists('.website' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
