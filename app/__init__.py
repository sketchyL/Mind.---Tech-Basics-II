# combines all parts of app
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

App = Flask(__name__)
App.config.from_object(Config)
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(App, metadata=metadata)
migrate = Migrate(App, db, render_as_batch=True)
login = LoginManager(App)
login.login_view = "login"

App.app_context().push()
from app import routes, models
