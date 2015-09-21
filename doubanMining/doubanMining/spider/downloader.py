import re
import copy
import time
import datetime
import logging
import urllib2
import threading
import Queue
from bs4 import BeautifulSoup

import configure
import DataAgent
import Worker

class Downloader(object):
    """@Brief: Download the url from the web.
    Using multi-thread to fetch pages from the web.
    Class Downloader is equal to a thread-handler.
    Class Worker is the real thread class object to execute tasks.
    """
    thread_lock = threading.Lock()
    checker_lock = threading.Lock()
    
    
    def __init__(self, thread_num=1, seed_list=[], buffer=10000, conf_type='movie'):
        self.thread_num = thread_num

        self.buffer = buffer
        self.url_crawled_pool = []
        self.url_ready_pool = []
        self.request_queue = Queue.Queue()
        self.visited_set = set([])

        self.conf = configure.Configure()
        self.database = self.conf.conf_dict[conf_type]['url_database']
        self.collection = self.conf.conf_dict[conf_type]['url_collection']
        self.db_handler = DataAgent.DataAgent()
        
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        start_time = datetime.datetime.now()
        self.url_ready_pool = self.load_seed_list()
        if len(self.url_ready_pool) == 0:
            self.logger.warning('Url pool get nothing')

        for ele in self.url_ready_pool:
            self.request_queue.put((ele, 0))
        self.logger.debug('Downloader start running, thread number is %s', self.thread_num)

        for x in range(self.thread_num):
            worker = Worker.Worker(self.conf, self.request_queue,
                                 self.visited_set, self.url_crawled_pool)
            worker.start()
        time.sleep(10)
        # TODO: timer to avoid thread death
        # DONE: timer to store data into database
        while not self.request_queue.empty():
            time_now = datetime.datetime.now()
            delta = time_now - start_time
            if delta.seconds % 10 == 0:
                self.logger.info("Running for %s seconds" % delta.seconds)
                Worker.Worker.mutex.acquire()
                buffer2database = copy.deepcopy(self.url_crawled_pool)
                self.logger.info(','.join([ele[0] for ele in buffer2database]))
                while len(self.url_crawled_pool) != 0:
                    self.url_crawled_pool.pop(0)
                Worker.Worker.mutex.release()
                self.save_data_into_database(buffer2database)
                time.sleep(1)
        
    def load_seed_list(self):
        id_list = []
        try:
            id_list = self.db_handler.load_data_id(self.database, self.collection)
        except Exception as err:
            self.logger.error('Load seed list error[%s]' % err, exc_info=True)

        self.logger.info('Load seed list complete')
        return id_list
        
    def save_data_into_database(self, buffer2databse):
        js_dict = {}
        for ele in buffer2databse:
            js_dict['id'] = ele[0]
            js_dict['content'] = ele[1]
        self.db_handler.store_data(self.database, self.collection, js_dict)

if __name__ == '__main__':
    instance = Downloader()
    instance.run()
