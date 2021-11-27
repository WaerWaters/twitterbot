import tweepy


friends = ["martin", "charlotte", "mai", "sia", "daniel"]
check_friends = ["daniel", "bitch", "ho"]

for name in check_friends:
    if name in friends:
        print("Already following: @" + name)
        continue
    print("Followed: @" + name)
    friends.append(name)
    just_retweet_streak = 0
    print(friends)