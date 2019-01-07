from api.todos.views import users_blueprint
from api.users.views import users_blueprint

from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/robson/Projects/Flask/restful-api/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(users_blueprint, url_prefix='/user')
app.register_blueprint(todos_blueprint, url_prefix='/todo')


# @app.route('/')
# def root():
#     pass
