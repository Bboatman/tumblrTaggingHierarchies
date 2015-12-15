# tumblrTaggingHierarchies
Repository for Rebecca Gold and Brooke Boatman undergraduate capstone work on tagging hierarchy formation and data clustering visualizations

Python Files:
- usernameCollector.py: Grab usernames from the trending page for pseudorandom collections of user posts
- tagFetch.py: Walk through the last n posts (default is 100) and collect data on tag co-occurance frequency
- tumblruser.py: Classes to make the organization of clustering and tag vector manipulation more managable
	- Includes: User, TagVector, and TagCluster classes
- kMeansClustering.py: Generate random clusters of tags and recursively resort n times (default is 10) before calculating every tag's distance from every cluster, then compressing those values into 2 dimensional points for visualizing similarities.

TODO:
- Look into python processes to speed everything up
- Figure out how to separate overlapping tags for greater visibility
- Keep track of which users a tag belongs to to further visualize clustering success
- Color code tag tesselations based on which user said that tag most
- Draw bounding borders of clustered tesselations
