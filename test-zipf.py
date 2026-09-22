import unittest
from zipf import *

class TestZipf(unittest.TestCase):

    def testReadOne(self):

        counts = read_one("/courses/cs159/data/blake-poems.txt")
        self.assertEqual(counts["little"], 45)
        self.assertEqual(counts["father"], 22)
        self.assertEqual(counts["william"], 2)
        self.assertEqual(counts["unhinderd"], 1) # yes, the spelling is on purpose
        self.assertEqual(counts[","], 684)

    def testReadAll(self):

        counts = read_all("/courses/cs159/data/brown/")
        self.assertEqual(counts["the"], 14559)
        self.assertEqual(counts["american"], 176)
        self.assertEqual(counts["cattle"], 55)
        self.assertEqual(counts["student"], 24)
        self.assertEqual(counts["corinthian"], 1)

if __name__ == "__main__":
    unittest.main()