from secret import accounts
import tweepy as ty
import time
from time import mktime
from datetime import datetime, timedelta
import sys
from urllib import request, parse
import json
import random
import xlwt
import xlsxwriter
import xlrd

#################################################### VARIABLES #########################################################
time_delay_min = 0
time_delay_max = 10
tweet_days = 1



#################################################### FUNCTIONS ###########################################################

def set_twitter_auth(credentials):

    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_SECRET = credentials['ACCESS_SECRET']

    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth ,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
    print('Credentials Verified')
    return api

def get_last_tweet(api, user,ids_chunk):
    users_chunk = api.lookup_users(ids_chunk)
    return users_chunk


def custom_delay(delay_value):
    print('Delay of ', delay_value, 'seconds starting')
    for i in range(delay_value):
        time.sleep(1)
        print(i, ' seconds passed')


def get_previous_followed(file_name):
    fetched_list = []
    with open(file_name) as my_file:
        for line in my_file:
            fetched_list.append(line.rstrip('\n'))
    return fetched_list


def enter_in_record(username,file_name):
    file = open(file_name, 'a')
    username = str(username)
    file.write(username)
    file.write('\n')
    file.close()
    print(username, 'Entered in file')

def erase_record(file_name):
    f = open(file_name, 'r+')
    f.truncate(0)


def user_follow(api,id):
        try:
            api.create_friendship(id)
            print('Followed user', api.get_user(id).screen_name, 'after all filter checks....!!! ')
        except ty.TweepError as e:
            print(e)


def get_previous_followed(file_name):
    fetched_list = []
    with open(file_name) as my_file:
        for line in my_file:
            fetched_list.append(line.rstrip('\n'))
    return fetched_list


def enter_in_record(username,file_name):
    file = open(file_name, 'a')
    username = str(username)
    file.write(username)
    file.write('\n')
    file.close()
    print(username, 'Entered in file')

def erase_record(file_name):
    f = open(file_name, 'r+')
    f.truncate(0)


def dp_check(follow_user):
    filter_status = True
    try:
        if follow_user.default_profile_image:
            filter_status = False
            print(follow_user.screen_name, 'has avatar')
    except Exception as e:
        print(e)
    return filter_status


def location_check(follow_user, location):
    filter_status = False
    if follow_user.location in location:
        filter_status = True
        print(follow_user.screen_name, 'Location Matched')
    return filter_status


def last_tweeted(follow_user):
    filter_status = False
    try:
        tweet = follow_user.status.created_at
        if(datetime.today()-tweet).days < 1:
            filter_status = True
            print(follow_user.screen_name, 'has recent tweet')
    except Exception as e:
        print(e)
    return filter_status


def get_my_tweets(api,user_id,number_of_tweets):
    tweets_object = api.user_timeline(user_id = user_id, count = number_of_tweets, include_rts = False)
    retweets = []
    for tweet in tweets_object:
        retweets.append(tweet._json)
    return retweets


def get_tweet_ids(tweets):
    tweet_ids = []
    for tweet in tweets:
        #print(type(datetime.today()))
        #print(datetime.today())
        tweet_time = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        #print(tweet_time)
        #print(type(tweet_time))
        tweet_time = datetime.fromtimestamp(mktime(tweet_time))
        #print(type(tweet_time))
        if (datetime.today() - tweet_time).days <= tweet_days:
            tweet_ids.append(tweet['id'])
    return tweet_ids


def get_retweeting_users(api,tweet_id):
    user_data = api.retweets(tweet_id)
    retweet_users = []
    for rt_user in user_data:
        if rt_user.user['following'] is False:
            retweet_users.append((rt_user.user_.json['id']))
    return (retweet_users)


if __name__ == "__main__":
    for account in accounts:
        api = set_twitter_auth(account)
        user = api.me()
        id = user.id
        # Get Tweets of Authenticated users
        number_of_tweets = 20
        tweets = get_my_tweets(api, id, number_of_tweets)
        tweet_ids = get_tweet_ids(tweets)
        for tweet_id in tweet_ids:
            rt_users = get_retweeting_users(api,tweet_id)
            for rt_user in rt_users:
                user_follow(api,rt_user)
                custom_delay(time_delay)
            print(len(rt_users))

        print('Bottom...!')
