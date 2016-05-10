''' 
Author: Brooke Boatman
Date: April 2016
Auto-rescale visualization for best fit in the window frame
'''

import htmlWrite
import numpy as np

from random import randint
from sklearn import cluster
from sklearn.datasets import make_blobs
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score


IMGSIZE = 2000

def readInData(filename):
	''' 
	Read in tag point location and coloring values
	Param: filename - the .txt file that contains the coloring and 
					  location values of tag points
	'''
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
	''' 
	Reflexively resize for best spacing and legibility
	Param: indexList - an array that contains the coloring and 
					   location values of tag points
	'''
	# Standardize possible inputs or break
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

	# Scale  for best fit
	maxVal = max(x) if max(x) > max(y) else max(y)
	spread = IMGSIZE / (maxVal * 2)
	avgDist = abs(np.average(np.diff(x + y)))
	scaleVal =  spread if spread > .02/avgDist else .02 / avgDist
	x = [loc * scaleVal for loc in x]
	y = [loc * scaleVal for loc in y]
	subtract = min(x) if min(x) < min(y) else min(y)

	# Write to file and repredict cluster coloring
	x = [int(loc - subtract + 5) for loc in x]
	y = [int(loc - subtract + 5) for loc in y]
	numClusters = predictNumClusters(x,y)

	# Zip back together, print results and return
	pointList = zip(x,y)
	itemList = zip(pointList,label)
	print(max(x), max(y))
	print("avg difference", avgDist)
	print("num clusters", numClusters)
	return list(itemList), avgDist, numClusters

def predictNumClusters(x, y):
	''' 
	Optimize the cluster coloring based on rescaled data
	through iterative reclustering in KMeans
	Param: x - an array of x values for point location
		   y - an array of y values for point location
	'''
	X = np.array(list(zip(x,y)))
	range_n_clusters = range(5, len(x) // 3, 3)
	bestFit = 0
	numClusters = 0

	for n_clusters in range_n_clusters:
		clusterer = MiniBatchKMeans(n_clusters=n_clusters, random_state=10)
		cluster_labels = clusterer.fit_predict(X)
		silhouette_avg = silhouette_score(X, cluster_labels)

		# Keep track of best fit and return if greater than 90% matching
		if silhouette_avg > bestFit:
			print(silhouette_avg, "with k =", n_clusters)
			numClusters = n_clusters
			bestFit = silhouette_avg
			if silhouette_avg >= .9:
				return numClusters
	return numClusters

def visualCluster(indexList, htmlFile):
	''' 
	Rewrite the visualizer HTML File
	Param: indexList - an array of index values for point location
		   htmlFile - a HTML filename to overwrite or write to
	'''
	indexList, avgDist, numClusters = reSize(indexList)
	affinity = cluster.AgglomerativeClustering(n_clusters = numClusters)
	points, labels = zip(*indexList)
	clusters = affinity.fit_predict(points)
	hues = [360/max(clusters) * x for x in clusters]
	litRange = [randint(80,95) for x in range(max(clusters + 1))]
	lits = [litRange[x] for x in clusters]
	writeList = list(zip(points, labels, hues, lits))
	
	displayFile = open(htmlFile, "w")
	dataFile = open("./data/data.txt", "w")
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