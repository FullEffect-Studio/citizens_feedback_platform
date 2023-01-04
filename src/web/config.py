import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base Configuration"""
    TESTING = False
    MONGODB_URL = None
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'secret')
    FILE_UPLOADS = os.curdir


class ProductionConfig(Config):
    """Production configuration"""
    """try loading """
    MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb+srv://admin:fulleffect@cluster0.b7xsp.mongodb.net'
                                                '/cfp_prod_db?retryWrites=true&w=majority')


class DevelopmentConfig(Config):
    """Development configuration"""
    MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb+srv://admin:fulleffect@cluster0.b7xsp.mongodb.net/cfp_dev_db'
                                                '?retryWrites=true&w=majority')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb+srv://admin:fulleffect@cluster0.b7xsp.mongodb.net'
                                                '/cfp_test_db?retryWrites=true&w=majority')

