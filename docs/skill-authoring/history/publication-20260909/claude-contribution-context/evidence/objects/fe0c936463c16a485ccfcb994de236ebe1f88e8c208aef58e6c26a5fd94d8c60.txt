import unittest
from src.store import save_and_list

class PersistenceTest(unittest.TestCase):
    def test_round_trip(self):
        self.assertEqual(save_and_list("hello"), ["hello"])

    def test_apostrophe_and_unicode(self):
        self.assertEqual(save_and_list("Bryan's café"), ["Bryan's café"])
