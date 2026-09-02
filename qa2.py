# -*- coding: utf-8 -*-
"""Comprehensive leak/completeness audit incl. grammar content. Cheap, no agents.
Flags a non-English translation that equals its English source (= untranslated leakage)."""
import io, os, json, re

LANGS = ["ru","tr","az","es","fr","it","pt"]
def L(p):
    try: return json.load(io.open(p, encoding="utf-8"))
    except: return None
def strip(s): return re.sub(r"<[^>]+>","", s or "").strip()

GD = L("c1_src/grammar_full.json") or []
src = {str(g["n"]): g for g in GD}

report = {}
for lang in LANGS:
    r = {"lessons":0, "missing_lessons":[], "item_leak":0, "note_leak":0,
         "rule_leak":0, "title_leak":0, "instr_leak":0, "items_seen":0, "items_missing":0}
    for n in range(1,11):
        p = f"c1_tr/{lang}/grammar/lesson_{n}.json"
        d = L(p)
        if not d:
            r["missing_lessons"].append(n); continue
        r["lessons"] += 1
        s = src.get(str(n), {})
        # rule
        if d.get("rule") and strip(d["rule"]) == strip(s.get("rule","")):
            r["rule_leak"] += 1
        # instr
        if d.get("instr") and d["instr"].strip() == (s.get("instr","") or "").strip():
            r["instr_leak"] += 1
        # groups titles
        for gi,title in enumerate(d.get("groups",[]) or []):
            st = (s.get("groups",[]) or [])
            if gi < len(st) and title and title.strip() == (st[gi].get("title","") or "").strip():
                r["title_leak"] += 1
        # items
        items = d.get("items",{}) or {}
        sg = s.get("groups",[]) or []
        for gi,gr in enumerate(sg):
            for ii,it in enumerate(gr.get("items",[]) or []):
                key = f"{gi}-{ii}"
                v = items.get(key)
                if not v or not v.get("m"):
                    r["items_missing"] += 1; continue
                r["items_seen"] += 1
                if v.get("m","").strip() == (it.get("en","") or "").strip() and len(it.get("en",""))>3:
                    r["item_leak"] += 1
                if it.get("note") and v.get("note","").strip() == (it.get("note","") or "").strip() and len(it.get("note",""))>3:
                    r["note_leak"] += 1
    report[lang] = r

print(json.dumps(report, ensure_ascii=False, indent=1))
print("\n=== GRAMMAR FLAGS ===")
ok=True
for lang,r in report.items():
    issues=[]
    if r["lessons"]!=10: issues.append(f"lessons={r['lessons']} missing={r['missing_lessons']}")
    if r["items_missing"]: issues.append(f"items_missing={r['items_missing']}")
    if r["item_leak"]>3: issues.append(f"item_leak={r['item_leak']}")
    if r["note_leak"]>3: issues.append(f"note_leak={r['note_leak']}")
    if r["rule_leak"]: issues.append(f"rule_leak={r['rule_leak']}")
    if r["title_leak"]>1: issues.append(f"title_leak={r['title_leak']}")
    if r["instr_leak"]: issues.append(f"instr_leak={r['instr_leak']}")
    if issues: ok=False; print(f"{lang}: "+", ".join(issues))
if ok: print("grammar all languages: PASS")
