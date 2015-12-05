import pytumblr, collections, pickle, tumblruser, warnings
USERDATA = "usernames.txt"
WRITETAGS = "ObjectTest.txt"
THRESHOLD = 2


def accessAPI(filename):
	''' # Open up an API client using a csv file for input '''
	info = open(filename, 'r')
	key, secret, usr, password = info.read().split(",")
	info.close()
	return pytumblr.TumblrRestClient(key, secret, usr, password)


def collectUserTags(iterations, allUsers ={}, usernames = []):
	''' # Holy nested loops batman! Update our fancy schmancy object dictionary '''
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
					if  len(objectPosts) < 100: #If it's full, just skip it.
						break
					printCount += 1
				offset += 20
			except: # Note the exception in case of error in reading in posts
				warnstring = "User", usr, "threw an exception"
				warnings.warn(warnstring, RuntimeWarning, stacklevel=2)
		# If a user gets updated, print the update
		if count > 0:
			print allUsers[usr]
		# Keep me from getting all neurotic
		if printCount > 400:
			print "Still working, not broken"
			printCount = 0
	return allUsers 


def primeData(noNames = False, resetTags = False):
	'''Set up data priming in a way that allows adjustments for data resets or lack of usernames '''
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
	objectDictionary = collectUserTags(5, userDict, usernames)

	
	# Save to file for later
	tagFile = open(WRITETAGS, 'w')
	pickle.dump(objectDictionary, tagFile)
	tagFile.close()



CLIENT = accessAPI("data.txt")
main()