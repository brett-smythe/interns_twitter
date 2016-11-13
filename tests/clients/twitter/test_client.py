"""Tests for inters_twitter twitter client"""
# pylint: disable=import-error
import unittest

from logging import RootLogger

import mock

from interns_twitter.clients.twitter import client
from aquatic_twitter import client as twitter_client


class TestTweetUser(object):
    """Class to emulate a tweet user object"""

    def __init__(self, screen_name):
        self.screen_name = screen_name


class TestTweetHashtag(object):
    """Class to emulate a tweet hashtag object"""

    def __init__(self, hashtag):
        self.text = hashtag


class TestTweetUrl(object):
    """Class to emulate tweet url object"""

    def __init__(self, url):
        self.expanded_url = url


class TestTweet(object):
    """Class emulating a tweet object"""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, user, id_str, tweet_text, created_at, mentions,
                 hashtags, urls, retweet_data=None):
        # pylint: disable=too-many-arguments
        self.user = user
        self.id_str = id_str
        self.text = tweet_text
        self.created_at = created_at
        self.user_mentions = mentions
        self.hashtags = hashtags
        self.urls = urls
        self.retweeted_status = retweet_data


class InternsTwitterClientCases(unittest.TestCase):
    """Tests for twitter client"""
    # pylint: disable=too-many-public-methods

    def create_test_tweet(self):
        """Create test tweet object for testing"""
        # pylint: disable=no-self-use
        testTweetUser = TestTweetUser("Jean-Luc")
        test_tweet_mentions = [
            TestTweetUser("NumberOne"),
            TestTweetUser("Mr.Data"),
            TestTweetUser("Worf"),
            TestTweetUser("Dr.Crusher")
        ]
        test_tweet_hashtags = [
            TestTweetHashtag("BeingTenForward")
        ]
        test_tweet_urls = [
            TestTweetUrl("http://memory-alpha.wikia.com/wiki/Ten_Forward")
        ]
        testTweet = TestTweet(
            testTweetUser, "46154.2", "What a cat", "15/6/2369",
            test_tweet_mentions, test_tweet_hashtags, test_tweet_urls
        )
        return testTweet

    @mock.patch('interns_twitter.clients.twitter.client.get_twitter_client')
    @mock.patch('interns_twitter.clients.twitter.client.eleanor_twitter')
    @mock.patch('interns_twitter.clients.twitter.client.interns_logger')
    def test_get_user_timeline_tweets_with_last_entry(self,
                                                      mock_interns_utils,
                                                      mock_eleanor_twitter,
                                                      mock_get_twitter_client):
        """Test getting a user's timeline tweets"""
        # pylint: disable=no-self-use
        test_last_entry_id = 10
        test_screen_name = 'Jean-Luc'
        mock_interns_utils.return_value = mock.Mock(RootLogger)
        mock_internal_client = mock.Mock(twitter_client.AquaticTwitter)
        mock_internal_client.get_timeline_tweets_since_id.return_value = []
        mock_get_twitter_client.return_value = mock_internal_client
        mock_eleanor_twitter.get_username_last_tweet_id.return_value = \
            test_last_entry_id
        client.get_user_timeline_tweets(test_screen_name)
        mock_internal_client.get_timeline_tweets_since_id.assert_called_with(
            test_screen_name,
            test_last_entry_id
        )

    @mock.patch('interns_twitter.clients.twitter.client.get_twitter_client')
    @mock.patch('interns_twitter.clients.twitter.client.eleanor_twitter')
    @mock.patch('interns_twitter.clients.twitter.client.interns_logger')
    def test_get_user_timeline_tweets__no_last_entry(self,
                                                     mock_interns_utils,
                                                     mock_eleanor_twitter,
                                                     mock_get_twitter_client):
        """Test getting a user's timeline tweets"""
        # pylint: disable=no-self-use
        test_last_entry_id = None
        test_screen_name = 'Jean-Luc'
        mock_interns_utils.return_value = mock.Mock(RootLogger)
        mock_internal_client = mock.Mock(twitter_client.AquaticTwitter)
        mock_internal_client.get_timeline_tweets.return_value = []
        mock_get_twitter_client.return_value = mock_internal_client
        mock_eleanor_twitter.get_username_last_tweet_id.return_value = \
            test_last_entry_id
        client.get_user_timeline_tweets(test_screen_name)
        mock_internal_client.get_timeline_tweets.assert_called_with(
            test_screen_name
        )

    @mock.patch('interns_twitter.clients.twitter.client.eleanor_twitter')
    @mock.patch('interns_twitter.clients.twitter.client.interns_logger')
    def test_insert_tweet_data(self, mock_interns_utils, mock_eleanor_twitter):
        """Test inserting tweet data"""
        test_tweet = self.create_test_tweet()
        mock_interns_utils.get_logger.return_value = mock.Mock(RootLogger)
        expected_tweet_data = {
            "user_name": "Jean-Luc",
            "tweet_id": "46154.2",
            "url": "https://twitter.com/Jean-Luc/status/46154.2",
            "tweet_text": "What a cat",
            "tweet_created": "15/6/2369",
            "is_retweet": False,
            "user_mentions": ["NumberOne", "Mr.Data", "Worf", "Dr.Crusher"],
            "hashtags": ["BeingTenForward"],
            "tweet_urls": ["http://memory-alpha.wikia.com/wiki/Ten_Forward"],
            "retweet_data": {}
        }
        client.insert_tweet_data(test_tweet)
        mock_eleanor_twitter.add_tweet_data.assert_called_with(
            expected_tweet_data
        )
