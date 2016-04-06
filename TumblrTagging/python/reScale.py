from sklearn import cluster
import numpy as np
import htmlwrite
import random

IMGSIZE = 2000

def readInData(filename):
	pointList = []
	with open(filename, 'r') as dataFile:
		for line in dataFile.readlines():
			rawData = line[1:len(line) - 3]
			listItem = rawData.split(', ')
			listItem[0] = float(listItem[0]) / 30
			listItem[1] = float(listItem[1]) / 30
			listItem[2] = listItem[2][1:len(listItem[2])-1]
			pointList.append(tuple(listItem[0:3]))
	return pointList

def reSize(indexList):
	if len(indexList) > 0:
		if len(indexList[0]) == 2:
			point, label = zip(*indexList)
			x,y = zip(*point)
		elif len(indexList[0]) == 3:
			x, y, label = zip(*indexList)
		else:
			return []
	else:
		return []
	maxVal = max(x) if max(x) > max(y) else max(y)
	spread = IMGSIZE / (maxVal * 2)
	avgDist = abs(np.average(np.diff(x + y)))
	scaleVal =  spread if spread > .02/avgDist else .02 / avgDist
	x = [loc * scaleVal for loc in x]
	y = [loc * scaleVal for loc in y]
	subtract = min(x) if min(x) < min(y) else min(y)

	x = [int(loc - subtract + 5) for loc in x]
	y = [int(loc - subtract + 5) for loc in y]
	pointList = zip(x,y)
	itemList = zip(pointList,label)
	print(max(x), max(y))
	print("avg difference", avgDist)
	return list(itemList), avgDist

def visualCluster(indexList, htmlFile):
    indexList, avgDist = reSize(indexList)
    approxClusters = int(len(indexList) * avgDist)
    print(approxClusters, "Clusters")
    affinity = cluster.AgglomerativeClustering(n_clusters=300)
    points, labels = zip(*indexList)
    clusters = affinity.fit_predict(points)
    hues = [360/max(clusters) * x for x in clusters]
    litRange = [random.randint(80,95) for x in range(max(clusters + 1))]
    lits = [litRange[x] for x in clusters]
    writeList = list(zip(points, labels, hues, lits))
    
    displayFile = open(htmlFile, "w")
    dataFile = open("./data.txt", "w")
    displayFile.write(htmlwrite.getTop())
    for entry in writeList:
        try:
            point, label, hue, lit = entry
            x,y = point
            writeStr = "[" + str(x) + ", " + str(y) + ", "+ '\"' + label + '\"' + ", " + str(int(hue)) + ", " + str(lit) + "],\n"
            displayFile.write(writeStr)    
            dataFile.write("[" + str(x) + ", " + str(y) + ", "+ '\"' + label + '\"' + "],\n")
        except(UnicodeEncodeError): 
            print("Failed to write")
    
    displayFile.write(htmlwrite.getBottom())
    dataFile.close()
    displayFile.close()

def rescaleNoRecluster(dataFile, htmlFile):
	pointList = readInData(dataFile)
	visualCluster(pointList, htmlFile)
	print(pointList[0])