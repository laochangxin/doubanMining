class Configure(object):
    """common conf & common var"""
    def __init__(self, *args, **kwargs):
        """ database conf """
        self.host = 'localhost'
        self.port = 27017
        self.database = 'douban'

        """ movie info """
        self.movie_collection = 'movie_collection'
        self.MOVIE_INFO_PREURL = 'http://movie.douban.com/subject/'
        self.MOVIE_INFO_API = 'http://api.douban.com/v2/movie/subject/'
        self.MOVIE_NOWPLAYING_URL = 'http://movie.douban.com/nowplaying/'
