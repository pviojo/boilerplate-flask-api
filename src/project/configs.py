import os


class BaseConfig:
    """ Base configuration """
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.getenv('SECRET_KEY', "\xb2\xbe\x03\xe90\x11\xcc\x7f\x08yr.?\xb5\xe7\x7c\xe1@\xc4F\xbb\xed\xd7i")
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    DEFAULT_AWS_BUCKET_NAME = os.environ.get('DEFAULT_AWS_BUCKET_NAME')


class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    SQLALCHEMY_ECHO = True
    pass


class TestingConfig(BaseConfig):
    """ Testing configuration """
    TESTING = True


class StagingConfig(BaseConfig):
    """ Staging configuration """
    pass


class ProductionConfig(BaseConfig):
    """ Production configuration """
    DEBUG = False
