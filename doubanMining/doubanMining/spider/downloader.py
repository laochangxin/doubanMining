import re
import logging
import urllib2
import threading
from bs4 import BeautifulSoup

import configure
import DataAgent


class Downloader(object):
    """@Brief: Download the url from the web"""
    thread_lock = threading.Lock()
    checker_lock = threading.Lock()

    def __init__(self, thread_num=1, seed_list=[], buffer=10000, conf_type='movie'):
        self.thread_num = thread_num
        self.seed_list = seed_list

        self.buffer = buffer
        self.url_crawled_pool = []
        self.url_ready_pool = []
        self.url_ready_pool_checker = set([])

        self.conf = configure.Configure()
        self.database = self.conf.conf_dict[conf_type]['url_databse']
        self.collection = self.conf.conf_dict[conf_type]['url_collection']
        self.db_handler = DataAgent.DataAgent()
        
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        self.url_ready_pool = self.load_seed_list()
        if len(url_ready_pool) == 0:
            self.logger.warning('Url pool get nothing')
        self.logger.debug('Downloader start running...')
        self.crawl_url_data(self.thread_num)
        # TODO: Thread running need JOIN operation to wait for threads' completion

    def load_seed_list(self):
        Downloader.thread_lock.acquire()
        try:
            tmp_list = self.db_handler.load_data(self.database, self.collection)
        except Exception as err:
            self.logger.error('Thread[%d] load seed list error[%s]' % (thread_num, err), exc_info=True)
        finally:
            Downloader.thread_lock.release()
        if len(tmp_list) > 1:
            self.seed_list = tmp_list
        self.logger.info('thread[%d] load seed list complete' % (thread_num))
        
    def save_data_into_database(self):
        if len(self.url_crawled_pool) >= self.buffer:
            self.db_handler.store_data(self.database, self.collection, self.url_crawled_pool)
            self.url_crawled_pool = []

    def crawl_url_data(self, num):
        """@Brief: Crawl url using BFS by default"""
        # TODO: While using BFS, the depth of BFS should be considered to avoid being trapped
        while len(self.url_ready_pool) != 0:
            top_id = self.url_ready_pool.pop(0)
            url = self.conf.MOVIE_HOMEPAGE_URL + top_id
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                content = response.read()
            except Exception as err:
                self.logger.error('Request movie[%s] homepage error[%s]' % (top_id, err), exc_info=True)
            self.download_page(top_id, content)
           
            #TODO: add neighbor movie to the url_crawled_pool
            neighbor_url_list = self.get_neighbor_url_list(content)
            neighbor_id_list = []
            for url in neighbor_url_list:
                id = self.extract_movie_id(url)
                if id is not None:
                    neighbor_id_list.append(id)
            self.update_ready_pool(neighbor_id_list)
            self.url_crawled_pool.append(top_id)

        # random judges
        self.save_data_into_database()
    
    def update_ready_pool(self, to_add_list):
        for id in to_add_list:
            if id in self.url_ready_pool_checker:
                continue
            Downloader.checker_lock.acquire()
            try:
                self.url_ready_pool_checker.add(id)
                self.url_ready_pool.append(id)
            finally:
                Downloader.checker_lock.release()     

    def download_page(self, top_id, content):
        f_path = './data/movie/%s.html' % top_id
        f_handler = open(f_path, 'w')
        try:
            f_handler.write(content)
        except Exception as err:
            self.logger.error('movie[%s] download failed[%s]' % (top_id, content), exc_info=True)
        finally:
            f_handler.close()   

    def get_neighbor_url_list(self, content):
        return_list = []
        soup = BeautifulSoup(content, 'html.parser')
        recommend_class = soup.find(class_='recommendations-bd')
        item_list = recommend_class.find_all('dd')
        try:
            for item in item_list:
                movie_url = item.a['href']
                return_list.append(movie_url)
        except Exception as err:
            self.logger.error('Get neighbor_list Error[%s]' % err, exc_info=True)        
        return return_list

    def extract_movie_id(self, url):
        movie_id = None
        pattern = re.compile(r'https?://movie\.douban\.com/subject/(.+)/.*')
        m = pattern.match(url)
        if m:
            movie_id = m.group(1)
        return movie_id