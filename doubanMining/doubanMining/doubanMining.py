import urllib2
import os
import MovieSpider
import configure
import DataAgent

def main():
    conf = configure.Configure()
    a_spider = MovieSpider.MovieSpider()
    movie_list = a_spider.get_nowplaying_movies('shenzhen')
    #js_res = a_spider.get_movie_info('1292001')
    data_agent = DataAgent.DataAgent()
    print movie_list, len(movie_list)
    #data_agent.store_data(conf.database, conf.movie_collection, movie_list)
    return

if __name__ == '__main__':
    main()
