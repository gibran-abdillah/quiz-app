from pymongo import MongoClient

class Mongo_Utils:

    def __init__(self, app=None):
        self.app = app 
        self.current_db = None
        self.collections = None 
    
    def init_app(self, app):
        
        if not app.config.get('MONGODB_URI'):
            raise RuntimeError('MONGODB_URI not found')

        self.app = app
        for key, value in self.app.config.items():
            setattr(self, key.lower(), value)
    
    def get_db(self):
        client = MongoClient(self.mongodb_uri)
        db = client[self.db_name]
        collections = db[self.collections_name]

        return db, collections
