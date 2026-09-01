# German Vocabulary in Context — C1

A self-contained, offline German **C1** vocabulary-learning web app (PWA), part of the
"German Vocabulary in Context" family. Single-file app: `German-C1-Vocabulary.html`.

## Content
- **10** grammar lessons · **26** topic units · **1,560** words
- Per unit: words, reading text, dialogue, exercises, answer key — with German audio (TTS, `de-DE`)

## Languages
German is the learning/source language. Translations of meanings, examples, titles,
reading texts, dialogues and the full UI are available in **8** languages via a
horizontal selector: English, Russian, Turkish, Azerbaijani, Spanish, French, Italian, Portuguese.
German source text and German audio never change with the language selection.

## Design
Navy/gold premium theme (`#1e1b4b` / `#fcd34d`), mobile-first, sticky language bar,
tabbed unit/grammar views. Works fully offline (service worker).

## Files
| File | Purpose |
|---|---|
| `German-C1-Vocabulary.html` | The app (HTML + CSS + JS + all content & translations) |
| `manifest.json`, `service-worker.js` | PWA (installable, offline) |
| `privacy.html` | Privacy policy (no data collected) |
| `icon-*.png` | App icons (navy/gold) |
| `c1_src/` | Extracted German/English source strings |
| `c1_tr/<lang>/` | Per-language translation data (baked into the HTML by `merge.py`) |
| `extract.js`, `merge.py`, `pending.py`, `qa.py`, `build_shell.py`, `wf_translate.js` | Build pipeline |

## Build pipeline
1. `build_shell.py` — turns the base English app into an 8-language shell (selector, engine, overlay).
2. `node extract.js` — dumps translatable source into `c1_src/`.
3. Translation agents fill `c1_tr/<lang>/…`.
4. `python merge.py` — injects translations into the HTML (idempotent).
5. `python qa.py` — completeness / leakage checks.

## License / ownership
© 2026 Ziya Learning Apps. All rights reserved.
