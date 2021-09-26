from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
# from config import Config

load_dotenv(override=True)
app = Flask(__name__)
# app.config.from_object(Config)
# app.secret_key = os.environ['SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = os.environ['GMAIL_ACCOUNT']
app.config['MAIL_PASSWORD'] = os.environ['GMAIL_PASSWORD']  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)