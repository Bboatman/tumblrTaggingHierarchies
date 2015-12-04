import urllib
import json
import pytumblr
import pickle
import time
USRFILE = 'usernames.txt'
CLIENTFILE = 'data.txt'


def getUrls(doPrint=False):
    ''' Crawl trending page for starte blogs because tumblr api isn't
    written to produce random blogs because they suck '''
    basePage = "https://www.tumblr.com/explore/trending"
    keyWord = "\"dashboard_url\""  # Looking for the urls in the html
    handle = urllib.urlopen(basePage)
    html = handle.read()
    blogList = []
    for word in html.split(","):  # Grab blogspecific url
	    if word[:len(keyWord)] == keyWord:
	        url = word.split("/")[-1][:-1]
	        blogList.append(url)
	        if doPrint:
	        	for url in blogList:
	        		print url
    return blogList


def accessAPI(filename):
''' # Open up an API client using a csv file for input '''
	info = open(filename, 'r')
	key, secret, usr, password = info.read().split(",")
	info.close()
	return pytumblr.TumblrRestClient(key, secret, usr, password)


def makeBlogList(urlList, offset = 0):
''' # Generate a list of blogs  '''
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
				
	# Save it all to file
	nameFile = open(USRFILE, 'w')
	pickle.dump(usernames, nameFile)
	print "End length", len(usernames)
	nameFile.close()
	return sumAdded


def cleanList():
''' # Throw out defunct blogs and blogs with less than 20 posts '''
	userfile = open(USRFILE, 'r')
	usernames = pickle.load(userfile)
	userfile = userfile.close()
	makeBlogList(usernames) 


def main():
	runtime = 300
	now = time.time()
	breaktime = now + runtime # Don't let it run for more than five minutes for sanity's sake
	added = 1
	while added > 0 and now < breaktime:
		added = makeBlogList(getUrls())

	#cleanList # If you're getting a lot of exception warnings uncomement this to throw out bad blogs


client = accessAPI(CLIENTFILE)
main()
