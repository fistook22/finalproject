import os
import random

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'app/static/whisky_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)

app.config['SECRET_KEY'] = random._urandom(80)
db_info = {'host': 'localhost',
           'database': 'dram',
           'psw': os.environ['psw'],
           'user': 'postgres',
           'port': ''}
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/" \
                                 f"{db_info['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import models, routes
