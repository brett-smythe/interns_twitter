"""Client for twitter API"""
# pylint can't seem to find this even though it's installed
# pylint: disable=import-error

from interns_twitter.creds import creds
from interns_twitter import utils as interns_utils

from aquatic_twitter import client as twitter_client

from eleanor_client.endpoints import twitter as eleanor_twitter

logger = interns_utils.get_logger(__name__)

twitterClient = twitter_client.AquaticTwitter(
    creds.twitter_consumer_key,
    creds.twitter_consumer_secret,
    creds.twitter_access_token_key,
    creds.twitter_access_token_secret,
    False
)


def get_user_timeline_tweets(screen_name):
    """Pull as many tweets as possible for a newly added user"""
    logger.info('Making twitter timeline request')
    last_entry_id = eleanor_twitter.get_username_last_tweet_id(screen_name)
    timeline_tweets = []

    if last_entry_id:
        timeline_tweets = twitterClient.get_timeline_tweets_since_id(
            screen_name,
            last_entry_id
        )
    else:
        timeline_tweets = twitterClient.get_timeline_tweets(screen_name)

    for tweet in timeline_tweets:
        insert_tweet_data(tweet)


def insert_tweet_data(tweet):
    """
    Pulls data from a tweet and makes a request to eleanor to add tweet data
    """
    logger.debug('Making call to eleanor to add tweet data')
    base_twitter_url = 'https://twitter.com/{0}/status/{1}'
    source_url = base_twitter_url.format(tweet.user.screen_name, tweet.id_str)

    user_mentions = [user.screen_name for user in tweet.user_mentions]
    hashtags = [hashtag.text for hashtag in tweet.hashtags]
    tweet_urls = [url.expanded_url for url in tweet.urls]

    retweet_data = {}
    if tweet.retweeted_status is not None:
        retweet = tweet.retweeted_status
        is_retweet = True
        retweet_url = base_twitter_url.format(
            retweet.user.screen_name,
            tweet.id_str
        )
        retweet_data["user_name"] = retweet.user.screen_name
        retweet_data["tweet_id"] = retweet.id_str
        retweet_data["url"] = retweet_url
        retweet_data["tweet_text"] = retweet.text
        retweet_data["tweet_created"] = retweet.created_at
        retweet_data["is_retweet"] = False

        user_mentions = [user.screen_name for user in retweet.user_mentions]
        retweet_data["user_mentions"] = user_mentions

        hashtags = [hashtag.text for hashtag in retweet.hashtags]
        retweet_data["hashtags"] = hashtags

        tweet_urls = [url.expanded_url for url in retweet.urls]
        retweet_data["tweet_urls"] = tweet_urls
    else:
        is_retweet = False

    tweet_data = {
        "user_name": tweet.user.screen_name,
        "tweet_id": tweet.id_str,
        "url": source_url,
        "tweet_text": tweet.text,
        "tweet_created": tweet.created_at,
        "is_retweet": is_retweet,
        "user_mentions": user_mentions,
        "hashtags": hashtags,
        "tweet_urls": tweet_urls,
        "retweet_data": retweet_data
    }
    eleanor_twitter.add_tweet_data(tweet_data)
