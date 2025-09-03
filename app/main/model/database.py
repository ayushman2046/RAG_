from pymongo import MongoClient


class Database:
    def __init__(self, app):
        db_host = app.config['MONGO_DATABASE_HOST']
        db_port = app.config['MONGO_DATABASE_PORT']
        db_name = app.config['MONGO_DATABASE_NAME']
        
        connection_string = f"mongodb://{db_host}:{db_port}/{db_name}"
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            print("MongoDB connection established successfully.")
        except Exception as e:
            print("Failed to establish MongoDB connection:", str(e))
    def get_collection(self, collection_name):
        return self.db[collection_name]
    