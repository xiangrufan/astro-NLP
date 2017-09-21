#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
I copied this file from http://blog.csdn.net/churximi/article/details/61210129
original author 竹聿Simon
I modified this file to add GBK compatibility
功能：一个类，执行文本转换
输入：分词文本
输出：句子列表，全文的词汇列表，TF，DF
时间：2016年5月17日 19:08:34
"""

import codecs
import re


class TextSta:
    # 定义基本属性，分词文本的全路径
    # filename = ""

    # 定义构造方法
    def __init__(self, path,encoding="utf-8"):    # 参数path，赋给filename
        self.filename = path
        self.encoding = encoding

    def sen(self,all_return = True):    # 获取句子列表
        f1 = codecs.open(self.filename, "r", encoding=self.encoding)
        # 获得句子列表，其中每个句子又是词汇的列表
        if all_return:
            file = f1.readlines()
            file_out = ""
            for line in file:
                file_out = file_out+ line
            f1.close()
            return file_out
        else:
            sentences_list = []
            for line in f1:
                single_sen_list = line.strip()
                while "" in single_sen_list:
                    single_sen_list.remove("")
                sentences_list.extend(single_sen_list)
            print (u"句子总数：", len(sentences_list))

            f1.close()
            return sentences_list

if __name__ == "__main__":
    pass