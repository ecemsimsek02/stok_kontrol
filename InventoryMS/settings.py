import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g_n2+2bznu6e@1wel!i(&-4tp86_7lop5395ww+i4x%9*7^old'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'axes',
    'corsheaders',
    

    'phonenumber_field',
    'crispy_forms',
    'crispy_bootstrap5',
    'imagekit',
    'django_extensions',
    'django_filters',
    'django_tables2',

    'store.apps.StoreConfig',
    'accounts.apps.AccountsConfig',
    'transactions.apps.TransactionsConfig',
    'invoice.apps.InvoiceConfig',
    'bills.apps.BillsConfig',
    'stocks.apps.StocksConfig',
    'cash.apps.CashConfig',
    'tasks.apps.TasksConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    
]
AXES_FAILURE_LIMIT = 3

# IP bazlı engelleme (varsayılan True)


# Engelleme süresi (saniye cinsinden) - örn. 15 dakika
AXES_COOLOFF_TIME = 1/96  # 15 dakika = 1/96 gün

# Bloklu denemelerde mesaj gösterilsin
AXES_LOCKOUT_TEMPLATE = 'registration/account_locked.html'

ROOT_URLCONF = 'InventoryMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'InventoryMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'FJpCZcfKhpnELHdQalqjOyGjJDhrwFqC',
        'HOST': 'postgres.railway.internal',
        'PORT': '5432',
    }
}
"""
from dotenv import load_dotenv
load_dotenv()  # .env dosyasını yükler

RAILWAY_ENV = os.getenv("RAILWAY_ENV", False)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE', 'railway'),
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'yQOVhBRXvDMCrcmTQtdefSLgHGgyEZGq'),
        'HOST': os.getenv('PGHOST', 'ballast.proxy.rlwy.net' if not RAILWAY_ENV else 'postgres.railway.internal'),
        'PORT': os.getenv('PGPORT', '53974' if not RAILWAY_ENV else '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
    {
    'NAME': 'accounts.validators.CustomPasswordValidator',
},

]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'user-login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'logout'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')
]
#MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
#MEDIA_URL = '/images/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
      'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        
      ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '1000/day'
    },
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
     'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',  # bu da kalmalı
]

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','http://192.168.1.156:8000','http://localhost:3000','http://192.168.1.33:8000']  # API'yi kullanacak domain
CSRF_COOKIE_HTTPONLY = False  # Bu frontend'in JS tarafında CSRF cookie'sine erişebilmesi için
"""
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend'in çalıştığı port
]"""
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Geliştirme ortamı için güvenliğe takılmasın:

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
#x
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'detailed': {
            'format': '[{asctime}] {levelname} - {name} - {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'activity.log'),
            'formatter': 'detailed',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'custom': {  # senin kendi logların için
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}