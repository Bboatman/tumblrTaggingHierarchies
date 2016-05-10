''' 
Author: Brooke Boatman
Date: December 2015
Tag collector for gathering data from tumblr posts
'''

import pytumblr
import collections 
import pickle
import tumblruser
import warnings 
import random

USERDATA = "../data/usernames.txt"
WRITETAGS = "../data/tagfile.txt"
APIKEYS = "../data/data.txt"
THRESHOLD = 2
POST_LIM = 100
SAMPLE_SIZE = 150

def accessAPI(filename):
	''' 
	Open up an API client without directly needing to input credentials
	so I can share my code
	Param: filename - the .txt file that contains the api keys
	'''
	info = open(filename, 'r')
	key, secret, usr, password = info.read().split(",")
	info.close()
	return pytumblr.TumblrRestClient(key, secret, usr, password)


def collectUserTags(iterations, allUsers = {}, usernames = []):
	''' 
	Holy nested loops batman! Add unseen posts to user object 
	Param: iterations - the number of pages (each conatining 20 posts) to look through
		   allUsers - the tumblruser object dictionary being updated
		   usernames - the list of usernames to be processed
	Return: allUsers - an updated tumblruser object dictionary
	'''
	printCount = 0
	for usr in usernames:
		count = 0
		if usr not in allUsers:
			allUsers[usr] = tumblruser.User(usr)
		offset = 0

		# Search through n pages of posts where n is our number of iterations 
		for step in range(iterations):
			try:
				objectPosts = allUsers[usr].getPosts()
				if  len(objectPosts) >= POST_LIM: #If user has hit post limit, just skip them
						break
				posts = CLIENT.posts(usr, offset=offset)['posts']
				for post in posts:
					if str(post['id']) not in objectPosts and len(objectPosts) < POST_LIM:
						if len(post['tags']) > THRESHOLD:  #Ignore posts that don't have at least THRESHOLD tags
							allUsers[usr].addPost(post)
							count += 1
					printCount += 1
				offset += 20
			except: # Note the exception in case of error in reading in posts
				# This is usually due to deactivated users or users with less than 20 posts
				warnstring = "User", usr, "threw an exception"
				warnings.warn(warnstring, RuntimeWarning, stacklevel=2)

		# If a user gets updated, print the update
		if count > 0:
			print(allUsers[usr])
	return allUsers 


def primeData(noNames = False, noTags = False):
	'''
	Set up data priming in a way that allows adjustments for data resets or lack of usernames 
	Param: noNames - boolean value indicating if there exists a file of usernames available for usernames
		   noTags - boolean value indicating if a file of tumblruser objects exists to be updated
		   			   this is good for reseting tags if the data set somehow gets mucked up
	Return: userDict - a dictionary of user objects 
			usernames - a list of usernames
	'''

	if noNames:
		usernames = []
	else:
		userFile = open(USERDATA, 'r')
		usernames = pickle.load(userFile)
		userFile.close()

	if noTags:
		userDict = {}
	else:
		tagFile = open(WRITETAGS, 'r')
		userDict = pickle.load(tagFile)
		tagFile.close
	return userDict, usernames


def main():
	userDict, usernames = primeData(noTags=True)
	usernames = random.sample(usernames, SAMPLE_SIZE)
	objectDictionary = collectUserTags(5, userDict, usernames) #Get the last 100 posts from every user

	
	# Save to file for later
	tagFile = open(WRITETAGS, 'w')
	pickle.dump(objectDictionary, tagFile)
	tagFile.close()
	count = 0
	printstr = ""


CLIENT = accessAPI(APIKEYS)
main()