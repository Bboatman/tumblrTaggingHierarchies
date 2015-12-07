import collections
class User(object):
	def __init__(self, username):
		self.userId = username
		self.tagDict =  {}
		self.posts = []


	def __str__(self):
		return self.userId + ", Number of Posts: " + str(len(self.posts)) + ", Number of unique tags: " + str(len(self.tagDict.keys())) 


	def addPost(self, tumblrPost):
		''' 
		Update a user object with a tumblr post
		Param: tumblrPost - a single post's dictionary from the pytumblr api client
		'''
		tagList = tumblrPost['tags'] # Duplicate for length counting purposes
		newList = tumblrPost['tags']
					
		for x in range(len(tagList)): # When you're popping things off lists, it gets weird, this prevents that
			tag = tagList[0].encode('utf-8')
			if tag in newList: # Get the list of all tags that have cooccured with the tag we just got, add it to the dict
				if tag not in self.tagDict:
					self.tagDict[tag] = collections.Counter()
				newList.remove(tag)
				for word in newList:
					self.tagDict[tag][word] += 1
				newList.append(tag)
		self.posts.append(str(tumblrPost['id']))		


	def getName(self):
		return self.userId


	def getTags(self):
		return self.tagDict


	def getPosts(self):
		return self.posts


class TagVector(object):
	""" 
	A vector object to hold information about a specific 
	tag for cosine similarity processing and clustering
	"""
	def __init__(self, name, counter = collections.Counter()):
		self.tagName = name
		self.tagCount = counter


	def __str__(self):
		return self.tagName

	def updateVector(self, tagCollection):
		""" Update a vector with a new collection of data """
		self.tagCount += tagCollection

	def getName(self):
		return self.tagName


	def setName(self, name):
		self.tagName = name
	

class TagCluster(object):
	""" Cluster for hierarchical ranking of tag vectors"""
	def __init__(self):
		self.memberList = []
		self.rawVector = collections.Counter()
		self.centroid = collections.defaultdict(float)


	def __str__(self):
		returnString = ""
		for tag in self.memberList[:-1]:
			returnString += (tag + ", ")
		returnString += self.memberList[-1]
		return returnString


	def wipeMembers(self):
		self.memberList = []
		self.rawVector = collections.Counter()


	def addMember(self, tagVector):
		self.memberList.append(tagVector.getName())
		self.rawVector += tagVector.tagCount
		frac = float(len(self.memberList))
		for tag in self.rawVector:
			self.centroid[tag] = float(self.rawVector[tag]) / frac

		



