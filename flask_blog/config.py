from os import environ

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')