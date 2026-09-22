# -*- coding: utf-8 -*-
import unittest
from tools.corpus_stats import analyze_corpus
from tools.translation_explorer import TranslationExplorer

class TestCorpusStats(unittest.TestCase):
    def test_analyze_corpus(self):
        stats = analyze_corpus()
        self.assertGreaterEqual(stats["total_monographs"], 18, "En az 18 monografi bulunmali.")
        self.assertGreaterEqual(stats["total_manuscripts"], 24, "En az 24 fihristlenmis yazma bulunmali.")
        self.assertGreaterEqual(stats["total_translations"], 7, "En az 7 tercume kaydi bulunmali.")
        self.assertGreaterEqual(stats["total_historiography"], 6, "En az 6 tarihyazimi makalesi bulunmali.")
        self.assertGreater(stats["monograph_word_count"], 5000, "Monografiler yeterli kelime hacmine sahip olmali.")
        self.assertEqual(len(stats["disciplines"]), 6, "6 temel disiplin olmali.")

class TestTranslationExplorer(unittest.TestCase):
    def setUp(self):
        self.explorer = TranslationExplorer()

    def test_load_translations(self):
        self.assertGreaterEqual(len(self.explorer.translations), 7, "Toledo tercumeleri yuklenmeli.")

    def test_search_by_translator(self):
        results = self.explorer.search(translator="Gerard")
        self.assertGreater(len(results), 0, "Gerard of Cremona aramasi sonuc vermeli.")

    def test_search_by_discipline(self):
        results = self.explorer.search(discipline="Medicine")
        self.assertGreater(len(results), 0, "Tip disiplini aramasi sonuc vermeli.")

    def test_export_markdown(self):
        md = self.explorer.export_markdown_table()
        self.assertIn("| Latince Başlık |", md)
        self.assertIn("Gerard of Cremona", md)

if __name__ == "__main__":
    unittest.main()
