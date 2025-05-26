import unittest
from pybleau.workbooks import WorkbookManager

class TestWorkbookManager(unittest.TestCase):
    def setUp(self):
        self.manager = WorkbookManager("fake_token", "fake_site_id", "https://fake-server")

    def test_initialization(self):
        self.assertEqual(self.manager.token, "fake_token")
        self.assertEqual(self.manager.site_id, "fake_site_id")
        self.assertEqual(self.manager.server_url, "https://fake-server")
