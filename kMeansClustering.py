import random 
import math
import pickle
import collections as c
import tumblruser, htmlwrite
import numpy as np
from scipy import spatial
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

TAGFILE = "tagfile.txt"
NUM_RESORTS = 10
NUM_CLUSTERS = 20
STEP_SIZE = 3
POST_THRESH = 90


def shrinkDict(postThreshold = POST_THRESH):
    '''
    Throw away all blogs with less than a certain number of tags and/or posts attached to them. 
    This prevents big corporate blogs and professional bloggers from overwhelming the results
    Param: postThreshold - the minimum number of posts a user must have to be considered viable
    Return: returnDict - dictionary of tumblruser objects counting frequency of tag occurance
    '''
    tagfile = open(TAGFILE, 'r')
    userDict = pickle.load(tagfile)
    tagfile.close()
    userDict = {usrId: usrObj for (usrId, usrObj) in userDict.items() if len(usrObj.posts) >= POST_THRESH}
    return userDict


def generateTagVectors():
    ''' 
    Generate tag vectors for cosine similarity analysis
    Param: userDict - a dictionary of tumblruser objects
    Return: vectorDict - a dictionary of tag vectors with tags as keys and counters as values
    '''
    vectorDict = {}
    userDict = shrinkDict()
    for user in userDict:
        usrObj = userDict[user]
        for tag in usrObj.tagDict:
            if tag not in vectorDict:
                vectorDict[tag] = tumblruser.TagVector(tag)
            vectorDict[tag].updateVector(usrObj.tagDict[tag])
    return vectorDict


def randomCluster(numClusters):
    '''
    Set up for recursive clustering, randomly distributing urls across n clusters
    Param: numClusters - the number of clusters to randomly distribute links across
    Return: clusteredUrls - a list of n lists containing a random distribution of tuples where the first item is a url
                            and the second is a default dictionary where key=tag value = frequency of occurance
    '''
    clusterList = [tumblruser.TagCluster() for x in xrange(numClusters)] # Courtesy of user 279627, Stack Overflow
    for entry in TAG_DICT:
        loc = random.randint(0, numClusters - 1)
        clusterList[loc].addMember(TAG_DICT[entry])
    for cluster in clusterList:
        cluster.setCentroid()
    return clusterList



def evenCluster(numClusters):
    '''
    Set up for recursive clustering, uniformly distributing urls across n clusters
    Param: numClusters - the number of clusters to evenly distribute links across
    Return: clusteredUrls - a list of n lists containing a uniform distribution of tuples where the first item is a url
                            and the second is a default dictionary where key=tag value = frequency of occurance
    '''
    clusterList = [tumblruser.TagCluster() for x in xrange(numClusters)] 
    partition = len(TAG_DICT) / numClusters
    loc = 0
    step = 0
    for entry in TAG_DICT:
        clusterList[loc].addMember(TAG_DICT[entry])
        step += 1
        if step > partition:
            loc += 1
            step = 0
    return clusterList


def calculateCosineSimilarity(centroid, tagVector):
    '''
    Calculate the cosine similiarity of any url's tags and that of a centroid for a given cluster
    Param: centroid - one averaged vector of tags for one cluster
           urlVector - a dictionary of tags and their occurances for one url
    Return: cosineSimilarity - the similarity of occurance of tags shared between the two vectors
    TODO: Why does this sometimes return > 1?????
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
    Param: clusterList - a list of n centroid vectors, stored as dictionaries of key=tag, value=average occurance
           urlVector - a single url's dictionary of key=tags, value=occurance of tag
    Return: index of the best matching cluster in the cluster list
    '''
    cosineSim = []
    index = 0;
    for cluster in clusterList:
        similarity = calculateCosineSimilarity(cluster.getCentroid(), vector.getTagCounter())
        cosineSim.append((index, similarity))
        index += 1
    return sorted(cosineSim, key=lambda tup: tup[1], reverse=False) #sort by tuple's second value; courtesy of user 303180, stackOverflow


def reCluster(clusterList):
    '''
    Resort the clusters according to which centroid is closest
    Param: centroidList - a list of every cluster's centroid dictionary where key=tag, value=avg frequency of occurance
    '''
    iterCount = 0
    avg = 0
    for cluster in clusterList:
        cluster.wipeMembers()
    tagList = TAG_DICT.values()

    for tag in tagList:
        matchTuple = clusterMatch(clusterList, tag)[0]
        bestIndex = matchTuple[0]
        avg += matchTuple[1]
        iterCount +=1
        clusterList[bestIndex].addMember(tag)
        if iterCount % 500 == 0:
            print matchTuple[1], tag.getName(), matchTuple[0]
    avg = avg/iterCount
    for cluster in clusterList:
        cluster.setCentroid() 
    return clusterList, avg


def bestFit(centroid, cluster, showNumber):
    '''
    Find which urls are the best represtatives of their cluster
    Param: centroid - the vector value of a cluster to compare urls agains
           cluster - a list of urls and their dictionaries that contain tags and frequencies
           showNumber - the number of urls to show as best representatives of their cluster
    Return: a sorted list that contains the n most representative urls
    '''
    cosineSim = []
    index = 0;
    for url in cluster:
        tags = url[1]
        similarity = calculateCosineSimilarity(centroid, tags)
        cosineSim.append((url[0], similarity))
        index += 1
    cosineSim = sorted(cosineSim, key=lambda tup: tup[1], reverse=True) 
    if showNumber > len(cluster):
        return cosineSim
    else:
        return cosineSim[:showNumber - 1]


def printBestItems(clusterList):
    index = 0
    
    for cluster in sortedClusters:
        index += 1
        if len(cluster) > 0:
            print "Cluster", index
            bestFitUrls = bestFit(centroidList[index], cluster, 5)
            for url in bestFitUrls:
                print url


def mergeClusters(clusterList):
    '''
    TODO : This is wrong don't use it yet
    '''
    newClusters = []
    for cluster in clusterList: #for all remaining clusters in list
        holderList = []
        for x in range(0, STEP_SIZE - 1): # number of clusters merged together - 1 for final merge of comparison cluster
            cosineSim = []
            centroidList = calculateCentroids(clusterList)
            # get all similarities
            for i in range(0, len(centroidList)): 
                cosineSim.append((i,calculateCosineSimilarity(centroidList[i],centroidList[0])))
                cosineSim = sorted(cosineSim, key=lambda tup: tup[1], reverse=True)
            holderList.append(clusterList[cosineSim[0][0]])
            clusterList.remove(clusterList[cosineSim[0][0]])
        holderList.append(clusterList[0])
        clusterList.remove(clusterList[0])
        newClusters.append(holderList[0])
    return newClusters
     

def mergingTest():
    '''
    TODO : This is wrong don't use it yet
    '''
    numClusters = TOTAL_TAGS
    clusters = evenClusters(numClusters)
    centroidList = calculateCentroids(clusters)
    index = 0
    while numClusters > NUM_CLUSTERS:
        if index > 0: 
            numClusters /= STEP_SIZE
            clusters = mergeClusters(clusters)
            centroidList = calculateCentroids(clusters)
            numClusters = len(clusters)
        index = 0
        while index < NUM_RESORTS:
            clusters, avg = reCluster(centroidList, numClusters)
            centroidList = calculateCentroids(clusters)
            print "Sort number", index, "Average correlation", avg
            index += 1
        print numClusters
    printClusterUrls(clusters)
    return clusters, centroidList


def makeSimVectors():
    count = 0
    for i in range(NUM_RESORTS):
        clusterList = randomCluster(numClusters)
        clusterList, avg = reCluster(clusterList)
        print avg, i
    visualiserDict ={}
    for tag in TAG_DICT:
        vector = TAG_DICT[tag]
        cosineSim = clusterMatch(clusterList, vector)
        similarityList = range(numClusters)
        for tupleVal in cosineSim:
            index = tupleVal[0]
            similarityList[index] = tupleVal[1]
        visualiserDict[tag] = similarityList
        count += 1
        if count % 500 == 0:
            print tag
    return visualiserDict


TAG_DICT = generateTagVectors()
print len(TAG_DICT)
numClusters = 1000
simVector = makeSimVectors()
tsne = TSNE(n_components=2, init='pca', random_state=0)
labels = sorted(simVector.keys())
fData = tsne.fit_transform([simVector[w] for w in labels])



def scale(value, mult = 20, add = 500 + int(10*random.random())):
    return str(float(value)*mult + add)


np.savetxt('rawData.txt', fData, fmt="%.9f", delimiter=' ')
raw = open("rawData.txt")
displayFile = open("display.html", "w")
displayFile.write(htmlwrite.getTop())
for i, line in enumerate(raw.readlines()):
    x, y = line.split()
    displayFile.write("[" + scale(x) + ", " + scale(y) + ", " + '\"' + labels[i] + '\"' + "],\n")
raw.close()
displayFile.write(htmlwrite.getBottom())
displayFile.close()

