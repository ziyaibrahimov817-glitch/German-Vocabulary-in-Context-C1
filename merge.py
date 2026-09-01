# -*- coding: utf-8 -*-
"""
Merge translation files under c1_tr/<lang>/ into the C1 HTML as an inline
<script id="c1-translations"> block that populates the TR overlay and UI table.
Idempotent: re-running replaces the previous block. Robust to partial data.
"""
import io, os, json, re, sys

HTML = "German-C1-Vocabulary.html"
TRDIR = "c1_tr"
SRC = "c1_src"

def load(p, default=None):
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return default

# source references for keys
src_vocab = load(os.path.join(SRC, "vocab.json"), {})     # {unit:[{n,en,...}]}
src_groups = load(os.path.join(SRC, "groups.json"), {})   # {unit:[title,...]}
src_match = load(os.path.join(SRC, "match.json"), {})      # {unit:[{de,en}]}

TR = {"vm": {}, "ve": {}, "ut": {}, "gt": {}, "mt": {}, "rd": {}, "dl": {}, "gr": {}}
UI = {}

langs = []
if os.path.isdir(TRDIR):
    langs = sorted(d for d in os.listdir(TRDIR) if os.path.isdir(os.path.join(TRDIR, d)))

report = {}
for lang in langs:
    base = os.path.join(TRDIR, lang)
    cnt = {"vocab": 0, "reading": 0, "dialogue": 0, "titles": 0, "match": 0}

    # vocab -> vm/ve
    vdir = os.path.join(base, "vocab")
    if os.path.isdir(vdir):
        for fn in os.listdir(vdir):
            mo = re.match(r"unit_(\d+)\.json$", fn)
            if not mo:
                continue
            unit = mo.group(1)
            data = load(os.path.join(vdir, fn), {})
            for n, v in (data or {}).items():
                key = f"{unit}-{n}"
                if isinstance(v, dict) and v.get("m"):
                    TR["vm"].setdefault(key, {})[lang] = v["m"]
                    cnt["vocab"] += 1
                if isinstance(v, dict) and v.get("e"):
                    TR["ve"].setdefault(key, {})[lang] = v["e"]

    # reading -> rd
    rdir = os.path.join(base, "reading")
    if os.path.isdir(rdir):
        for fn in os.listdir(rdir):
            mo = re.match(r"unit_(\d+)\.json$", fn)
            if not mo:
                continue
            unit = mo.group(1)
            data = load(os.path.join(rdir, fn), {}) or {}
            html = data.get("html") or (data.get("reading") or {}).get("html") if isinstance(data.get("reading"), dict) else data.get("html")
            if html:
                TR["rd"].setdefault(unit, {})[lang] = html
                cnt["reading"] += 1

    # dialogue -> dl
    ddir = os.path.join(base, "dialogue")
    if os.path.isdir(ddir):
        for fn in os.listdir(ddir):
            mo = re.match(r"unit_(\d+)\.json$", fn)
            if not mo:
                continue
            unit = mo.group(1)
            data = load(os.path.join(ddir, fn), {}) or {}
            dd = data.get("dialogue") if isinstance(data.get("dialogue"), dict) else data
            if dd.get("i") or dd.get("box"):
                TR["dl"].setdefault(unit, {})[lang] = {"i": dd.get("i", ""), "box": dd.get("box", "")}
                cnt["dialogue"] += 1

    # titles -> ut / gt / gr  (tolerate dict OR list shapes)
    def as_dict(x, key_field=None):
        """Coerce a list to a {key: item} dict; pass dicts through."""
        if isinstance(x, dict):
            return x
        if isinstance(x, list):
            d = {}
            for i, item in enumerate(x):
                if key_field and isinstance(item, dict) and item.get(key_field) is not None:
                    d[str(item[key_field])] = item
                else:
                    d[str(i + 1)] = item
            return d
        return {}
    tt = load(os.path.join(base, "titles.json"), None)
    if tt:
        for unit, val in as_dict(tt.get("units")).items():
            # val may be a string, or {de,en}/{title}
            if isinstance(val, dict):
                val = val.get("title") or val.get(lang) or val.get("en") or ""
            if val:
                TR["ut"].setdefault(str(unit), {})[lang] = val
                cnt["titles"] += 1
        for unit, arr in as_dict(tt.get("groups")).items():
            srcarr = src_groups.get(str(unit)) or src_groups.get(unit) or []
            if isinstance(arr, list):
                for i, title in enumerate(arr):
                    if i < len(srcarr) and title:
                        TR["gt"].setdefault(str(unit), {}).setdefault(srcarr[i], {})[lang] = title
        for gn, gobj in as_dict(tt.get("grammar"), key_field="n").items():
            if isinstance(gobj, dict):
                g = {"t": gobj.get("t", ""), "s": gobj.get("s", ""), "tag": gobj.get("tag", "")}
                if any(g.values()):
                    TR["gr"].setdefault(str(gn), {})[lang] = g

    # UI
    ui = load(os.path.join(base, "ui.json"), None)
    if ui:
        UI[lang] = ui

    # derive match (mt) from vocab translations: match.en -> vocab item with same en -> its vm
    for unit, pairs in src_match.items():
        vlist = src_vocab.get(str(unit)) or src_vocab.get(unit) or []
        en2n = {}
        for it in vlist:
            en2n.setdefault(it.get("en"), it.get("n"))
        for p in pairs or []:
            en = p.get("en")
            n = en2n.get(en)
            if n is None:
                continue
            key = f"{unit}-{n}"
            tr = TR["vm"].get(key, {}).get(lang)
            if tr:
                TR["mt"].setdefault(unit, {}).setdefault(en, {})[lang] = tr
                cnt["match"] += 1

    report[lang] = cnt

# build injection
payload = {"TR": TR, "UI": UI}
js = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
js = js.replace("</", "<\\/")  # keep the </script> parser safe
block = ('<script id="c1-translations">(function(){var P=' + js +
         ';for(var k in P.TR){for(var kk in P.TR[k]){TR[k][kk]=P.TR[k][kk];}}'
         'for(var l in P.UI){UI[l]=Object.assign(UI[l]||{},P.UI[l]);}'
         'if(typeof renderUI==="function")renderUI();})();</script>')

html = io.open(HTML, encoding="utf-8").read()
html = re.sub(r'<script id="c1-translations">.*?</script>', "", html, flags=re.S)
assert html.count("</body>") == 1, "expected exactly one </body>"
html = html.replace("</body>", block + "\n</body>")
io.open(HTML, "w", encoding="utf-8").write(html)

print("languages merged:", langs)
print(json.dumps(report, ensure_ascii=False, indent=1))
print("payload size:", len(js), "bytes")
