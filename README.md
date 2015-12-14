# tumblrTaggingHierarchies
Repository for Rebecca Gold and Brooke Boatman undergraduate capstone work on tagging hierarchy formation and data clustering visualizations

usernameCollector.py: Grab usernames from the trending page for pseudorandom collections of user posts

tagFetch.py: Walk through the last n posts (default is 100) and collect data on tag co-occurance frequency

tumblruser.py: Classes to make the organization of clustering and tag vector manipulation more managable

	Includes: User, TagVector, and TagCluster classes
	
kMeansClustering.py: Generate random clusters of tags and recursively resort n times (default is 10) before calculating every tag's distance from every cluster, then compressing those values into 2 dimensional points for visualizing similarities.
