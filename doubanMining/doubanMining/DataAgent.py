import sys
import pymongo
import configure

class DataAgent(object):
    """@brief: responsible of data reading and writing"""
    def __init__(self, *args, **kwargs):
        self.conf = configure.Configure()
        self.client = pymongo.MongoClient(self.conf.host, self.conf.port)
    
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

    def load_data(self, database_name, collection_name):
        return 0
