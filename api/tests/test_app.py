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

    def test_possible_artist_id(self):
        primary_artists = [
            {"id": 690350},
            {"id": 1593971},
            {"id": 123456},
            {"id": 690350},
            {"id": 690350},
            {"id": 654321},
        ]
        self.assertEqual(app.possible_artist_id(primary_artists), 690350)
        primary_artists = [
            {"id": 123456},
            {"id": 123456},
            {"id": 123456},
            {"id": 123456},
            {"id": 690350},
            {"id": 690350},
        ]
        self.assertEqual(app.possible_artist_id(primary_artists), 123456)
        self.assertEqual(app.possible_artist_id([]), None)
