# Usage:
# python gettweet.py <list of hashtags to search for>
# python gettweet.py #deeznuts3d
# based off twitter sample code:
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import os
import sys
import requests
import json
import time
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

tweet_list = []
search_url = "https://api.twitter.com/2/tweets/search/recent"
hashtags = []
default_hashtag = "#deeznutsnft"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields

def get_query_params(query_string, next_token = None):
    if next_token == None:
        query_params = {'query': query_string, 'tweet.fields': 'created_at', 'expansions': 'author_id'}
    else:
        query_params = {'query': query_string, 'tweet.fields': 'created_at', 'expansions': 'author_id', 'next_token' : next_token}
    return query_params

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def process_response(resp):
    for item in resp['data']:
        tweet = {}
        tweet['author_id'] = item['author_id']
        tweet['created_at'] = item['created_at']
        cleaned_text = item['text'].replace('\n', ' ').replace('\r', '')
        tweet['text'] = cleaned_text
        for item2 in resp['includes']['users']:
            if item2['id'] == item['author_id']:
                tweet['username'] = item2['username']
        #print (tweet)
        tweet_list.append(tweet)


def main():

    total_count = 0
    query_string = ''

    #read hashtags from command line.  if there are none, use default
    if len(sys.argv) == 1:
        hashtags.append(default_hashtag)
    else:
        for item in range(1, len(sys.argv)):
            if ("#" not in sys.argv[item]):
                hashtags.append("#" + sys.argv[item])
            else:
                hashtags.append(sys.argv[item])
    print("searching for the hashtags:")
    print(hashtags)

    #generate the query string using list of hashtags
    for i in range(0, len(hashtags)):
        query_string = query_string + hashtags[i]
        if i < (len(hashtags) - 1):
            query_string = query_string + " OR "
    #print(query_string)

    params = get_query_params(query_string)
    json_response = connect_to_endpoint(search_url, params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    process_response(json_response)
    count_value = json_response['meta']['result_count']
    total_count = total_count + int(count_value)
    print(total_count)
    
    try:
        while json_response['meta']['next_token'] != "null":
            time.sleep(1)
            next_token = json_response['meta']['next_token']
            next_query = get_query_params(query_string, next_token)
            json_response = connect_to_endpoint(search_url, next_query)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            process_response(json_response)
            count_value = (json_response['meta']['result_count'])
            total_count = total_count + int(count_value)
            print(total_count)
    except (KeyError):
        pass

    print("records processed: %d" %total_count)

    #print to screen the list of tweets
    for item in tweet_list:
        print("%s, %s, %s" %(item['username'], item['created_at'], item['text']))

    #output to file
    with open('deeztweets.txt', 'w', encoding="utf-8") as f:
        for item in tweet_list:
            f.write("%s,%s,%s\n" % (item['username'], item['created_at'], item['text']))

if __name__ == "__main__":
    main()
