import unittest
from ngrams import *
from spacy.lang.en import English
nlp = English(pipeline=[])

class TestNgrams(unittest.TestCase):

    text = nlp("All the king's horses and all the king's men couldn't put Humpty Dumpty together again.")

    def testGetUnigrams(self):
        expected = ['all', 'the', 'king', "'s", 'horses', 'and', 'all', 'the', 'king', "'s", 'men', 'could', "n't", 'put', 'humpty', 'dumpty', 'together', 'again', '.']
        # sort lists before comparing just in case different implementations result in different orders
        self.assertEqual(sorted(get_unigrams(self.text)), sorted(expected))

    def testGetBigrams(self):
        expected = [('all', 'the'), ('the', 'king'), ('king', "'s"), ("'s", 'horses'), ('horses', 'and'), 
                    ('and', 'all'), ('all', 'the'), ('the', 'king'), ('king', "'s"), ("'s", 'men'), ('men', 'could'), 
                    ('could', "n't"), ("n't", 'put'), ('put', 'humpty'), ('humpty', 'dumpty'), ('dumpty', 'together'), 
                    ('together', 'again'), ('again', '.')]
        self.assertEqual(sorted(get_bigrams(self.text)), sorted(expected))

    def testGetTrigrams(self):
        expected = [('all', 'the', 'king'), ('the', 'king', "'s"), ('king', "'s", 'horses'), ("'s", 'horses', 'and'), 
                    ('horses', 'and', 'all'), ('and', 'all', 'the'), ('all', 'the', 'king'), ('the', 'king', "'s"), 
                    ('king', "'s", 'men'), ("'s", 'men', 'could'), ('men', 'could', "n't"), ('could', "n't", 'put'), 
                    ("n't", 'put', 'humpty'), ('put', 'humpty', 'dumpty'), ('humpty', 'dumpty', 'together'), 
                    ('dumpty', 'together', 'again'), ('together', 'again', '.')]
        self.assertEqual(sorted(get_trigrams(self.text)), sorted(expected))

    def testCompare(self):
        self.assertEqual(compare(Counter([]), Counter([1,2,3])), (3,3))
        self.assertEqual(compare(Counter([]), Counter([1,2,3]), unique=True), (3,3))
        self.assertEqual(compare(Counter([]), Counter([1,1,2,3])), (4,4))
        self.assertEqual(compare(Counter([]), Counter([1,1,2,3]), unique=True), (3,3))

if __name__ == "__main__":
    unittest.main()