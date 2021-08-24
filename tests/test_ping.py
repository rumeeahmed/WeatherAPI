import unittest
import requests
from requests import Response


class PingTest(unittest.TestCase):
    """
    Object that tests the Ping route for the weather API.
    """
    @staticmethod
    def ping() -> Response:
        return requests.get('http://127.0.0.1:5005/ping')

    def test_ping_status(self):
        """
        Check that the status code returned from this endpoint is 200.
        :return:
        """
        response = self.ping()
        self.assertEqual(response.status_code, 200)

    def test_ping_response(self):
        """
        Check that the json returned from the ping endpoint is equal to the value that is expected.
        :return: None
        """
        response = self.ping()
        expected_data = {"name": "weatherservice", "status": "ok", "version": "1.0.0"}
        self.assertEqual(response.json(), expected_data)
