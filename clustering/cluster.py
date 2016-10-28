import pickle
class cluster:
    
    fList = []
    name = ""
    
    def __init__(self,name):
        self.name = name
        self.fList = []
        
    
    def addPoint(self,point):
        self.fList.append(point)
        
    def getPoints(self):
        return self.fList
    
    def erase(self):
        self.fList = []
    
    def has(self,point):
        
        if point in self.fList:
            return True
        
        return False
        
    def printPoints(self):
        f2=open('E:\\web services project\\cluster1\\'+self.name+'.txt','w')
        print '-----------------'
        print self.fList
        pickle.dump(self.fList,f2)
        print len(self.fList)
        print '-----------------'
    
        
        
        