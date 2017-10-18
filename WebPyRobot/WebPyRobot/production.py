"""
Setting file for deployment
"""

from .settings import *

ALLOWED_HOSTS = ['maturepyrobot.com']
DEBUG = False
SECRET_KEY = 'p11%65*p)r)^1)0bw%-@+%-2bgpik&v&*tu8f$@djc&(6z(^n!'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'maturepyrobot',
        'USER': 'maturepyrobot',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}