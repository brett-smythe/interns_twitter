"""Worker for gathering twitter timeline data"""
# pylint: disable=import-error
from time import sleep
from datetime import datetime, timedelta

from interns_twitter.settings import timeline as timeline_settings
from interns_twitter.clients.twitter import client as twitter_client
from interns_twitter import utils as interns_utils

from eleanor_client.endpoints import twitter as eleanor_twitter

logger = interns_utils.get_logger(__name__)


class TimelineWorker(object):
    """Worker class to get twitter timeline data"""

    def __init__(self):
        """Worker class to get twitter timeline data"""
        logger.info('Starting twitter timeline worker')
        self.last_request = datetime.utcnow()
        self.sleep_time = 5
        self.calculate_sleep()
        self.user_index = 0
        self.tracked_users = set()

    def calculate_sleep(self):
        """Calculate how long the worker should sleep between API requests"""
        sleep_time = (
            timeline_settings.time_window /
            timeline_settings.requests_per_window
        )
        logger.debug(
            'Calculated sleep time between requests to be: %i', sleep_time
        )
        self.sleep_time = timedelta(seconds=sleep_time)

    def update_tracked_users(self):
        """Update the local list of tracked twitter users"""
        logger.debug('Updating tracked twitter users')
        tracked_users = eleanor_twitter.get_tracked_twitter_users()
        self.tracked_users = set(tracked_users)

    def do_work(self):
        """Sleep until execution time and then pull data from twitter timelines
        """
        if len(self.tracked_users) == 0:
            self.update_tracked_users()
        now = datetime.utcnow()
        elapsed_time = now - self.last_request
        if elapsed_time >= self.sleep_time:
            current_twitter_user = self.tracked_users.pop()
            logger.info(
                'Getting timeline tweets for user: %s', current_twitter_user
            )
            self.last_request = now
            twitter_client.get_user_timeline_tweets(current_twitter_user)
        else:
            sleep_secs = self.sleep_time - elapsed_time
            logger.debug('Sleeping for %i seconds', sleep_secs.seconds)
            sleep(sleep_secs.seconds)
