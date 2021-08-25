import unittest
import requests
from requests import Response


class ForecastTest(unittest.TestCase):
    """
    Object that tests the forecast endpoint.
    """
    @staticmethod
    def get(city: str, units: str = None, date: str = None) -> Response:
        """
        Perform a Get request on the `forecast` endpoint.
        :param city: a string object that represents the city to query the weather for.
        :param units: a string object that represents the units the weather data should return.
        :param date: a string object that represents the date to get weather from.
        :return: a Response object.
        """
        if not date and not units:
            return requests.get(f'http://127.0.0.1:5005/forecast/{city}')
        elif units and not date:
            return requests.get(f'http://127.0.0.1:5005/forecast/{city}?unit={units}')
        elif date and not units:
            return requests.get(f'http://127.0.0.1:5005/forecast/{city}?at={date}')
        else:
            return requests.get(f'http://127.0.0.1:5005/forecast/{city}?unit={units}&at={date}')

    def test_city(self):
        response = self.get('London')
        self.assertEqual(response.status_code, 200)
