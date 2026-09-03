# -*- coding: utf-8 -*-
"""Apply the REAL B2 visual shell (extracted from German-B2-TEST APK assets/www/index.html)
to C1, keeping ALL C1 content/stats/text. Visual-only. Fail-safe exact replaces."""
import io, re, hashlib

P = "German-C1-Vocabulary.html"
h = io.open(P, encoding="utf-8").read()
orig = h
def rep(old, new, tag):
    global h
    if h.count(old) != 1:
        raise SystemExit("ABORT [%s]: found %d" % (tag, h.count(old)))
    h = h.replace(old, new)

def bigs(t): return sorted(hashlib.md5(l.encode("utf-8")).hexdigest() for l in t.split("\n") if len(l) > 2000)
before = bigs(h)

# 1) :root -> B2 navy/royal-blue palette
rep(":root{--ink:#0f172a;--paper:#f8fafc;--accent:#1e3a8a;--accent2:#fcd34d;--accent-light:#dbeafe;--red:#b91c1c;--red-light:#fee2e2;--blue:#1e40af;--border:#cbd5e1;--muted:#475569;--card:#fff;--dark-card:#172554;--green:#a16207;--green-light:#fef9c3;--navy:#0f1e46;--navy2:#1e3a8a;--gold:#fbbf24;}",
    ":root{--ink:#0f172a;--paper:#f8fafc;--accent:#1d4ed8;--accent2:#93c5fd;--accent-light:#dbeafe;--red:#b91c1c;--red-light:#fee2e2;--blue:#1d4ed8;--border:#cbd5e1;--muted:#475569;--card:#fff;--dark-card:#16305e;--green:#a16207;--green-light:#fef9c3;}", "root")

# 2) hero CSS block (home-hero .. hstat span) -> B2 exact
OLD_HERO_CSS = """.home-hero{background:linear-gradient(160deg,#0f1e46 0%,#1e3a8a 58%,#101d43 100%);color:#fff;padding:36px 22px 30px;text-align:center;position:relative;overflow:hidden;}
.home-hero::before{content:'';position:absolute;top:-50px;right:-50px;width:220px;height:220px;background:radial-gradient(circle,rgba(252,211,77,.28) 0%,transparent 70%);border-radius:50%;}
.home-hero .skyline{position:absolute;left:0;right:0;bottom:0;width:100%;height:54px;opacity:.55;pointer-events:none;display:block;}
.home-series{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#fcd34d;margin-bottom:8px;position:relative;}
.home-hero h1{font-family:Georgia,serif;font-size:1.72rem;font-weight:700;margin-bottom:8px;position:relative;line-height:1.2;}
.home-hero h1 span{color:#fbbf24;}
.home-hero .tag{font-size:.9rem;color:rgba(255,255,255,.82);margin-bottom:4px;position:relative;font-style:normal;}
.home-hero .hero-sub{font-size:.72rem;letter-spacing:.03em;color:#fcd34d;margin-bottom:16px;position:relative;font-weight:600;}
.home-stats{display:flex;justify-content:center;gap:14px;position:relative;}
.hstat{background:rgba(255,255,255,.12);border-radius:12px;padding:9px 18px;text-align:center;}
.hstat b{font-size:1.4rem;font-weight:800;display:block;line-height:1;}
.hstat span{font-size:.62rem;opacity:.8;text-transform:uppercase;letter-spacing:.6px;}"""
NEW_HERO_CSS = """.home-hero{background:linear-gradient(180deg,#16305e 0%,#0e1f4c 48%,#0a1636 100%);color:#fff;padding:26px 20px 60px;text-align:center;position:relative;overflow:hidden;}
.home-hero::before{content:'';position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:380px;height:240px;background:radial-gradient(circle,rgba(251,191,36,.16) 0%,transparent 68%);pointer-events:none;}
.hero-orn{position:relative;color:#fbbf24;font-size:13px;letter-spacing:.4em;margin-bottom:12px;line-height:1;}
.hero-orn::before,.hero-orn::after{content:'';display:inline-block;width:44px;height:1px;vertical-align:middle;margin:0 12px;}
.hero-orn::before{background:linear-gradient(90deg,transparent,rgba(251,191,36,.75));}
.hero-orn::after{background:linear-gradient(90deg,rgba(251,191,36,.75),transparent);}
.home-series{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#93c5fd;margin-bottom:8px;position:relative;}
.home-hero h1{font-family:Georgia,'Times New Roman',serif;font-size:2.1rem;font-weight:700;margin:0 0 10px;position:relative;line-height:1.05;letter-spacing:.4px;text-shadow:0 2px 14px rgba(0,0,0,.4);}
.home-hero h1 span{display:block;color:#fbbf24;}
.hero-sub{position:relative;font-size:1.04rem;font-weight:600;color:#f8fafc;margin-bottom:5px;}
.hero-feat{position:relative;font-size:.77rem;color:rgba(255,255,255,.62);letter-spacing:.03em;margin-bottom:16px;}
.home-hero .tag{font-size:.85rem;color:rgba(255,255,255,.65);font-style:italic;margin-bottom:16px;position:relative;}
.home-stats{display:flex;justify-content:center;gap:9px;position:relative;flex-wrap:wrap;}
.hstat{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.15);border-radius:13px;padding:8px 14px;text-align:center;min-width:60px;}
.hstat b{font-size:1.3rem;font-weight:800;display:block;line-height:1;color:#fbbf24;}
.hstat span{font-size:.6rem;opacity:.82;text-transform:uppercase;letter-spacing:.6px;color:#e2e8f0;}
.hero-skyline{position:absolute;left:0;right:0;bottom:0;width:100%;height:56px;display:block;opacity:.6;pointer-events:none;}"""
rep(OLD_HERO_CSS, NEW_HERO_CSS, "heroCSS")

# 3) book-header -> B2 navy
rep(""".book-header{background:linear-gradient(160deg,#0f1e46 0%,#1e3a8a 58%,#101d43 100%);color:#fff;position:relative;overflow:hidden;}
.book-header::before{content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;background:radial-gradient(circle,rgba(252,211,77,.20) 0%,transparent 70%);border-radius:50%;}""",
""".book-header{background:linear-gradient(180deg,#16305e 0%,#0e1f4c 60%,#0a1636 100%);color:#fff;position:relative;overflow:hidden;}
.book-header::before{content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;background:radial-gradient(circle,rgba(16,185,129,.18) 0%,transparent 70%);border-radius:50%;}""", "bookheader")

# 4) langbar CSS -> B2 exact (label selector .ll to match C1 markup)
OLD_LB = """.langbar{background:var(--card);display:flex;align-items:center;gap:7px;padding:10px 14px;overflow-x:auto;scrollbar-width:none;position:relative;z-index:9;border-bottom:1px solid var(--border);}
.langbar::-webkit-scrollbar{display:none;}
.langbar .ll{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);white-space:nowrap;margin-right:3px;font-weight:700;flex-shrink:0;}
.lang-btn{border:1px solid var(--border);background:#fff;color:var(--muted);border-radius:999px;padding:6px 13px;font-family:inherit;font-size:12.5px;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;transition:all .15s;}
.lang-btn:active{transform:scale(.96);}
.lang-btn.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:800;}
.lang-flag{font-size:14px;margin-right:5px;}"""
NEW_LB = """.langbar{background:var(--card);border-bottom:1px solid var(--border);padding:.55rem .9rem;display:flex;align-items:center;gap:.4rem;overflow-x:auto;-webkit-overflow-scrolling:touch;position:relative;z-index:9;}
.langbar::-webkit-scrollbar{display:none;}
.langbar .ll{font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);white-space:nowrap;margin-right:.15rem;font-weight:700;flex-shrink:0;}
.lang-btn{border:1.5px solid var(--border);background:#fff;color:var(--muted);border-radius:999px;padding:.28rem .7rem;font-size:.76rem;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;font-family:inherit;}
.lang-btn.on{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 2px 6px rgba(23,37,84,.28);}
.lang-flag{margin-right:5px;}"""
rep(OLD_LB, NEW_LB, "langbarCSS")

# 5) theme-color -> navy
rep('<meta name="theme-color" content="#172554">', '<meta name="theme-color" content="#16305e">', "themecolor")

# 6) hero MARKUP -> B2 structure with C1 content (regex; removes old wrong skyline)
SKYLINE = ('<svg class="hero-skyline" viewBox="0 0 400 56" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<g fill="none" stroke="#ecd08a" stroke-width="1.2" stroke-linejoin="round" stroke-linecap="round">'
 '<line x1="0" y1="53" x2="400" y2="53"/><rect x="18" y="22" width="72" height="4"/>'
 '<line x1="26" y1="26" x2="26" y2="53"/><line x1="40" y1="26" x2="40" y2="53"/><line x1="54" y1="26" x2="54" y2="53"/><line x1="68" y1="26" x2="68" y2="53"/><line x1="82" y1="26" x2="82" y2="53"/>'
 '<path d="M48 22 v-5 h12 v5"/><line x1="50" y1="12" x2="50" y2="17"/><line x1="54" y1="11" x2="54" y2="17"/><line x1="58" y1="12" x2="58" y2="17"/>'
 '<path d="M108 53 v-13 a14 14 0 0 1 28 0 v13"/><line x1="122" y1="26" x2="122" y2="19"/><path d="M119 22 h6"/>'
 '<line x1="164" y1="53" x2="164" y2="16"/><circle cx="164" cy="28" r="5"/><line x1="164" y1="16" x2="164" y2="6"/>'
 '<path d="M184 53 v-21 l8 -18 l8 18 v21"/><path d="M200 53 v-21 l8 -18 l8 18 v21"/><line x1="192" y1="14" x2="192" y2="9"/><line x1="208" y1="14" x2="208" y2="9"/>'
 '<path d="M232 53 v-9 a10 10 0 0 1 20 0 v9"/><line x1="242" y1="34" x2="242" y2="28"/>'
 '<path d="M270 53 v-15 h6 v-6 h6 v6 h6 v15"/><path d="M276 32 l3 -6 l3 6"/><path d="M288 32 l3 -6 l3 6"/>'
 '<path d="M300 53 v-19 h9 v19"/><path d="M300 34 l4.5 -8 l4.5 8"/>'
 '<path d="M322 53 l18 -21 l14 13 l12 -17 l16 25"/></g>'
 '<g fill="#ecd08a"><circle cx="150" cy="12" r="1"/><circle cx="230" cy="10" r="1"/><circle cx="96" cy="10" r="1"/><circle cx="330" cy="13" r="1"/><circle cx="380" cy="8" r="1"/></g></svg>')
NEW_HERO_MK = ('<div class="home-hero">\n'
 '    <div class="hero-orn">&#10022;</div>\n'
 '    <div class="home-series" data-i18n="series">Advanced &middot; Proficient</div>\n'
 '    <h1>German Vocabulary <span>in Context</span></h1>\n'
 '    <div class="hero-sub">Learn German in 8 languages</div>\n'
 '    <div class="hero-feat">Vocabulary &bull; Grammar &bull; Dialogues &bull; Audio</div>\n'
 '    <div class="home-stats">\n'
 '      <div class="hstat"><b>10</b><span data-i18n="sGrammar">Grammar</span></div>\n'
 '      <div class="hstat"><b>26</b><span data-i18n="sUnits">Units</span></div>\n'
 '      <div class="hstat"><b>1560</b><span data-i18n="sWords">Words</span></div>\n'
 '      <div class="hstat"><b>C1</b><span data-i18n="sLevel">Level</span></div>\n'
 '    </div>\n'
 '    ' + SKYLINE + '\n'
 '  </div>\n  ')
new_h, n = re.subn(r'<div class="home-hero">[\s\S]*?</div>\s*(?=<div class="langbar")', NEW_HERO_MK, h, count=1)
if n != 1:
    raise SystemExit("ABORT: hero markup regex matched %d" % n)
h = new_h

# verify German data lines untouched
if bigs(h) != before:
    raise SystemExit("ABORT: a data line changed!")
io.open(P, "w", encoding="utf-8").write(h)
print("OK - B2 skin applied. hero markup replaced:", n)
print("purple left #1e3a8a:", h.count("#1e3a8a"), "| #4f46e5:", h.count("#4f46e5"))
