from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from config import Config

load_dotenv(override=True)
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ['SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
mail = Mail(app)