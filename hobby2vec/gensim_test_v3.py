import gensim
import numpy as np
from gensim.models import word2vec
import jieba
from TextSta_v2 import TextSta
from gensim.corpora.dictionary import Dictionary
import os
import _pickle as pickle
import jieba.posseg as psg

folder_path = u"C:\\Users\\xiangrufan\\Desktop\\NLP\\Astro_NLP\\resource\\复旦分类语料\\answer"
path_list = []
for genre in os.listdir(folder_path):
    genre_path = folder_path+'\\'+genre
    for file in os.listdir(genre_path):
        file_path = genre_path+'\\'+file
        path_list.append(file_path)

whole_list = []

for index in [""]+[str(i) for i in range(3,14)]:
    with open(u".\\astrology_spider\\topic_list{:s}.db".format(str(index)),"rb") as file:
        topic_list =pickle.load(file)
        out = ""
        for line in topic_list:
            for part in line:
                out =  out+part
        # out = [""+item[0] for topic in topic_list for item in topic]

        # whole_list.extend(topic_list)
        word_list = psg.lcut(out)
        whole_list.extend(word_list)

word_list = [tmp.word for tmp in whole_list]
word2type_dict = {}
for pair in whole_list:
    if pair.word not in word2type_dict.keys():
        word2type_dict[pair.word] = pair.flag
    elif word2type_dict[pair.word] == pair.flag:
        pass
    else:
        word2type_dict[pair.word] = pair.flag + ' ' + word2type_dict[pair.word]

model = word2vec.Word2Vec()
model.sort_vocab()
model.build_vocab([word_list])
key_word_list = ['白羊','金牛','双子','巨蟹','狮子','处女','天秤','天蝎','射手','摩羯','水瓶','双鱼']
for sign in key_word_list:
    try:
        pred_relation = model.similar_by_word(sign,40)
        all_top_noun = [tmp[0] for tmp in pred_relation if word2type_dict[tmp[0]] == 'n']
        pred_relation_show = all_top_noun[:3]
        print ('the sign {:s}is most related with following word'.format(sign), pred_relation_show)
    except:
        print ('{:s} is not found'.format(sign))
        # todo Add frequency screener

# model = word2vec.Word2Vec(tmp_dic, size=10)  # 默认window=5