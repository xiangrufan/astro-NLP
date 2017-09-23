# -*- coding: UTF-8 -*-
import sys
import time
import re
import requests
import numpy as np
from bs4 import BeautifulSoup
import _pickle as pickle
from importlib import reload
'''
A simple crawler for downloading all douban topics from one given douban page
'''
def topic_crawler(topic_url):
    topic_content = requests.get(topic_url).content
    topic_text = topic_content.decode('utf-8')
    posts_soup = BeautifulSoup(topic_text, "lxml")
    tmp_blob = posts_soup.findAll('div', {'class': 'topic-content'})
    first_floor = [tmp for tmp in tmp_blob if 'clearfix' not in tmp['class']]
    return first_floor[0].find('p').text
def store_result(topic_list):
    with open("topic_list.db","wb") as file:
        pickle.dump(topic_list, file)
douban_url = 'https://www.douban.com/group/sz-love/'
time.sleep(np.random.rand() * 5)
content = requests.get(douban_url).content
main_page_text = content.decode('utf-8')
topics_soup = BeautifulSoup(main_page_text,"lxml")
all_topic =topics_soup.findAll('a',{'href':re.compile('.*topic.*'),'class':""})
topic_filtered = [topic for topic in all_topic if not topic.parent.find('img',{'alt':re.compile('.置顶.')}) and topic.has_attr('class')]
topic_list = []
for topic in topic_filtered:
    time.sleep(np.random.rand() * 5)
    topic_address = topic['href']
    topic_title = topic['title']
    try:
        topic_text = topic_crawler(topic_address)
    except:
        topic_text = ""
    topic = [topic_title,topic_text]
    topic_list.append(topic)
    print(topic_title+'\n'+topic_text)
    print('----------')
store_result(topic_list)





