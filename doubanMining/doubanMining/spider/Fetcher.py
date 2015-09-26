import os
import random
import logging
import gzip
import StringIO
import logging
import urllib2
import httplib

import configure
import ProxyCrawler

class Fetcher(object):
    """Get url from the web"""
    def __init__(self, proxy, timeout=3.0, compress=True):
        self.logger = logging.getLogger(__name__)
        self.conf = configure.Configure()
        self.proxy = proxy
        self.isCompress = compress
    
    def url_fetch(self, url):
        """
        @Brief
        Fetch url content
        Add User-Agent to pretend browser
        Add gzip to compress response content
        Use proxy to avoid being blocked
       
        @Return
        Return a tuple containing status, reason and content.
        status: response status(e.g. 200, 403, 404, 500)
        reason: response reason(e.g. 'OK', 'Forbidden')
        content: response content of url if status == 200
        """
        user_agent = random.choice(self.conf.user_agents)
        headers = {
            'Uesr-Agent': user_agent,
            "Accept-Encoding": "gzip,deflate",
            "Accept-Charset" : "UTF-8,*"
            }
        try:
            conn = httplib.HTTPConnection(self.proxy, timeout=3.0)
            conn.request('GET', url, None, headers)
            response = conn.getresponse()
        except Exception as err:
            self.logger.error('connect error[%s]' % err)
            return '999', 'Request failed', ''
            
        content = ''
        if response.status == '200':
            raw_data = response.read()
            stream = StringIO.StringIO(raw_data)
            decompressor = gzip.GzipFile(fileobj=stream)
            content = decompressor.read()

        conn.close()
        return response.status, response.reason, content