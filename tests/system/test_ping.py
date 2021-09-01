from system_base import SystemBase
import json


class PingTest(SystemBase):
    """
    Object that system tests the Ping route for the weather API.
    """
    def test_ping_status(self):
        """
        Check that the status code returned from this endpoint is 200.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/ping')
            self.assertEqual(response.status_code, 200)

    def test_ping_response(self):
        """
        Check that the json returned from the ping endpoint is equal to the value that is expected.
        :return: None
        """
        with self.test_client() as test_client:
            response = test_client.get('/ping')
            expected_data = {"name": "weatherservice", "status": "ok", "version": "1.0.0"}
            self.assertDictEqual(json.loads(response.data), expected_data)
