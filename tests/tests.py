import unittest
from pybleau.auth import TableauClient

class TestAuth(unittest.TestCase):
    def test_init(self):
        client = TableauClient("http://localhost", "token_name", "token_secret")
        self.assertEqual(client.server_url, "http://localhost")
