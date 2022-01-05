import time
import json
from t_request import TRequest


class TApi:

    def get_followers(self, user):

        followers_url = "https://api.twitter.com/1.1/followers/ids.json"
        count = 5000 #number of records to get per request
        user_name = user
        follower_list = []

        #internal functions below
        def _get_followers_query_params(user_name, next_cursor = None):
            if next_cursor is None:
                query_params = {'screen_name': user_name, 'count': count}
            else:
                query_params = {'screen_name': user_name, 'count': count, 'cursor' : next_cursor}
            return query_params

        def _process_followers_response(resp):
            for item in resp['ids']:
                follower_list.append(str(item))
            return

        #prepare request to get followers
        followers_request = TRequest(followers_url)
        query = _get_followers_query_params(user_name)

        #make request to get followers
        json_response = followers_request.connect_to_endpoint(query)
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        
        #process the followers
        _process_followers_response(json_response)
    
        #make more requests if next cursor is not 0
        try:
            while json_response['next_cursor'] != 0:
                time.sleep(1)
                next_cursor = json_response['next_cursor']
                #print(next_cursor)
                next_query = _get_followers_query_params(user_name, next_cursor)
                json_response = followers_request.connect_to_endpoint(next_query)
                #print(json.dumps(json_response, indent=4, sort_keys=True))
                _process_followers_response(json_response)
        except:
            print("Unexpected response from followers endpoint, likely missing some followers.")

        return follower_list


    def get_tweets(self, search_items, followers_list = None):

        tweet_search_url = "https://api.twitter.com/2/tweets/search/recent"
        total_tweet_count = 0
        query_string = ''
        tweet_list = []

        #internal functions below
        def _get_tweets_query_params(query_string, next_token = None):
            # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
            # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
            if next_token == None:
                query_params = {'query': query_string, 'tweet.fields': 'created_at', 'expansions': 'author_id', 
                    'max_results': 100}
            else:
                query_params = {'query': query_string, 'tweet.fields': 'created_at', 'expansions': 'author_id', 
                    'max_results': 100, 'next_token' : next_token}
            return query_params


        def _process_tweet_response(resp, followers_list = None):
            for item in resp['data']:
                tweet = {}
                username_match = False

                tweet['author_id'] = item['author_id']
                tweet['created_at'] = item['created_at']
                cleaned_text = item['text'].replace('\n', ' ').replace('\r', '')
                tweet['text'] = cleaned_text
                for item2 in resp['includes']['users']:
                    if item2['id'] == item['author_id']:
                        tweet['username'] = item2['username']
                        if followers_list is not None and len(followers_list) > 0:
                            #check author_id is in followers list
                            if item['author_id'] in followers_list:
                                tweet['follows'] = True
                            else:
                                tweet['follows'] = False
                        break #stop matching usernames

                #print (tweet)
                tweet_list.append(tweet)
            return


        if len(search_items) == 0:
            print("Unexpected empty list of seach items.")
            return

        #generate the query string using list of search items
        for i in range(0, len(search_items)):
            query_string = query_string + search_items[i]
            if i < (len(search_items) - 1):
                query_string = query_string + " "
        print(query_string)

        #prepare request to search tweets
        query_request = TRequest(tweet_search_url)
        query = _get_tweets_query_params(query_string)

        #make request to get tweets 
        json_response = query_request.connect_to_endpoint(query)
        #print(json.dumps(json_response, indent=4, sort_keys=True))

        #process tweets
        _process_tweet_response(json_response, followers_list)

        count_value = json_response['meta']['result_count']
        total_tweet_count = total_tweet_count + int(count_value)
        print(total_tweet_count)

        #make more requests if next token is present
        try:
            while json_response['meta']['next_token'] != "null":
                time.sleep(1)
                next_token = json_response['meta']['next_token']
                next_query = _get_tweets_query_params(query_string, next_token)
                json_response = query_request.connect_to_endpoint(next_query)
                #print(json.dumps(json_response, indent=4, sort_keys=True))
                _process_tweet_response(json_response, followers_list)
                count_value = (json_response['meta']['result_count'])
                total_tweet_count = total_tweet_count + int(count_value)
                print(total_tweet_count)
        except (KeyError):
            print("end of tweets reached")

        print("total records processed: %d" %total_tweet_count)

        return tweet_list

