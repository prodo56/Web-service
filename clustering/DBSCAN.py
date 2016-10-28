from cluster import *
from pylab import *

#
#Every point in the the dataset would be a filename 
#


#for file in files;add the file to visited array;get neighbours of the file with epsilon;see if satisfies the condition then name the name the cluster
#for a new cluster by calling the cluster increase the count value(just for naming the cluering)
#add the point to the cluster,for every file in neighbours of the original_file add the file if not visited to the visited list
#then get the neighboring files of the new file form a union with old neighbours
#if point in any clusters add it to the cluster,add the cluster to the existing clusters

class dbscanner:
    
    dataSet = []
    count = 0
    visited = []
    member = []
    Clusters = []
    Distance_values={}
    
    def dbscan(self,D,ids, eps,MinPts):
        self.dataSet = ids
        self.Distance_values=D
        #print self.Distance_values
        C = -1
        for file in ids:
            if file not in self.visited:
                #self.visited.append(file)
                NeighbourPoints = self.regionQuery(file,eps)
                
                if len(NeighbourPoints) < MinPts:
                    print "noise"
                else:
                    name = 'Cluster'+str(self.count);#modify the name to filename
                    C = cluster(name)
                    self.count+=1;
                    self.expandCluster(file,NeighbourPoints,C,eps,MinPts)
                    
                    
        
      
    def expandCluster(self,file,NeighbourPoints,C,eps,MinPts):
        C.addPoint(file)
        for f in NeighbourPoints:
            if f not in self.visited:
                self.visited.append(f)
                #print self.visited
                np = self.regionQuery(f,eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)
            for c in self.Clusters:
                if not c.has(f):
                    if not C.has(f):
                        C.addPoint(f)
            if len(self.Clusters) == 0:
                if not C.has(f):
                    C.addPoint(f)
        self.Clusters.append(C)
        #picle c
        print C.printPoints()
        
                    
    #here instead of considering the the euclidean distance calculate the pre-computed similarity score             
    #so for file in files for every other file computer the similarity metric and add the 

    def regionQuery(self,P,eps):
        result = []
        for d in self.dataSet:
            if P<d:
                key = str(P) + "," +str(d)
            
                try:
                    if (self.Distance_values[key])<=eps:
                        result.append(d)
                except:
                    print key
        return result
    
            
#So at the end of it the cluster will have fileNames and extract content words from each file and get the tfidf of the words so formed and
#cluster names will be the top tfidf results
            
        
                
                 
            
            
            
            
        
