#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 22:57:20 2022

@author: shreeyeshmenon
"""

import pandas as pd
import os
path='/Users/shreeyeshmenon/Desktop/MPC_Analysis/MPC Minutes/Brazil_Analysis/'
folder=os.listdir(path)

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')

monthNames=['january','february','march','april','may','june','july','august','september','october','november','december']
def lemmatize_stemming(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3 and token not in monthNames:
            result.append(lemmatize_stemming(token))
    return result

proc_doc=dict()
iter=0;
docs=[];
pdocs=[];
for file in folder:    
    filepath=path+str(file)
    f=open(filepath,'r',encoding="latin-1")
    text_str=f.read()
    text_str=text_str.lower()
    docs.append(text_str)
    words = []
    for word in text_str.split(' '):
        words.append(word)
    proc_doc[file[:-4]]=preprocess(text_str)
    pdocs.append(preprocess(text_str))

dictionary = gensim.corpora.Dictionary(pdocs)

count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)


bow_corpus = [dictionary.doc2bow(doc) for doc in pdocs]
doc10=bow_corpus[10]

for i in range(len(doc10)):
    print("Word {} (\"{}\") appears {} time.".format(doc10[i][0], 
                                                     dictionary[doc10[i][0]], 
                                                     doc10[i][1]))

from gensim import corpora, models

tfidf = models.TfidfModel(bow_corpus)

corpus_tfidf = tfidf[bow_corpus]


from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break

lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

pdocs[10]
for index, score in sorted(lda_model[bow_corpus[10]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))


lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))
    
for index, score in sorted(lda_model_tfidf[bow_corpus[10]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))    
    
    
w=open()    