import threading
import time
import random
import re
import logging
import urllib2
import httplib
from bs4 import BeautifulSoup

import configure
import Fetcher

class Worker(threading.Thread):
    """@Brief: the object that execute tasks"""
    
    # static variables of Worker
    mutex = threading.Lock()

    def __init__(self, conf_var, proxy_slot, job_queue, visited_set, result_queue):
        self.conf = conf_var
        self.proxy_slot = proxy_slot
        self.job_queue = job_queue
        self.visited_set = visited_set
        self.result_queue = result_queue
        self.method = 'BFS'
        self.logger = logging.getLogger(__name__)
        threading.Thread.__init__(self)

    def set_method(self, method='BFS', depth=10):
        """ Default 'BFS', can use 'DFS' and suppose to set depth threshold """
        self.method = method
        if self.method == 'DFS':
            self.depth = depth

    def run(self):
        self.logger.info('Running...')
        if self.method == 'BFS':
            self.run_by_BFS()
        elif self.method == 'DFS':
            self.run_by_DFS()
        
    def run_by_BFS(self):
        counter = 0
        while True:
            counter += 1
            if counter % 10 == 0:
                s_time = random.randint(1, 10)
                time.sleep(s_time)
            if self.job_queue.qsize() > 0:
                job_id, depth = self.job_queue.get()
                Worker.mutex.acquire()
                #self.logger.info('visited set: %s' % self.visited_set)
                #print ','.join([ele[0] for ele in self.result_queue])
                #time.sleep(10)
                if job_id in self.visited_set:
                    Worker.mutex.release()
                    continue
                else:
                    Worker.mutex.release()
                    self.process_job(job_id, depth)
            else:
                self.logger.info('Thread break loop')
                break

    def process_job(self, job_id, depth):
        """ Crawl url data from web """
        entrance = '?from=subject-page'
        url = '%s%s/%s' % (self.conf.MOVIE_HOMEPAGE_URL, job_id, entrance)
        
        # Use Class Fetcher to get url content
        proxy_item = self.choose_a_proxy()
        fetcher = Fetcher.Fetcher(proxy_item['proxy'], compress=False)
        ret_data = fetcher.url_fetch(url)
        status, reason, content = fetcher.url_fetch(url)
        #self.logger.info('proxy: %s' % proxy_item)
        Worker.mutex.acquire()
        proxy_item['occupied'] = False
        Worker.mutex.release()
        self.logger.info('proxy[%s] status[%s] content_len[%d]' % (proxy_item['proxy'], status, len(content)))
        if status != 200:
            result = (job_id, '', [], status, reason)
            Worker.mutex.acquire()
            self.visited_set.add(job_id)
            self.result_queue.append(result)
            Worker.mutex.release()
            return
        
        self.download_page(job_id, content)

        neighbor_url_list = self.get_neighbor_url_list(content)
        neighbor_id_list = []
        for url in neighbor_url_list:
            id = self.extract_movie_id(url)
            if id is not None:
                neighbor_id_list.append(id)
        Worker.mutex.acquire()
        self.visited_set.add(job_id)
        self.result_queue.append((job_id, content, neighbor_id_list, status, reason))
        Worker.mutex.release()
        for id in neighbor_id_list:
            self.job_queue.put((id, depth+1))                
            
    def choose_a_proxy(self):
        got = False
        return_proxy = {}
        while not got:
            proxy_item = random.choice(self.proxy_slot)
            if proxy_item['occupied'] == False:
                Worker.mutex.acquire()
                proxy_item['occupied'] = True
                return_proxy = proxy_item
                Worker.mutex.release()
                got = True
        return return_proxy

    def download_page(self, job_id, content):
        Worker.mutex.acquire()
        f_path = './data/movie/%s.html' % job_id
        f_handler = open(f_path, 'w')
        try:
            f_handler.write(content)
        except Exception as err:
            self.logger.error('movie[%s] download failed[%s]' % (job_id, content), exc_info=True)
        finally:
            f_handler.close()
            Worker.mutex.release()

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
