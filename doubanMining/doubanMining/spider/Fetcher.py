import urllib2
import os
import logging
import gzip
import StringIO
import logging
import random

import configure
import ProxyCrawler

class Fetcher(object):
    """Get url from the web"""
    def __init__(self, timeout=10, compress=True):
        self.logger = logging.getLogger(__name__)
        self.conf = configure.Configure()
        self.isCompress = compress
        self.load_proxy_pool()

    PROXY_FILE_PATH = './data/proxy.txt'
    def load_proxy_pool(self):
        self.proxy_pool = []
        proxy_file = Fetcher.PROXY_FILE_PATH
        if not os.path.exists(proxy_file):
            proxy_crawler = ProxyCrawler.ProxyCrawler()
            ret = proxy_crawler.run()
            if ret != 0:
                self.logger.warning('Proxy crawler run failed!')
        f = open(proxy_file, 'r')
        for line in open(f):
            linelist = line.strip().split('=')
            protocol, proxy = linelist
            self.proxy_pool.append((protocol, proxy))
        self.logger.info('Proxy pool count: %d' % len(self.proxy_pool))
        
    def url_fetch(self, url):
        user_agent = random.choice(self.conf.user_agents)
        headers = {
            'Uesr-Agent': user_agent,
            "Accept-Encoding": "gzip,deflate",
            "Accept-Charset" : "UTF-8,*"
            }
        pass
