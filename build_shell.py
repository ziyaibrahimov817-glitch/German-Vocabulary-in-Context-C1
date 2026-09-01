# -*- coding: utf-8 -*-
"""
Stage 1 shell transform for C1 -> 8-language-capable app.
Adds langbar (navy/gold) + LANG engine + UI table (EN complete, others fallback) +
TR translation-overlay + resolvers, and refactors render funcs to honour the language.
NEVER edits the giant German data lines. Fail-safe: exact occurrence counts or abort.
"""
import io, hashlib

SRC = OUT = "German-C1-Vocabulary.html"
html = io.open(SRC, "r", encoding="utf-8").read()
orig = html
edits = []
GESC = "\\ud83d\\udd0a"  # literal JS-escaped speaker emoji, as stored in the grammar label

def rep(old, new, n=1, tag=""):
    global html
    c = html.count(old)
    if c != n:
        raise SystemExit("ABORT [%s]: expected %d, found %d" % (tag, n, c))
    html = html.replace(old, new)
    edits.append(tag)

def line_hashes(text):
    return {i: hashlib.md5(ln.encode("utf-8")).hexdigest()
            for i, ln in enumerate(text.split("\n"), 1) if len(ln) > 2000}
before = set(line_hashes(orig).values())

# ---------- 1) CSS ----------
CSS = """
/* ---------- language selector (navy/gold) ---------- */
.langbar{background:var(--dark-card);display:flex;align-items:center;gap:7px;padding:9px 14px;overflow-x:auto;scrollbar-width:none;position:sticky;top:0;z-index:19;border-bottom:1px solid rgba(255,255,255,.08);}
.langbar::-webkit-scrollbar{display:none;}
.langbar .ll{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:#fcd34d;white-space:nowrap;margin-right:3px;font-weight:700;flex-shrink:0;}
.lang-btn{border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);color:rgba(255,255,255,.85);border-radius:999px;padding:6px 13px;font-family:inherit;font-size:12.5px;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;transition:all .15s;}
.lang-btn:active{transform:scale(.96);}
.lang-btn.on{background:#fbbf24;border-color:#fbbf24;color:#1e1b4b;font-weight:800;}
.lang-flag{font-size:14px;margin-right:5px;}
</style>"""
rep("</style>", CSS, 1, "css")

# ---------- 2) langbar markup (home + unit + grammar) ----------
LB = ('<div class="langbar" data-langbar="1"><span class="ll" data-i18n="transLabel">Translation</span>'
 '<button class="lang-btn on" data-lang="en"><span class="lang-flag">🇬🇧</span>English</button>'
 '<button class="lang-btn" data-lang="ru"><span class="lang-flag">🇷🇺</span>Русский</button>'
 '<button class="lang-btn" data-lang="tr"><span class="lang-flag">🇹🇷</span>Türkçe</button>'
 '<button class="lang-btn" data-lang="az"><span class="lang-flag">🇦🇿</span>Azərbaycan</button>'
 '<button class="lang-btn" data-lang="es"><span class="lang-flag">🇪🇸</span>Español</button>'
 '<button class="lang-btn" data-lang="fr"><span class="lang-flag">🇫🇷</span>Français</button>'
 '<button class="lang-btn" data-lang="it"><span class="lang-flag">🇮🇹</span>Italiano</button>'
 '<button class="lang-btn" data-lang="pt"><span class="lang-flag">🇵🇹</span>Português</button></div>')
rep('  </div>\n  <div class="sb">', '  </div>\n' + LB + '\n  <div class="sb">', 1, "lb-home")
_us = '<nav class="tab-nav"><div class="tab-nav-inner">\n    <button class="tab-btn active" onclick="showTab(\'vocab\',event)">📚 Words</button>'
rep(_us, LB + '\n  ' + _us, 1, "lb-unit")
_gs = '<nav class="tab-nav"><div class="tab-nav-inner">\n    <button class="tab-btn active" onclick="showGTab(\'rule\',event)">&#128216; Rule</button>'
rep(_gs, LB + '\n  ' + _gs, 1, "lb-gram")

# ---------- 3) data-i18n hooks (home) ----------
rep('<div class="home-series">Advanced · Proficient</div>',
    '<div class="home-series" data-i18n="series">Advanced · Proficient</div>', 1, "series")
rep('<div class="tag">Grammar explained in English &middot; texts, dialogues, exercises &amp; audio</div>',
    '<div class="tag" data-i18n="tag">Grammar explained in English &middot; texts, dialogues, exercises &amp; audio</div>', 1, "tag")
rep('<div class="hstat"><b>10</b><span>Grammar</span></div>', '<div class="hstat"><b>10</b><span data-i18n="sGrammar">Grammar</span></div>', 1, "sG")
rep('<div class="hstat"><b>26</b><span>Units</span></div>', '<div class="hstat"><b>26</b><span data-i18n="sUnits">Units</span></div>', 1, "sU")
rep('<div class="hstat"><b>1560</b><span>Words</span></div>', '<div class="hstat"><b>1560</b><span data-i18n="sWords">Words</span></div>', 1, "sW")
rep('<div class="hstat"><b>C1</b><span>Level</span></div>', '<div class="hstat"><b>C1</b><span data-i18n="sLevel">Level</span></div>', 1, "sL")
rep('<input id="si" type="text" placeholder="🔍 Search unit..." oninput="flt(this.value)">',
    '<input id="si" type="text" data-i18n-ph="searchPh" placeholder="🔍 Search unit..." oninput="flt(this.value)">', 1, "search")
rep('<div class="sec-title">&#127891; Start here &middot; Grammar Basics <span>how German works</span></div>',
    '<div class="sec-title">&#127891; <span data-i18n="secGrammar">Start here &middot; Grammar Basics</span> <span data-i18n="secGrammarSub">how German works</span></div>', 1, "secG")
rep('<div class="sec-title">&#128218; Vocabulary Units <span>building up</span></div>',
    '<div class="sec-title">&#128218; <span data-i18n="secUnits">Vocabulary Units</span> <span data-i18n="secUnitsSub">building up</span></div>', 1, "secU")

# ---------- grammar screen ----------
rep('<button class="tab-btn active" onclick="showGTab(\'rule\',event)">&#128216; Rule</button>',
    '<button class="tab-btn active" onclick="showGTab(\'rule\',event)">&#128216; <span data-i18n="gRule">Rule</span></button>', 1, "gRule")
rep('<button class="tab-btn" onclick="showGTab(\'ex\',event)">&#128266; Examples</button>',
    '<button class="tab-btn" onclick="showGTab(\'ex\',event)">&#128266; <span data-i18n="gExamples">Examples</span></button>', 1, "gEx")
rep('<button class="tab-btn" onclick="showGTab(\'pr\',event)">&#9999;&#65039; Practice</button>',
    '<button class="tab-btn" onclick="showGTab(\'pr\',event)">&#9999;&#65039; <span data-i18n="gPractice">Practice</span></button>', 1, "gPr")
rep('<button class="tab-btn" onclick="showGTab(\'an\',event)">&#10022; Answers</button>',
    '<button class="tab-btn" onclick="showGTab(\'an\',event)">&#10022; <span data-i18n="gAnswers">Answers</span></button>', 1, "gAn")
rep('<div class="section-tag">&#128216; How it works</div>', '<div class="section-tag">&#128216; <span data-i18n="gHow">How it works</span></div>', 1, "gHow")
rep('<div class="section-tag">&#128266; Examples</div>', '<div class="section-tag">&#128266; <span data-i18n="gExSec">Examples</span></div>', 1, "gExSec")
rep('<span class="audio-label">Tap the speaker to hear a single example</span>',
    '<span class="audio-label" data-i18n="gTapHint">Tap the speaker to hear a single example</span>', 1, "gTap")
rep('<div class="section-tag">&#9999;&#65039; Quick check</div>', '<div class="section-tag">&#9999;&#65039; <span data-i18n="gQuick">Quick check</span></div>', 1, "gQuick")
rep('<div class="ex-title">Practice</div>', '<div class="ex-title" data-i18n="gPracticeTitle">Practice</div>', 1, "gPrT")
rep('<button class="check-btn" onclick="checkGEx()">&#10003; Check</button>',
    '<button class="check-btn" onclick="checkGEx()">&#10003; <span data-i18n="check">Check</span></button>', 1, "gChk")
rep('<div class="section-tag">&#10022; Answer key</div>', '<div class="section-tag">&#10022; <span data-i18n="gAnsKey">Answer key</span></div>', 1, "gAK")
rep('<div class="answer-key-title">&#10022; Quick check</div>',
    '<div class="answer-key-title">&#10022; <span data-i18n="gQuick">Quick check</span></div>', 1, "gAKT")
rep('<button class="nb" id="gbp" onclick="navG(-1)">&#8592; Back</button>',
    '<button class="nb" id="gbp" onclick="navG(-1)">&#8592; <span data-i18n="back">Back</span></button>', 1, "gBk")
rep('<button class="nb p" id="gbn" onclick="navG(1)">Next &#8594;</button>',
    '<button class="nb p" id="gbn" onclick="navG(1)"><span data-i18n="next">Next</span> &#8594;</button>', 1, "gNx")

# ---------- unit screen ----------
rep('<button class="tab-btn active" onclick="showTab(\'vocab\',event)">📚 Words</button>',
    '<button class="tab-btn active" onclick="showTab(\'vocab\',event)">📚 <span data-i18n="tWords">Words</span></button>', 1, "tW")
rep('<button class="tab-btn" onclick="showTab(\'reading\',event)">📖 Text</button>',
    '<button class="tab-btn" onclick="showTab(\'reading\',event)">📖 <span data-i18n="tText">Text</span></button>', 1, "tT")
rep('<button class="tab-btn" onclick="showTab(\'dialogue\',event)">💬 Dialog</button>',
    '<button class="tab-btn" onclick="showTab(\'dialogue\',event)">💬 <span data-i18n="tDialog">Dialog</span></button>', 1, "tD")
rep('<button class="tab-btn" onclick="showTab(\'exercises\',event)">✏️ Practice</button>',
    '<button class="tab-btn" onclick="showTab(\'exercises\',event)">✏️ <span data-i18n="tPractice">Practice</span></button>', 1, "tP")
rep('<button class="tab-btn" onclick="showTab(\'answers\',event)">✦ Answers</button>',
    '<button class="tab-btn" onclick="showTab(\'answers\',event)">✦ <span data-i18n="tAnswers">Answers</span></button>', 1, "tA")
rep('<div class="section-tag">📚 A · Words</div>', '<div class="section-tag">📚 <span data-i18n="secA">A · Words</span></div>', 1, "secA")
rep('<span class="audio-label">Word + example sentence in German</span>',
    '<span class="audio-label" data-i18n="hintWords">Word + example sentence in German</span>', 1, "hW")
rep('<div class="word-check-title">🎯 All words in this unit</div>',
    '<div class="word-check-title">🎯 <span data-i18n="allWords">All words in this unit</span></div>', 1, "aw")
rep('<div class="section-tag">📖 B · Reading</div>', '<div class="section-tag">📖 <span data-i18n="secB">B · Reading</span></div>', 1, "secB")
rep('<span class="audio-label">The whole text in German</span>',
    '<span class="audio-label" data-i18n="hintText">The whole text in German</span>', 1, "hT")
rep('<div class="section-tag">💬 C · Dialog</div>', '<div class="section-tag">💬 <span data-i18n="secC">C · Dialog</span></div>', 1, "secC")
rep('<span class="audio-label">All lines in German</span>',
    '<span class="audio-label" data-i18n="hintDialog">All lines in German</span>', 1, "hD")
rep('<div class="section-tag">✏️ D · Exercises</div>', '<div class="section-tag">✏️ <span data-i18n="secD">D · Exercises</span></div>', 1, "secD")
rep('<div class="ex-label">Exercise 1</div>', '<div class="ex-label"><span data-i18n="exLabel">Exercise</span> 1</div>', 1, "eL1")
rep('<div class="ex-label">Exercise 2</div>', '<div class="ex-label"><span data-i18n="exLabel">Exercise</span> 2</div>', 1, "eL2")
rep('<div class="ex-label">Exercise 3</div>', '<div class="ex-label"><span data-i18n="exLabel">Exercise</span> 3</div>', 1, "eL3")
rep('<div class="ex-label">Exercise 4</div>', '<div class="ex-label"><span data-i18n="exLabel">Exercise</span> 4</div>', 1, "eL4")
rep('<div class="ex-title">Gap-fill</div>', '<div class="ex-title" data-i18n="gapFill">Gap-fill</div>', 2, "gf")
rep('<div class="ex-title">Matching</div>', '<div class="ex-title" data-i18n="matching">Matching</div>', 1, "mt")
rep('<div class="ex-title">True or False?</div>', '<div class="ex-title" data-i18n="trueFalse">True or False?</div>', 1, "tf")
rep('<div class="ex-instr">Write the missing German word.</div>',
    '<div class="ex-instr" data-i18n="gapInstr">Write the missing German word.</div>', 2, "gfi")
rep('<div class="ex-instr">Tap a word on the left, then its translation on the right.</div>',
    '<div class="ex-instr" data-i18n="matchInstr">Tap a word on the left, then its translation on the right.</div>', 1, "mti")
rep('<div class="ex-instr">Write &quot;true&quot; or &quot;false&quot;.</div>',
    '<div class="ex-instr" data-i18n="tfInstr">Write &quot;true&quot; or &quot;false&quot;.</div>', 1, "tfi")
rep('<button class="check-btn" onclick="checkEx(1)">✓ Check</button>', '<button class="check-btn" onclick="checkEx(1)">✓ <span data-i18n="check">Check</span></button>', 1, "c1")
rep('<button class="check-btn" onclick="checkEx(2)">✓ Check</button>', '<button class="check-btn" onclick="checkEx(2)">✓ <span data-i18n="check">Check</span></button>', 1, "c2")
rep('<button class="check-btn" onclick="checkMatch()">✓ Check</button>', '<button class="check-btn" onclick="checkMatch()">✓ <span data-i18n="check">Check</span></button>', 1, "cm")
rep('<button class="check-btn" onclick="checkEx(4)">✓ Check</button>', '<button class="check-btn" onclick="checkEx(4)">✓ <span data-i18n="check">Check</span></button>', 1, "c4")
rep('<div class="section-tag">✦ E · Answer Key</div>', '<div class="section-tag">✦ <span data-i18n="secE">E · Answer Key</span></div>', 1, "secE")
rep('<div class="answer-key-title">✦ Exercise 1</div>', '<div class="answer-key-title">✦ <span data-i18n="exLabel">Exercise</span> 1</div>', 1, "aK1")
rep('<div class="answer-key-title">✦ Exercise 2</div>', '<div class="answer-key-title">✦ <span data-i18n="exLabel">Exercise</span> 2</div>', 1, "aK2")
rep('<div class="answer-key-title">✦ Exercise 3 · Matching</div>',
    '<div class="answer-key-title">✦ <span data-i18n="exLabel">Exercise</span> 3 · <span data-i18n="matching">Matching</span></div>', 1, "aK3")
rep('<div class="answer-key-title">✦ Exercise 4</div>', '<div class="answer-key-title">✦ <span data-i18n="exLabel">Exercise</span> 4</div>', 1, "aK4")
rep('<button class="nb" id="bp" onclick="navU(-1)">← Back</button>', '<button class="nb" id="bp" onclick="navU(-1)">← <span data-i18n="back">Back</span></button>', 1, "uBk")
rep('<button class="nb p" id="bn" onclick="navU(1)">Next →</button>', '<button class="nb p" id="bn" onclick="navU(1)"><span data-i18n="next">Next</span> →</button>', 1, "uNx")

# ---------- 4) tab highlight fix (both showTab & showGTab) ----------
rep("if(ev&&ev.target)ev.target.classList.add('active');",
    "if(ev&&ev.target){var _b=ev.target.closest('.tab-btn');if(_b)_b.classList.add('active');}", 2, "tabfix")

# ---------- 5) render-function refactors ----------
rep("en-inline\">'+w.en+'</div>", "en-inline\">'+pv(w,'m')+'</div>", 1, "vm-mob")
rep("font-size:13px\">'+w.en+'</td>", "font-size:13px\">'+pv(w,'m')+'</td>", 1, "vm-desk")
rep("example-az\">'+w.exEn+'</div>", "example-az\">'+pv(w,'e')+'</div>", 2, "vex")
rep("gh.innerHTML='▸ '+g.title;", "gh.innerHTML='▸ '+pgt(g);", 1, "gtitle")
rep("t.innerHTML='<thead><tr><th>#</th><th>🇩🇪 Deutsch</th><th>🇬🇧 English</th><th>Example</th><th>🔊</th></tr></thead>';",
    "t.innerHTML='<thead><tr><th>#</th><th>🇩🇪 Deutsch</th><th>'+langFlag()+' '+langName()+'</th><th>'+uiT('thExample')+'</th><th>🔊</th></tr></thead>';", 1, "thead")
rep("document.getElementById('uLabel').innerHTML=cU.de+' <span>· '+cU.en+'</span>';",
    "document.getElementById('uLabel').innerHTML=cU.de+' <span>· '+put(cU)+'</span>';", 1, "utitle")
rep("sh.forEach(function(item,i){r.innerHTML+='<div class=\"match-item\" id=\"mr-'+i+'\" data-en=\"'+item.en.replace(/\"/g,'&quot;')+'\" onclick=\"selR('+i+')\">'+item.en+'</div>';});",
    "sh.forEach(function(item,i){var mt=pm(item);r.innerHTML+='<div class=\"match-item\" id=\"mr-'+i+'\" data-en=\"'+mt.replace(/\"/g,'&quot;')+'\" data-key=\"'+item.en.replace(/\"/g,'&quot;')+'\" onclick=\"selR('+i+')\">'+mt+'</div>';});", 1, "match")
rep("var en=document.getElementById('mr-'+ri).dataset.en;", "var en=document.getElementById('mr-'+ri).dataset.key;", 1, "matchcmp")
rep("ak3.innerHTML+='<div class=\"answer-item\"><span class=\"answer-num\">'+(i+1)+'.</span><span class=\"answer-text\">'+item.de+' → '+item.en+'</span></div>';",
    "ak3.innerHTML+='<div class=\"answer-item\"><span class=\"answer-num\">'+(i+1)+'.</span><span class=\"answer-text\">'+item.de+' → '+pm(item)+'</span></div>';", 1, "ansmatch")
rep("document.getElementById('readingContent').innerHTML=RH[cU.num]||'';",
    "document.getElementById('readingContent').innerHTML=(LANG!=='en'&&TR.rd[cU.num]&&TR.rd[cU.num][LANG])?TR.rd[cU.num][LANG]:(RH[cU.num]||'');", 1, "reading")
rep("var d=DH[cU.num]||{};",
    "var d=(LANG!=='en'&&TR.dl[cU.num]&&TR.dl[cU.num][LANG])?TR.dl[cU.num][LANG]:(DH[cU.num]||{});", 1, "dialogue")

# ---------- 6) dynamic labels ----------
rep("var id='mainAudioBtn',label='🔊 Listen to all words';", "var id='mainAudioBtn',label='🔊 '+uiT('listenWords');", 1, "lblV")
rep("var id='readingAudioBtn',label='🔊 Read aloud';", "var id='readingAudioBtn',label='🔊 '+uiT('readAloud');", 1, "lblR")
rep("var id='dialogueAudioBtn',label='🔊 Play dialogue';", "var id='dialogueAudioBtn',label='🔊 '+uiT('playDialogue');", 1, "lblD")
rep("gAudioBtn',label='" + GESC + " Listen to all'", "gAudioBtn',label='" + GESC + " '+uiT('gListenAll')", 1, "lblG")
rep("document.getElementById('uSeries').textContent='German Vocabulary in Context · Unit '+n;",
    "document.getElementById('uSeries').textContent=uiT('uSeriesPrefix')+' '+n;", 1, "useries")
rep("document.getElementById('uWordBadge').textContent=cU.count+' words';",
    "document.getElementById('uWordBadge').textContent=cU.count+' '+uiT('wordsUnit');", 1, "ubadge")

# ---------- 7) shell engine ----------
SHELL = r"""
<script>
/* ===================== C1 multilingual shell ===================== */
var LANG='en';
var LANGS=[{c:'en',n:'English',f:'🇬🇧'},{c:'ru',n:'Русский',f:'🇷🇺'},{c:'tr',n:'Türkçe',f:'🇹🇷'},{c:'az',n:'Azərbaycan',f:'🇦🇿'},{c:'es',n:'Español',f:'🇪🇸'},{c:'fr',n:'Français',f:'🇫🇷'},{c:'it',n:'Italiano',f:'🇮🇹'},{c:'pt',n:'Português',f:'🇵🇹'}];
var UI={en:{
 series:"Advanced · Proficient",
 tag:"Grammar explained in your language · texts, dialogues, exercises & audio",
 sGrammar:"Grammar", sUnits:"Units", sWords:"Words", sLevel:"Level",
 secGrammar:"Start here · Grammar Basics", secGrammarSub:"how German works",
 secUnits:"Vocabulary Units", secUnitsSub:"building up",
 searchPh:"🔍 Search unit...", transLabel:"Translation",
 gRule:"Rule", gExamples:"Examples", gPractice:"Practice", gAnswers:"Answers",
 gHow:"How it works", gExSec:"Examples", gListenAll:"Listen to all",
 gTapHint:"Tap the speaker to hear a single example",
 gQuick:"Quick check", gPracticeTitle:"Practice", gAnsKey:"Answer key",
 check:"Check", back:"Back", next:"Next",
 tWords:"Words", tText:"Text", tDialog:"Dialog", tPractice:"Practice", tAnswers:"Answers",
 secA:"A · Words", secB:"B · Reading", secC:"C · Dialog", secD:"D · Exercises", secE:"E · Answer Key",
 listenWords:"Listen to all words", readAloud:"Read aloud", playDialogue:"Play dialogue",
 hintWords:"Word + example sentence in German", hintText:"The whole text in German", hintDialog:"All lines in German",
 allWords:"All words in this unit", thExample:"Example",
 exLabel:"Exercise", gapFill:"Gap-fill", matching:"Matching", trueFalse:"True or False?",
 gapInstr:"Write the missing German word.",
 matchInstr:"Tap a word on the left, then its translation on the right.",
 tfInstr:"Write “true” or “false”.",
 uSeriesPrefix:"German Vocabulary in Context · Unit", wordsUnit:"words"
}};
var TR={vm:{}, ve:{}, gt:{}, ut:{}, mt:{}, rd:{}, dl:{}, gr:{}};
function uiT(k){var d=UI[LANG]; if(d&&d[k]!=null&&d[k]!=='')return d[k]; return UI.en[k]!=null?UI.en[k]:k;}
function langName(){for(var i=0;i<LANGS.length;i++)if(LANGS[i].c===LANG)return LANGS[i].n; return 'English';}
function langFlag(){for(var i=0;i<LANGS.length;i++)if(LANGS[i].c===LANG)return LANGS[i].f; return '🇬🇧';}
function pv(w,kind){var en=(kind==='m')?w.en:w.exEn; if(LANG==='en')return en; var st=(kind==='m'?TR.vm:TR.ve)[cU.num+'-'+w.n]; return (st&&st[LANG]!=null&&st[LANG]!=='')?st[LANG]:en;}
function pgt(g){if(LANG==='en')return g.title; var st=TR.gt[cU.num]; return (st&&st[g.title]&&st[g.title][LANG])?st[g.title][LANG]:g.title;}
function put(u){if(LANG==='en')return u.en; var st=TR.ut[u.num]; return (st&&st[LANG]!=null&&st[LANG]!=='')?st[LANG]:u.en;}
function pm(item){if(LANG==='en')return item.en; var st=TR.mt[cU.num]; return (st&&st[item.en]&&st[item.en][LANG])?st[item.en][LANG]:item.en;}
function renderUI(){
 document.querySelectorAll('[data-i18n]').forEach(function(e){var t=uiT(e.getAttribute('data-i18n')); if(t!=null)e.textContent=t;});
 document.querySelectorAll('[data-i18n-ph]').forEach(function(e){var t=uiT(e.getAttribute('data-i18n-ph')); if(t!=null)e.placeholder=t;});
 document.querySelectorAll('.langbar').forEach(function(bar){bar.querySelectorAll('.lang-btn').forEach(function(b){b.classList.toggle('on',b.dataset.lang===LANG);});});
}
function reRender(){
 renderUI();
 if(document.getElementById('US').style.display==='block' && typeof cU!=='undefined' && cU){buildAll();}
 if(document.getElementById('GS').style.display==='block' && typeof cG!=='undefined' && cG && typeof buildG==='function'){buildG();}
}
function setLang(code){LANG=code; if(window.speechSynthesis)try{window.speechSynthesis.cancel();}catch(e){} reRender();}
document.addEventListener('click',function(ev){var b=ev.target.closest?ev.target.closest('.lang-btn'):null; if(b&&b.dataset.lang){setLang(b.dataset.lang);}});
document.addEventListener('DOMContentLoaded',renderUI);
renderUI();
</script>
</body>"""
rep("</body>", SHELL, 1, "shell")

# ---------- verify German data lines untouched ----------
after = set(line_hashes(html).values())
if before - after:
    raise SystemExit("ABORT: a giant German data line changed!")

io.open(OUT, "w", encoding="utf-8").write(html)
print("OK -", len(edits), "edits; German data lines preserved:", len(before & after), "/", len(before))
