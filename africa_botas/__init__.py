import os
from flask import Flask
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_pymongo import PyMongo

MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGO_URI'] = f'mongodb+srv://kasparov:{MONGO_PASSWORD}@cluster0.em4to.mongodb.net/africaBotas?retryWrites=true&w=majority'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# mongo = PyMongo(app)
# login_manager.login_message = 'Por favor inicie sesión para ver esta página'

from africa_botas import routes