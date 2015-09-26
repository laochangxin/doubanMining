﻿import threading
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
        while True:
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
                break

    def process_job(self, job_id, depth):
        """ Crawl url data from web """
        top_id = job_id
        entrance = '?from=subject-page'
        url = '%s%s/%s' % (self.conf.MOVIE_HOMEPAGE_URL, top_id, entrance)
        # Use Class Fetcher to get url content
        
        proxy_item = self.choose_a_proxy()
        fetcher = Fetcher.Fetcher(proxy_item['proxy'])
        ret_data = fetcher.url_fetch(url)
        status, reason, content = fetcher.url_fetch(url)

        if status != 200:
            if status == 404:
                result = (job_id, '', [], status, reason)
                Worker.mutex.acquire()
                self.result_queue.append(result)
                Worker.mutex.release()
                return
            else:
                retry_num = proxy_item['retry']
                if retry_num > self.conf.MAX_RETRY_NUM:
                    Worker.mutex.acquire()
                    self.proxy_slot.remove(proxy_item)
                    self.job_queue.put(job_id)
                proxy_item['retry'] += 1

        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
            content = response.read()
        except Exception as err:
            self.logger.error('Request movie[%s] url[%s] homepage error[%s]' % (top_id, url, err), exc_info=True)
            err_info = '%s' % err
            content = {'id': job_id, 'err': err_info}
            Worker.mutex.acquire()
            self.visited_set.add(top_id)
            self.result_queue.append((job_id, content, []))
            Worker.mutex.release()
            return
                
        self.download_page(top_id, content)

        neighbor_url_list = self.get_neighbor_url_list(content)
        neighbor_id_list = []
        for url in neighbor_url_list:
            id = self.extract_movie_id(url)
            if id is not None:
                neighbor_id_list.append(id)
        Worker.mutex.acquire()
        self.visited_set.add(top_id)
        self.result_queue.append((top_id, content, neighbor_id_list))
        Worker.mutex.release()
        for id in neighbor_id_list:
            self.job_queue.put((id, depth+1))
    
    def choose_a_proxy(self):
        got = False
        return_proxy = {}
        while not got:
            proxy_item = random.choice(self.proxy_slot)
            if proxy_item['using'] == False:
                Worker.mutex.acquire()
                proxy_item['using'] = True
                return_proxy = proxy_item
                Worker.mutex.release()
                got = True
        return return_proxy

    def download_page(self, top_id, content):
        Worker.mutex.acquire()
        f_path = './data/movie/%s.html' % top_id
        f_handler = open(f_path, 'w')
        try:
            f_handler.write(content)
        except Exception as err:
            self.logger.error('movie[%s] download failed[%s]' % (top_id, content), exc_info=True)
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
