# -*- coding: utf-8 -*-
"""Emit a Workflow args.jobs JSON covering only MISSING translation work.
Usage: python pending.py "vocab,titles"  (types to consider; default vocab,titles)
Prints the JSON to stdout and a human summary to stderr."""
import os, sys, json

LANGS = [
    ("ru", "Russian", "Русский"),
    ("tr", "Turkish", "Türkçe"),
    ("az", "Azerbaijani", "Azərbaycan"),
    ("es", "Spanish", "Español"),
    ("fr", "French", "Français"),
    ("it", "Italian", "Italiano"),
    ("pt", "Portuguese", "Português"),
]
UNITS = list(range(1, 27))
types_arg = (sys.argv[1] if len(sys.argv) > 1 else "vocab,titles").split(",")

def has(lang, sub, unit):
    return os.path.isfile(os.path.join("c1_tr", lang, sub, f"unit_{unit}.json"))

jobs = []
summary = []
for lang, name, native in LANGS:
    job = {"lang": lang, "name": name, "native": native, "types": [], "units": []}
    missing_units = set()
    for t in ("vocab", "reading", "dialogue"):
        if t in types_arg:
            miss = [u for u in UNITS if not has(lang, t, u)]
            if miss:
                job["types"].append(t)
                missing_units.update(miss)
    if "titles" in types_arg and not os.path.isfile(os.path.join("c1_tr", lang, "titles.json")):
        job["types"].append("titles")
    if missing_units:
        job["units"] = sorted(missing_units)
    if job["types"]:
        jobs.append(job)
        summary.append(f"{lang}: types={job['types']} units={len(job['units']) or '-'}")

sys.stderr.write("PENDING WORK:\n" + ("\n".join(summary) if summary else "(nothing missing)") + "\n")
sys.stderr.write(f"total jobs: {len(jobs)}\n")
print(json.dumps({"jobs": jobs}, ensure_ascii=False))
