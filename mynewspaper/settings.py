#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django settings for mynewspaper project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!#r2*ilc^es(zl5d0bkvsy5!br-w*7w$-sm*57*8q5^m(ko$+*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = True
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'accounts.MyUser'

# Application definition




INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainpage',
    "captcha",
    'article',
    'accounts',
    'topic',
    'comment',
    'notifications',
    'ckeditor',
    'ckeditor_uploader',
    'djcelery',
    'djsupervisor',
    'company',
    'investment',
    'products',
    'DjangoUeditor',
    'updatenew',
    'judgement',
    'scorebill',
    'finance',
    'discovery',
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mynewspaper.urls'

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

WSGI_APPLICATION = 'mynewspaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newspaper',
        'USER': 'root',
        'PASSWORD': 'WuTong123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")

#CKEDITOR 富文本编辑框设置
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'language': 'zh-cn',
        #'toolbar': 'Basic',
    },
}

import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'

CACHE_EXPIRETIME = 1209600 #redis缓存过期时间

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge' #验证码样式，数学

LOGIN_URL = '/user/loggin/'
