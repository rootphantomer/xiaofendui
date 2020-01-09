# -*- coding: utf-8 -*-
import logging
import crawler
from bs4 import BeautifulSoup
from crawler.post import PostDetail

#0818团URL
BASE_URL='http://www.0818tuan.com'
FIRST_URL='http://www.0818tuan.com/list-1-0.html'

class Zero818Crawler(object):
    def __init__(self):
        pass
    def crawler(self):
        post_list = []
        logging.info('Crawl url: ' + FIRST_URL)
        result1 = crawler.get_resp(FIRST_URL)
        tag_a = BeautifulSoup(result1.text,features='html.parser')
        contents = tag_a.find(id='redtag').contents
        for x in range(len(contents)-1,-1,-1):
            if contents[x] == '\n':
                contents.pop(x)
        return contents