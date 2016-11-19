#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter import *
import pprint as pp
from quickstart import *
 

auth = OAuth(
	consumer_key = 'xFre00lK9fqxswhS4vcT5Ztj3',
	consumer_secret = 'dM4qUBaS24jRBB65XgMYJIHkbmY4syAKx11FJ4XO4kbtUAQlpZ',
	token = '800047930459594752-DmKz6JefS5HYdqYA6ihk7j0J4LWdMRU',
	token_secret = 'drj6w5CywOLwAWGNjhnhm7QdacJgWXoi8XbfaD0exTKeP'
)

# TODO build this list from database of user ID
follow = "25073877,20733972,7270292,18061669"

# comma separated list of phrases to follow
# TODO need method to build this list
#track = "things"


# results in list of tweets from the google spreadsheet
list_of_tweets = get_tweetlist()
print(list_of_tweets)

# create stream
twitter_stream = TwitterStream(auth = auth)
# pass follow list to stream
iterator = twitter_stream.statuses.filter(follow = follow)
# stream tweets from and to all users on the list
for tweet in iterator:
	try:
		# TODO evaluate tweet method, choose from database
		pp.pprint(tweet['text'])
	except AttributeError:
		pass
	except KeyError:
		pass



