import sys
import pymongo
import configure
import logging

class DataAgent(object):
    """@Brief: responsible of data reading and writing"""
    def __init__(self, *args, **kwargs):
        self.conf = configure.Configure()
        self.client = pymongo.MongoClient(self.conf.host, self.conf.port)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Connect to mongoDB[%s:%s]' % (self.conf.host, self.conf.host))
    
    def __del__(self):
        self.client.close()

    def store_data(self, database_name, collection_name, entity):
        try:
            db = self.client[database_name]
            collection = db[collection_name]
        except Exception, err:
            print >> sys.stderr, 'db[%s] collection[%s] load error[%s]' % (database_name, collection_name, err)
            return -1
        try:
            collection.insert(entity)
        except Exception, err:
            print >> sys.stderr, 'db[%s] collection[%s] write entity[%s] error[%s]' % (database_name, collection_name, entity, err)
            return -1
        return 0

    def load_data_id(self, database_name, collection_name):
        try:
            id_list = []
            db = self.client[database_name]
            collection = db[collection_name]
            for item in collection.find():
                id_list.append(item['id'])
        except Exception as err:
            self.logger.error('db[%s] collection[%s] load data error[%s]' % (database_name, collection, err), exc_info=True)
            return -1
        return id_list        