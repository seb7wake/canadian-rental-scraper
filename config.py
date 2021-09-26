import os
import app
import vcr
from flask_mail import Message, email_dispatched

def config_vcr():
    x = vcr.use_cassette('fixtures/scraping.yaml', match_on=['path'])
    x.__enter__()
    return x

def log_message(message, app):
    app.logger.debug(message.subject)

class Config(object):
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('GMAIL_ACCOUNT')
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    VCR = config_vcr()
email_dispatched.connect(log_message)