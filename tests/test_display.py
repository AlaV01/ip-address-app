import unittest
from io import StringIO
from unittest.mock import patch
from src.display import Display


class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.display = Display()

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_ip(self, out):
        self.display.show_ip(4, "1.2.3.4")
        self.assertIn("1.2.3.4", out.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_table(self, out):
        self.display.show_table({"city": "Monastir", "country": "TN"})
        self.assertIn("Monastir", out.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_table_empty(self, out):
        self.display.show_table({})
        self.assertIn("Aucune donnée", out.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_error(self, out):
        self.display.show_error("timeout")
        self.assertIn("timeout", out.getvalue())

    @patch("builtins.input", return_value=" 1 ")
    def test_ask_choice_strips(self, _):
        self.assertEqual(self.display.ask_choice(), "1")


if __name__ == "__main__":
    unittest.main()