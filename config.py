from pymongo import MongoClient
import os 


class GeneralConfig:
    SECRET_KEY = os.urandom(12)

class DevelopmentConfig(GeneralConfig):
    MONGODB_URI = 'mongodb+srv://'
    DB_NAME = 'quiz_app'
    COLLECTIONS_NAME = 'development'

class ProductionConfig(GeneralConfig):
    MONGODB_URI = 'mongodb+srv://'
    DB_NAME = 'quiz_app'
    COLLECTIONS_NAME = 'production'

class TestingConfig(GeneralConfig):
    MONGODB_URI = 'mongodb+srv://'
    DB_NAME = 'quiz_app'
    COLLECTIONS_NAME = 'testing'
    DEBUG = True

configuration = {
    'production':ProductionConfig,
    'development':DevelopmentConfig,
    'default':DevelopmentConfig,
    'testing':TestingConfig
}

