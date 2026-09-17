# -*- coding: utf-8 -*-
import unittest
from tools.quote_engine import QuoteEngine

class TestQuoteEngine(unittest.TestCase):
    def setUp(self):
        self.engine = QuoteEngine("data/quotes-archive/historical_quotes.json")

    def test_quotes_loaded(self):
        self.assertGreater(len(self.engine.quotes), 10, "En az 10 alıntı yüklenmiş olmalı.")

    def test_categories(self):
        scholars = self.engine.search(category="andalusian_scholars")
        self.assertGreater(len(scholars), 0, "Endülüslü bilginler kategorisi dolu olmalı.")
        historians = self.engine.search(category="western_historians")
        self.assertGreater(len(historians), 0, "Batılı tarihçiler kategorisi dolu olmalı.")

    def test_random_quote(self):
        q = self.engine.get_random()
        self.assertIsNotNone(q)
        self.assertIn("text_tr", q)
        self.assertIn("speaker", q)

    def test_markdown_formatting(self):
        q = self.engine.quotes[0]
        md = self.engine.format_quote_markdown(q)
        self.assertTrue(md.startswith("> *\""))
        self.assertIn(q["speaker"], md)

if __name__ == "__main__":
    unittest.main()
