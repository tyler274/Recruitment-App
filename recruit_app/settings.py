# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

os_env = os.environ

class Config(object):
    SECRET_KEY = os_env.get('RECRUIT_APP_SECRET', 'secret-key')  # TODO: Change me
    REDIS_URL = os.getenv('REDISTOGO_URL')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = True
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'null')  # Can be "memcached", "redis", etc.
    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_PASSWORD_HASH', 'bcrypt')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'fasc89erek')
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_TRACKABLE = True

    SECURITY_REGISTER_USER_TEMPLATE = 'public/register.html'
    SECURITY_LOGIN_USER_TEMPLATE = 'public/login.html'
    SECURITY_FORGOT_PASSWORD_TEMPLATE = 'public/forgot.html'
    SECURITY_CHANGE_PASSWORD_TEMPLATE = 'public/change.html'
    SECURITY_RESET_PASSWORD_TEMPLATE = 'public/reset.html'

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    JACK_KNIFE_URL = 'http://ridetheclown.com/eveapi/audit.php'

    SENTRY_DSN = os.getenv('SENTRY_DSN')

    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    # Get your recaptcha settings from google, search "google recaptcha" for the link
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

    MAX_NUMBER_PER_PAGE = 100
    # MAX_LENGTH_FIELDS = 2000
    GSF_USERNAME = os.getenv('GSF_USERNAME', '')
    GSF_PASSWORD = os.getenv('GSF_PASSWORD', '')
    GSF_BLACKLIST_URL = os.getenv('GSF_BLACKLIST_URL')

    API_MASK = 1073741823
    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EVEAPI_URL = os.getenv('EVEAPI_URL', 'api.eveonline.com')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL', 'postgresql://recruit@localhost:5432/recruit')
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    WHOOSH_BASE = os.path.join(basedir, 'search.db')


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    #DB_NAME = 'dev.db'
    # Put the db file in project root
    #DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL', 'postgresql://recruit@localhost:5432/recruit')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    #DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    ASSETS_DEBUG = True
    CACHE_TYPE = 'redis'
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL', 'postgresql://recruit@localhost:5432/recruit')
    
