"""
Django settings for AI_DCS project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os


import logging
import django.utils.log
import logging.handlers


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDlHWUCUujw1pQolsDfutdseFZdPvH6HwL'      # 替换为用户的 secretId
secret_key = 'HMBj8JEtHOEn5GEwVoqb5INOAiV3O9cl'      # 替换为用户的 secretKey
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys


BASE_DIR_father =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_LOG_DIR = os.path.join(BASE_DIR, "log")

# 使各个模块，可以导入
# 注意init文件
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR, 'extra_apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,BASE_DIR_father)





# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
#                       '[%(levelname)s][%(message)s]'
#         },
#         'simple': {
#             'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
#         },
#         'collect': {
#             'format': '%(message)s'
#         }
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'default': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR, "aidcs_info.log"),
#             'maxBytes': 1024 * 1024 * 50,
#             'backupCount': 3,
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#         'error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR, "aidcs_err.log"),
#             'maxBytes': 1024 * 1024 * 50,
#             'backupCount': 5,
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#         'collect': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR, "aidcs_collect.log"),
#             'maxBytes': 1024 * 1024 * 50,
#             'backupCount': 5,
#             'formatter': 'collect',
#             'encoding': "utf-8"
#         },
#         'file_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename':os.path.join(BASE_LOG_DIR, "aidcs_all.log"),
#             'formatter':'standard'
#          },
#         'mail_admins': {
#              'level': 'ERROR',
#              'class': 'django.utils.log.AdminEmailHandler',
#               'formatter':'standard'
#          },
#
#     },
#     'loggers': {
#         '': {
#             'handlers': ['default','file_handler', 'console', 'error'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'collect': {
#             'handlers': ['console', 'collect'],
#             'level': 'INFO',
#         },
#         'django': {
#              'handlers': ['console','file_handler'],
#              'level':'DEBUG',
#              'propagate': True,
#          },
#          'django.request': {
#              'handlers': ['mail_admins'],
#              'level': 'ERROR',
#              'propagate': False,
#          },
#
#
#     },
# }



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qp5wa05m41^eb*f%)i7m1_bh+^%5)$hdd^2lzp(rkg$k)nr0iz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.105','192.168.1.109','192.168.1.113','192.168.1.106','192.168.1.108','0.0.0.0','127.0.0.1','192.168.1.102','121.193.204.81','106.13.37.131','www.aidcs.cn','aidcs.cn','192.168.1.112','192.168.1.111','*.*.*.*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'users',
    'captcha',
    'works',
    'operation',
    'channels',
    'chat'
]

# 此处重载是为了使我们的UserProfile生效
AUTH_USER_MODEL = "users.UserProfile"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AI_DCS.urls'

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
                'django.template.context_processors.media',

            ],
        },
    },
]
ASGI_APPLICATION = 'AI_DCS.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

WSGI_APPLICATION = 'AI_DCS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'aidcs02',

            'USER': 'root',
            'PASSWORD': '8831366.',
            'HOST': "127.0.0.1"
        }
}


# 'USER': 'debian-sys-maint',
# 'PASSWORD': 'zr8Va1UeDZy8JgcH',
# django.db.utils.OperationalError: (1698, "Access denied for user 'root'@'localhost'")

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# 相当于nginx 的映射
STATIC_URL = '/static/'

# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有STATICFILES_DIRS中所有文件夹中的文件，以及各app中static中的文件都复制过来
# 把这些文件放到一起是为了用apache等部署的时候更方便 ，比如nginx 的反向代理
STATIC_ROOT = '/home/ai/AI_DCS/static/'

# 其它 存放静态文件的文件夹，可以用来存放项目中公用的静态文件，里面不能包含 STATIC_ROOT
# 如果不想用 STATICFILES_DIRS 可以不用，都放在 app 里的 static 中也可以

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 静态文件放在对应的 app 下的 static 文件夹中 或者 STATICFILES_DIRS 中的文件夹中。
# 当 DEBUG = True 时，Django 就能自动找到放在里面的静态文件。（Django 通过 STATICFILES_FINDERS 中的“查找器”，
# 找到符合的就停下来，寻找的过程 类似于 Python 中使用 import xxx 时，找 xxx 这个包的过程）

EMAIL_HOST = "smtp.ym.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "no-reply@aidcs.cn"
EMAIL_HOST_PASSWORD = "aidcsaidcs"
EMAIL_USE_TLS= False
EMAIL_FROM = "no-reply@aidcs.cn"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Active_IP='http://106.13.37.131'
#Active_IP='http://127.0.0.1:8000'

#'http://www.aidcs.cn'

# 1.清空apps文件夹下的各个 migrations文件夹下的py 文件，不要删除ini文件，然后先进行makemigrations，后migrate
# 2.将dafult.png 文件放到media 文件夹下的image 文件夹下


# WX_APP_SECRET="6436914e5d61afdfec8d8d1cf953ef12"
WX_APP_SECRET="a1809483e3265c1d026f4b7c760dc202"

USE_PROXY={}
