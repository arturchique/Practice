import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'yhi8h!wup^_*$05hd*15iw81)1=6_^ihh4kddf198(r=x%)*e='

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '161.35.95.197']


STATIC_ROOT = '/home/john/Practice/practice/static'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'practice',
        'USER': 'userdb',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}