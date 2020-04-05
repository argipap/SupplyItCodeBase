# project/config.py


import os


class BaseConfig:
    """Base configuration"""

    DEBUG = False
    TESTING = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    USERS_SERVICE_URL = os.environ.get("USERS_SERVICE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    MAILSLURP_API_KEY = os.environ.get("MAILSLURP_API_KEY")


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    MAILSLURP_API_KEY = os.environ.get("MAILSLURP_API_KEY")


class StagingConfig(BaseConfig):
    """Staging configuration"""

    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(BaseConfig):
    """Production configuration"""

    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
