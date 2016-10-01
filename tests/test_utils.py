"""Test file for interns_twitter utilities"""
# pylint: disable=import-error
import unittest

import mock

from interns_twitter import utils


class InternsTwitterUtilsCases(unittest.TestCase):
    """Test cases for interns twitter utilities"""
    # pylint: disable=too-many-public-methods

    @mock.patch('interns_twitter.utils.logging')
    def test_get_logger(self, mock_logging):
        """Test getting interns twitter logger"""
        # pylint: disable=no-self-use
        utils.get_logger(__name__)
        mock_logging.getLogger.assert_called_with(__name__)
