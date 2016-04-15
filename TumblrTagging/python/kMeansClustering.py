''' 
Author: Brooke Boatman
Date: December 2015
Clustering visualiser for tumblr tag data
'''
import random 
import math
import json
import collections as c
import tumblruser, htmlwrite
import numpy as np
from scipy import spatial
from sklearn.manifold import TSNE
from sklearn import cluster
import matplotlib.pyplot as plt
from collections import Counter
from reScale import *

#TAGFILE = "../data/tagfile.txt"
RAWDATA = "../data/rawData.txt"
HTMLFILE = "./new.html"
JAVATAGLOC = "../../../../IdeaProjects/TumblrHierachyGenerator/src/unicodeJSON.txt"
NUM_RESORTS = 5
STEP_SIZE = 3
POST_THRESH = 50
def openTagFile():
    '''
    Open the JSON doc made by the java part of the code
    '''
    with open(JAVATAGLOC, encoding="ISO-8859-1") as data_file:    
        data = json.load(data_file)
    return data

def shrinkDict(postThreshold = POST_THRESH):
    '''
    Throw away all blogs with less than a certain number of tags and/or posts attached to them. 
    This helps weed down the data so that we have less to attempt to run.
    Param: postThreshold - the minimum number of posts a user must have to be considered viable
    Return: tagDict - dictionary of tagVector dictionaries counting frequency of tag occurance
    '''
    tagList = openTagFile()
    badTags = []
    tagDict = {}
    for tagVector in tagList:
        try:
            if len(tagVector["tagName"]) >= 15:
                print(tagVector["tagName"], len(tagVector["posts"]))
            if len(tagVector["posts"]) > POST_THRESH:
                tagDict[tagVector["tagName"]] = tagVector["coOccurrenceCounter"]
        except:
            badTags.append(tagVector["tagName"])
    print(len(tagDict.keys()), "Valid Tags")
    return tagDict

TAG_DICT = shrinkDict()
with open("holdFile.txt", "w") as h:
    for val in TAG_DICT["cat"].items():
        h.write(str(val) + "\n")

def randomCluster(numClusters, tagDict):
    '''
    Set up for recursive clustering, randomly distributing urls across n clusters
    Param: numClusters - the number of clusters to randomly distribute tag vectors across
    Return: clusteredUrls - a list of size numClusters of TagCluster objects
    '''
    clusterList = [tumblruser.TagCluster() for x in range(numClusters)]
    for entry in tagDict:
        loc = random.randint(0, numClusters - 1)
        clusterList[loc].addMember(entry, tagDict[entry])
    for cluster in clusterList:
        cluster.setCentroid()
    return clusterList 


def calculateCosineDistance(centroid, tagVector):
    '''
    Calculate the cosine distance of any tag vector and a cluster's centroid
    Param: centroid - averaged vector of tags for one cluster
           urlVector - a dictionary of tags occurances one tag
    Return: cosine distance of a and b
    '''
    a = []
    b =[]
    for item in tagVector:
        if item in centroid:
            a.append(float(tagVector[item]))
            b.append(float(centroid[item]))

    if len(a) == 0:
        return 1
    else:
        return spatial.distance.cosine(a,b)


def clusterMatch(clusterList, vector):
    '''
    Find which cluster a tag vector is best placed in given its current centroid
    Param: clusterList - a list of cluster objects
           vector - a single tagVector object
    Return: index of the best matching cluster in the cluster list
    '''
    cosineSim = []
    index = 0;
    for cluster in clusterList:
        similarity = calculateCosineDistance(cluster.getCentroid(), Counter(vector))
        cosineSim.append((index, similarity))
        index += 1
    return cosineSim


def reCluster(clusterList):
    '''
    Resort the clusters according to which centroid is closest
    Param: clusterList - a list of every cluster to be reclustered
    Return: clusterList - the resorted list of clusters
            avg - the average distance of a tag and it's new cluster after resorting
    '''
    iterCount = 0
    avg = 0
    for cluster in clusterList:
        cluster.wipeMembers()
    tagList = TAG_DICT.keys()

    for tag in tagList:
        vector = TAG_DICT[tag]
        matchTuple = sorted(clusterMatch(clusterList, vector), key=lambda tup: tup[1], reverse=False)[0]
        if matchTuple[0] > 0:
            bestIndex = matchTuple[0]
            avg += matchTuple[1]
            clusterList[bestIndex].addMember(tag, vector)
        iterCount +=1
        # if iterCount % 500 == 0:
        #     print(matchTuple[1], tag, matchTuple[0])
    avg = avg/iterCount
    for cluster in clusterList:
        cluster.setCentroid() 
    return clusterList, avg


def makeSimVectors():
    '''
    Create dense vectors for each tag by finding their distance from every cluster
    Return: visualiserDict - dictionary of dense tag vectors
    '''
    count = 0
    numClusters = len(TAG_DICT) // 3
    numResorts = numClusters // 20 if numClusters // 20 < 20 else 20
    print(numClusters, "Clusters")
    print("Resorting", str(numResorts), "Times")
    clusterList = randomCluster(numClusters, TAG_DICT)
    for i in range(numResorts):
        clusterList, avg = reCluster(clusterList)
        print(avg, i)
    visualiserDict ={}
    for tag in TAG_DICT:
        vector = TAG_DICT[tag]
        cosineSim = clusterMatch(clusterList, vector)
        indices, values = zip(*cosineSim) 
        visualiserDict[tag] = values
        count += 1
    return visualiserDict

def generateDataPoints(dFile):
    ''' 
    Create the .txt file of 2d points and their corresponding tags
    '''
    simVector = makeSimVectors()
    tsne = TSNE(n_components=2, init='pca', random_state=0)
    labels = sorted(simVector.keys())
    fData = tsne.fit_transform([simVector[w] for w in labels])

    np.savetxt(RAWDATA, fData, fmt="%.9f", delimiter=' ')
    raw = open(RAWDATA)
    with open(dFile, 'w') as dataFile:
        for i, line in enumerate(raw.readlines()):
            x, y = line.split()
            try:
                writeStr = "[" + str(x) + ", " + str(y) + ", "+ '\"' + labels[i] + "\"],\n"
                dataFile.write(writeStr)
            except(UnicodeEncodeError):
                print("Failed to write")
    raw.close()

def generateHtml(dataFile, htmlFile):
    '''
    Generate the html file for visualizaton
    '''
    generateDataPoints(dataFile)
    indexList = readInData(dataFile)
    visualCluster(indexList, htmlFile)

#rescaleNoRecluster('./data.txt', './new.html')
generateHtml("testData.txt", "new2.html")

