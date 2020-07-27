from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('DATABASE_URI'))
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = getenv("MY_SECRET_KEY") or "dev"
bcrypt = Bcrypt(app)

from Application import route
