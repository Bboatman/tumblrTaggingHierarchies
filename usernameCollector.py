import urllib, json, pytumblr, pickle, time
USRFILE = 'usernames.txt'
CLIENTFILE = 'data.txt'


def getUrls():
    ''' 
    Crawl trending page for starter blogs because tumblr api isn't
    written to produce random blogs because they suck (but we still love them anyways)
    '''
    basePage = "https://www.tumblr.com/explore/trending"
    keyWord = "\"dashboard_url\""  # Looking for the urls in the html
    handle = urllib.urlopen(basePage)
    html = handle.read()
    blogList = []
    for word in html.split(","):  # Grab blogspecific url
	    if word[:len(keyWord)] == keyWord:
	        url = word.split("/")[-1][:-1]
	        blogList.append(url)
    return blogList


def accessAPI(filename):
	''' 
	Open up an API client without directly needing to input credentials
	so I can share my code
	Param: filename - the .txt file that contains the api credentials
	'''
	info = open(filename, 'r')
	key, secret, usr, password = info.read().split(",")
	info.close()
	return pytumblr.TumblrRestClient(key, secret, usr, password)


def makeBlogList(urlList, offset = 0):
	''' 
	Generate a list of blogs usernames for later processing 
	Param: urlList - if a list of blogs to be added to the USRFILE
		   offset - number of pages to troll through looking for posts 
		   			they've reblogged to get more usernames 
	TODO: may not actually be worth it computationally to look for reblogs, 
		  need to look into marginal benifit
	'''
	nameFile = open(USRFILE, 'r')
	usernames = pickle.load(nameFile)
	nameFile.close()
	print "Start length", len(usernames)
	sumAdded = 0
	for url in urlList:
		try: 				
			rawPosts = client.posts(url, offset=offset)
			allPosts = rawPosts['posts']
			for post in allPosts:
				if 'post_author' in post.keys():  # This one gets the original author if the poster reblogged the post
					name = item['post_author'].encode('utf-8')
					if name not in current:
						usernames.append(name)
						sumAdded += 1
				name = post['blog_name'].encode('utf-8') # Get the name of the poster
				if name not in usernames and offset == 0: # If a user no longer exists remove them from the list
					usernames.append(name)
					sumAdded += 1
		except: # This catches bad entries into our user table, deactivated accounts usually, and removes them from the file
			if url in usernames and offset == 0:
				usernames.remove(url)
				print "Removed user", url
				
	# Save it all to file and visually show change
	nameFile = open(USRFILE, 'w')
	pickle.dump(usernames, nameFile)
	print "End length", len(usernames)
	nameFile.close()
	return sumAdded


def cleanList():
	''' 
	Run through complete list without offset to throw out defunct blogs 
	blogs with less than 20 posts or anything else that throws warnings
	'''
	userfile = open(USRFILE, 'r')
	usernames = pickle.load(userfile)
	userfile = userfile.close()
	makeBlogList(usernames) 


def main():
	runtime = 40 
	sampleRate = 10
	now = time.time()
	breaktime = now + runtime # Don't let it run for more than five minutes for sanity's sake
	added = 1
	sampleTime = 10 + now
	while time.time() < breaktime:
		now = time.time()
		if now > sampleTime:
			added = makeBlogList(getUrls())
			sampleTime += sampleRate

	#cleanList # If you're getting a lot of exception warnings uncomement this to throw out bad blogs


client = accessAPI(CLIENTFILE)
main()
