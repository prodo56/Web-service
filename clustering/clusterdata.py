import pymongo
import pickle
from clustering import *
import unicodedata
#db = MySQLdb.connect("localhost", "root", "pdeep123", "test")
#conn=pymongo.MongoClient()
#db=conn.test
#=================================================================================================================================

def getScore(id1,id2):
    #cursor = db.cursor()
    #query={}
    #query['wsdl_id1']=id1
    #query['wsdl_id2']=id2
    #query.append({'cosine_similarity': 1})
    #query = dict('{"wsdl_id1": %d,"wsdl_id2": %d}, {"cosine_similarity": 1}'%(id1,id2))
    
    
    results = db.similarity.find({"wsdl_id1": id1,"wsdl_id2": id2}, {"cosine_similarity": 1})
    if(results.count() >0):
        return float(results[0]['cosine_similarity'])
    else:
        return 0

#=================================================================================================================================

def make_matrix(ids):
    Distance_matrix={}
    Distance_matrix1=(pickle.load(open('E:\\web services project\\Distance_matrix_950.txt')))
    for i in ids:
            for j in ids:
                if i<j:
                    
                    key = str(i) + "," +str(j)
                    print key
                    Distance_matrix[key]=Distance_matrix1[key]
                    Distance_matrix[str(j)+","+str(i)]=Distance_matrix[key]
                elif i==j:
                    Distance_matrix[str(j)+","+str(i)]=0
                
    print "dataMatrix done"
    pickle.dump(Distance_matrix,open('E:\\web services project\\Distance_matrix_rand.txt','w'))
    return Distance_matrix

#=================================================================================================================================
    
def compute_Clustering():
    
    file_ids=pickle.load(open("E:\\web services project\\rand_wsdls.txt"))
    Distance_matrix=make_matrix(file_ids)
    print len(Distance_matrix)
    dbc= dbscanner()
    eps=0.92
    MinPts=3
    dbc.dbscan(Distance_matrix,file_ids, eps, MinPts)

compute_Clustering()