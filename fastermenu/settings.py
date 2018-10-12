import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'o9undphnksx)_+_x9g9o*l)$neksr4wcibi1*&dlk+z-r0jcij'

DEBUG = True


ALLOWED_HOSTS = ['localhost', 'www.localhost', '127.0.0.1', '.fastermenu.com', '.elasticbeanstalk.com', 'fastermenu-214511.appspot.com']



# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	'django_cleanup',
	'bootstrap3',
	'storages',
	'fastermenu',
	'enterprise',
	'barcode',
	'menu',
	'cart',
	'account',
	'order',
	'locale',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LANGUAGES = (
    ('en', _('English')),
    ('tr', _('Turkish')),
)

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


ROOT_URLCONF = 'fastermenu.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
		],
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

WSGI_APPLICATION = 'fastermenu.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#       'ENGINE': 'django.db.backends.postgresql',
#       'HOST': os.environ['DB_HOST'],
#       'PORT': os.environ['DB_PORT'],
#       'NAME': os.environ['DB_NAME'],
#       'USER': os.environ['DB_USER'],
#       'PASSWORD': os.environ['DB_PASSWORD']
#     }
# }

if 'PRODUCTION' in os.environ:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'fasterdb',
			'USER': 'fasteruser',
			'PASSWORD': 'faster(MENU)',
			'HOST': '35.240.13.81',
			'PORT': '5432',
		}
	}

else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			
			'NAME': 'fasterdb',
			'USER': 'fasteruser',
			'PASSWORD': 'faster(MENU)',
			'HOST': '35.241.252.147',
			'PORT': '5432',
		}
	}

# Password validation

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




LOGIN_REDIRECT_URL = '/enterprise/'
LOGOUT_REDIRECT_URL = '/enterprise/login'
LOGIN_URL = '/enterprise/login'



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# EMAIL
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'support@fastermenu.com'
EMAIL_HOST_PASSWORD = 'fastermail123'
DEFAULT_FROM_EMAIL = 'FasterMenu Support <support@fastermenu.com>'



# where static files
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]


# STATIC_URL = os.environ['STATIC_URL'] # /static/ if DEBUG else Google Cloud bucket url

# collectstatic directory (located OUTSIDE the base directory)
# TODO: configure the name and path to your static bucket directory (where collectstatic will copy to)
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')


AWS_ACCESS_KEY_ID = 'AKIAIROXVV3GRHIOIIVQ'
AWS_REGION = 'eu-central-1'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'fastermenu-assets'
AWS_S3_CUSTOM_DOMAIN = '{}.s3.{}.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME, AWS_REGION)

if 'AWS_STATIC' in os.environ:
	AWS_LOCATION = 'static'
	AWS_S3_OBJECT_PARAMETERS = {
		'CacheControl': 'max-age=86400',
	}
	STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
	STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
else:
	STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
	STATIC_URL = '/static/'



MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'fastermenu.storage_backends.MediaStorage'


# AWS EC2 Specific Configuration
if 'PRODUCTION' in os.environ or 'STAGING' in os.environ:
	import requests
	EC2_PRIVATE_IP  =   None
	try:
		EC2_PRIVATE_IP  =   requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout = 0.01).text
	except requests.exceptions.RequestException:
		pass

	if EC2_PRIVATE_IP:
		ALLOWED_HOSTS.append(EC2_PRIVATE_IP)


BOOTSTRAP3 = {'set_placeholder': False, 'set_required': False}

