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

# comma separated list of phrases to follow
# TODO need method to build this list
#track = "things"


# results in list of tweets from the google spreadsheet
list_of_tweets = get_tweetlist()

# results in list of user IDs to follow
user_ID_list = get_userIDlist()

# process list of IDs into string
id_string = ""
for i in user_ID_list:
    id_string = id_string + i
    id_string = id_string + ","

id_string = id_string[:-1]

# results in list of terms to track
term_track_list = get_track_list()
pp.pprint(term_track_list)

term_string = ""
for i in term_track_list:
	term_string = term_string + i
	term_string = term_string + ","

term_string = id_string[:-1]



# create stream
twitter_stream = TwitterStream(auth = auth)
# pass follow list to stream
iterator = twitter_stream.statuses.filter(follow = id_string, track = term_string)
# stream tweets from and to all users on the list
for tweet in iterator:
	try:
		# TODO evaluate tweet method, choose from database
		pp.pprint(tweet['text'])
	except AttributeError:
		pass
	except KeyError:
		pass



