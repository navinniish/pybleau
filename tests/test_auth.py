import unittest
from pybleau.auth import TableauClient

class TestTableauClient(unittest.TestCase):
    def test_initialization(self):
        client = TableauClient("https://fake-server", "fake_name", "fake_secret")
        self.assertEqual(client.server_url, "https://fake-server")
        self.assertEqual(client.token_name, "fake_name")
        self.assertEqual(client.token_secret, "fake_secret")
