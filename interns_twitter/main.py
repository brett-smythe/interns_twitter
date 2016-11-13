"""Entry point for interns_twitter service"""
from interns_twitter.utils import interns_logger
from interns_twitter.workers.timeline import worker as timeline_worker


def run():
    """Entry point to run twitter_interns service"""
    interns_logger.info('Starting interns_twitter service')
    timelineWorker = timeline_worker.TimelineWorker()
    while True:
        timelineWorker.do_work()
