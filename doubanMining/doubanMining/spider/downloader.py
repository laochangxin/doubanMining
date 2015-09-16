import logging
import urllib2
import DataAgent
import threading
import configure

class Downloader(object):
    """@Brief: Download the url from the web"""
    def __init__(self, thread_num=1, seed_list=[], buffer=10000, conf_type='movie'):
        self.thread_num = thread_num
        self.seed_list = seed_list
        self.buffer = buffer
        self.url_crawled_pool = []
        self.url_ready_pool = []
        self.conf = configure.Configure()
        self.database = self.conf.conf_dict[conf_type]['url_databse']
        self.collection = self.conf.conf_dict[conf_type]['url_collection']
        self.db_handler = DataAgent.DataAgent()
        self.logger = logging.getLogger(__name__)
    thread_lock = threading.Lock()
    
    def load_seed_list(self):
        Downloader.thread_lock.acquire()
        tmp_list = self.db_handler.load_data('url_lib', self.url_type)
        Downloader.thread_lock.release()
        if len(tmp_list) > 1:
            self.seed_list = tmp_list
        
        self.logger.info('thread[%d] load seed list complete' % (thread_num))
        
    def save_data_into_database(self):
        if len(self.url_crawled_pool) >= self.buffer:
            self.db_handler.store_data(self.database, self.collection, self.url_crawled_pool)
            self.url_crawled_pool = []

    def crawl_url_data(self):
        """@Brief: Crawl url using BFS default"""
        while len(self.url_ready_pool) != 0:
            top_id = self.url_ready_pool.pop(0)
            url = self.conf.MOVIE_HOMEPAGE_URL + top_id
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                content = response.read()
            except Exception as err:
                self.logger.error('Request movie[%s] homepage error[%s]' % (top_id, err), exc_info=True)
            #TODO add neighbor movie to the url_crawled_pool
            self.url_crawled_pool.append(content)
        # random judges
        self.save_data_into_database()
        
    def download(self):
        return
        
