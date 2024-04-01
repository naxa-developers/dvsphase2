from .settings import *
from pymongo import MongoClient

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply.dfid@gmail.com'
EMAIL_HOST_PASSWORD = 'ldymrhxnhiwjgcpf'
EMAIL_PORT = 587

LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/main/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'
SITE_URL = 'https://admin.dvs-nepal.org/'

CORS_ORIGIN_ALLOW_ALL = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Mongo
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "root")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "root")
MONGO_HOST = os.environ.get("MONGO_HOST", "mongo")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "dvs")

client = MongoClient(
    f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}')
MONGO_DB = client["dvs"]
