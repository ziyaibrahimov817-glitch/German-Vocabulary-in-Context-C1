# -*- coding: utf-8 -*-
"""Local QA over c1_tr: completeness + English/German leakage heuristics. Cheap, no agents."""
import io, os, json, re

LANGS = ["ru","tr","az","es","fr","it","pt"]
UNITS = list(range(1,27))
src_vocab = json.load(io.open("c1_src/vocab.json",encoding="utf-8"))

def L(p):
    try: return json.load(io.open(p,encoding="utf-8"))
    except: return None

def strip(s): return re.sub(r"<[^>]+>","",s or "")

report = {}
for lang in LANGS:
    r = {"vocab_units":0,"vocab_items":0,"empty":0,"eq_en":0,"has_html":0,
         "reading":0,"dialogue":0,"read_missing_de":0,"read_untranslated":0}
    # vocab
    for u in UNITS:
        d = L(f"c1_tr/{lang}/vocab/unit_{u}.json")
        if not d: continue
        r["vocab_units"] += 1
        src = {str(v["n"]): v for v in src_vocab.get(str(u),[])}
        for n,val in d.items():
            r["vocab_items"] += 1
            m = (val or {}).get("m",""); e = (val or {}).get("e","")
            if not m or not e: r["empty"] += 1
            if "<" in m or "<" in e: r["has_html"] += 1
            sv = src.get(str(n))
            if sv and (m.strip()==(sv.get("en") or "").strip() and len(m)>3): r["eq_en"] += 1
    # reading: German preserved + something translated
    for u in UNITS:
        d = L(f"c1_tr/{lang}/reading/unit_{u}.json")
        if not d: continue
        html = d.get("html") or (d.get("reading") or {}).get("html","")
        r["reading"] += 1
        srcr = L(f"c1_src/reading/unit_{u}.json") or {}
        srch = srcr.get("html","")
        # sample: first german <h3> word present?
        mde = re.search(r"<h3>([^<>]{6,40})", srch)
        if mde and mde.group(1)[:12] not in html: r["read_missing_de"] += 1
        if strip(html).strip() == strip(srch).strip(): r["read_untranslated"] += 1
    for u in UNITS:
        d = L(f"c1_tr/{lang}/dialogue/unit_{u}.json")
        if not d: continue
        r["dialogue"] += 1
    report[lang] = r

print(json.dumps(report, ensure_ascii=False, indent=1))
# summary flags
print("\n=== FLAGS ===")
ok=True
for lang,r in report.items():
    issues=[]
    if r["vocab_units"]!=26: issues.append(f"vocab_units={r['vocab_units']}")
    if r["vocab_items"]!=1560: issues.append(f"vocab_items={r['vocab_items']}")
    if r["empty"]: issues.append(f"empty={r['empty']}")
    if r["has_html"]: issues.append(f"has_html={r['has_html']}")
    if r["eq_en"]>30: issues.append(f"eq_en={r['eq_en']}")
    if r["reading"]!=26: issues.append(f"reading={r['reading']}")
    if r["dialogue"]!=26: issues.append(f"dialogue={r['dialogue']}")
    if r["read_missing_de"]>2: issues.append(f"read_missing_de={r['read_missing_de']}")
    if r["read_untranslated"]: issues.append(f"read_untranslated={r['read_untranslated']}")
    if issues: ok=False; print(f"{lang}: "+", ".join(issues))
if ok: print("all languages: PASS (complete, no leakage flags)")
