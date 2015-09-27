import re
import copy
import time
import datetime
import logging
import urllib2
import httplib
import threading
import Queue
from bs4 import BeautifulSoup

import configure
import DataAgent
import Worker
import ProxyCrawler

class Downloader(object):
    """@Brief: Download the url from the web.
    Using multi-thread to fetch pages from the web.
    Class Downloader is equal to a thread-handler.
    Class Worker is the real thread class object to execute tasks.
    """
    thread_lock = threading.Lock()
    checker_lock = threading.Lock()
    PROXY_FILE_PATH = './data/valid_proxy.txt'
    
    
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

    def init_run(self):
        seed_id_list = self.load_seed_list()
        neighbor_list = []
        for id in seed_id_list:
            cur_neighbor_list = self.get_seed_neighbor(id)
            neighbor_list += cur_neighbor_list
            self.visited_set.add(id)
        self.url_ready_pool = list(set(neighbor_list))
        if len(self.url_ready_pool) == 0:
            self.logger.warning('Url ready pool get nothing')
        for id in self.url_ready_pool:
            self.request_queue.put((id, 0))

    def run(self):
        start_time = datetime.datetime.now()
        self.load_proxy_slot()
        self.check_proxy_validation()
        self.init_run()
        self.logger.info('Downloader start running, thread number is %s', self.thread_num)
        for x in range(self.thread_num):
            worker = Worker.Worker(self.conf, self.proxy_slot, self.request_queue,
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
                self.logger.info('%s\t%s' % ('The id list that going to be stored in database',
                                             ','.join([ele[0] for ele in buffer2database])))
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

    def get_seed_neighbor(self, seed_id):
        neighbor_list = []
        try:
            neighbor_list = self.db_handler.get_neighbor_list(self.database, self.collection, seed_id)
        except Exception as err:
            self.logger.error('Get seed neighbor error[%s]' % err, exc_info=True)
        return neighbor_list

    def save_data_into_database(self, buffer2databse):
        js_dict = {}
        dup_set = set([])
        for ele in buffer2databse:
            if len(ele) != 3:
                continue
            if ele[0] in dup_set:
                continue
            dup_set.add(ele[0])
            js_dict['id'] = ele[0]
            js_dict['content'] = ele[1]
            js_dict['neighbor_list'] = ele[2]
            self.logger.info('id: %s' % ele[0])
            self.db_handler.store_data(self.database, self.collection, js_dict)
        
    def load_proxy_slot(self):
        self.proxy_slot = []
        proxy_file = Downloader.PROXY_FILE_PATH
        if not os.path.exists(proxy_file):
            proxy_crawler = ProxyCrawler.ProxyCrawler()
            ret = proxy_crawler.run()
            if ret != 0:
                self.logger.warning('Proxy crawler run failed!')
            proxy_crawler.get_valid_proxy()

        f = open(proxy_file, 'r')
        for line in open(f):
            linelist = line.strip().split('=')
            protocol, proxy = linelist
            item = {
                'proxy': proxy,
                'ocupied': False
                }
            self.proxy_slot.append(item)
        self.logger.info('Proxy slot count: %d' % len(self.proxy_slot))

    def check_proxy_validation(self):
        check_url = self.conf.check_url
        for proxy_item in self.proxy_slot:
            proxy = proxy_item['proxy']
            try:
                conn = httplib.HTTPConnection(proxy, timeout=3.0)
                conn.request('GET', url)
                res = conn.getresponse()
            except Exception as err:
                self.logger.error('proxy[%s] connection error[%s]' % (proxy, err))
            self.logger.info('proxy connection status[%s]: %s' % (proxy, res.status, res.reason))

if __name__ == '__main__':
    instance = Downloader()
    instance.run()
