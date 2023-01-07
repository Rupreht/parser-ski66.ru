""" Init """
import os
import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__) + '/../')

date_format = '%d %B %Y %H:%M'

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(test_config=None):
    """ Init App """

    from .models import User
    from . import auth as auth_blueprint
    from .posts import routes as main_blueprint

    app = Flask(__name__, instance_relative_config=True)
    locale.setlocale(locale.LC_ALL, os.getenv('LANGUAGE', 'ru_RU'))
    csrf.init_app(app)

    if not os.getenv("SQLALCHEMY_DATABASE"):
        raise RuntimeError("SQLALCHEMY_DATABASE is not set")

    app.config.from_prefixed_env()
    app.config['ASSETS_DEBUG'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' +\
        os.path.join(BASEDIR, os.getenv('SQLALCHEMY_DATABASE'))
    app.config['TIMEZONE'] = os.getenv("TZ")
    # tz = timezone(app.config['TIMEZONE'])
    # data_updated_time = datetime.datetime.now().strftime(app.date_format)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user
        # table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint.auth)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint.main)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
