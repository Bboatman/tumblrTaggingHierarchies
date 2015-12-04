import random, math, pickle, collections as c, tumblruser
TAGFILE = 
NUM_RESORTS = 10
TOTAL_TAGS = 235
NUM_CLUSTERS = 5
STEP_SIZE = 3
MIN_THRESHOLD = 700 #Minimum number of tags needed for a url to be considered


def makeDict(fileName):
'''
Read in a tab separated file and sort it into a dictionary of urls and their tags
Param: filename - the name of the file to be read int
Return: returnDict - dictionary of dicts counting frequency of occurance
        key=url value=defaultdict(int)
         key=tag value=frequency of occurance
'''
    returnDict = {}
    urls = open(fileName, 'r')
    #TODO : Create a dictionary of user objects from the pickle file
    return returnDict

def shrinkDict(minThreshold, rawDict):
'''
Throw away all urls with less than a certain number of tags attached to them
Param: minThreshold - the minimum number of tags a url must have
       rawDict - the intial dictionary of urls and their tags made by makeDict
Return: returnDict - dictionary of dicts counting frequency of tag occurance
        key=url value=defaultdict(int)
        key=tag value=frequency of occurance
'''
    returnDict = {}
    for entry in rawDict:
        sumTags = 0
        # TODO : Iterate through every user object in the dict
    return returnDict

def randomClusters(numClusters):

'''
# Set up for recursive clustering, randomly distributing urls across n clusters
# Param: numClusters - the number of clusters to randomly distribute links across
# Return: clusteredUrls - a list of n lists containing a random distribution of tuples where the first item is a url
#                         and the second is a default dictionary where key=tag value = frequency of occurance
'''
    clusteredUrls = [[] for x in xrange(numClusters)] # Courtesy of user 279627, Stack Overflow
    for entry in URL_DICT:
        loc = random.randint(0, numClusters - 1)
        clusteredUrls[loc].append((entry, URL_DICT[entry]))
    return clusteredUrls

def evenClusters(numClusters):
'''
# Set up for recursive clustering, uniformly distributing urls across n clusters
# Param: numClusters - the number of clusters to evenly distribute links across
# Return: clusteredUrls - a list of n lists containing a uniform distribution of tuples where the first item is a url
#                         and the second is a default dictionary where key=tag value = frequency of occurance
'''
    clusteredUrls = [[] for x in xrange(numClusters)] 
    divided = len(URL_DICT) / numClusters
    loc = 0
    step = 0
    for entry in URL_DICT:
        clusteredUrls[loc].append((entry, URL_DICT[entry]))
        step += 1
        if step >= divided:
            loc += 1
            step = 0
    return clusteredUrls

def calculateCentroids(clusterList):
'''
# Set up for recursive clustering, uniformly distributing urls across n clusters
# Param: numClusters - the number of clusters to evenly distribute links across
# Return: clusteredUrls - a list of n lists containing a uniform distribution of tuples where the first item is a url
#                         and the second is a default dictionary where key=tag value = frequency of occurance
'''
    centroidList = []
    for cluster in clusterList:
        centroid = c.defaultdict(int)
        for item in cluster:
            tags = item[1]
            for entry in tags:
                centroid[entry] += (float(tags[entry]) / float(len(cluster)))
        centroidList.append(centroid)
    return centroidList

def calculateCosineSimilarity(centroid, urlVector):
'''
# Calculate the cosine similiarity of any url's tags and that of a centroid for a given cluster
# Param: centroid - one averaged vector of tags for one cluster
#        urlVector - a dictionary of tags and their occurances for one url
# Return: cosineSimilarity - the similarity of occurance of tags shared between the two vectors
'''
    numerator = 0.0 
    squaredA = 0.0
    squaredB = 0.0
    count = 0;
    for item in urlVector:
        if item in centroid:
            a = float(urlVector[item])
            b = float(centroid[item])
            squaredA += float(math.pow(a,2))
            squaredB += float(math.pow(b,2))
            numerator += float(a*b)
            count += 1
    if count == 0:
        return 0
    else:
        return numerator / (math.sqrt(squaredA) * math.sqrt(squaredB))

def clusterMatch(clusterCentroids, vector, numClusters):
'''
# Find which cluster a url is best placed in given its current centroid
# Param: clusterCentroids - a list of n centroid vectors, stored as dictionaries of key=tag, value=average occurance
#        urlVector - a single url's dictionary of key=tags, value=occurance of tag
# Return: a sorted list of the similiarites of the vector
'''
    cosineSim = []
    index = 0;
    for centroid in clusterCentroids:
        similarity = calculateCosineSimilarity(centroid, vector)
        cosineSim.append((index, similarity))
        index += 1
    return sorted(cosineSim, key=lambda tup: tup[1], reverse=True) #sort by tuple's second value; courtesy of user 303180, stackOverflow

def reCluster(centroidList, numClusters):
'''
# Resort the clusters according to which centroid is closest
# Param: centroidList - a list of every cluster's centroid dictionary where key=tag, value=avg frequency of occurance
'''
    iterCount = 0
    avg = 0
    newClusters = [[] for x in xrange(numClusters)] 
    for url in URL_DICT:
        similaritiesList = clusterMatch(centroidList, URL_DICT[url], NUM_CLUSTERS)
        avg += similaritiesList[0][1]
        iterCount +=1
        if similaritiesList[0][1] == 0:
            newIndex = random.randint(0, numClusters-1)
        else:
            newIndex = similaritiesList[0][0]
        newClusters[newIndex].append((url, URL_DICT[url]))
    avg = avg/iterCount
    return newClusters, avg

def printClusterUrls(clusters):
    index = 0
    for cluster in clusters:
        print "Cluster", index, ":"
        index += 1
        for url in cluster:
            print url[0]
    
def solve():
''' # Solve for k-means with random distribution '''
    clusters = randomClusters(NUM_CLUSTERS) # each cluster is a list of tuples containing a string and a dict
    centroidList = calculateCentroids(clusters)
    index = 0
    while index < NUM_RESORTS:
        clusters, avg = reCluster(centroidList, NUM_CLUSTERS)
        centroidList = calculateCentroids(clusters)
        print "Sort number", index, "Average correlation", avg
        index += 1
    printClusterUrls(clusters)
    return  clusters, centroidList

def bestFit(centroid, cluster, showNumber):
'''
# Find which urls are the best represtatives of their cluster
# Param: centroid - the vector value of a cluster to compare urls agains
#        cluster - a list of urls and their dictionaries that contain tags and frequencies
#        showNumber - the number of urls to show as best representatives of their cluster
# Return: a sorted list that contains the n most representative urls
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
# Merge most similar groups evenly by step size
# Param: clusterList - the list of clusters to be merged
# Return: the new cluster list once all have been merged
# TODO: Look into ways of throwing out empty clusters because nothing will ever be saved there
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
# Test the application of a merging method of clustering, takes the total number of tags, distributes evenly
# accross a huge list of clusters and reduces down to num clusters
# Might want to look into a clever way of flexible step size for merging clusters together
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
    
URL_DICT = processUrls() # Dictionary of urls and their tags, and individual frequency of occurance
sortedClusters, centroidList = solve()
printBestItems(sortedClusters, centroidList)
clusters, centroidList = mergingTest()
printBestItems(clusters, centroidList)