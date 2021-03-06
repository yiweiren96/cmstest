"""
Django settings for cmstest project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# 开发环境下使用的配置文件
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_b(t03@bs7fuu%@c1&_(f$6v!%#(y$+0_#glojx6fd(@)6vw(6'

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

    # 第三方包的注册
    'rest_framework',   # 注册 django rest framwork 应用
    'corsheaders',   # 解决跨域问题的第三方包
    # 项目中的功能模块
    'users',            # 用户
    'goods',            # 商品
    'cart',             # 购物车
    'news',             # 新闻


]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.cmstest.site']

MIDDLEWARE = [
    # 解决跨域问题的第三方包
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 指定可以跨域访问当前服务器(127.0.0.1:8000)的白名单
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.cmstest.site:8080',
    'api.cmstest.site:8000',

)
# 指定在跨域访问中，后台是否支持cookie操作
CORS_ALLOW_CREDENTIALS = True

# 注册自定义的用户模型类
AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'cmstest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'cmstest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'cmstest',
        'PASSWORD': 'cmstest',
        'NAME': 'cmstest'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Redis相关配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # 保存session数据到redis中
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 保存 session数据到 Redis中，主要给django的admin后台使用
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# 日志文件配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  					# 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {  	# django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  		# 日志处理方法
        'console': {  	# 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': { 		 # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/cmstest.log"),
            'maxBytes': 300 * 1024 * 1024,   # 日志文件的最大容量
            'backupCount': 10,   # 300M * 10
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  	# 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  	# 可以同时向终端与文件中输出日志
            'level': 'INFO',  					# 日志器接收的最低日志级别
        },
    }
}


# 建议：项目开发完成再添加进来
# DRF相关配置
REST_FRAMEWORK = {
    # 自定义异常处理
    # 'EXCEPTION_HANDLER': 'cmstest.utils .exceptions.custom_exception_handler',

    # 配置项目支持的认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt认证
        'rest_framework.authentication.SessionAuthentication',  # 管理后台使用
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# jwt认证配置
JWT_AUTH = {    # 导包： import datetime
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  	# jwt有效时间

    # 修改登录成功接口返回的响应参数， 新增 user_id 和 username两个字段
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# 使用自定义的认证类: 实现用户名或手机号登录
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend',
]


# drf扩展: 缓存配置, 获取省份和区县接口使用到
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,	# 缓存时间(1小时)
    'DEFAULT_USE_CACHE': 'default',				# 缓存到哪里 (caches中配置的default)
}