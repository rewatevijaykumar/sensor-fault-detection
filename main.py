from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
import sys

def test_exception():
    try:
        logging.info('Divide number')
        a = 1/0
        
    except Exception as e:
        raise SensorException(e,sys)

if __name__ == '__main__':
    # mongodb_client = MongoDBClient()
    # print("collection name:", mongodb_client.database.list_collection_names())
    try:
        test_exception()
    except Exception as e:
        print(e)
