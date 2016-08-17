"""Credentials for interns_twitter service"""
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/opt/interns/interns_auth.cfg')
# Twitter Auth
twitter_consumer_key = config.get('Twitter', 'twitter_consumer_key')
twitter_consumer_secret = config.get('Twitter', 'twitter_consumer_secret')
twitter_access_token_key = config.get(
    'Twitter',
    'twitter_access_token_key'
)
twitter_access_token_secret = config.get(
    'Twitter',
    'twitter_access_token_secret'
)
