from api import app
from unittest import TestCase


class SystemBase(TestCase):
    """
    Object that serves as the base class for the systems test
    """
    def setUp(self) -> None:
        """
        Set up a test_client for every test.
        :return: None
        """
        self.test_client = app.test_client
