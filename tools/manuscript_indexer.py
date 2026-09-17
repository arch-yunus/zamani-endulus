# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - Manuscript Indexer & Cross-Repository Search Tool
Author: arch-yunus
"""
import os
import sys
import json
import glob
import argparse

class ManuscriptCatalog:
    def __init__(self, data_dir="data/manuscripts"):
        self.data_dir = data_dir
        self.catalogs = []
        self.manuscripts = []
        self.load_catalogs()

    def load_catalogs(self):
        self.catalogs = []
        self.manuscripts = []
        pattern = os.path.join(self.data_dir, "*_catalog.json")
        for filepath in glob.glob(pattern):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.catalogs.append(data)
                    repo_name = data.get("repository", os.path.basename(filepath))
                    for ms in data.get("manuscripts", []):
                        ms_copy = dict(ms)
                        ms_copy["_repository"] = repo_name
                        ms_copy["_catalog_file"] = os.path.basename(filepath)
                        self.manuscripts.append(ms_copy)
            except Exception as e:
                print(f"[WARN] Failed to load {filepath}: {e}", file=sys.stderr)

    def total_count(self):
        return len(self.manuscripts)

    def search(self, query=None, subject=None, author=None, repository=None):
        results = self.manuscripts
        if query:
            q = query.lower()
            results = [
                m for m in results
                if q in m.get("shelfmark", "").lower()
                or q in m.get("title_translit", "").lower()
                or q in m.get("title_turkish", "").lower()
                or q in m.get("author", "").lower()
                or q in m.get("subject", "").lower()
                or q in m.get("historical_importance", "").lower()
            ]
        if subject:
            s = subject.lower()
            results = [m for m in results if s in m.get("subject", "").lower()]
        if author:
            a = author.lower()
            results = [m for m in results if a in m.get("author", "").lower()]
        if repository:
            r = repository.lower()
            results = [m for m in results if r in m.get("_repository", "").lower()]
        return results

    def export_markdown_table(self, items=None):
        if items is None:
            items = self.manuscripts
        lines = [
            "| Demirbaş / Raf No | Eser (Transkripsiyon / Türkçe) | Müellif | Konu / Alan | Bulunduğu Kütüphane |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for m in items:
            shelfmark = m.get("shelfmark", "-")
            title = f"{m.get('title_translit', '')} ({m.get('title_turkish', '')})"
            author = m.get("author", "-")
            subj = m.get("subject", "-")
            repo = m.get("_repository", "-")
            lines.append(f"| `{shelfmark}` | {title} | {author} | {subj} | {repo} |")
        return "\n".join(lines)

    def validate_schema(self):
        required_fields = ["shelfmark", "title_translit", "author", "subject", "historical_importance"]
        errors = []
        for ms in self.manuscripts:
            for field in required_fields:
                if not ms.get(field):
                    errors.append(f"Missing field '{field}' in manuscript {ms.get('shelfmark', 'UNKNOWN')}")
        return errors

def main():
    parser = argparse.ArgumentParser(description="Zamân-ı Endülüs Manuscript Indexer CLI")
    parser.add_argument("--search", "-s", type=str, help="Search term across manuscripts")
    parser.add_argument("--subject", "-sub", type=str, help="Filter by subject/discipline")
    parser.add_argument("--author", "-a", type=str, help="Filter by author")
    parser.add_argument("--repo", "-r", type=str, help="Filter by holding library")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--validate", action="store_true", help="Run schema integrity checks")

    args = parser.parse_args()
    catalog = ManuscriptCatalog()

    if args.validate:
        errors = catalog.validate_schema()
        if errors:
            print(f"Validation FAILED with {len(errors)} errors:")
            for err in errors:
                print(" -", err)
            sys.exit(1)
        else:
            print(f"Validation SUCCESS: {catalog.total_count()} manuscripts validated across {len(catalog.catalogs)} catalogs.")
            sys.exit(0)

    results = catalog.search(query=args.search, subject=args.subject, author=args.author, repository=args.repo)

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(catalog.export_markdown_table(results))
    else:
        print(f"=== Zamân-ı Endülüs Yazma Eserler Fihristi (Bulunan: {len(results)}/{catalog.total_count()}) ===")
        for i, m in enumerate(results, 1):
            print(f"\n[{i}] {m.get('shelfmark')} | {m.get('_repository')}")
            print(f"    Başlık   : {m.get('title_arabic')} / {m.get('title_translit')}")
            print(f"    Türkçe   : {m.get('title_turkish')}")
            print(f"    Müellif  : {m.get('author')} ({m.get('author_death_year', '')})")
            print(f"    Konu     : {m.get('subject')}")
            print(f"    Latince  : {m.get('latin_translation', 'Yok')}")
            print(f"    Önem     : {m.get('historical_importance')}")

if __name__ == "__main__":
    main()
