# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 23:32:51 2014

@author: pradeep
"""
from bs4 import BeautifulSoup
import re
import nltk
import itertools
from gensim import corpora, models, similarities

wsdl=str(open(r'E:\web services project\data\business\service0.Specialist.wsdl','r').read())
soup = BeautifulSoup(wsdl)
stoplist = set(open("stopwords.txt","r").read().split())
pos_filter=["JJ","JJR","JJS","NN","NNS","NNP","NNPS","SYM","VB","VBD","VBG","VBN","VBP","VBZ"]

def extract_info(text):
    info={}
    types=[]
    info['service']=text.find("service").get("name")
    info['binding']=text.find("binding").get("name")
    info['message']=text.find("message").get("name")
    info['port']=text.find("port").get('name')
    info['operation']=text.find("operation").get('name')
    for tag in soup.find_all("xsd:element"):    
        if "string" not in str(tag.get("type")):
            types.append(tag.get("type").replace("-"," "))
    info['type']=types
    return info

def tokenisation(info):
    listt=[]
    info['service']=[x.lower() for x in re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",info['service'])]
    info['binding']=[x.lower() for x in re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",info['binding'])]
    info['port']=[x.lower() for x in re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",info['port'])]
    for word in info['type']:
        if "-" in word:
            listt = list(itertools.chain(listt, word.split()))
        else:
            listt = list(itertools.chain(listt,[x.lower() for x in re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",word)]))
    info['type']=list(set(listt))
    return info    
    
def stopwordremoval(info):
    info['service']=[w for w in info['service'] if not w in stoplist]
    info['binding']=[w for w in info['binding'] if not w in stoplist]
    info['port']=[w for w in info['port'] if not w in stoplist]
    info['type']=[w for w in info['type'] if not w in stoplist]
    return info
    
def POS(info):
    info['service']=nltk.pos_tag(info['service'])
    info['binding']=nltk.pos_tag(info['binding']) 
    info['port']=nltk.pos_tag(info['port'])
    info['type']=nltk.pos_tag(info['type'])
    return info
    
def posfilter(info):
    info['service'] = [(name, tag) for name, tag in info['service'] if tag in pos_filter]
    info['binding'] = [(name, tag) for name, tag in info['binding'] if tag in pos_filter]
    info['port'] = [(name, tag) for name, tag in info['port'] if tag in pos_filter]
    info['type'] = [(name, tag) for name, tag in info['type'] if tag in pos_filter]
    return info

data=extract_info(soup)
#print data
filtered_data={'service':data['service'],'binding':data['binding'],'port':data['port'],'type':data['type']}
#print filtered_data
#tokenise
tokenised_data=tokenisation(filtered_data)
#print tokenised_data
#stopword removal
filtered_data=stopwordremoval(tokenised_data)
#print filtered_data
#POS
filtered_data=POS(filtered_data)
#print filtered_data
#pos filtering
filtered_data=posfilter(filtered_data)
print filtered_data

data=[]#contains names for tfidf from (name,value) after pos filter
for key in filtered_data.keys():
    data.append([name for name,tag in filtered_data[key]])
print data
dictionary = corpora.Dictionary(data)
print(dictionary)
print(dictionary.token2id)
corpus = [dictionary.doc2bow(d) for d in data]
print(corpus)
tfidf = models.TfidfModel(corpus)
print tfidf[corpus]