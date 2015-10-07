# -*- coding: utf-8 -*-
import os
import json
import pymongo
import logging
import logging.config

import MovieParser
import configure
import DataAgent
import spider.Downloader

def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
        """Setup logging configuration"""
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

def main():
    conf = configure.Configure()
   
    '''download all movies from the web'''
    #downloader = spider.Downloader.Downloader(thread_num=10)
    #downloader.run()
    #downloader.load_proxy_slot()

    '''test MovieParser'''
    movie_parser = MovieParser.MovieParser()
    client = pymongo.MongoClient()
    collection = client.douban_info.movieid_all_content
    tester = None
    for ele in collection.find():
        if ele['status'] == 200:
            tester = ele['content']
            res = movie_parser.parse_movie_homepage(tester)
    

    #a_spider = MovieSpider.MovieSpider()
    #a_spider.parse_movie_homepage('10727641')
    #a_spider.parse_movie_homepage('25885212')
    #a_spider.parse_movie_homepage('1291546')
    
    #movie_list = a_spider.get_nowplaying_movies('shenzhen')
    #js_res = a_spider.get_movie_info('1292001')
    #data_agent = DataAgent.DataAgent()
    #print movie_list, len(movie_list)
    #data_agent.store_data(conf.database, conf.movie_collection, movie_list)
    return

if __name__ == '__main__':
    setup_logging('logging.json')
    #logging.config.dictConfig(
    logger = logging.getLogger(__name__)
    logger.info('Hello, this is main')
    main()
