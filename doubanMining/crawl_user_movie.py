import sys
import json
import time
import types
import urllib2

from bs4 import BeautifulSoup

# TODO: Exchange codes into Class
# TODO: Replace urllib by httplib
# TODO: Add "try except" control flow
# TODO: Put global variables into "configure.py"

USER_COLLECT_PREFIX = 'http://movie.douban.com/people'
USER_COLLECT_POSTFIX = 'collect?start=15&sort=time&rating=all&filter=all&mode=grid'
MOVIE_PREFIX = 'http://movie.douban.com/subject/'

def crawl_user_movie(user_id):
    movie_id_list = []
    delta = 0
    while True:
        postfix = 'collect?start=%s&sort=time&rating=all&filter=all&mode=grid' % delta
        url = '%s/%s/%s' % (USER_COLLECT_PREFIX, user_id, postfix)
        content = urllib2.urlopen(url).read()
        ret = crawl_single_page(content, movie_id_list)
        if ret == -1:
            break
        delta += 15
        time.sleep(1)
        print len(movie_id_list)
    print movie_id_list

def crawl_single_page(content, movie_id_list):
    soup = BeautifulSoup(content, 'html.parser')
    article = soup.find('div', class_='article')
    movie_cards = article.find_all('div', class_='item')
    if len(movie_cards) == 0:
        return -1
    for card in movie_cards:
        title = card.find('li', class_='title')
        link = title.a['href']
        link = link.strip('/')
        movie_id = link.replace(MOVIE_PREFIX, '')
        if movie_id.isdigit():
            movie_id_list.append(movie_id)
    return 0

def crawl_user_tags(user_id):
    tag_list = []
    url = '%s/%s/collect' % (USER_COLLECT_PREFIX, user_id)
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    tag_soup_list = soup.find_all('li', class_='clearfix')
    for item in tag_soup_list:
        tag = item.a.text
        count = item.span.text
        tag_list.append((tag, count))

    # It exists a open-tag button if there are too many tags.
    extra_tag_button = soup.find('a', id='open_tags')
    if type(extra_tag_button) != types.NoneType:
        extra_link_prefix = 'http://movie.douban.com/j/people'
        extra_link_postfix = 'get_collection_tags?offset=90&tags_sort=count&cat_id=1002&action=collect'
        extra_link_url = '%s/%s/%s' % (extra_link_prefix, user_id, extra_link_postfix)
        result = urllib2.urlopen(extra_link_url).read()
        js_result = json.loads(result)
        for item in js_result:
            tag_list.append((item['tag'], item['count']))
        
    for ele in tag_list:
        print ele[0].encode('gbk'), str(ele[1])

if __name__ == '__main__':
    #f = open('my_collect', 'r')
    #content = f.readlines()
    #content = ''.join(content)
    #crawl_single_page(content)

    user_id = 'Jericho'
    user_id = '53675879'
    crawl_user_tags(user_id)
    #crawl_user_movie(user_id)
