from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import math
import MySQLdb
import os
import requests
import string
import pickle
import itertools as IT
from textblob import Word
#global initialization
tokenExp = '([A-z][a-z]+)([A-Z][a-z]+)|[\\W_]'

pos_filter=["JJ","JJR","JJS","NN","NNS","NNP","NNPS","SYM","VB","VBD","VBG","VBN","VBP","VBZ"]

#initilization
def spellCheck(list):
	corrections = []
	for word in list:
		if not wordnet.synsets(word):
	 		w = Word(word)
			correction = w.spellcheck()[0][0]
			corrections.append(str(correction))
		else:
			corrections.append(word)
	return corrections
	

#=====================================================================================================================================

def getScore(id1,id2):
	cursor = db.cursor()
	sql = "select cosine_similarity from test.similarity where wsdl_id1=%d and wsdl_id2=%d"%(id1,id2)
	cursor.execute(sql)
	results = cursor.fetchall()
	if(len(results)):
  		print 0
  	else
  		print results[0][0]
  	



#=====================================================================================================================================

def insertWSDL(file):
	cursor = db.cursor()
	sql = "INSERT INTO wsdl_info(wsdl_name) VALUES('%s')"%(file)
 	try:
  		cursor.execute(sql)
  		db.commit()
   	except:
		print 'screwed up'


#=====================================================================================================================================
def isUpdated(wsdl_name):
	cursor = db.cursor()
	sql = "UPDATE wsdl_info SET is_updated=1 WHERE wsdl_name='%s'"%(wsdl_name) 

	try:
		try:
  			cursor.execute(sql)
   		except:
   			db.rollback()
   			raise
   		else:
   			db.commit()
   	finally:
   		cursor.close()

#=====================================================================================================================================
def isNotUpdated(wsdl_name):
	cursor = db.cursor()
	sql = "select is_updated from wsdl_info WHERE wsdl_name='%s'"%(wsdl_name) 
	cursor.execute(sql)
  	results = cursor.fetchall()
	result = results[0]
	return not result[0]


#=====================================================================================================================================

def similarity(word1,word2):
	response = requests.get('http://www.linguatools.de/cgi-bin/disco-gui_en.pl?wort1=%s&wort2=%s&index=en-wikipedia-20080101'%(word1,word2))
	soup = BeautifulSoup(response.content)
	sim_value = [float(str(element.text).split(':')[-1]) for element in soup.find_all('center') if(element.text.find('(S2)') >= 0)]
	return sim_value[0]

#=====================================================================================================================================

def wordnetSimilarity(word1, word2):
    wordFromList1 = wordnet.synsets(word1)[0]
    wordFromList2 = wordnet.synsets(word2)[0]
    s = wordFromList1.wup_similarity(wordFromList2)
    return(wordFromList1.wup_similarity(wordFromList2))

#=====================================================================================================================================
def getCosine(a,b):
	list_a = a.split(" ")
	list_b = b.split(" ")
	if len(list_a)==0 or len(list_b)==0:
		return 0
	matches = sum([1 if wa.lower() == wb.lower() else 0 for wa in list_a for wb in list_b])
	return matches/float(math.sqrt(len(list_a)*len(list_b)))


#=====================================================================================================================================
def insertSimilarity(wsdl_id1,wsdl_id2,similarity_score):
	cursor = db.cursor()
	sql = "INSERT INTO similarity(wsdl_id1,wsdl_id2,cosine_similarity) VALUES('%d','%d','%s')"%(wsdl_id1,wsdl_id2,str(similarity_score))
 	try:
  		cursor.execute(sql)
  		db.commit()
   	except:
		print 'screwed up'

#=====================================================================================================================================

def computeCosine():

  cursor = db.cursor()
  service_similarity = ()
  sql = "SELECT * FROM wsdl_info"
  cursor.execute(sql)
  results = cursor.fetchall()
  print len(results)
  for i,row_outer in enumerate(results):
  	service1 = row_outer[3].split(" ")
  	# except:
  	# print row_outer[3]
  	for j,row_inner in enumerate(results):
  		# try:
  		service2 = row_outer[3].split(" ")
  		# except:
  			# print row_outer[3]
  		if i < j and len(service1) > 0 and len(service2) > 0:
  			# print 
  			insertSimilarity(row_outer[0],row_inner[0],getCosine(str(row_outer[3]).lstrip().rstrip(),str(row_inner[3]).lstrip().rstrip()))
  		else:
  			print 'sanms was here'
  			insertSimilarity(row_outer[0],row_inner[0],0)

  	isUpdated(row_outer[0])		

#=====================================================================================================================================
def tf(word, blob):
 	return blob.words.count(word) / float(len(blob.words))
 
def n_containing(word, bloblist):
 	return sum(1 for blob in bloblist if word in blob)
 
def idf(word, bloblist):
	if n_containing(word,bloblist) == 0:
		return 0
	else:
		return math.log(len(bloblist) / (n_containing(word, bloblist)))
 
def tfidf(word, blob, bloblist):
	return tf(word, blob) * idf(word, bloblist)






#=====================================================================================================================================
def update(service_names,unique_names,wsdl_name):
	cursor = db.cursor()
	sql = "UPDATE wsdl_info SET service_names='%s',unique_names='%s' WHERE wsdl_name='%s'"%(service_names,unique_names,wsdl_name) 
	try:
		try:
  			cursor.execute(sql)
   		except:
   			db.rollback()
   			raise
   		else:
   			db.commit()
   			isUpdated(wsdl_name)	
   	finally:
   		cursor.close()

#=====================================================================================================================================

def remove_non_english(list):
	l = []
	for word in list:
  		if wordnet.synsets(word):
  			l.append(word)

  	return l
#=====================================================================================================================================

def tokenize(list):
	dup = [' '.join(filter(None,re.split(tokenExp,word))).lower() for word in list]
	dup = set(' '.join(dup).split())
	list = []
	for word in dup:
		list.append(word)
	return list
   			
 #=====================================================================================================================================

def removeStopWords(lst):
	l = []
	stop = stopwords.words('english')
	stop.append("soap")
	stop.append("service")
	stop.append("port")
	stop.append("binding")
	stop.append("response")
	stop.append("http")
	stop.append("string")
	stop.append("array")
	stop.append("type")
	stop.append("get")
	stop.append("xml")
	stop.append("request")
	stop.append("ok")
	stop.append("url")
	stop.append("html")
 	stop = list(string.ascii_lowercase) + stop
	for word in lst:
		if word is not None and word.lower() not in stop:
			l.append(word)
		
	return l

#=====================================================================================================================================


def posTag(list):
	 return nltk.pos_tag(list)
		
#=====================================================================================================================================

def posFilter(list):
	for item in list:
		word,tag = item
		if tag not in pos_filter:
			list.remove(item)
			
	return list

#=====================================================================================================================================
def intersection(list1,list2):
	count = 0
	for a in list1:
		for b in list2:
			if a == b:
				count = count+1;

	return count

#=====================================================================================================================================

def convert_to_list(tuple):
	list = []
	for item in tuple:
		list.append(item[0])	

	return list
#=====================================================================================================================================
def preprocess(list):
	list = tokenize(list)
	list = spellCheck(list)
	list = removeStopWords(list)
	list =  posTag(list)
	list = posFilter(list)
	list = convert_to_list(list)
	return list

#=====================================================================================================================================


def getdata(file):
	
	list = []
	try:
		text = BeautifulSoup(open(file))
		print 'here'
	except:
		print 'screwed up'
		return


	service_list = []
	message_list = []
	porttype_list = []
	operation_list = []
	content_words = []
	service_names = ""
	proto_names = ""
	operations_names = ""
	message_names =  ""

	print 'here'
	try:
		service_list.append(str(text.find("wsdl:service").get("name")))
		print 'here'
	except:
		print 'screwed up in service'

	try:
		porttype_list =  [str(child['name']) for child in text.find_all('wsdl:porttype')]
		print 'here'
	except:
		print 'screwed up in port'
	try:
		operation_list =  [str(child['name']) for child in text.find_all('wsdl:operation')]
		print 'here'
	except:
		print 'screwed up in operations'
	try:
		message_list = [str(child['name']) for child in text.find_all('wsdl:message') if child.has_attr('name')]
	except:
		print 'screwed up in type'


	print 'here'
	content_words = set(preprocess(service_list) + preprocess(porttype_list) + preprocess(operation_list) + preprocess(message_list))
	unique_names = " ".join(content_words)
	service_names = " ".join(preprocess(service_list))
	
	print "updating ...."

	try:
		update(service_names,unique_names,file[:file.index(".xml")])
	except:
		print "except"
#=====================================================================================================================================

def getFiles():
  file_names = [] 
  cursor = db.cursor()
  sql = "SELECT * FROM wsdl_info where is_updated = 0"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
  	file_names.append(row[1])
    
  return file_names


#=====================================================================================================================================

db = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "",
                        db = "test")



getScore(1,4)
# computeCosine()

# files = getFiles()
# for file in files:
# 	getdata(file+".xml")


# # computeSynset()
# files = os.listdir('.')

# for file in files:
# 	if file.endswith('.xml') and isNotUpdated(file[:file.index(".xml")]):
# 		getdata(file)

# for i,file in enumerate(files):
# 	if file.endswith('.xml'):
# 		# insertWSDL(file[:file.index(".xml")])
# 		getdata(file)
		

# getdata('service20.DeveloperTools.xml')
