"""
Django settings for ProEurope project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from django.core.urlresolvers import reverse_lazy
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&69z)^1^j9dd=4_klv&@r&w2z##n$@&qirexap$vlf96d%_p*a'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
ALLOWED_HOSTS = ['ProEurope.pythonanywhere.com'] # inserire nel deploy il dominio
CONN_MAX_AGE = 10
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'azienda',
    'user',
    'localflavor',
    'registration',
    'registrationuSER',
    'gruppi',
    'guardian',
    'client',
    'multiselectfield',
    'modulistica',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ProEurope.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'static','templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProEurope.wsgi.application'

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ProEurope$default',
        'USER': 'ProEurope',
        'PASSWORD':'giuseppedb2016',
        'HOST':'ProEurope.mysql.pythonanywhere-services.com',


    }
}

#Email Configuration

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = "sirbin"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Webmaster Proeurope-Project.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = 'Nuovo Utente Registrato'


SITE_NAME = ('sirbin.pythonanywhere')

#SITE_ID = 2 #da modificare in caso di deploy

# Url Connect
LOGIN_REDIRECT_URL = reverse_lazy('base')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

#nuovo in django 10
#LOGOUT_REDIRECT_URL = reverse_lazy('userManagement')

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

#Data formato
DATE_INPUT_FORMATS = (
    '%d-%m-%Y','%d.%m.%y',
    '%d/%m/%Y',
)

DATETIME_INPUT_FORMATS = (
    '%d-%m-%Y %H:%M%:%S','%d.%m.%Y %H:%M%:%S',
    '%d/%m/%Y %H:%M%:%S',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us' #'it-IT'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),'ProEurope-Project','static','root')

TMP_ROOT = os.path.join(os.path.dirname(BASE_DIR),'ProEurope-Project','tmp')

ZIP_ROOT = os.path.join(os.path.dirname(BASE_DIR),'ProEurope-Project','zip')

FORM_ROOT = os.path.join(os.path.dirname(BASE_DIR),'ProEurope-Project','forms')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR),'ProEurope-Project','static','media')

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR ),'ProEurope-Project','static','static'),
    )

#Gestione Admins
#ADMINS = [('alessio','alessiobino@hotmail.com')]

MANAGERS = [('Alessio','alessiobino@hotmail.com')]

AUTH_USER_MODEL = 'user.UserProfile'

ACCOUNT_ACTIVATIONS_DAYS = 7
REGISTRATION_OPEN = True

try:
    from .local_setting import *
except ImportError:
    pass
