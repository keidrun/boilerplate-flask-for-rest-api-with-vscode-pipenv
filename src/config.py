class Config(object):
    PORT = 5000
    DEBUG = False
    TESTING = False
    REMOTE_DEBUGGING = False
    MONGODB_URI = 'mongodb://db:27017/dev_db'
    MONGODB_DATABASE_NAME = 'dev_db'


class ProductionConfig(Config):
    MONGODB_URI = 'mongodb://db:27017/prod_db'
    MONGODB_DATABASE_NAME = 'prod_db'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class DebuggingConfig(Config):
    REMOTE_DEBUGGING = True
    REMOTE_DEBUGGING_PORT = 3000


object_name = {
    'production': 'config.ProductionConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'debugging': 'config.DebuggingConfig',
}
