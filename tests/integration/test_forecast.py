from unittest import TestCase
from resources.forecast import Forecast
import api


class TestForecast(TestCase):
    """
    Object that handles the `integration` test for the `Forecast` route.
    """
    def setUp(self) -> None:
        """
        Initialise each test by creating a new instance of the Forecast object.
        :return: None
        """
        self.resource = Forecast()

    def test_get_weather_success_response(self) -> None:
        """
        Test the response of a successful call of the `get_weather` method in the Forecast Resource object.
        :return: None
        """
        response = self.resource.get_weather('London', 'metric')
        data, unit = response
        self.assertIsInstance(
            response, tuple, f'Expected to the response to be a tuple object but is instead {type(response)}.'
        )
        self.assertEqual(
            200, int(data['cod'])
            , f'Expected the code inside the data returned to be 200, got {int(data["cod"])} instead.'
        )
        self.assertEqual(
            'metric', unit, f'Expected the units to be metric, got {unit} instead.'
        )

    def test_get_weather_failed_response(self) -> None:
        """
        Test the response of a failed call of the `get_weather` method in the Forecast Resource object.
        :return: None
        """
        response = self.resource.get_weather('Winterfell', 'metric')
        data, unit = response
        print(data.response.status_code)
        self.assertIsInstance(
            response, tuple, f'Expected to the response to be a tuple object but is instead {type(response)}.'
        )
        self.assertEqual(
            404, data.response.status_code
            , f'Expected the code inside the data returned to be 200, got {data.response.status_code} instead.'
        )
        self.assertEqual(
            'metric', unit, f'Expected the units to be metric, got {unit} instead.'
        )
