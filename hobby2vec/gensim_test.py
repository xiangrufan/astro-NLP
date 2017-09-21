import gensim
import numpy as np
from gensim.models import word2vec
import jieba
from TextSta_v2 import TextSta
from gensim.corpora.dictionary import Dictionary

path = u"C:\\Users\\xiangrufan\\Desktop\\NLP\\Astro_NLP\\resource\\复旦分类语料\\answer\\C3-Art\\C3-Art0002.txt"
text = TextSta(path,encoding="GBK")
sentense_file = text.sen(all_return=True)

word_list = jieba.lcut(sentense_file)
tmp_dic = Dictionary()
tmp_dic(word_list)
# sentences = word2vec.Text8Corpus()  # 加载语料
# model = word2vec.Word2Vec(sentences, size=10)  # 默认window=5