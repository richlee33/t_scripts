# Gets a list of tweets containing word(s) and if the tweet author follows a certain account
# Usage:
# gettweetfollows.py -w <list of words to search for in tweet>
# Optionally check if tweet author follows an account:
# gettweetfollows -w <list of words to search for> -f <account to verify is being followed>
# Example:
# $ python gettweetfollows.py -w "#bayc" "#giveaway" -f midnightwrench
# Output:
# a csv file tweet_list.csv containing a list of tweets containing search words and a False or True column if tweet author follows account
# Help example:
# $python gettweetfollowspy -h
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
    parser.add_argument("-f", "--follows", nargs='?', help="account to check if followed by tweet author")
    parser.add_argument("-p", "--print", action="store_true", default=False, help="print tweets to screen")
    args = parser.parse_args()

    #read search words from command line.  if there are none, exit
    if len(args.words) < 1:
        print("Error, missing words to search for")
        return

    #handle case where the is 1 word to search
    if (isinstance(args.words, str)):
        search_words.append(args.words)
    else:
        search_words = args.words

    if (args.follows is None):
        follow_option = False
    elif (isinstance(args.follows, str)):
        follow_option = True
        follows_username = args.follows
    elif len(args.follows) > 1:
        print("Sorry only 1 account to follow is supported")
        return

    print("Searching tweets for the word(s):")
    print(search_words)

    if follow_option == True:
        print("Checking for users following account %s" %follows_username)

    ######################################
    #get followers of an account
    #
    my_api = TApi()

    if follow_option == True:
        result_followers = my_api.get_followers(follows_username)
        if result_followers is None:
            follow_option = False
        else:
            print("Number of followers of %s: %d" %(follows_username, len(result_followers)))


    ######################################
    # get tweets containing desired word
    #
    tweet_list = my_api.get_tweets(search_words, result_followers)


    #print to screen the list of tweets
    if args.print:
        for item in tweet_list:
            #print("%s, %s, %s" %(item['username'], item['created_at'], item['text']))
            print(item)

    #output to file if there are tweets found containg the word
    if (len(tweet_list) > 0):
        with open(csv_file_name, 'w', encoding="utf-8") as f:
            if follow_option == True:
                f.write("%s,%s,%s,%s\n" % ("username", "tweet_dt_utc", "follows_" + follows_username, "text"))
                for item in tweet_list:
                    f.write("%s,%s,%s,%s\n" % (item['username'], item['created_at'], item['follows'], item['text']))
                print("Tweets and whether or not author follows account saved to %s." %csv_file_name)

            else:
                f.write("%s,%s,%s\n" % ("username", "tweet_dt_utc", "text"))
                for item in tweet_list:
                    f.write("%s,%s,%s\n" % (item['username'], item['created_at'], item['text']))
                print("Tweets saved to %s" %csv_file_name)

if __name__ == "__main__":
    main()
