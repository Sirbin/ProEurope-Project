from .settings import INSTALLED_APPS, MIDDLEWARE


DEBUG = True
ADMINS = ()
SITE_ID = 1 #da modificare in caso di deploy
ALLOWED_HOSTS = ['*',]
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'proeurope',
        'USER': 'root',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT':'',
    }
}