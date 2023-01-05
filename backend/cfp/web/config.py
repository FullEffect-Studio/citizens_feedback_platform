import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base Configuration"""
    TESTING = False
    MONGODB_URL = None
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'secret')
    FILE_UPLOADS = os.curdir
    LOGGING = log_config = {
        "version": 1,
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG"
        },
        "handlers": {
            "console": {
                "formatter": "std_out",
                "class": "logging.StreamHandler",
                "level": "DEBUG"
            },
            "file": {
                "formatter": "std_out",
                "class": "logging.FileHandler",
                "level": "INFO",
                "filename": "cfp_logs.log"
            }
        },
        "formatters": {
            "std_out": {
                "format": "%(levelname)s : %(module)s : %(funcName)s : %(message)s",
            }
        },
    }


class DockerConfig(Config):

    """Docker configuration"""

    # Can also use /run/secrets/mongo_url if running on docker
    # db_url = open('/run/secrets/mongo_url.txt')
    MONGODB_URL = "mongodb://db:27017/admin"


class ProductionConfig(Config):
    """Production configuration"""
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
