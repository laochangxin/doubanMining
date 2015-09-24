from bs4 import BeautifulSoup
import urllib2
import httplib

class ProxyCrawler(object):
    """@Brief: Crawl proxy host&port from a proxy providing web"""
    def run(self):
        of = open('proxy.txt' , 'w')
        for page in range(1, 10):
            html_doc = urllib2.urlopen('http://www.xici.net.co/nn/' + str(page) ).read()
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

if __name__ == '__main__':
#    proxy_crawler = ProxyHandler()
#    proxy_crawler.run()
    proxy_list = []
    for line in open('proxy.txt', 'r'):
        linelist = line.strip().split('=')
        proxy_list.append((linelist[0], linelist[1]))

    url = 'http://movie.douban.com/subject/1292063/?from=subject-page'
    for protocol, proxy in proxy_list:
        try:
            conn = httplib.HTTPConnection(proxy, timeout=3.0)
            conn.request('GET', url)
            res = conn.getresponse()
            content = res.read()
            writer = open('./data/proxy/%s.html' % proxy.split(':')[0], 'w')
            writer.write(content)
            writer.close()
        except Exception as err:
            print err
