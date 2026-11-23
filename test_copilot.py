import unittest
from copilot import answer, load_corpus, retrieve

class RetrievalTest(unittest.TestCase):
    def setUp(self):
        self.corpus = load_corpus()

    def test_ranking(self):
        for name in self.corpus:
            with self.subTest(name=name):
                self.assertEqual(retrieve(name, self.corpus)[0], name)

    def test_citation(self):
        result = answer("restore backups", self.corpus)
        self.assertIn("[backup]", result["answer"])
        self.assertIn("backup", result["sources"])

    def test_unknown(self):
        self.assertEqual(answer("xyzzy", self.corpus)["sources"], [])

    def test_empty(self):
        self.assertEqual(retrieve("", self.corpus), [])
