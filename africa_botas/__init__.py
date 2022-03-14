# import os
from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_pymongo import PyMongo

# PASSWORD = os.getenv('MONGO_CRUD_PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bb1131c414ecf54fbcb5ff9253dbff52'
# app.config['MONGO_URI'] = f'mongodb+srv://kasparov:{PASSWORD}@cluster0.em4to.mongodb.net/petshop?retryWrites=true&w=majority'
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# mongo = PyMongo(app)
# login_manager.login_message = 'Por favor inicie sesión para ver esta página'

from africa_botas import routes