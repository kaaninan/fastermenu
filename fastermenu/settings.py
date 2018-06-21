import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'o9undphnksx)_+_x9g9o*l)$neksr4wcibi1*&dlk+z-r0jcij'

DEBUG = True

ALLOWED_HOSTS = ['localhost', 'www.localhost', '127.0.0.1', 'app.fastermenu.com', '.elasticbeanstalk.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'storages',
    'fastermenu',
    'enterprise',
    'barcode',
    'menu',
    'cart',
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

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Email

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'smtp.yandex.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'info@exammodule.net'
# EMAIL_HOST_PASSWORD = 'exam3module'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'ExamModule <info@exammodule.net>'



# where static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]




AWS_ACCESS_KEY_ID = 'AKIAIROXVV3GRHIOIIVQ'
AWS_REGION = 'eu-central-1'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'fastermenu-assets'
AWS_S3_CUSTOM_DOMAIN = '{}.s3.{}.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME, AWS_REGION)

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'fastermenu.storage_backends.MediaStorage'
