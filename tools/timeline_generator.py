# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - 711-1492 Historical & Scientific Chronology Compiler
Author: arch-yunus
"""
import sys
import json
import argparse

TIMELINE_EVENTS = [
    {
        "year": 711,
        "date_str": "711 CE (92 AH)",
        "era": "Fetih ve Valiler Dönemi",
        "title": "Târık bin Ziyâd ve Guadalete Zaferi",
        "description": "Târık bin Ziyâd komutasındaki kuvvetlerin Cebelitarık'ı geçmesi ve Vizigot Kralı Rodrigo'yu mağlup ederek Endülüs medeniyetinin temelini atması.",
        "category": "political"
    },
    {
        "year": 756,
        "date_str": "756 CE (138 AH)",
        "era": "Kurtuba Emevî Emirliği",
        "title": "I. Abdurrahman (ed-Dâhil) ve Bağımsız Emirlik",
        "description": "Abbasilerden kurtulan I. Abdurrahman'ın Kurtuba'yı başkent yaparak bağımsız Endülüs Emevî Emirliğini kurması.",
        "category": "political"
    },
    {
        "year": 785,
        "date_str": "785 CE (170 AH)",
        "era": "Kurtuba Emevî Emirliği",
        "title": "Kurtuba Ulu Camii'nin (Mezquita) İnşası",
        "description": "I. Abdurrahman tarafından çift katlı kemer sistemi ve Roma-Vizigot sütunlarının meczedildiği cami inşasının başlaması.",
        "category": "architecture"
    },
    {
        "year": 822,
        "date_str": "822 CE",
        "era": "Kurtuba Emevî Emirliği",
        "title": "Ziryâb'ın Kurtuba'ya Gelişi ve Kültür Devrimi",
        "description": "Bağdat'tan gelen ud üstadı Ziryâb'ın beş telli ud, konservatuvar, sofra adabı, mevsimlik giyim ve gastronomi kültürünü İberya'ya taşıması.",
        "category": "culture"
    },
    {
        "year": 875,
        "date_str": "875 CE",
        "era": "Kurtuba Emevî Emirliği",
        "title": "Abbâs bin Fırnâs'ın Süzülme ve Uçuş Denemesi",
        "description": "Polimat bilgin Abbâs bin Fırnâs'ın Cebelü'l-Arûs tepesinde kanat takarak aerodinamik süzülme denemesi ve ilk cam/gözlük lensi imalatı.",
        "category": "science"
    },
    {
        "year": 929,
        "date_str": "929 CE (316 AH)",
        "era": "Kurtuba Emevî Hilafeti",
        "title": "III. Abdurrahman (en-Nâsır) ve Hilafetin İlanı",
        "description": "Endülüs'ün altın çağı; III. Abdurrahman'ın halife unvanını alması ve Akdeniz'in en güçlü devleti konumuna yükselmesi.",
        "category": "political"
    },
    {
        "year": 936,
        "date_str": "936–940 CE",
        "era": "Kurtuba Emevî Hilafeti",
        "title": "Medînetü'z-Zehrâ Saray Şehrinin İnşası",
        "description": "Kurtuba yakınlarında teraslı bahçeler, fıskiyeler, drenaj kanalları ve mermir kabul salonlarıyla devasa hilafet saray-kentinin kuruluşu.",
        "category": "architecture"
    },
    {
        "year": 961,
        "date_str": "961–976 CE",
        "era": "Kurtuba Emevî Hilafeti",
        "title": "II. el-Hakem Devri ve 400.000 Ciltlik Kütüphane",
        "description": "Bağdat, Şam ve İskenderiye'den toplanan yazmalarla Kurtuba Saray Kütüphanesi'nin dünyanın en büyük ilim merkezine dönüştürülmesi; halk mekteplerinin yaygınlaştırılması.",
        "category": "science"
    },
    {
        "year": 1000,
        "date_str": "c. 1000 CE",
        "era": "Kurtuba Emevî Hilafeti",
        "title": "Ez-Zehrâvî'nin Kitâbü't-Tasrîf'i Tamamlaması",
        "description": "200'den fazla cerrahi aletin çizimini ve kedi bağırsağından dikiş tekniğini içeren 30 ciltlik tıp şaheserinin telifi.",
        "category": "science"
    },
    {
        "year": 1031,
        "date_str": "1031 CE",
        "era": "Mülûkü't-Tavâif (Beylikler)",
        "title": "Hilafetin İlgası ve Beylikler Dönemi",
        "description": "Kurtuba Hilafeti'nin yıkılıp Sevilla, Toledo, Zaragoza, Granada gibi bağımsız taife emirliklerinin kurulması; ilim ve sanatın şehirlere yayılması.",
        "category": "political"
    },
    {
        "year": 1080,
        "date_str": "c. 1080 CE",
        "era": "Mülûkü't-Tavâif",
        "title": "Ez-Zerkâlî ve Toledo Zîci / Azafea Usturlabı",
        "description": "İbnü'z-Zerkâle'nin her enlemde çalışan evrensel usturlabı icat etmesi ve güneş evcinin hareketini ispatlaması.",
        "category": "science"
    },
    {
        "year": 1085,
        "date_str": "1085 CE",
        "era": "Mülûkü't-Tavâif / Reconquista",
        "title": "Toledo'nun Düşüşü ve Tercüme Mektebinin Başlaması",
        "description": "VI. Alfonso'nun Toledo'yu ele geçirmesi ve kütüphanelerdeki Arapça bilim mirasının Başpiskopos Raymond gözetiminde Latinceye çevrilmeye başlanması.",
        "category": "transmission"
    },
    {
        "year": 1130,
        "date_str": "1130–1187 CE",
        "era": "Murâbıtlar / Muvahhidler",
        "title": "Gerard of Cremona ve Toledo Tercüme Hareketi",
        "description": "Zehrâvî, Zerkâli, İbn Heysem, Hârizmî ve Batlamyus metinlerinin Latinceye aktarılması; Avrupa üniversitelerinin doğuşu.",
        "category": "transmission"
    },
    {
        "year": 1170,
        "date_str": "c. 1170–1185 CE",
        "era": "Muvahhidler Devri",
        "title": "İbn Tufeyl ve Hayy bin Yakzân",
        "description": "İbn Tufeyl'in tabula rasa ve ampirist felsefenin öncüsü olan alegorik romanını yazması.",
        "category": "philosophy"
    },
    {
        "year": 1179,
        "date_str": "1179–1198 CE",
        "era": "Muvahhidler Devri",
        "title": "İbn Rüşd: Faslü'l-Makâl ve Büyük Şerhler",
        "description": "Aklın ve felsefenin meşruiyetini savunan Faslü'l-Makâl, Tehâfütü't-Tehâfüt ve Aristo külliyatı şerhlerinin telifi; Latin İbn Rüşdçülüğü tohumlarının atılması.",
        "category": "philosophy"
    },
    {
        "year": 1238,
        "date_str": "1238 CE",
        "era": "Benî Ahmer (Nasrîler)",
        "title": "Gırnata Nasrî Emirliği ve Elhamra'nın Yükselişi",
        "description": "İbnü'l-Ahmer tarafından Gırnata'da son Endülüs devletinin kurulması; Elhamra Sarayı ve Cennetü'l-Ârif bahçelerinin inşası.",
        "category": "architecture"
    },
    {
        "year": 1248,
        "date_str": "1248 CE",
        "era": "Benî Ahmer",
        "title": "İbnü'l-Baytâr'ın Vefatı ve el-Câmi' Eseri",
        "description": "1.400'den fazla bitki ve ilacı içeren dev farmakope ansiklopedisinin tıp dünyasına mirası.",
        "category": "science"
    },
    {
        "year": 1277,
        "date_str": "1277 CE",
        "era": "Batı Skolastiği",
        "title": "Paris 1277 Mahkûmiyeti (Condemnations)",
        "description": "İbn Rüşdçü felsefe tezlerinin Sorbonne'da aforoz edilmesi ve Avrupa'da bağımsız fizik/doğa bilimleri tartışmalarının hız kazanması.",
        "category": "transmission"
    },
    {
        "year": 1492,
        "date_str": "2 Ocak 1492 CE",
        "era": "Son Dönem",
        "title": "Gırnata'nın Düşüşü ve Endülüs'ün Sonu",
        "description": "Son emir XII. Muhammed'in (Boabdil) anahtarları teslim etmesi; İberya'da 781 yıllık İslam egemenliğinin sona ermesi ve Rönesans'a devredilen muazzam miras.",
        "category": "political"
    }
]

class TimelineGenerator:
    def __init__(self, events=None):
        self.events = events or TIMELINE_EVENTS

    def get_by_category(self, cat):
        return [e for e in self.events if e.get("category") == cat]

    def get_by_era(self, era):
        return [e for e in self.events if era.lower() in e.get("era", "").lower()]

    def to_markdown(self):
        lines = [
            "# Zamân-ı Endülüs Kronolojisi (711–1492 CE)",
            "",
            "Endülüs medeniyetinin siyasi, felsefi, bilimsel ve mimari dönüşüm kilometre taşları.",
            ""
        ]
        for e in self.events:
            lines.append(f"### {e['date_str']} — {e['title']}")
            lines.append(f"- **Dönem:** {e['era']} | **Kategori:** `{e['category']}`")
            lines.append(f"- {e['description']}")
            lines.append("")
        return "\n".join(lines)

    def to_mermaid(self):
        lines = [
            "timeline",
            "    title Endülüs Medeniyeti Tarihsel ve Bilimsel Çizgisi (711-1492)"
        ]
        eras = {}
        for e in self.events:
            era = e["era"]
            if era not in eras:
                eras[era] = []
            eras[era].append(f"{e['year']}: {e['title']}")

        for era, items in eras.items():
            lines.append(f"    section {era}")
            for item in items:
                lines.append(f"        {item}")
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Zamân-ı Endülüs Timeline CLI")
    parser.add_argument("--format", "-f", choices=["text", "markdown", "mermaid", "json"], default="text")
    parser.add_argument("--category", "-c", choices=["political", "science", "philosophy", "architecture", "culture", "transmission"])
    args = parser.parse_args()

    tg = TimelineGenerator()
    events = tg.get_by_category(args.category) if args.category else tg.events

    if args.format == "json":
        print(json.dumps(events, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(tg.to_markdown())
    elif args.format == "mermaid":
        print(tg.to_mermaid())
    else:
        print("=== Zamân-ı Endülüs Kronolojik Hadiseler ===")
        for e in events:
            print(f"[{e['year']}] {e['title']} ({e['era']})")
            print(f"      {e['description']}\n")

if __name__ == "__main__":
    main()
