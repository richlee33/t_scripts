# Usage:
# gettweetfollows.py -w <list of words to search for>
# Optionally check if tweet follows an account:
# gettweetfollows -w <list of words to search for> -f <account name to verify is followed>
# $ python gettweetfollows.py -w "#bayc" "#giveaway" -f midnightwrench
# Output:
# a csv file tweet_list.csv containing a list of tweets containing search words and a False or True column if user is followed
# roughly based off twitter sample code:
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import sys
import json
import datetime
import argparse
from t_api import TApi

def main():

    search_words = []
    result_followers = []
    result_tweets = []

    follow_option = False    #optionally get the list of followers
    follows_username = None  #twitter acccout a user needs to follow

    csv_file_name = "tweet_list.csv"

    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--words", nargs='+', help="words to search for in a tweet", required=True)
    parser.add_argument("-f", "--follows", nargs='?', help="account to check of user follows")
    args = parser.parse_args()

    #read search words from command line.  if there are none, exit
    if len(args.words) < 1:
        print("Error missing words to search for")
        return

    #handle case where the is 1 word to search
    if (isinstance(args.words, str)):
        search_words.append(args.words)
    else:
        search_words = args.words

    print(args.words)
    print(args.follows)

    if (isinstance(args.follows, str)):
        follow_option = True
        follows_username = args.follows
    elif len(args.follows) > 1:
        print("Sorry only 1 account to follow is supported right now")
        return

    print("Searching tweets for the word(s):")
    print(search_words)

    if follow_option == True:
        print("Checking for users following account:")
        print(follows_username)


    ######################################
    #get followers of an account
    #
    my_api = TApi()

    if follow_option == True:
        result_followers = my_api.get_followers(follows_username)
        print("number of followers in list is: %d" %len(result_followers))


    ######################################ßßß
    # get tweets containing desired string
    #
    tweet_list = my_api.get_tweets(search_words, result_followers)

    #print to screen the list of tweetsßßß
    for item in tweet_list:
        #print("%s, %s, %s" %(item['username'], item['created_at'], item['text']))
        print(item)

    #output to file
    with open(csv_file_name, 'w', encoding="utf-8") as f:
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
