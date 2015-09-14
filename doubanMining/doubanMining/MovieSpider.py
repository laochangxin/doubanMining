import sys
import datetime
import urllib2
import json
from bs4 import BeautifulSoup
import configure
import logging
#from Item.Movie import Movie


class MovieSpider(object):
    """@brief: Crawl data from douban movie, get movies' info and store in database"""
    def __init__(self, *args, **kwargs):
        self.conf = configure.Configure()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Generate a movie spider')
        
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
        soup = BeautifulSoup(content, 'html.parser')
        movie_list = self.soup.find('ul', 'lists')
        movies = movie_list.find_all('li', 'list-item')
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
                'day': today_str,
                'location': location
                }
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
        request = urllib2.Request(url)
        movie_eval_foo = lambda a: a.has_attr('property') and a['property'] == 'v:votes'
        movie_type_foo = lambda a: a.has_attr('property') and a['property'] == 'v:genre'
        movie_release_foo = lambda a: a.has_attr('property') and a['property'] == 'v:initialReleaseDate'

        try:
            response = urllib2.urlopen(request)
            content = response.read()
        except Exception, err:
            self.logger.error('Parse movie[%s] homepage error[%s]' % (movie_id, err), exc_info=True)
            #print >> sys.stderr, 'error'
        soup = BeautifulSoup(content, 'html.parser')
        # Note: all data below in UNICODE type
        movie_title = '%s' % soup.h1.span.string
        movie_star = '%s' % soup.strong.string
        movie_eval_num = '%s' % soup.find(movie_eval_foo).string
        movie_eval_percent_list = self.get_percent_list(soup, movie_id)
        movie_type_list = ['%s' % ele.string for ele in soup.find_all(movie_type_foo)]
        movie_production_areas = self.get_production_areas(soup, movie_id)
        movie_langs = self.get_movie_lang(soup, movie_id)
        movie_release_time = '/'.join([ele.string for ele in soup.find_all(movie_release_foo)])
        movie_tag_list = self.get_tag_list(soup, movie_id)
        self.logger.info(movie_title)
        self.logger.info(movie_star)
        self.logger.info(movie_eval_num)
        self.logger.info(movie_production_areas)
        self.logger.info(movie_langs)
        self.logger.info(movie_release_time)
        #this_movie = Movie.Movie(movie_title, movie_star, movie_eval_num, movie_production_areas, 
        #      movie_langs, movie_release_time)

    def get_tag_list(self, soup, movie_id):
        tag_list = soup.find(class_ = 'tags-body').find_all('a')
        try:
            return_list = ['%s' % ele.string for ele in tag_list]
        except Exception, err:
            self.logger.error('Movie[%s] cannot get tags' % movie_id, exc_info = True)
        return return_list

    def get_percent_list(self, soup, movie_id):
        prefix_div_list = soup.find_all(class_ = 'power')
        return_list = ['%s' % ele.next_sibling.strip()
                       for ele in prefix_div_list]
        if return_list == [] or len(return_list) != 5:
            self.logger.warning('Cannot get movie[%s] percent_list' % movie_id)
        return return_list

    def get_production_areas(self, soup, movie_id):
        keyword= u'\u5236\u7247\u56fd\u5bb6/\u5730\u533a:' # Chinese: Zhi Pian Guo Jia / Di Qu
        foo = lambda a: a.has_attr('id') and a['id'] == 'info'
        result = soup.find(foo)
        content_iter = result.contents
        for x in range(len(content_iter) - 2):
            if content_iter[x].string == keyword:
                return content_iter[x + 1].strip()
        self.logger.warning('Cannot get production[%s] areas' % movie_id)
        return 'None'

    def get_movie_lang(self, soup, movie_id):
        keyword = u'\u8bed\u8a00:'
        foo = lambda a: a.has_attr('id') and a['id'] == 'info'
        result = soup.find(foo)
        content_iter = result.contents
        for x in range(len(content_iter) - 2):
            if content_iter[x].string == keyword:
                return content_iter[x + 1].strip()
        self.logger.warning('Cannot get movie[%s] language' % movie_id)
        return 'None'

    def crawl_movies_data(self, movies_pool):
        return
    
if __name__ == '__main__':
    a_spider = MovieSpider()
    a_spider.parse_movie_homepage('10727641')
    #a_spider.get_nowplaying_movies('shenzhen')
    #js_res = a_spider.get_movie_info('1292001')
    #print js_res