# -*- coding: utf-8 -*-
import unittest
import os
from tools.manuscript_indexer import ManuscriptCatalog

class TestManuscriptIndexer(unittest.TestCase):
    def setUp(self):
        self.catalog = ManuscriptCatalog(data_dir="data/manuscripts")

    def test_catalogs_loaded(self):
        self.assertGreater(len(self.catalog.catalogs), 0, "En az bir yazma katalogu yüklenmeli.")
        self.assertGreater(self.catalog.total_count(), 0, "Toplam yazma sayısı 0 dan büyük olmalı.")

    def test_schema_validation(self):
        errors = self.catalog.validate_schema()
        self.assertEqual(len(errors), 0, f"Şema doğrulama hataları bulundu: {errors}")

    def test_search_by_author(self):
        results = self.catalog.search(author="Zehrâvî")
        self.assertGreater(len(results), 0, "Zehrâvî araması sonuç döndürmeli.")
        for r in results:
            self.assertIn("Zehrâvî", r["author"])

    def test_search_by_subject(self):
        results = self.catalog.search(subject="Astronomy")
        self.assertGreater(len(results), 0, "Astronomi araması sonuç döndürmeli.")

    def test_markdown_export(self):
        md = self.catalog.export_markdown_table()
        self.assertIn("| Demirbaş / Raf No |", md)
        self.assertIn("MS Árabe 887", md)

if __name__ == "__main__":
    unittest.main()
