# -*- coding: utf-8 -*-
import os
import json
import logging
import logging.config
import MovieSpider
import configure
import DataAgent

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
    a_spider = MovieSpider.MovieSpider()
    #a_spider.parse_movie_homepage('10727641')
    #a_spider.parse_movie_homepage('25885212')
    a_spider.parse_movie_homepage('1291546')
    
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
