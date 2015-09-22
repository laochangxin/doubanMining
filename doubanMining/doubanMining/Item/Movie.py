import json
class Movie(object):
    """
    @breif: Class of Movie, containing infomation of movie item
    @func: Provide function to output json format data
    """
    def __init__(self, movie_id, movie_title, movie_star, movie_eval_num, movie_eval_percent_list, movie_type_list, movie_production_areas, 
              movie_langs, movie_release_time, movie_tag_list):
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.movie_star = movie_star
        self.movie_eval_num = movie_eval_num
        self.movie_eval_percent_list = movie_eval_percent_list
        self.movie_type_list = movie_type_list
        self.movie_production_areas = movie_production_areas.replace(' ', '')
        self.movie_langs = movie_langs.replace(' ', '')
        self.movie_release_time = movie_release_time.replace(' ', '')
        self.movie_tag_list = movie_tag_list
        self.js_dict = {}
        
    def js_format(self):
        movie_eval_per_str = self.change_list2str(self.movie_eval_percent_list)
        movie_type_str = self.change_list2str(self.movie_type_list)
        movie_tag_str = self.change_list2str(self.movie_tag_list)
        self.js_dict = {
            "id": self.movie_id,
            "title": self.movie_title,
            "star": self.movie_star,
            "eval_num": self.movie_eval_num,
            "eval_percent": movie_eval_per_str,
            "type": movie_type_str,
            "areas": self.movie_production_areas,
            "language": self.movie_langs,
            "time": self.movie_release_time,
            "tags": movie_tag_str
            }
        result = self.js_dict
        return result

    def print_func(self):
        movie_list = self.js_dict.items()
        print '========Movie Info========'
        for ele in movie_list:
            print ele[0], ele[1]
        print '=========================='

    def change_list2str(self, input_list):
        return '/'.join(input_list)