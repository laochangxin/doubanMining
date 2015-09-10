import sys
import datetime
import urllib2
import json
from bs4 import BeautifulSoup
import configure


class MovieSpider(object):
    """@brief: Crawl data from douban movie, get movies' info and store in database"""
    def __init__(self, *args, **kwargs):
        self.conf = configure.Configure()

        
    def get_nowplaying_movies(self, location):
        url = self.conf.MOVIE_NOWPLAYING_URL + location
        today = datetime.date.today()
        today_str = datetime.datetime.strftime(today, '%Y%m%d')
        return_list = []
        try:
            content = urllib2.urlopen(url).read()
        except Exception, err:
            print >> sys.stderr, 'location[%s] get nowplaying movies error[%s]' % (location, err)
        content = content.strip('\n\r')
        self.soup = BeautifulSoup(content, 'html.parser')
        movie_list = self.soup.find('ul', 'lists')
        #print ('%s' % movie_list).decode('utf8').encode('gbk')
        movies = movie_list.find_all('li', 'list-item')
        #print movies
        print >> sys.stderr, '%s: Today\'s new movies: %d ' % (today, len(movies))
        for movie_soup in movies:
            id = movie_soup.get('id')
            title = movie_soup.get('data-title')
            score = movie_soup.get('data-score')
            director = movie_soup.get('data-director')
            js_dict = {
                'id': id,
                'title': title,
                'score': score,
                'director': director,
                'day' : today_str
                }
            #js_str = json.dumps(js_dict)
            return_list.append(js_dict)
            #print '%s\t%s\t%s\t%s' % (id, title, director, score)
        return return_list

    def get_movie_info(self, movie_id):
        js_res = None
        movie_item_api = self.conf.MOVIE_INFO_API
        req = movie_item_api + movie_id
        try:
            js_str = urllib2.urlopen(req).read()
        except Exception, err:
            print >> sys.stderr, 'movie_id[%s] info get error[%s]' % (movie_id, err)
        js_res = json.loads(js_str, 'utf8')
        return js_res

    def parse_movie_homepage(self, movie_id):
        url = self.conf.MOVIE_HOMEPAGE_URL + movie_id
        try:
            content = urllib2.urlopen(url).read()
        except:
            print >> sys.stderr, 'error'
        return

    def crawl_movies_data(self, movies_pool):
        return
    
    def store_data_into_db(self):
        return 
       
if __name__ == '__main__':
    a_spider = MovieSpider()
    a_spider.get_nowplaying_movies('shenzhen')
    js_res = a_spider.get_movie_info('1292001')
    print js_res