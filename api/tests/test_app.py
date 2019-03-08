from unittest import TestCase
from api import app


class TestApp(TestCase):
    def test_format_query(self):
        self.assertEqual(app.format_query("killer queens"), "killer%20queens")
        self.assertEqual(
            app.format_query("mumford and sons"), "mumford%20and%20sons"
        )
        self.assertEqual(
            app.format_query("   mumford and sons    "), "mumford%20and%20sons"
        )
