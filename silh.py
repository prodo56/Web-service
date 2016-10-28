# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 11:51:59 2014

@author: pradeep
"""

import numpy as np
from scipy.cluster.vq import kmeans2
from scipy.spatial.distance import pdist, squareform
from sklearn import datasets
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle

def silhouette(X, cIDX,matrix):
    """
    Computes the silhouette score for each instance of a clustered dataset,
    which is defined as:
        s(i) = (b(i)-a(i)) / max{a(i),b(i)}
    with:
        -1 <= s(i) <= 1

    Args:
        X    : A M-by-N array of M observations in N dimensions
        cIDX : array of len M containing cluster indices (starting from zero)

    Returns:
        s    : silhouette value of each observation
    """

    N = 250              # number of instances
    K = len(np.unique(cIDX))-1    # number of clusters

    # compute pairwise distance matrix
    D = matrix

    # indices belonging to each cluster
    kIndices = [np.flatnonzero(cIDX==k) for k in range(K)]
    # compute a,b,s for each instance
    a = np.zeros(N)
    b = np.zeros(N)
    for i in range(N):
        # instances in same cluster other than instance itself
        if cIDX[i]!=999:
            for ind in kIndices[cIDX[i]]:
                if ind!=i:
                    a[i] = np.mean( D[str(X[i])+","+str(X[ind])])
        #a[i] = np.mean( [D[str(i+1)+","+str(ind+1)] for ind in kIndices[cIDX[i]] if ind!=i and cIDX[i]!=999] )
        # instances in other clusters, one cluster at a time
        #b[i] = np.min( [np.mean(D[str(i+1)+","+str(ind+1)]) for k,ind in enumerate(kIndices) if cIDX[i]!=k and cIDX[i]!=999] )
            for k,ind in enumerate(kIndices):
                if cIDX[i]!=k:
                    print k,ind
                    #print type(k),type(ind)
                    for e in ind:
                        b[i]=np.min(np.mean(D[str(X[i])+","+str(X[e])]))
    print len(a),len(b)    
    s = np.zeros(N)
    for i in range(N):
        if a[i]!=0 and b[i]!=0:
            s[i] = (b[i]-a[i])/np.maximum(a[i],b[i])
        else:
            s[i]=0
    s=np.mean(s)
    return s

def main():
    # load Iris dataset
    #data = datasets.load_iris()
    X = pickle.load(open("E:\\web services project\\rand_wsdls.txt"))
    #print X
    # cluster and compute silhouette score
    
    Dis_matrix=pickle.load(open('E:\\web services project\\Distance_matrix_rand.txt'))
    
    
    #C, cIDX = kmeans2(X, K)
    cIDX=np.load(open("E:\\web services project\\rand_cIDX.txt"))
    print cIDX
    s = silhouette(X, cIDX,Dis_matrix)
    print "avg s" +str(s)
    K=5
    # plot
    

   

if __name__ == '__main__':
    main()