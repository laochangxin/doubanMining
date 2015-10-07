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
        if self.isCompress == True:
            headers = {
                'Uesr-Agent': user_agent,
                "Accept-Encoding": "gzip,deflate",
                "Accept-Charset" : "UTF-8,*"
                }
        else:
            headers = {
                'Uesr-Agent': user_agent,
                "Accept-Charset" : "UTF-8,*"
                }
        raw_data = ''
        try:
            conn = httplib.HTTPConnection(self.proxy, timeout=3.0)
            conn.request('GET', url, None, headers)
            response = conn.getresponse()
            raw_data = response.read()
        except Exception as err:
            self.logger.error('connect error[%s]' % err)
            return '999', 'Request failed', ''
        finally:
            conn.close()
            
        content = ''
        if self.isCompress == True:
            if response.status == 200:
                try:
                    stream = StringIO.StringIO(raw_data)
                    decompressor = gzip.GzipFile(fileobj=stream)
                    content = decompressor.read()
                except:
                    self.logger.error('status[%s] len_raw_data[%d]' % (response.status, len(raw_data)))
                    return '998', 'content err', ''
        else:
            if response.status == 200:
                content = raw_data            

        return response.status, response.reason, content

if __name__ == '__main__':
    proxy = '180.166.112.47:8888'
    url = 'http://movie.douban.com/subject/25710912/?from=showing'
    fetcher = Fetcher(proxy)
    result = fetcher.url_fetch(url)
    print result[0], result[1], len(result[2])