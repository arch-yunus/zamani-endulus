# -*- coding: utf-8 -*-
import unittest
from tools.timeline_generator import TimelineGenerator, TIMELINE_EVENTS

class TestTimelineGenerator(unittest.TestCase):
    def setUp(self):
        self.tg = TimelineGenerator()

    def test_events_count(self):
        self.assertGreaterEqual(len(self.tg.events), 10, "Zaman çizelgesinde en az 10 hadise olmalı.")

    def test_first_and_last_events(self):
        years = [e["year"] for e in self.tg.events]
        self.assertEqual(min(years), 711, "İlk hadise 711 fetih yılı olmalı.")
        self.assertEqual(max(years), 1492, "Son hadise 1492 Gırnata düşüşü olmalı.")

    def test_filter_by_category(self):
        sci_events = self.tg.get_by_category("science")
        self.assertGreater(len(sci_events), 0, "Bilim kategorisinde hadiseler bulunmalı.")
        for e in sci_events:
            self.assertEqual(e["category"], "science")

    def test_mermaid_generation(self):
        mermaid = self.tg.to_mermaid()
        self.assertTrue(mermaid.startswith("timeline"))
        self.assertIn("711:", mermaid)
        self.assertIn("1492:", mermaid)

if __name__ == "__main__":
    unittest.main()
