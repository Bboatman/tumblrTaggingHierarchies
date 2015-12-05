import collections
class User:
	def __init__(self, username):
		self.userId = username
		self.tagDict =  {}
		self.posts = []

	def __cmp__ (self, x):
		if type(self) != type(x):
			return -1
		else:
			if self.userId == x.userId:
				return 0
			else:
				return 1

	def __str__(self):
		return self.userId + ", Number of Posts: " + str(len(self.posts)) + ", Number of unique tags: " + str(len(self.tagDict.keys())) 

	def addPost(self, tumblrPost):
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

	