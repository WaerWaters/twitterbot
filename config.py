
"""
Allowed to like 1000 tweets a day | 1000 / 24-hour
Allowed to retweet 300 tweets every 3 hours | 300 / 3-hour 180
Allowed to comment 300 tweets every 3 hours | 300 / 3-hour
Allowed to follow 400 users a day | 400 / 24-hour
If user auth, Allowed to search 180 times every 15-min | 180 / 15-min
If app auth, Allowed to search 450 times every 15 min | 450 / 15-min
"""


#, "cnft", "#cnftgiveaway", "cnftgiveaways", "#cnftgiveaways", "cnftgiveaway"


# Twitter API credentials. If you need any help have a look at README.md
twitter_credentials = {
    "consumer_key": '',
    "consumer_secret": '',
    "access_token": '',
    "access_secret": '',
}
# DON'T WRITE ANYTHING IN CAPS, AS THE BOT AUTOMATICALLY FLATTERS ALL INPUT TEXTS. THUS ANY WORD WITH CAPS WON'T BE RECOGNIZED
# Tags that Twitter will use to look up our tweets. Really important as all the script will be based on them
search_tags = ["cnftgiveaway", "cnftgiveaways", "nftgiveaway" ,"nftgiveaways"]
# Don't start the bot if friends weren't correctly retrieved
wait_retrieve = True
# Enable this if you want the bot to send a DM in case it detects any message_tags
use_msgs = False

#Ignore tweets that contain any of these words
BadList = ["throat","bone","naked","selfie","photo","onlyfans","nude","+18","femdom","fendom","whatsapp","sex","xxx","daddy","mommy","sugar","vid","#imgxnct","pic","tits" ,"booty" ,"boob", "freenude","cum", "dick" ,"gay" ,"onlyfans.com", "ass", "fuck", "suck", "cock", "lick","pussy" ]

# What words will the bot check in order to retweet a tweet. It's important because if the bot doesnt
# recognize any, it will skip the whole tweet and it wont check if it has to like, msg, or follow
retweet_tags = ["retweet", "rt"]
# What words will trigger to send the author a DM with a random message_text
message_tags = ["retweet", "rt"]
# What words will the bot check in order to follow the author of the tweet plus all the users mentioned in the text
# (we assume that a retweet tag was recognized)
follow_tags = ["follow", "fl"]
# What words will the bot look for in order to like a tweet (it also needs to contain a retweet tag)
like_tags = ["like", "fav", "favorite", "retweet", "rt"]
# These are supposed to be random msgs the bot would send if DMing is required
message_text = ["let's get this win", "let's win", "giveaway"]
# Add to this list all the users whose contests (actually tweets that contain retweet_tags keywords) the script will
# always skip (this is for the user's username, not name!) (username is the @ one)
# Variables related to avoiding users don't need to have a value
banned_users = []
# Same but but in this case applied to the author's name
banned_name_keywords = ["bot", "spotting", "spot", "spotter", "MegaGiveaways"]
# Search_rate means how long it'll have to wait to loop again after checking all tweets
search_rate = 2
# How long to wait to pass to next tweet + follow_rate or dm_rate if it has to follow or dm someone
retweet_rate = 20
# How long to wait after following someone. 1st time the diff is added, afterwards the entire rate is added to the sleep
follow_rate = 10
# Enable printing in colors
print_in_color = True
