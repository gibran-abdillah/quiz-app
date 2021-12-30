from pymongo import MongoClient
import os 


class GeneralConfig:
    SECRET_KEY = os.urandom(12)
    MONGODB_URI = os.environ.get('MONGODB_URI','')

class DevelopmentConfig(GeneralConfig):
    DB_NAME = 'quiz_development'
    COLLECTIONS_NAME = 'development'

class ProductionConfig(GeneralConfig):
    DB_NAME = 'quiz_production'
    COLLECTIONS_NAME = 'production'

class TestingConfig(GeneralConfig):
    DB_NAME = 'quiz_testing'
    COLLECTIONS_NAME = 'testing'
    DEBUG = True

configuration = {
    'production':ProductionConfig,
    'development':DevelopmentConfig,
    'default':DevelopmentConfig,
    'testing':TestingConfig
}

