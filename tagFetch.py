import pytumblr, collections, pickle, tumblruser, warnings
USERDATA = "usernames.txt"
WRITETAGS = "tagfile.txt"
THRESHOLD = 2

# Open up an API client using a csv file for input
def accessAPI(filename):
	info = open(filename, 'r')
	key, secret, usr, password = info.read().split(",")
	info.close()
	return pytumblr.TumblrRestClient(key, secret, usr, password)

# Holy nested loops batman! Update our fancy schmancy object dictionary
def rudimentaryTagVector(iterations, allUsers ={}, usernames = []):
	printCount = 0
	for usr in usernames:
		count = 0
		if usr not in allUsers:
			allUsers[usr] = tumblruser.User(usr)
		offset = 0
		# Search through n pages of posts where n is our number of iterations
		for step in range(iterations):
			try: # Catch any deactivated blogs, or blogs with less than n pages of posts
				posts = CLIENT.posts(usr, offset=offset)['posts']
				for post in posts:
					objectPosts = allUsers[usr].getPosts()
					if str(post['id']) not in objectPosts and len(objectPosts) < 100:
						if len(post['tags']) > 2:  #Ignore posts that don't have at least two tags
							allUsers[usr].addPost(post)
							count += 1
							printCount += 1
				offset += 20
			except: # Note the exception in case of error in reading in posts
				warnstring = "User", usr, "threw an exception"
				warnings.warn(warnstring, RuntimeWarning, stacklevel=2)
		# If a user gets update, print the update
		if count > 0:
			print allUsers[usr]
		# Keep me from getting all neurotic
		if printCount % 200 == 0:
			print "Still working, not broken"
	return allUsers 

# Set up data priming in a way that allows adjustments for data resets or lack of usernames
def primeData(noNames = False, resetTags = False):
	if noNames:
		usernames = []
	else:
		userFile = open(USERDATA, 'r')
		usernames = pickle.load(userFile)
		userFile.close()

	if resetTags:
		userDict = {}
	else:
		tagFile = open(WRITETAGS, 'r')
		userDict = pickle.load(tagFile)
		tagFile.close
	return userDict, usernames

def main():
	userDict, usernames = primeData()
	objectDictionary = rudimentaryTagVector(5, userDict, usernames)
	
	# Save to file for later
	tagFile = open(WRITETAGS, 'w')
	pickle.dump(objectDictionary, tagFile)
	tagFile.close()



CLIENT = accessAPI("data.txt")
main()