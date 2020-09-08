import os.path
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,' sgi_storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

SECRET_KEY = 'uma-chave-bem-segura'