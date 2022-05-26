# t_scripts
A set of python scripts to get and aggregate twitter tweets

## Requirements
python 3

## Installation
set up environment:  
`git clone <repo url>`  
`cd t_scripts`  
`python3 -m venv .`  
`source bin/activate`  
`pip install -r requirements.txt`  

## Scripts
### gettweetfollows
Gets a list of tweets containing word(s) and if the tweet author follows a certain account
#### Usage:
gettweetfollows.py -w <list of words to search for in tweet>
#### Example:
`python gettweetfollows.py -w "#bayc" "#giveaway"`
#### Optionally check if tweet author follows an account:
gettweetfollows.py -w <list of words to search for> -f <account to verify is being followed>
#### Example:
`python gettweetfollows.py -w "#bayc" "#giveaway" -f midnightwrench`
#### Output:
By default, a csv file `tweet_list.csv` will be written containing a list of tweets with specified words and a `False` or `True` whether or not the tweet author follows specified account.  To also output the list of tweets to the screen add the `-p` flag to the command line.
#### Help:
`python gettweetfollows.py -h`
#### Sample Run:
```
$ python gettweetfollows.py -w "#bayc" "#giveaway" -f midnightwrench
Searching tweets for the word(s):
['#bayc', '#giveaway']
Checking for users following account midnightwrench
Number of followers of midnightwrench: 1045
.
.
. <one dot per 100 tweets found>
.
.
Total tweets processed: 3993
Found 3 tweets that follows account
Tweets and whether or not author follows account saved to tweet_list.csv.
```
#### Sample Output File Exceprt:
```
username,tweet_dt_utc,follows_midnightwrench,text
Truesmt,2022-05-20T22:51:37.000Z,False,RT @DavyBoy1888: 🤯 #NFTGiveaway 🤯  🏆 WIN 1 X MetaManz #900 NFT 🏆  1️⃣ Must Follow  @DavyBoy1888  @YoumanzC @lKenny_Tl 2️⃣ ♥️ &amp; RT  3️⃣ Tag…
Truemass88,2022-05-20T00:00:13.000Z,False,RT @cbeaudoin92: Almost sold out get your #caws before it's too late. #rolex #Giveaway #staking for #eth rewards @dypfinance @garyvee @Twit…
Saitamaenthu,2022-05-19T20:05:46.000Z,True,RT @TheeHustleHouse: 🔥#Giveaway🚨  We are super excited about the @IsmToys x #BAYC Chess set that is releasing soon  There is only a very li…
```
