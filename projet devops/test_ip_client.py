import unittest
from unittest.mock import patch, MagicMock

import requests
from ip_client import IPClient, APIError


def fake_response(json_data=None, http_error=False, bad_json=False):
    """Build a fake answer, so tests never call the real internet."""
    response = MagicMock()
    if http_error:
        response.raise_for_status.side_effect = requests.HTTPError("500 error")
    if bad_json:
        response.json.side_effect = ValueError("not json")
    else:
        response.json.return_value = json_data
    return response


class TestIPClient(unittest.TestCase):

    def setUp(self):
        self.client = IPClient()

    @patch("ip_client.requests.get")
    def test_get_ipv4_success(self, mock_get):
        mock_get.return_value = fake_response({"ip": "8.8.8.8"})
        self.assertEqual(self.client.get_ipv4(), "8.8.8.8")

    @patch("ip_client.requests.get")
    def test_get_ipv6_success(self, mock_get):
        mock_get.return_value = fake_response({"ip": "2001:db8::1"})
        self.assertEqual(self.client.get_ipv6(), "2001:db8::1")

    @patch("ip_client.requests.get")
    def test_no_internet_raises_apierror(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()
        with self.assertRaises(APIError):
            self.client.get_ipv4()

    @patch("ip_client.requests.get")
    def test_timeout_raises_apierror(self, mock_get):
        mock_get.side_effect = requests.ReadTimeout()
        with self.assertRaises(APIError):
            self.client.get_ipv4()

    @patch("ip_client.requests.get")
    def test_http_error_raises_apierror(self, mock_get):
        mock_get.return_value = fake_response(http_error=True)
        with self.assertRaises(APIError):
            self.client.get_ipv4()

    @patch("ip_client.requests.get")
    def test_invalid_json_raises_apierror(self, mock_get):
        mock_get.return_value = fake_response(bad_json=True)
        with self.assertRaises(APIError):
            self.client.get_ipv4()

    @patch("ip_client.requests.get")
    def test_missing_ip_field_raises_apierror(self, mock_get):
        mock_get.return_value = fake_response({"wrong": "data"})
        with self.assertRaises(APIError):
            self.client.get_ipv4()

    @patch("ip_client.requests.get")
    def test_get_details_returns_dict(self, mock_get):
        mock_get.return_value = fake_response({"ip": "8.8.8.8", "city": "Tunis", "org": "Test"})
        details = self.client.get_details("8.8.8.8")
        self.assertEqual(details["city"], "Tunis")

    @patch("ip_client.requests.get")
    def test_get_details_private_ip_raises_apierror(self, mock_get):
        mock_get.return_value = fake_response({"ip": "192.168.1.1", "bogon": True})
        with self.assertRaises(APIError):
            self.client.get_details("192.168.1.1")


if __name__ == "__main__":
    unittest.main()
