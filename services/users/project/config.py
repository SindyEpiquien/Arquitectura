# services/users/project/config.py


import os  # nuevo


class BaseConfig:
    """Configuración base"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_secretkey'
    DEBUG_TB_ENABLED = False  # nuevo
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # nuevo


class DevelopmentConfig(BaseConfig):
    """Configuración de desarrollo"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True  # nuevo


class TestingConfig(BaseConfig):
    """Configuración de prueba"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Configuración de producción"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
