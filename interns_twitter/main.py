"""Entry point for interns_twitter service"""
from interns_twitter import utils as interns_utils
from interns_twitter.workers.timeline import worker as timeline_worker


logger = interns_utils.get_logger(__name__)


def run():
    """Entry point to run twitter_interns service"""
    logger.info('Starting interns_twitter service')
    timelineWorker = timeline_worker.TimelineWorker()
    while True:
        timelineWorker.do_work()
