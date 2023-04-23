import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca= certifi.where()
import os
from dotenv import load_dotenv
load_dotenv()


class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME ) -> None:
        try:
            if MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(os.getenv('MONGO_DB_URL'), tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

        except Exception as e:
            raise e