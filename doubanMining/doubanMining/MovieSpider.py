import sys
import datetime
import urllib2
from bs4 import BeautifulSoup

class MovieSpider(object):
    """description of class"""

    def get_nowplaying_movies(self):
        url = 'http://movie.douban.com/nowplaying/beijing/'
        content = urllib2.urlopen(url).read()
        content = content.strip('\n\r')
        self.soup = BeautifulSoup(content, 'html.parser')
        movie_list = self.soup.find('ul', 'lists')
        #print ('%s' % movie_list).decode('utf8').encode('gbk')
        movies = movie_list.find_all('li', 'list-item')
        #print movies
        print >> sys.stderr, '%s: Today\'s new movies: %d ' % (datetime.date.today(), len(movies))
        for movie_soup in movies:
            id = movie_soup.get('id')
            title = movie_soup.get('data-title')
            score = movie_soup.get('data-score')
            director = movie_soup.get('data-director')
            print '%s\t%s\t%s\t%s' % (id, title, director, score)
        
        
if __name__ == '__main__':
    spider_obj = MovieSpider()
    spider_obj.get_nowplaying_movies()