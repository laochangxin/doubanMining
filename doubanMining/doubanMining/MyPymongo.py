import pymongo

class MyPymongo:
    """NoSql for storing data"""
    def __init__(self, host, port):
        try:
            self.conn = pymongo.connection(host, port)
        except:
            print 'connect to %s:%s failed' % (host, port)
            exit(0)
    
    def __del__(self):
        self.conn.close()

    def init_database(self):
        conn = pymongo.connection('localhost', 27017)

