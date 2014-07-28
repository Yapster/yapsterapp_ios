"""
Django settings for yapsterapp_ios project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f5=d26y-v&qgg_9sctw6jms00+wd4%*q!-)xn54*c8b11%m3vo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
        BASE_DIR + '/email_templates/',
    )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'location',
    'notification',
    'search',
    'users',
    'report',
    'stream',
    'yap',
    'manual_override',
    'south',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yapsterapp_ios.urls'

WSGI_APPLICATION = 'yapsterapp_ios.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": 'django.contrib.gis.db.backends.postgis',
        "HOST": "ye-1-db-1.cagmlb1zwzjw.us-east-1.rds.amazonaws.com",
        "PORT": "5432",
        "NAME": "ye_1_db_1",
        "USER": "yapster",
        "PASSWORD": "Yapster1000000000",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Email Configuration

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@yapster.co'
EMAIL_HOST_PASSWORD = 'Yapster1234'
DEFAULT_FROM_EMAIL = 'info@yapster.co'

#Push Production Notifications Configuration
#'''
APNS_USE_SANDBOX = False
APNS_CERT_FILE = '/home/ec2-user/api/yapsterapp_ios/yapster_ios_push_cert.pem'
APNS_KEY_FILE = '/home/ec2-user/api/yapsterapp_ios/yapster_ios_push_key.pem'
#'''

#Push Development Notification Configuration
'''
APNS_USE_SANDBOX = False
APNS_CERT_FILE = 'yapster_ios_push_cert.pem'
APNS_KEY_FILE = 'yapster_ios_push_key.pem'
#'''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


