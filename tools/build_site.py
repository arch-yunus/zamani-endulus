# -*- coding: utf-8 -*-
"""
Zamân-ı Endülüs - Automated Site Compiler and Static Asset Synchronizer
Author: arch-yunus
"""
import os
import sys
import glob
import json
import re

def extract_metadata_from_markdown(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().split("\n")
    title = ""
    summary = ""
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("> ") and not summary:
            summary = line[2:].strip()

    if not title:
        title = os.path.basename(filepath).replace(".md", "").replace("_", " ").title()
    if not summary:
        summary = "Akademik Endülüs monografisi ve kaynakça incelemesi."

    return {
        "id": os.path.basename(filepath).replace(".md", ""),
        "title": title,
        "summary": summary,
        "content": content,
        "filename": os.path.relpath(filepath, ".").replace("\\", "/")
    }

def compile_corpus(base_dir="."):
    # 1. Monographs
    monographs = []
    disciplines = {
        "medicine-surgery": "Cerrahi ve Klinik Tıp Ekolü",
        "astronomy-mechanics": "Astronomi, Matematik ve Mekanik",
        "philosophy-episteme": "Rasyonalist Felsefe ve Epistemoloji",
        "hydraulic-engineering": "Hidrolik Mühendisliği ve Ziraat (Filâha)",
        "geography-cartography": "Coğrafya, Kartografya ve Seyahatnâme",
        "literature-aesthetics": "Edebiyat, Mûsiki ve Estetik"
    }

    for disc_dir in disciplines.keys():
        pattern = os.path.join(base_dir, "monographs", disc_dir, "*.md")
        for mf in sorted(glob.glob(pattern)):
            meta = extract_metadata_from_markdown(mf)
            meta["discipline"] = disc_dir
            meta["discipline_name"] = disciplines[disc_dir]
            monographs.append(meta)

    # 2. Historiography
    historiography = []
    hist_patterns = [
        os.path.join(base_dir, "historiography", "myth-busting", "*.md"),
        os.path.join(base_dir, "historiography", "western-reception", "*.md")
    ]
    for pattern in hist_patterns:
        for hf in sorted(glob.glob(pattern)):
            meta = extract_metadata_from_markdown(hf)
            meta["category"] = os.path.basename(os.path.dirname(hf))
            historiography.append(meta)

    # 3. Manuscripts
    manuscripts = []
    ms_pattern = os.path.join(base_dir, "data", "manuscripts", "*_catalog.json")
    for msf in sorted(glob.glob(ms_pattern)):
        try:
            with open(msf, "r", encoding="utf-8") as f:
                d = json.load(f)
                repo = d.get("repository", os.path.basename(msf))
                for ms in d.get("manuscripts", []):
                    m_copy = dict(ms)
                    m_copy["_repository"] = repo
                    manuscripts.append(m_copy)
        except Exception as e:
            print(f"[WARN] Error reading manuscript {msf}: {e}", file=sys.stderr)

    # 4. Translations
    translations = []
    t_file = os.path.join(base_dir, "data", "translations", "toledo_school_corpus.json")
    try:
        with open(t_file, "r", encoding="utf-8") as f:
            translations = json.load(f).get("translations", [])
    except Exception as e:
        print(f"[WARN] Error reading translations: {e}", file=sys.stderr)

    # 5. Quotes
    quotes = []
    q_file = os.path.join(base_dir, "data", "quotes-archive", "historical_quotes.json")
    try:
        with open(q_file, "r", encoding="utf-8") as f:
            quotes = json.load(f).get("quotes", [])
    except Exception as e:
        print(f"[WARN] Error reading quotes: {e}", file=sys.stderr)

    # 6. Timeline
    sys.path.insert(0, base_dir)
    from tools.timeline_generator import TIMELINE_EVENTS
    timeline = TIMELINE_EVENTS

    return {
        "monographs": monographs,
        "historiography": historiography,
        "manuscripts": manuscripts,
        "translations": translations,
        "quotes": quotes,
        "timeline": timeline
    }

def generate_html(data, output_file="index.html"):
    json_payload = json.dumps(data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zamân-ı Endülüs — Bilimsel, Felsefi ve Teknolojik Miras Külliyatı</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        andalus: {{
                            gold: '#D4AF37',
                            darkgold: '#AA820A',
                            emerald: '#005A36',
                            deepgreen: '#032B1A',
                            sand: '#F4EBD9',
                            darkbg: '#0D1117',
                            cardbg: '#161B22',
                            border: '#30363D'
                        }}
                    }},
                    fontFamily: {{
                        cinzel: ['Cinzel', 'serif'],
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                        arabic: ['Amiri', 'serif']
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .geometric-pattern {{
            background-color: #0D1117;
            background-image: radial-gradient(#D4AF37 0.75px, transparent 0.75px), radial-gradient(#005A36 0.75px, #0D1117 0.75px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
        }}
        .glass-panel {{
            background: rgba(22, 27, 34, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(212, 175, 55, 0.2);
        }}
        .prose h1, .prose h2, .prose h3 {{ color: #D4AF37; font-family: 'Cinzel', serif; }}
        .prose blockquote {{ border-left-color: #D4AF37; font-style: italic; background: rgba(212, 175, 55, 0.05); padding: 0.75rem 1rem; border-radius: 0 0.5rem 0.5rem 0; }}
        .prose table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; margin-bottom: 1rem; font-size: 0.85rem; }}
        .prose th, .prose td {{ border: 1px solid #30363D; padding: 0.5rem 0.75rem; text-align: left; }}
        .prose th {{ background: rgba(212, 175, 55, 0.1); color: #D4AF37; }}
        .prose pre {{ background: #0b0e14; border: 1px solid #30363D; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }}
        .prose code {{ color: #E5C07B; }}
    </style>
</head>
<body class="bg-andalus-darkbg text-gray-100 min-h-screen font-sans selection:bg-andalus-gold selection:text-black">

    <!-- Header -->
    <header class="border-b border-andalus-border bg-andalus-darkbg/95 sticky top-0 z-40 backdrop-blur">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-10 h-10 rounded-full border-2 border-andalus-gold flex items-center justify-center bg-andalus-deepgreen shadow-lg shadow-andalus-gold/20">
                    <span class="text-andalus-gold font-bold text-lg font-cinzel">ⵣ</span>
                </div>
                <div>
                    <h1 class="text-xl font-bold font-cinzel tracking-wider text-andalus-gold flex items-center gap-2">
                        ZAMÂN-I ENDÜLÜS
                        <span class="text-xs font-sans px-2 py-0.5 rounded bg-andalus-emerald/40 text-emerald-300 border border-emerald-500/30">Külliyat v2.0</span>
                    </h1>
                    <p class="text-xs text-gray-400">711–1492 Bilimsel, Felsefi ve Teknolojik Miras Korpusu</p>
                </div>
            </div>

            <!-- Navigation Tabs -->
            <nav class="hidden md:flex space-x-1 font-medium text-sm">
                <button onclick="setTab('monographs')" id="nav-monographs" class="tab-btn px-3.5 py-2 rounded-lg text-andalus-gold bg-andalus-gold/10 border border-andalus-gold/30">Monografiler ({len(data['monographs'])})</button>
                <button onclick="setTab('manuscripts')" id="nav-manuscripts" class="tab-btn px-3.5 py-2 rounded-lg text-gray-300 hover:text-andalus-gold hover:bg-white/5">Yazma Eserler ({len(data['manuscripts'])})</button>
                <button onclick="setTab('translations')" id="nav-translations" class="tab-btn px-3.5 py-2 rounded-lg text-gray-300 hover:text-andalus-gold hover:bg-white/5">Toledo Tercümeleri ({len(data['translations'])})</button>
                <button onclick="setTab('timeline')" id="nav-timeline" class="tab-btn px-3.5 py-2 rounded-lg text-gray-300 hover:text-andalus-gold hover:bg-white/5">Kronoloji ({len(data['timeline'])})</button>
                <button onclick="setTab('quotes')" id="nav-quotes" class="tab-btn px-3.5 py-2 rounded-lg text-gray-300 hover:text-andalus-gold hover:bg-white/5">Alıntılar ({len(data['quotes'])})</button>
                <button onclick="setTab('mythbuster')" id="nav-mythbuster" class="tab-btn px-3.5 py-2 rounded-lg text-gray-300 hover:text-andalus-gold hover:bg-white/5">Mit Çürütücü ({len(data['historiography'])})</button>
            </nav>
        </div>
    </header>

    <!-- Hero Banner -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div class="relative rounded-2xl overflow-hidden border border-andalus-gold/30 shadow-2xl">
            <img src="docs/images/zamani_endulus_banner.jpg" alt="Zamân-ı Endülüs Medeniyet Panoraması" class="w-full h-64 md:h-72 object-cover" />
            <div class="absolute inset-0 bg-gradient-to-t from-andalus-darkbg via-andalus-darkbg/50 to-transparent flex flex-col justify-end p-6 md:p-8">
                <span class="text-xs font-cinzel text-andalus-gold uppercase tracking-widest mb-1">Akdeniz'in Kurucu Bilim, Felsefe ve Sanat Havzası</span>
                <h2 class="text-2xl md:text-4xl font-bold font-cinzel text-white drop-shadow-md">Kayıp Bir Bahçenin İzinde</h2>
                <p class="text-xs md:text-sm text-gray-300 max-w-3xl mt-1">Kurtuba kütüphanelerinden Toledo tercüme mekteplerine, cerrahi enstrümanlardan evrensel usturlaplara, İdrîsî haritalarından Ziryâb makamlarına uzanan 781 yıllık açık araştırma külliyatı.</p>
                <div class="flex flex-wrap gap-4 mt-3 text-xs text-gray-300">
                    <span class="bg-black/50 px-2.5 py-1 rounded border border-andalus-gold/30 font-mono text-andalus-gold">📚 {len(data['monographs'])} Akademik Monografi</span>
                    <span class="bg-black/50 px-2.5 py-1 rounded border border-andalus-gold/30 font-mono text-emerald-400">🏛️ 6 Uluslararası Kütüphane</span>
                    <span class="bg-black/50 px-2.5 py-1 rounded border border-andalus-gold/30 font-mono text-yellow-300">📜 {len(data['manuscripts'])} Fihristli Yazma</span>
                    <span class="bg-black/50 px-2.5 py-1 rounded border border-andalus-gold/30 font-mono text-cyan-300">⏱️ 711–1492 Kronolojisi</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- TAB: MONOGRAPHS -->
        <section id="tab-monographs" class="tab-content space-y-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-andalus-border pb-4">
                <div>
                    <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">Disiplinlerarası Monografiler</h2>
                    <p class="text-gray-400 text-sm">6 temel bilim ve düşünce sahasında telif edilmiş {len(data['monographs'])} akademik araştırma monografisi.</p>
                </div>
                <div class="flex gap-2">
                    <select id="monograph-filter" onchange="filterMonographs()" class="bg-andalus-cardbg border border-andalus-border rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-andalus-gold">
                        <option value="all">Tüm Disiplinler ({len(data['monographs'])})</option>
                        <option value="medicine-surgery">Cerrahi ve Tıp Ekolü (3)</option>
                        <option value="astronomy-mechanics">Astronomi ve Mekanik (3)</option>
                        <option value="philosophy-episteme">Felsefe ve Epistemoloji (3)</option>
                        <option value="hydraulic-engineering">Hidrolik ve Ziraat (3)</option>
                        <option value="geography-cartography">Coğrafya ve Kartografya (3)</option>
                        <option value="literature-aesthetics">Edebiyat ve Mûsiki (3)</option>
                    </select>
                </div>
            </div>

            <div id="monographs-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- TAB: MANUSCRIPTS -->
        <section id="tab-manuscripts" class="tab-content hidden space-y-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-andalus-border pb-4">
                <div>
                    <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">Yazma Eser Katalogları</h2>
                    <p class="text-gray-400 text-sm">El Escorial, BnF Paris, Bodleian Oxford, Vatikan, Süleymaniye ve Leiden kütüphanelerindeki temel Endülüs yazmaları ({len(data['manuscripts'])} Kayıt).</p>
                </div>
                <div class="flex gap-3">
                    <input type="text" id="ms-search" oninput="filterManuscripts()" placeholder="Yazma, kütüphane, müellif ara..." class="bg-andalus-cardbg border border-andalus-border rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-andalus-gold w-72">
                </div>
            </div>

            <div id="manuscripts-list" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- TAB: TRANSLATIONS -->
        <section id="tab-translations" class="tab-content hidden space-y-6">
            <div class="border-b border-andalus-border pb-4">
                <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">Toledo Tercüme Mektebi Külliyatı (12.–13. yy)</h2>
                <p class="text-gray-400 text-sm">Arapça bilim ve felsefe metinlerinin Latinceye ve Kastilyancaya aktarımı ve Avrupa üniversitelerine intikali ({len(data['translations'])} Temel Eser).</p>
            </div>

            <div id="translations-list" class="space-y-4">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- TAB: TIMELINE -->
        <section id="tab-timeline" class="tab-content hidden space-y-6">
            <div class="border-b border-andalus-border pb-4 flex justify-between items-center">
                <div>
                    <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">711–1492 Tarih ve Bilim Kronolojisi</h2>
                    <p class="text-gray-400 text-sm">Fetih'ten Gırnata'nın düşüşüne 781 yıllık medeniyet ve telif çizgisi ({len(data['timeline'])} Dönüm Noktası).</p>
                </div>
            </div>

            <div class="relative border-l-2 border-andalus-gold/30 ml-4 space-y-8 pl-6" id="timeline-container">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- TAB: QUOTES -->
        <section id="tab-quotes" class="tab-content hidden space-y-6">
            <div class="border-b border-andalus-border pb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">Alıntılar & Tarihsel Tanıklıklar</h2>
                    <p class="text-gray-400 text-sm">Doğu ve Batı kaynaklarında Endülüs'ün yankıları ve birincil belgeler ({len(data['quotes'])} Kayıt).</p>
                </div>
                <div class="flex gap-2">
                    <button onclick="getRandomQuote()" class="bg-andalus-gold text-black font-semibold text-xs px-3 py-2 rounded-lg hover:bg-yellow-400 transition shadow-lg">Rastgele Alıntı Getir</button>
                </div>
            </div>

            <div id="random-quote-card" class="p-6 rounded-xl bg-gradient-to-r from-andalus-emerald/30 to-andalus-cardbg border border-andalus-gold/40 shadow-xl">
                <!-- Injected via JS -->
            </div>

            <div id="quotes-grid" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- TAB: MYTH BUSTER -->
        <section id="tab-mythbuster" class="tab-content hidden space-y-6">
            <div class="border-b border-andalus-border pb-4">
                <h2 class="text-2xl font-bold font-cinzel text-andalus-gold">Mit Çürütücü (Myth-Buster) & Tenkitli Tarihyazımı</h2>
                <p class="text-gray-400 text-sm">Endülüs tarihyazımındaki romantik efsanelerin, anokronizmlerin ve asılsız rivayetlerin akademik tenkidi ({len(data['historiography'])} Rapor).</p>
            </div>

            <div id="mythbuster-list" class="space-y-6">
                <!-- Injected via JS -->
            </div>
        </section>
    </main>

    <!-- Modal for Monograph Reading -->
    <div id="monograph-modal" class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-andalus-cardbg border border-andalus-gold/40 rounded-xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl">
            <div class="p-4 border-b border-andalus-border flex justify-between items-center">
                <h3 id="modal-title" class="font-cinzel text-andalus-gold font-bold text-lg">Monografi</h3>
                <button onclick="closeModal()" class="text-gray-400 hover:text-white text-2xl font-bold px-2">&times;</button>
            </div>
            <div id="modal-content" class="p-6 overflow-y-auto prose prose-invert max-w-none text-gray-200">
                <!-- Markdown rendered here -->
            </div>
        </div>
    </div>

    <!-- Data Injection & Frontend Logic -->
    <script>
        const APP_DATA = {json_payload};

        function setTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('text-andalus-gold', 'bg-andalus-gold/10', 'border', 'border-andalus-gold/30');
                el.classList.add('text-gray-300');
            }});

            const targetSection = document.getElementById('tab-' + tabName);
            const targetBtn = document.getElementById('nav-' + tabName);
            if (targetSection) targetSection.classList.remove('hidden');
            if (targetBtn) {{
                targetBtn.classList.remove('text-gray-300');
                targetBtn.classList.add('text-andalus-gold', 'bg-andalus-gold/10', 'border', 'border-andalus-gold/30');
            }}
        }}

        function renderMonographs(filter = 'all') {{
            const grid = document.getElementById('monographs-grid');
            grid.innerHTML = '';
            
            const list = filter === 'all' 
                ? APP_DATA.monographs 
                : APP_DATA.monographs.filter(m => m.discipline === filter);

            list.forEach(m => {{
                const card = document.createElement('div');
                card.className = 'bg-andalus-cardbg border border-andalus-border hover:border-andalus-gold/60 p-5 rounded-xl transition duration-200 flex flex-col justify-between group shadow-lg';
                card.innerHTML = `
                    <div class="space-y-2">
                        <div class="flex items-center justify-between text-xs">
                            <span class="text-emerald-400 font-mono">${{m.discipline_name}}</span>
                        </div>
                        <h3 class="text-base font-bold font-cinzel text-white group-hover:text-andalus-gold transition line-clamp-2">${{m.title}}</h3>
                        <p class="text-xs text-gray-400 line-clamp-3 leading-relaxed">${{m.summary}}</p>
                    </div>
                    <div class="pt-4 mt-4 border-t border-andalus-border/50 flex items-center justify-between">
                        <span class="text-[11px] text-gray-500 font-mono">${{m.filename}}</span>
                        <button onclick="viewMonograph('${{m.id}}')" class="text-xs font-semibold text-andalus-gold hover:underline flex items-center gap-1">
                            Oku <span>&rarr;</span>
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function filterMonographs() {{
            const filter = document.getElementById('monograph-filter').value;
            renderMonographs(filter);
        }}

        function viewMonograph(id) {{
            let item = APP_DATA.monographs.find(m => m.id === id);
            if (!item) {{
                item = APP_DATA.historiography.find(h => h.id === id);
            }}
            if (!item) return;

            document.getElementById('modal-title').innerText = item.title;
            document.getElementById('modal-content').innerHTML = marked.parse(item.content);
            document.getElementById('monograph-modal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('monograph-modal').classList.add('hidden');
        }}

        function renderManuscripts(query = '') {{
            const list = document.getElementById('manuscripts-list');
            list.innerHTML = '';
            const q = query.toLowerCase();

            const filtered = APP_DATA.manuscripts.filter(m => {{
                if (!q) return true;
                return (m.shelfmark || '').toLowerCase().includes(q)
                    || (m.title_turkish || '').toLowerCase().includes(q)
                    || (m.title_arabic || '').toLowerCase().includes(q)
                    || (m.author || '').toLowerCase().includes(q)
                    || (m._repository || '').toLowerCase().includes(q)
                    || (m.subject || '').toLowerCase().includes(q);
            }});

            filtered.forEach(m => {{
                const card = document.createElement('div');
                card.className = 'bg-andalus-cardbg border border-andalus-border p-5 rounded-xl space-y-3';
                card.innerHTML = `
                    <div class="flex items-start justify-between border-b border-andalus-border pb-2">
                        <div>
                            <span class="text-xs font-mono bg-andalus-gold/20 text-andalus-gold px-2 py-0.5 rounded">${{m.shelfmark}}</span>
                            <div class="text-[11px] text-gray-400 mt-1">${{m._repository}}</div>
                        </div>
                        <span class="text-xs text-emerald-400 font-sans">${{m.subject}}</span>
                    </div>
                    <div>
                        <h4 class="font-arabic text-md text-yellow-100/90 text-right dir-rtl leading-relaxed">${{m.title_arabic || ''}}</h4>
                        <h4 class="font-cinzel text-sm font-bold text-white mt-1">${{m.title_turkish}}</h4>
                        <div class="text-xs text-gray-400 mt-0.5"><strong class="text-gray-300">Müellif:</strong> ${{m.author}} (${{m.author_death_year || ''}})</div>
                    </div>
                    <p class="text-xs text-gray-300 leading-relaxed"><strong class="text-andalus-gold">Önemi:</strong> ${{m.historical_importance}}</p>
                    <div class="text-[11px] text-gray-400 border-t border-andalus-border/40 pt-2 flex flex-wrap gap-2">
                        <span>📄 ${{m.folios}}</span>
                        <span>📜 ${{m.script}}</span>
                        ${{m.illustrations ? '<span class="text-yellow-400">🎨 Minyatür/Alet Çizimli</span>' : ''}}
                    </div>
                `;
                list.appendChild(card);
            }});
        }}

        function filterManuscripts() {{
            const q = document.getElementById('ms-search').value;
            renderManuscripts(q);
        }}

        function renderTranslations() {{
            const list = document.getElementById('translations-list');
            list.innerHTML = '';
            APP_DATA.translations.forEach(t => {{
                const card = document.createElement('div');
                card.className = 'bg-andalus-cardbg border border-andalus-border p-5 rounded-xl space-y-3 shadow-md';
                card.innerHTML = `
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-andalus-border pb-2">
                        <h3 class="text-md font-bold text-andalus-gold font-cinzel">${{t.latin_title}}</h3>
                        <span class="text-xs bg-emerald-950/80 text-emerald-300 px-2.5 py-1 rounded border border-emerald-500/30">${{t.discipline}}</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs text-gray-300">
                        <div><span class="text-gray-500">Müellif:</span> ${{t.author_arabic}}</div>
                        <div><span class="text-gray-500">Mütercim:</span> ${{t.translator}}</div>
                        <div><span class="text-gray-500">Dönem:</span> ${{t.translation_period}}</div>
                    </div>
                    <div class="text-xs text-gray-300">
                        <span class="text-gray-500 font-semibold block mb-1">Aktarılan Temel Yenilikler:</span>
                        <ul class="list-disc list-inside space-y-0.5 text-gray-400">
                            ${{t.key_innovations_transferred.map(i => `<li>${{i}}</li>`).join('')}}
                        </ul>
                    </div>
                    <p class="text-xs text-yellow-100/70 bg-black/20 p-2.5 rounded border border-white/5"><strong class="text-andalus-gold">Avrupa'daki Etkisi:</strong> ${{t.impact_in_europe}}</p>
                `;
                list.appendChild(card);
            }});
        }}

        function renderTimeline() {{
            const container = document.getElementById('timeline-container');
            container.innerHTML = '';
            APP_DATA.timeline.forEach(e => {{
                const item = document.createElement('div');
                item.className = 'relative group';
                item.innerHTML = `
                    <div class="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-andalus-gold border-2 border-andalus-darkbg group-hover:scale-125 transition"></div>
                    <div class="bg-andalus-cardbg border border-andalus-border p-4 rounded-xl space-y-1.5 hover:border-andalus-gold/50 transition">
                        <div class="flex items-center justify-between text-xs">
                            <span class="font-bold text-andalus-gold font-mono">${{e.date_str}}</span>
                            <span class="text-gray-400 bg-white/5 px-2 py-0.5 rounded">${{e.era}}</span>
                        </div>
                        <h4 class="font-cinzel font-bold text-white text-md">${{e.title}}</h4>
                        <p class="text-xs text-gray-300 leading-relaxed">${{e.description}}</p>
                    </div>
                `;
                container.appendChild(item);
            }});
        }}

        function renderQuotes() {{
            const grid = document.getElementById('quotes-grid');
            grid.innerHTML = '';
            APP_DATA.quotes.forEach(q => {{
                const card = document.createElement('div');
                card.className = 'bg-andalus-cardbg border border-andalus-border p-5 rounded-xl flex flex-col justify-between space-y-3 shadow-md';
                card.innerHTML = `
                    <div>
                        <p class="text-sm italic text-gray-200 leading-relaxed font-serif">“${{q.text_tr}}”</p>
                    </div>
                    <div class="pt-3 border-t border-andalus-border/50 text-xs">
                        <div class="font-bold text-andalus-gold">${{q.speaker}}</div>
                        <div class="text-gray-400">${{q.speaker_title}}</div>
                        <div class="text-[11px] text-gray-500 mt-1 font-mono">Kaynak: ${{q.source}}</div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function getRandomQuote() {{
            const pool = APP_DATA.quotes;
            const q = pool[Math.floor(Math.random() * pool.length)];
            const card = document.getElementById('random-quote-card');
            card.innerHTML = `
                <div class="text-xs text-andalus-gold uppercase font-bold tracking-wider mb-2">⭐ Günün Tarihsel Tanıklığı</div>
                <p class="text-base md:text-lg italic text-white font-serif mb-3">“${{q.text_tr}}”</p>
                <div class="flex justify-between items-end text-xs text-gray-300 pt-2 border-t border-white/10">
                    <div>
                        <strong class="text-andalus-gold">${{q.speaker}}</strong> — ${{q.speaker_title}}
                        <div class="text-gray-400 text-[11px] mt-0.5 font-mono">${{q.source}}</div>
                    </div>
                    <span class="px-2 py-0.5 rounded bg-emerald-900/60 text-emerald-300 border border-emerald-500/30 text-[10px]">Doğrulandı</span>
                </div>
            `;
        }}

        function renderMythBuster() {{
            const container = document.getElementById('mythbuster-list');
            container.innerHTML = '';
            APP_DATA.historiography.forEach(h => {{
                const card = document.createElement('div');
                card.className = 'bg-andalus-cardbg border border-red-900/40 hover:border-red-500/60 p-6 rounded-xl space-y-3';
                card.innerHTML = `
                    <div class="flex items-center gap-2">
                        <span class="bg-red-950 text-red-400 border border-red-800 text-xs px-2.5 py-0.5 rounded font-bold uppercase">Kritik Analiz & Tenkit</span>
                        <span class="text-xs text-gray-400 font-mono">${{h.filename}}</span>
                    </div>
                    <h3 class="text-lg font-bold text-white font-cinzel">${{h.title}}</h3>
                    <p class="text-xs text-gray-300 line-clamp-3">${{h.content.split('\\n').slice(2, 6).join(' ').replace(/[#*`>]/g, '')}}</p>
                    <button onclick="viewMonograph('${{h.id}}')" class="text-xs font-bold text-red-400 hover:text-red-300 underline pt-2 block">
                        Raporu ve Kaynakça Tenkidini Oku →
                    </button>
                `;
                container.appendChild(card);
            }});
        }}

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {{
            renderMonographs();
            renderManuscripts();
            renderTranslations();
            renderTimeline();
            renderQuotes();
            getRandomQuote();
            renderMythBuster();
        }});
    </script>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] Successfully compiled {output_file} ({len(data['monographs'])} monographs, {len(data['manuscripts'])} manuscripts, {len(data['historiography'])} historiography essays)")

def main():
    data = compile_corpus(".")
    generate_html(data, "index.html")

if __name__ == "__main__":
    main()
