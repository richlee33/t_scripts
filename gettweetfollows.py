# Usage:
# python gettweetfollows.py <list of strings to search for>
# Optionally check if tweet follows an account:
# python gettweetfollows <list of strings to search for> -f <account name to verify is followed>
# $ python gettweetfollows.py #deeznuts3d giveaway -f deeznutznft
# roughly based off twitter sample code:
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import sys
import json
import datetime
from t_api import TApi

default_hashtag = "#deeznutsnft"

def main():

    followers_list = []
    hashtags_list = []
    tweet_list = []

    follow_option = False    #optionally get the list of followers
    follows_username = None  #twitter acccout a user needs to follow


    #read strings from command line.  if there are none, use default
    if len(sys.argv) == 1:
        hashtags.append(default_hashtag)
    else:
        for item in range(1, len(sys.argv)):
            if sys.argv[item] == "-f":
                follow_option = True
            elif follow_option is True:
                follows_username = sys.argv[item]
            else:
                hashtags_list.append(sys.argv[item])

    print("Searching for the terms:")
    print(hashtags_list)
    if follow_option == True:
        print("Checking for users following account:")
        print(follows_username)


    ######################################
    #get followers of an account
    #
    my_api = TApi()

    if follow_option == True:
        followers_list = my_api.get_followers(follows_username)
        print(followers_list)
        print("number of followers in list is: %d" %len(followers_list))


    ######################################
    # get tweets containing desired string
    #
    tweet_list = my_api.get_tweets(hashtags_list, followers_list)

    #print to screen the list of tweets
    for item in tweet_list:
        #print("%s, %s, %s" %(item['username'], item['created_at'], item['text']))
        print(item)

    #output to file
    with open('deeztweets_follow_test.txt', 'w', encoding="utf-8") as f:
        if follow_option == True:
            f.write("%s,%s,%s,%s\n" % ("username", "tweet_dt_utc", "follows_" + follows_username, "text"))
            for item in tweet_list:
                f.write("%s,%s,%s,%s\n" % (item['username'], item['created_at'], item['follows'], item['text']))
        else:
            f.write("%s,%s,%s\n" % ("username", "tweet_dt_utc", "text"))
            for item in tweet_list:
                f.write("%s,%s,%s\n" % (item['username'], item['created_at'], item['text']))

if __name__ == "__main__":
    main()
