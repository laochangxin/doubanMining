from bs4 import BeautifulSoup
import urllib2
import httplib
import threading

class ProxyCrawler(object):
    """@Brief: Crawl proxy host&port from a proxy providing web"""
    def run(self):
        of = open('./data/proxy.txt' , 'w')
        user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
        headers = {'User-Agent': user_agent}
        for page in range(1, 20):
            source_url = 'http://www.xici.net.co/nn/%s' % page
            request = urllib2.Request(source_url, headers=headers)
            html_doc = urllib2.urlopen(request).read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            trs = soup.find('table', id='ip_list').find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[2].text.strip()
                port = tds[3].text.strip()
                protocol = tds[6].text.strip()
                if protocol == 'HTTP' or protocol == 'HTTPS':
                    of.write('%s=%s:%s\n' % (protocol, ip, port) )
                    print '%s=%s:%s' % (protocol, ip, port)
        of.close()
        return 0

    f_lock = threading.Lock()
    writer = open('./data/valid_proxy.txt', 'w')
    reader = open('./data/proxy.txt', 'r')

    def get_valid_proxy(self):
        all_thread = []
        for i in range(50):
            t = threading.Thread(target=self.ping)
            all_thread.append(t)
            t.start()
        for t in all_thread:
            t.join()
        print 'success'
        ProxyCrawler.writer.close()
    
    
    def ping(self):
        url = 'http://movie.douban.com'
        while True:
            ProxyCrawler.f_lock.acquire()
            line = ProxyCrawler.reader.readline().strip()
            ProxyCrawler.f_lock.release()
            if len(line) == 0:
                break
            protocol, proxy = line.split('=')
            
            try:
                conn = httplib.HTTPConnection(proxy, timeout=3.0)
                conn.request('GET', url)
                res = conn.getresponse()
                ProxyCrawler.f_lock.acquire()
                print res.status, res.reason
                ProxyCrawler.f_lock.release()
                if res.status == 200:
                    ProxyCrawler.f_lock.acquire()
                    print protocol, proxy
                    ProxyCrawler.writer.write('%s\n' % proxy)
                    ProxyCrawler.f_lock.release()
            except Exception as err:
                print err


if __name__ == '__main__':
    proxy_crawler = ProxyCrawler()
    #proxy_crawler.run()
    print 'here'
    proxy_crawler.get_valid_proxy()
    #url = 'http://movie.douban.com'
    #conn = httplib.HTTPConnection(proxy, timeout=3.0)
    #conn.request('GET', url)
    #res = conn.getresponse()
    #content = res.read()
    #print res.status, res.reason