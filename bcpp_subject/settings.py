# coding=utf-8
import sys
import os

from pathlib import PurePath
from edc_device.constants import CENTRAL_SERVER

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')78^w@s3^kt)6lu6()tomqjg#8_%!381-nx5dtu#i=kn@68h_^'

APP_NAME = 'bcpp_subject'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR = str(PurePath(BASE_DIR).joinpath('etc'))
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.113.201.166']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'rest_framework.authtoken',
    'edc_base.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_lab.apps.AppConfig',
    'edc_sync.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    #     'bcpp.apps.AppConfig',
    #     'bcpp.apps.EdcMetadataAppConfig',
    #     'bcpp.apps.EdcIdentifierAppConfig',
    #     'bcpp.apps.EdcProtocolAppConfig',
    #     'bcpp.apps.SurveyAppConfig',
    #     'bcpp.apps.EdcMapAppConfig',
    #     'bcpp.apps.EdcBaseTestAppConfig',
    #     'bcpp.apps.EdcTimepointAppConfig',
    'household.apps.AppConfig',
    'member.apps.AppConfig',
    'member_clone.apps.AppConfig',
    'plot.apps.AppConfig',
    'enumeration.apps.AppConfig',
    'bcpp_communities.apps.AppConfig',
    'bcpp_referral.apps.AppConfig',
    'bcpp_subject.apps.EdcAppointmentAppConfig',
    'bcpp_subject.apps.EdcVisitTrackingAppConfig',
    'bcpp_subject.apps.EdcDeviceAppConfig',
    'bcpp_subject.apps.EdcMapAppConfig',
    'bcpp_subject.apps.AppConfig',
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

ROOT_URLCONF = 'bcpp_subject.urls'

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

WSGI_APPLICATION = 'bcpp_subject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'member', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'member', 'media')

KEY_PATH = os.path.join(BASE_DIR, 'crypto_fields')
GIT_DIR = BASE_DIR

ANONYMOUS_SURVEY = 'ano'
ANONYMOUS_CONSENT_GROUP = 'anonymous'
ANONYMOUS_ENABLED = True
CURRENT_MAP_AREA = 'test_community'
DEVICE_ID = '99'
DEVICE_ROLE = CENTRAL_SERVER
SURVEY_GROUP_NAME = 'test_survey'
SURVEY_SCHEDULE_NAME = 'year-1'
LOAD_SURVEYS = 'manual'  # 'manual' or 'autodetect' (default)

if 'test' in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher', )
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
