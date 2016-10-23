"""Utilities for interns_twitter service"""
import os
import logging
import logging.config
import time


def get_logger(module_name):
    """Get a logger with created with values from settings/logging.conf and
    using time.gmtime
    """
    log_path = '/tmp/interns-worker.log'
    if 'RUN_ENV' in os.environ:
        if os.environ['RUN_ENV'] == 'production':
            log_path = '/var/log/interns-twitter/worker.log'

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler(
        log_path, 'midnight', 1, 0, 'utf-8', False, True
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
