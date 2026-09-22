# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - Toledo Translation School Explorer & Query CLI
Author: arch-yunus
"""
import os
import sys
import json
import argparse

class TranslationExplorer:
    def __init__(self, data_file="data/translations/toledo_school_corpus.json"):
        self.data_file = data_file
        self.translations = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.translations = data.get("translations", [])
        except Exception as e:
            print(f"[WARN] Failed to load translations: {e}", file=sys.stderr)

    def search(self, query=None, discipline=None, translator=None):
        results = self.translations
        if query:
            q = query.lower()
            results = [
                t for t in results
                if q in t.get("author_arabic", "").lower()
                or q in t.get("latin_title", "").lower()
                or q in t.get("translator", "").lower()
                or q in t.get("discipline", "").lower()
                or q in t.get("impact_in_europe", "").lower()
                or any(q in inv.lower() for inv in t.get("key_innovations_transferred", []))
            ]
        if discipline:
            d = discipline.lower()
            results = [t for t in results if d in t.get("discipline", "").lower()]
        if translator:
            tr = translator.lower()
            results = [t for t in results if tr in t.get("translator", "").lower()]
        return results

    def export_markdown_table(self, items=None):
        if items is None:
            items = self.translations
        lines = [
            "| Latince Başlık | Müellif | Mütercim & Dönem | Disiplin | Avrupa'daki Etkisi |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for t in items:
            title = f"**{t.get('latin_title')}**"
            author = t.get("author_arabic", "-")
            trans = f"{t.get('translator', '-')} ({t.get('translation_period', '-')})"
            disc = t.get("discipline", "-")
            impact = t.get("impact_in_europe", "-")
            lines.append(f"| {title} | {author} | {trans} | `{disc}` | {impact} |")
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Zamân-ı Endülüs Toledo Translation Explorer CLI")
    parser.add_argument("--search", "-s", type=str, help="Search across translations")
    parser.add_argument("--discipline", "-d", type=str, help="Filter by scientific discipline")
    parser.add_argument("--translator", "-t", type=str, help="Filter by translator name")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text")

    args = parser.parse_args()
    explorer = TranslationExplorer()
    results = explorer.search(query=args.search, discipline=args.discipline, translator=args.translator)

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(explorer.export_markdown_table(results))
    else:
        print(f"=== Toledo Tercüme Mektebi Korpusu (Bulunan: {len(results)}/{len(explorer.translations)}) ===\n")
        for i, t in enumerate(results, 1):
            print(f"[{i}] {t.get('latin_title')}")
            print(f"    Arapça Müellif : {t.get('author_arabic')}")
            print(f"    Eser           : {t.get('work_arabic')}")
            print(f"    Mütercim       : {t.get('translator')} ({t.get('translation_period')})")
            print(f"    Disiplin       : {t.get('discipline')}")
            print("    Aktarılanlar   :")
            for inn in t.get("key_innovations_transferred", []):
                print(f"      * {inn}")
            print(f"    Avrupa Etkisi  : {t.get('impact_in_europe')}\n")

if __name__ == "__main__":
    main()
