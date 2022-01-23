from .base_settings import *
import dj_database_url
import os

DEBUG = os.getenv("DJANGO_ENABLE_DEBUG", default="False").lower() == "true"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", default="whatever you failed to put in a secret key")
DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

INTERNAL_IPS = ['127.0.0.1', 'localhost']
DOMAIN = os.getenv("DOMAIN", default="default.com")

ALLOWED_HOSTS = ['*']
