from flask import Flask
import os
from flask import Flask, request, current_app #test
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.update(
    SECRET_KEY='this-is-a-secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    POSTS_PER_PAGE = 3
)

db = SQLAlchemy(myapp_obj)

login = LoginManager(myapp_obj)

login.login_view = 'login'

from app import routes, models

with myapp_obj.app_context():
    db.create_all()

# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
