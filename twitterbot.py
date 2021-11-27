#!/usr/bin/env python
import tweepy
import logging
import json
import time
import random
import requests
import os
#from our keys module (keys.py), import the keys dictionary
import config


# Does so the code shows up synchronously instead of only at the end of the execution
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
import sys
sys.stdout = Unbuffered(sys.stdout)

# Output text color
class colors:
    HEADER = '\033[95m' if config.print_in_color else ""
    OKBLUE = '\033[94m' if config.print_in_color else ""
    OKGREEN = '\033[92m' if config.print_in_color else ""
    WARNING = '\033[93m' if config.print_in_color else ""
    FAIL = '\033[91m' if config.print_in_color else ""
    ENDC = '\033[0m' if config.print_in_color else ""
    BOLD = '\033[1m' if config.print_in_color else ""
    UNDERLINE = '\033[4m' if config.print_in_color else ""

# Authentication 
auth = tweepy.OAuthHandler(config.twitter_credentials["consumer_key"], config.twitter_credentials["consumer_secret"])
auth.set_access_token(config.twitter_credentials["access_token"], config.twitter_credentials["access_secret"])
api = tweepy.API(auth)

screen_name = api.verify_credentials().screen_name

friends = []

# Get friends
while len(friends) is not api.get_user(screen_name=screen_name).friends_count:
	try:
		f = api.get_friends(screen_name=screen_name, count=2000)
		friends = [x.screen_name for x in f]
		print(colors.OKGREEN + "Friends retrieved successfully")
		break
	except Exception as e:
		# Friends couldn't be retrieved
		print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
		print(colors.FAIL + colors.BOLD + "Couldn't retrieve friends. The bot won't unfollow someone random when we start"
                                            " following someone else. So your account might reach the limit (following 200"
                                            " users)" + colors.ENDC)
		if config.wait_retrieve is False:
			break
		time.sleep(600)

def check():
	print(colors.OKGREEN + "Started Analyzing (" + str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) + ":" + str(
        time.gmtime().tm_sec) + ")")
	# Retrieving the last 1000 tweets for each tag and appends them into a list
	just_retweet_streak = 0
	searched_tweets = []
	for x in config.search_tags:
		searched_tweets += api.search_tweets(q=x, count="100", result_type="recent", tweet_mode="extended")
		#print(json.dumps(searched_tweets[0]._json, indent=4))
	
	for tweet in searched_tweets:
		# Check if tweet contains any of the bad words in badlist
		Bad = False
		for BadWord in config.BadList:
			if (tweet._json["full_text"].lower().find(BadWord) != -1):
				Bad = True

		# only retweet if tweet has more than 20 retweets
		if tweet._json["retweet_count"] > 5:
			if not (Bad): # If tweet doesn't contain bad words
				# The script only cares about contests that require retweeting
				if any(x in tweet._json["full_text"].lower().split() or x in tweet._json["entities"]["hashtags"] for x in config.retweet_tags):
					#print(json.dumps(tweet.retweeted_status.user))
					# This clause checks if the text contains any retweet-tags
					if tweet._json["retweeted_status"] is not None:
						# In case it is a retweet, we switch to the original one
						if any(x in tweet._json["retweeted_status"]["full_text"].lower().split() for x in config.retweet_tags):
							tweet = tweet._json["retweeted_status"]
						else:
							continue
					if tweet["user"]["screen_name"].lower() in config.banned_users or any(x in tweet["user"]["name"].lower() for x in config.banned_name_keywords):
						# If it's the orignal one, we check if the author is banned
						print(colors.WARNING + "Avoided user with ID: " + tweet["user"]["screen_name"] + " & Name: " + tweet["user"]["name"] + colors.ENDC)
						
						continue

					try:
						# RETWEET
						# This is ran under a try clause because there's always an error when trying to retweet something
                        # already retweeted. So if that's the case, the except is called and we skip this tweet
                        # If the tweet wasn't retweeted before, we retweet it and check for other stuff
						api.retweet(id=tweet["id"])
						print(colors.OKBLUE + "Retweeted " + str(tweet["id"]))
						just_retweet_streak += 1


						# REPLY
						if any(x in tweet["full_text"].lower() for x in config.like_tags):
							sn = tweet["user"]["screen_name"]
							m = "@%s @aungchanphyo222 @james_7793 @HtetKaungLatt @MoeSoeNaing @AzPhyo7 @komyogyiie111 @Vish_uuu @Mrinali_Shetty @Varun_Agro @egemendis @BryamZr @borsathugger" % (sn)
							api.update_status(m, in_reply_to_status_id=tweet["id"])
							print("replied to: @" + tweet["user"]["screen_name"])


						# LIKE
						try:
							# So we don't skip the tweet if we get the "You have already favorited this status." error
							if any(x in tweet["full_text"].lower() for x in config.like_tags):
								# If the tweets contains any like_tags, it automatically likes the tweet
								api.create_favorite(id=tweet["id"])
								print("Liked: " + str(tweet["id"]))
								just_retweet_streak = 0
						except:
							pass	


						# FOLLOW
						if any(x in tweet["full_text"].lower() for x in config.follow_tags):
							# If the tweet contains any follow_tags, it automatically follows all the users mentioned in the
                            # tweet (if there's any) + the author
							addFriends = []
							#print(json.dumps(api.get_user(screen_name=screen_name)._json, indent=4))
							friends_count = api.get_user(screen_name=screen_name)._json["friends_count"]
							
							if tweet["user"]["screen_name"] not in friends:
								print("Followed: @" + tweet["user"]["screen_name"])
								api.create_friendship(screen_name=tweet["user"]["screen_name"])
								addFriends.append(tweet["user"]["screen_name"])
								just_retweet_streak = 0
								time.sleep(config.follow_rate - config.retweet_rate if config.follow_rate > config.retweet_rate else 0)
							for name in tweet["entities"]["user_mentions"]:
								if name["screen_name"] in friends or name["screen_name"] in addFriends:
									print("Already following: @" + name["screen_name"])
									continue
								print("Followed: @" + name["screen_name"])
								api.create_friendship(screen_name=name["screen_name"])
								addFriends.append(name["screen_name"])
								just_retweet_streak = 0
								time.sleep(config.retweet_rate)
							# Twitter sets a limit of not following more than 2k people in total (varies depending on followers)
                            # So every time the bot follows a new user, its deletes another one randomly
							if friends_count >= 2000:
								while friends_count < api.get_user(screen_name=screen_name)["friends_count"]:
									try:
										x = friends[random.randint(0, len(friends) - 1)]
										print("Unfollowed: @" + x)
										api.destroy_friendship(screen_name=x)
										friends.remove(x)
									except Exception as e:
										print(e)
							friends.extend(addFriends)
						# Max is 2400 tweets per day in windows of half an hour. Thus, 36s as interval guarantees as we won't
                        # pass that amount
						time.sleep(config.retweet_rate * (just_retweet_streak + 1))
					except Exception as e:
						# In case the error contains sentences that mean the app is probably banned or the user over daily
                        # status update limit, we cancel the function
						if "retweeted" not in str(e):
							print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
							return
					# And continues with the next item
	print(colors.OKGREEN + "Finished Analyzing (" + str(len(searched_tweets)) + " tweets analyzed")
	

while True:
	print("\n")
	try:
		check()
	except Exception as e:
		print(colors.FAIL + colors.BOLD + str(e) + colors.ENDC)
		time.sleep(100*len(config.search_tags))
	# This is here in case there were no tweets checked
	time.sleep(2*len(config.search_tags))


