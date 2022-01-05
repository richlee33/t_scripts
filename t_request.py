import os
import requests
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

class BearerOauth(requests.auth.AuthBase):
    def __call__(self, r):
        bearer_token = os.environ.get("BEARER_TOKEN")
        if bearer_token is None:
            raise Exception("Please set your twitter token in the BEARER_TOKEN environment variable")

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r


class TRequest:
    
    def __init__(self, url):
        self.url = url

    def connect_to_endpoint(self, params):
        response = requests.get(self.url, auth=BearerOauth(), params=params)
        #print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

