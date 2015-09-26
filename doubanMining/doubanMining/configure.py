class Configure(object):
    """common conf & common var"""
    def __init__(self, *args, **kwargs):
        """database conf"""
        self.host = 'localhost'
        self.port = 27017
        self.database = 'douban_info'

        """movie info"""
        self.movie_collection = 'movie_collection'
        self.MOVIE_INFO_PREURL = 'http://movie.douban.com/subject/'
        self.MOVIE_INFO_API = 'http://api.douban.com/v2/movie/subject/'
        self.MOVIE_NOWPLAYING_URL = 'http://movie.douban.com/nowplaying/'
        self.MOVIE_HOMEPAGE_URL = 'http://movie.douban.com/subject/'

        """configure for crawler"""
        self.conf_dict = {
            'movie': {
                'url_database': self.database,
                'url_collection': 'movieid_all_content'
                },
            'user': {
                'url_database': self.database,
                'url_collection': 'userid_all_content'
                }
            }

        """user-agents to pretend browser"""
        self.user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                    ]

        self.check_url = 'http://movie.douban.com'
        self.MAX_RETRY_NUM = 3