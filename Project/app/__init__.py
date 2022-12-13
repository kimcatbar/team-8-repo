from flask import Flask, request
from flask_babel import Babel
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

myapp_obj = Flask(__name__)                                                             # flask app name declaration

basedir = os.path.abspath(os.path.dirname(__file__))                                    # set directory path

myapp_obj.config.update(                                                                # configuration updates
    SECRET_KEY='this-is-a-secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    LANGUAGES = ['en', 'es', 'zh']
)

db = SQLAlchemy(myapp_obj)          # set db as database variable for the app

babel = Babel(myapp_obj)            # set babel as flask_babel variable for the app

@babel.localeselector               # tells app which language to set the app based on user locale settings
def get_locale():
    return request.accept_languages.best_match(myapp_obj.config['LANGUAGES'])

login = LoginManager(myapp_obj)

login.login_view = 'login'

from app import routes, models

with myapp_obj.app_context():       # creates database
    db.create_all()
    db.session.commit()