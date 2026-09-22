# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - Corpus Statistics & Analytics Engine
Author: arch-yunus
"""
import os
import glob
import json
import argparse

def analyze_corpus(base_dir="."):
    stats = {
        "disciplines": {},
        "total_monographs": 0,
        "total_historiography": 0,
        "total_manuscripts": 0,
        "total_translations": 0,
        "total_quotes": 0,
        "total_timeline_events": 0,
        "monograph_word_count": 0,
        "libraries": []
    }

    # Count monographs
    monograph_files = glob.glob(os.path.join(base_dir, "monographs", "**", "*.md"), recursive=True)
    stats["total_monographs"] = len(monograph_files)

    for mf in monograph_files:
        discipline = os.path.basename(os.path.dirname(mf))
        stats["disciplines"][discipline] = stats["disciplines"].get(discipline, 0) + 1
        with open(mf, "r", encoding="utf-8") as f:
            words = len(f.read().split())
            stats["monograph_word_count"] += words

    # Count historiography
    hist_files = glob.glob(os.path.join(base_dir, "historiography", "**", "*.md"), recursive=True)
    stats["total_historiography"] = len(hist_files)

    # Count manuscripts
    ms_files = glob.glob(os.path.join(base_dir, "data", "manuscripts", "*_catalog.json"))
    for msf in ms_files:
        try:
            with open(msf, "r", encoding="utf-8") as f:
                d = json.load(f)
                count = len(d.get("manuscripts", []))
                stats["total_manuscripts"] += count
                stats["libraries"].append({
                    "name": d.get("repository", os.path.basename(msf)),
                    "count": count,
                    "city": d.get("city", "-"),
                    "country": d.get("country", "-")
                })
        except Exception:
            pass

    # Count translations
    try:
        with open(os.path.join(base_dir, "data", "translations", "toledo_school_corpus.json"), "r", encoding="utf-8") as f:
            t_data = json.load(f)
            stats["total_translations"] = len(t_data.get("translations", []))
    except Exception:
        pass

    # Count quotes
    try:
        with open(os.path.join(base_dir, "data", "quotes-archive", "historical_quotes.json"), "r", encoding="utf-8") as f:
            q_data = json.load(f)
            stats["total_quotes"] = len(q_data.get("quotes", []))
    except Exception:
        pass

    # Count timeline events
    try:
        from tools.timeline_generator import TIMELINE_EVENTS
        stats["total_timeline_events"] = len(TIMELINE_EVENTS)
    except Exception:
        try:
            from timeline_generator import TIMELINE_EVENTS
            stats["total_timeline_events"] = len(TIMELINE_EVENTS)
        except Exception:
            pass

    return stats

def main():
    parser = argparse.ArgumentParser(description="Zamân-ı Endülüs Corpus Statistics CLI")
    parser.add_argument("--json", action="store_true", help="Output raw JSON statistics")
    args = parser.parse_args()

    stats = analyze_corpus()

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    print("===================================================================")
    print("           ZAMÂN-I ENDÜLÜS KÜLLİYAT İSTATİSTİK RAPORU             ")
    print("===================================================================")
    print(f"Toplam Akademik Monografi      : {stats['total_monographs']} Adet ({stats['monograph_word_count']:,} Kelime)")
    print(f"Toplam Tarihyazımı ve Tenkit   : {stats['total_historiography']} Makale")
    print(f"Fihristlenen Yazma Eser Sayısı : {stats['total_manuscripts']} Nüsha ({len(stats['libraries'])} Kütüphane)")
    print(f"Toledo Tercüme Korpusu         : {stats['total_translations']} Temel Eser")
    print(f"Birincil Alıntı ve Tanıklık    : {stats['total_quotes']} Kayıt")
    print(f"Tarih ve Bilim Kronolojisi     : {stats['total_timeline_events']} Dönüm Noktası (711-1492)")
    print("-------------------------------------------------------------------")
    print("Disiplinler Dağılımı:")
    for disc, cnt in stats["disciplines"].items():
        print(f"  * {disc:<26} : {cnt} Monografi")
    print("-------------------------------------------------------------------")
    print("Fihristlenen Kütüphaneler:")
    for lib in stats["libraries"]:
        print(f"  * {lib['name']} ({lib['city']}, {lib['country']}): {lib['count']} Yazma")
    print("===================================================================")

if __name__ == "__main__":
    main()
