from bs4 import BeautifulSoup
import glob
from textblob import TextBlob as tb
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import math
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import GaussianNB
import os
from itertools import chain, combinations
from collections import defaultdict
import operator
from collections import OrderedDict
#global initialization
tokenExp = '([A-z][a-z]+)([A-Z][a-z]+)|[\\W_]'

pos_filter=["JJ","JJR","JJS","NN","NNS","NNP","NNPS","SYM","VB","VBD","VBG","VBN","VBP","VBZ"]
bloblist = []
dataset = []
preset_dict = {}
#initilization
def init_data():

	dict = {}
	dict.setdefault('Service',[])
	dict.setdefault('Port',[])
	dict.setdefault('Type',[])
	return dict 



	
def uniqfy(list):
	dict = {}
	
	for item in list:
		word = str(item.lower())

		dict[word]=1

	return dict.keys()

def present_in(dict):
	
	for key,list in dict.items():
	 for word in list:
			preset_dict[word] = (word in dict['Service'],word in dict['Port'],word in dict['Type'])



def tokenize(dict):
	
	greater = 0
	words = ""
 	for key,list in dict.items():
		for word in list:

			if bool(re.search(tokenExp,word)):
				index = list.index(word)
				list[index:index+1] = filter(None,re.split(tokenExp,word))
  				

  		dict[key] = uniqfy(list)  


  	for key,list in dict.items():
  		for word in list:
  			
  			if not wordnet.synsets(word):
  				length = len(word)
  				index = list.index(word)
				for i in  range(length):
    				
					if wordnet.synsets(word[length-i-1:]) and wordnet.synsets(word[0:length-i-1]) and wordnet.synsets(word[length-i-1:]):
						    	words = word[0:length-i-1] + " " + word[length-i-1:]

				list[index:index+1] = words.split()


		dict[key] = uniqfy(list) 	
        present_in(dict)
	
	return dict




def removeStopWords(dict):
	stop = stopwords.words('english')
	stop.append("soap")
	for key,list in dict.items():
		for word in list:
			if word in stop or word == key.lower():
				list.remove(word)
		dict[key]=list

	return dict


def posTag(dict):
	for key,list in dict.items():
		dict[key] = nltk.pos_tag(dict.get(key))
		
	return dict


def posFilter(dict):
	for key,list in dict.items():
		for item in list:
			word,tag = item
			if tag not in pos_filter:
				list.remove(item)
		dict[key] = list
	return dict



def createBlob(dict):
	words = ""
	for key,value in dict.items():
		for word,tag in value:
			words=words + word + " "
 	
 	bloblist.append(tb(words.rstrip()))



def tf(word, blob):
 	return blob.split().count(word) / float(len(blob.split()))
 
def n_containing(word, bloblist):
 	return sum(1 for blob in bloblist if word in blob)
 
def idf(word, bloblist):
	if n_containing(word,bloblist) == 0:
		return 0
	else:
		return math.log(len(bloblist) / (n_containing(word, bloblist)))
 
def tfidf(word, blob, bloblist):
	return tf(word, blob) * idf(word, bloblist)

    

def getTFIDF():
	scores = {}
	for blob in bloblist:
		for word in blob.split():
			scores[word] = round(tf(word, blob) * idf(word, bloblist),5) 
    
   	return scores

	

def prepareData(dict,tfidf):
	
	features = {}
	for key,list in dict.items():
		for word,tag in list:
			(s,p,t) =  preset_dict[word]
			
			features['tfidf'] = tfidf[word]

			features['in_service'] = s
			print features['in_service']
			features['in_port'] = p
			print features['in_port']
			features['in_type'] = t
			print features['in_type']
			features['pos'] = tag
            
        	dataset.append(features)
        	
		

def getdata(file):
	dict = init_data()
	list = []
	text = BeautifulSoup(open(file))
	list.append(str(text.find("wsdl:service").get("name")))
	dict['Service'] = list
	del list[:]
	list.append(str(text.find("wsdl:port").get('name')))
	dict['Port'] = list 
	dict['Type'] = [str(child['name']) for child in text.find('wsdl:types').find_all(True) if child.has_attr('name')]

	dict = tokenize(dict)
	dict = removeStopWords(dict)
	dict =  posTag(dict)
	dict = posFilter(dict)
	createBlob(dict)

	return dict



os.chdir('E:\\web services project\\wsdl\\wsdl dataset\\')
files = glob.glob("*.wsdl")
datalist = []
for file in files:
	datalist.append(getdata(file))
#for blob in bloblist:
    #print blob
#print 'dataset'+str(datalist)
tfidf = getTFIDF()

for dict in datalist:
 	data = prepareData(dict,tfidf)

#print dataset
#print datalist
print tfidf
vec = DictVectorizer()

#gnb = GaussianNB()


data_vectorized = vec.fit_transform(dataset)


#print data_vectorized.toarray()
#print tfidf
#sorted_tfidf = sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True)
#initial_tags=[]
#def cutoff(threshold, data):
    
#    finalList = filter(lambda x: x[1] < threshold, data)
   
#    for t in finalList:
#        initial_tags.append(t[0])
    
#cutoff(2,sorted_tfidf)
#print initial_tags
#list_blob=[]
#for b in bloblist:
#    list_blob.append(str(b))
#refined=[]
#for l in list_blob:
#    refined.append(' '.join(set(l.split())).split())
#remove duplicate
#newlist=[]
#for i in refined:
#  if i not in newlist:
#    newlist.append(i)
