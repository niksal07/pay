from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER", "local_user")  # Default to 'local_user' if not set
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "local_pass")  # Default to 'local_pass' if not set
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")  # Default to 'localhost' if not set
MYSQL_DB = os.getenv("MYSQL_DB", "pay_app_db")  # Default to 'pay_app_db' if not set
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pay_app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Generate a random secret key for session management
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin_page'  # Redirect to signin page if not logged in
login_manager.login_message_category = 'info'  # Set the flash message category for login required messages


from pay_app import routes
