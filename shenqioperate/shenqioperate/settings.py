"""
Django settings for shenqioperate project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+0_q9@@4u6o1hj4f^mcay6%l4sei7#$lwu)j%j4u@utq4hc*gi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.Admin'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework.authtoken',  # token
    # 'rest_framework',
    'corsheaders',

    'users.apps.UsersConfig',
    'usermanage.apps.UsermanageConfig',
    'operatemanage.apps.OperatemanageConfig',
    'servemanage.apps.ServemanageConfig',
    'channelmanage.apps.ChannelmanageConfig',

]

REST_FRAMEWORK = {
    # 新增添加自定义的Token验证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'utils.authorization.ExpiringTokenAuthentication',  # 新增的自定义的Token认证
        'rest_framework.authentication.SessionAuthentication',  # session认证

    ),

    # 默认渲染器类，前后端分离用不到
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 允许跨域中间件
    # 'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shenqioperate.urls'

# CORS_ORIGIN_WHITELIST = (
#     'http://192.168.90.21:8080',
# )
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有的源访问
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie,指明在跨域访问中，后端是否支持对cookie的操作

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

WSGI_APPLICATION = 'shenqioperate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '116.62.156.115',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '12345678',
        'NAME': 'shenqioperatetest',

        'POOL': {  # 更多的配置请参考DBUtils的配置
            'minsize': 10,  # 初始化时，连接池中至少创建的空闲的链接，0表示不创建，不填默认为5
            'maxsize': 5,  # 连接池中最多闲置的链接，0不限制，不填默认为0
            'maxconnections': 0,  # 连接池允许的最大连接数，0表示不限制连接数, 默认为0
            'blocking': True,  # 连接池中如果没有可用连接后，是否阻塞等待。True:等待；False:不等待然后报错, 默认False
        }
    }
}

# session状态保持，缓存和数据库两种保存
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# logging日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s  %(lineno)d  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(module)s  %(lineno)d  %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django 在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方式
        'console': {  # 向终端中输出日志
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/shenqioperate.log"),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端和文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接受的最低级别日志
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
