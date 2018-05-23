"""
Django settings for WebPyRobot project.
It's actually a base file. All general settings come here
Settings for development or deployment are in specific files
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p11%65*p)r)^1)0bw%-@+%-2bgpik&v&*gu84$@djc&(6z(^n!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'backend',
    'pure_pagination',
    'ckeditor',
    'django_crontab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'WebPyRobot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'WebPyRobot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_REDIRECT_URL='backend:login'
LOGIN_URL='backend:login'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "backend.routing.channel_routing",
    },
}


CRONJOBS = [
    ("* * * * *", "backend.cron.OneMinuteJob", '>> ~/Master/M1/TER/MaturePyRobots/WebPyRobot/backend/cronOneMinuteJob.log'),
    ("* * * * *", "backend.cron.displayDataChampionship", '>> ~/Master/M1/TER/MaturePyRobots/WebPyRobot/backend/displayDataChampionship.log'),
    ("*/10 * * * *", "backend.cron.TenMinuteJob", '>> ~/Master/M1/TER/MaturePyRobots/WebPyRobot/backend/cronTenMinuteJob.log'),
    # Idk if it's the right way, may be different for deployment version
    # btw it works

    # ("* * * * *", "backend.cron.test", '>> cron.log')
    # seems not being executed
]

CRONTAB_COMMAND_SUFFIX = '2>&1'

MESSAGE_TAGS = {
    messages.DEBUG: 'deep-purple',
    messages.INFO: 'blue',
    messages.SUCCESS: 'green',
    messages.WARNING: 'orange',
    messages.ERROR: 'red',
}


NOT_ALLOWED_KW = ['import', 'exec']
ELO_PTS_MAX_DIFF = 400
ELO_PTS_AWARD_WIN = 1
ELO_PTS_AWARD_LOSE = 0


BATTLE_MAP_NAMES = ['terre', 'premiere']
BATTLE_MAP_SIZE = 32

EXP_CONSTANT = 0.1

# Players initial position
PLAYER_INITIAL_POS_X = 0
PLAYER_INITIAL_POS_Y = 0
OPPONENT_INITIAL_POS_X = 31
OPPONENT_INITIAL_POS_Y = 31

