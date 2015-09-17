class Configure(object):
    """common conf & common var"""
    def __init__(self, *args, **kwargs):
        """database conf"""
        self.host = 'localhost'
        self.port = 27017
        self.database = 'douban'

        """movie info"""
        self.movie_collection = 'movie_collection'
        self.MOVIE_INFO_PREURL = 'http://movie.douban.com/subject/'
        self.MOVIE_INFO_API = 'http://api.douban.com/v2/movie/subject/'
        self.MOVIE_NOWPLAYING_URL = 'http://movie.douban.com/nowplaying/'
        self.MOVIE_HOMEPAGE_URL = 'http://movie.douban.com/subject/'

        """configure for crawler"""
        self.conf_dict = {
            'movie': {
                'url_database': 'url_lib',
                'url_collection': 'url_movie_collection'
                },
            'user': {
                'url_database': 'url_lib',
                'url_collection': 'url_user_collection'
                }
            }