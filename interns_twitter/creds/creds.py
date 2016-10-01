"""Credentials for interns_twitter service"""
import ConfigParser


class InternsTwitterConfigs(object):
    """Class for loading and using interns_twitter configs"""

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('/etc/opt/interns/interns_auth.cfg')
        # Twitter Auth
        self.twitter_consumer_key = config.get(
            'Twitter', 'twitter_consumer_key'
        )
        self.twitter_consumer_secret = config.get(
            'Twitter', 'twitter_consumer_secret'
        )
        self.twitter_access_token_key = config.get(
            'Twitter', 'twitter_access_token_key'
        )
        self.twitter_access_token_secret = config.get(
            'Twitter', 'twitter_access_token_secret'
        )
