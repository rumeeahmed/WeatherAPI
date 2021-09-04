from resources.forecast import Forecast
from unittest import TestCase
from datetime import datetime
import api


class BaseTest(TestCase):
    """
    Object that handles tests for integration and unit tests.
    """
    def setUp(self) -> None:
        """
        Initialise each test by creating a new instance of the Forecast object.
        :return: None
        """
        self.resource = Forecast()
        self.resource.timezone = datetime.now().astimezone().tzinfo
        self.resource.error = {
            'error': '',
            'error_code': ''
        }
