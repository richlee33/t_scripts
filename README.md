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