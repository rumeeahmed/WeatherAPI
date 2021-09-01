from system_base import SystemBase
import json


class PingTest(SystemBase):
    """
    Object that system tests the Ping route for the weather API.
    """
    def test_ping_status(self) -> None:
        """
        Check that the status code returned from this endpoint is 200.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/ping')
            self.assertEqual(
                200, response.status_code, f'Expected the status code to be 200, got {response.status_code} instead.'
            )

    def test_ping_response(self) -> None:
        """
        Check that the json returned from the ping endpoint is equal to the value that is expected.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/ping')
            expected_data = {"name": "weatherservice", "status": "ok", "version": "1.0.0"}
            self.assertDictEqual(
                expected_data, json.loads(response.data),
                'The JSON returned from the endpoint is not equal to the expected JSON'
            )
