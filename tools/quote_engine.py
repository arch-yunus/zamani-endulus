# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - Quote Engine & Primary Source Citation CLI
Author: arch-yunus
"""
import os
import sys
import json
import random
import argparse

class QuoteEngine:
    def __init__(self, data_file="data/quotes-archive/historical_quotes.json"):
        self.data_file = data_file
        self.quotes = []
        self.load_quotes()

    def load_quotes(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quotes = data.get("quotes", [])
        except Exception as e:
            print(f"[WARN] Error loading quotes: {e}", file=sys.stderr)

    def search(self, query=None, category=None, speaker=None):
        results = self.quotes
        if query:
            q = query.lower()
            results = [
                r for r in results
                if q in r.get("text_tr", "").lower()
                or q in r.get("text_original", "").lower()
                or q in r.get("speaker", "").lower()
                or q in r.get("source", "").lower()
            ]
        if category:
            c = category.lower()
            results = [r for r in results if c == r.get("category", "").lower()]
        if speaker:
            s = speaker.lower()
            results = [r for r in results if s in r.get("speaker", "").lower()]
        return results

    def get_random(self, category=None):
        pool = self.search(category=category)
        return random.choice(pool) if pool else None

    def format_quote_markdown(self, q):
        return (
            f"> *\"{q.get('text_tr')}\"*\n"
            f"> — **{q.get('speaker')}** ({q.get('speaker_title', '')})\n"
            f"> *Kaynak:* `{q.get('source')}` | *Durum:* {q.get('verification_status', 'Doğrulandı')}"
        )

def main():
    parser = argparse.ArgumentParser(description="Zamân-ı Endülüs Primary Quotes Engine")
    parser.add_argument("--random", "-r", action="store_true", help="Pick a random historical quote")
    parser.add_argument("--category", "-c", choices=["western_historians", "medieval_witnesses", "andalusian_scholars", "elegies_and_laments"])
    parser.add_argument("--speaker", "-s", type=str, help="Filter by speaker name")
    parser.add_argument("--search", "-q", type=str, help="Search inside quotes")
    parser.add_argument("--format", "-f", choices=["text", "markdown", "json"], default="text")

    args = parser.parse_args()
    engine = QuoteEngine()

    if args.random:
        q = engine.get_random(category=args.category)
        if not q:
            print("Alıntı bulunamadı.")
            return
        if args.format == "json":
            print(json.dumps(q, ensure_ascii=False, indent=2))
        elif args.format == "markdown":
            print(engine.format_quote_markdown(q))
        else:
            print(f"\"{q.get('text_tr')}\"")
            print(f" — {q.get('speaker')} ({q.get('source')})")
        return

    results = engine.search(query=args.search, category=args.category, speaker=args.speaker)
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        for r in results:
            print(engine.format_quote_markdown(r))
            print()
    else:
        print(f"=== Zamân-ı Endülüs Alıntılar Arşivi ({len(results)} Kayıt) ===\n")
        for i, q in enumerate(results, 1):
            print(f"[{i}] \"{q.get('text_tr')}\"")
            print(f"    Söyleyen: {q.get('speaker')} ({q.get('speaker_title')})")
            print(f"    Kaynak  : {q.get('source')}")
            print(f"    Orijinal: {q.get('text_original')}\n")

if __name__ == "__main__":
    main()
