import gensim
import numpy as np
from gensim.models import word2vec
import jieba
from TextSta_v2 import TextSta
from gensim.corpora.dictionary import Dictionary
import os
import _pickle as pickle
import jieba.posseg as psg


class document():
    def __init__(self,text):
        self.text = text
        self.word_pos_list = psg.lcut(text)
    @property
    def word_list(self):
        return [tmp.word for tmp in self.word_pos_list]
    @property
    def pos_list(self):
        return [tmp.pos for tmp in self.word_pos_list]

class document_list():
    def __init__(self):
        self.all_docs = []
        return
    def add_list(self,document_obj):
        self.all_docs.append(document_obj)
    def get_TF(self,word):
        TF = 0
        for doc in self.all_docs:
            word_count = doc.word_list.count(word)
            TF += word_count
        return TF
    def get_IDF(self,word):
        nt = 0
        N = len(self.all_docs)
        for doc in self.all_docs:
            if word in doc.word_list:
                nt +=1
        return np.log(N/(1+nt))
    def get_TFIDF(self,word):
        return self.get_TF(word)*self.get_IDF(word)

def normalize(nparrayx):
    return (nparrayx - np.min(nparrayx) )/ (np.max(nparrayx) - np.min(nparrayx))

whole_list = []
# TODO reorganize the whole code in oop pattern
all_docs = document_list()
for index in [""]+[str(i) for i in range(3,14)]:
    with open(u".\\astrology_spider\\topic_list{:s}.db".format(str(index)),"rb") as file:
        topic_list =pickle.load(file)
        out = ""
        for topic in topic_list:
            topic_text = ""
            for part in topic:
                out =  out+part
                topic_text = topic_text + part
                all_docs.add_list(document(topic_text))
        word_list = psg.lcut(out) # cut the whole document with all topics concatenated together
        whole_list.extend(word_list)
        print (word_list.__len__(),whole_list.__len__())
        # a totoal of 14 piece of topic list downloaded

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
        pred_relation = model.similar_by_word(sign,100)
        all_top_noun = [tmp[0] for tmp in pred_relation if word2type_dict[tmp[0]] == 'n']
        all_top_noun_similarity = [model.similarity(sign,tmp) for tmp in all_top_noun]
        all_top_noun_TFIDF = [all_docs.get_TFIDF(tmp) for tmp in all_top_noun]
        score_array = normalize (np.array(all_top_noun_similarity) ) * normalize(np.array(all_top_noun_TFIDF))
        pred_relation_show = [all_top_noun[tmp] for tmp in np.argsort(score_array)[-3:]]

        all_docs.get_TFIDF(all_top_noun[0])
        print ()
        print ('the sign {:s}is most related with following word, corrected by TF-IDF'.format(sign), pred_relation_show)

    except:
        print ('{:s} is not found'.format(sign))
        # todo Add frequency screener

# model = word2vec.Word2Vec(tmp_dic, size=10)  # 默认window=5