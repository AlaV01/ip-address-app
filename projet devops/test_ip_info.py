import unittest
from ip_info import IPInfo


class TestIPInfo(unittest.TestCase):

    def test_valid_ipv4(self):
        info = IPInfo("8.8.8.8")
        self.assertEqual(info.ip, "8.8.8.8")
        self.assertEqual(info.ip_version, 4)

    def test_valid_ipv6(self):
        info = IPInfo("2001:4860:4860::8888")
        self.assertEqual(info.ip_version, 6)

    def test_invalid_ip_raises_error(self):
        with self.assertRaises(ValueError):
            IPInfo("abc")

    def test_ip_out_of_range_raises_error(self):
        with self.assertRaises(ValueError):
            IPInfo("999.1.1.1")

    def test_attributes_are_stored(self):
        info = IPInfo("1.1.1.1", city="Tunis", country="TN", isp="Test ISP")
        self.assertEqual(info.city, "Tunis")
        self.assertEqual(info.country, "TN")
        self.assertEqual(info.isp, "Test ISP")

    def test_properties_are_read_only(self):
        info = IPInfo("1.1.1.1")
        with self.assertRaises(AttributeError):
            info.ip = "2.2.2.2"

    def test_to_dict(self):
        info = IPInfo("1.1.1.1", city="Tunis")
        data = info.to_dict()
        self.assertEqual(data["ip"], "1.1.1.1")
        self.assertEqual(data["city"], "Tunis")

    def test_to_json_is_valid_json(self):
        import json
        info = IPInfo("1.1.1.1", city="Tunis")
        self.assertEqual(json.loads(info.to_json())["city"], "Tunis")

    def test_str_contains_ip(self):
        self.assertIn("1.1.1.1", str(IPInfo("1.1.1.1")))


if __name__ == "__main__":
    unittest.main()
