import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base Configuration"""


class ProductionConfig(Config):
    """Production configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Production configuration"""

    TESTING = True

