// Extract translatable source strings from the C1 HTML by evaluating the data
// script in a stubbed sandbox. Emits JSON files under c1_src/.
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const html = fs.readFileSync('German-C1-Vocabulary.html', 'utf8');
// first <script> block holds UD, RH, DH, GD + functions
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) throw new Error('no script block');
let code = m[1];

// Stub browser globals so the data script evaluates without a DOM.
const noop = () => {};
const elStub = new Proxy({}, { get: () => noop, set: () => true });
const documentStub = new Proxy({
  getElementById: () => elStub,
  querySelectorAll: () => [],
  querySelector: () => elStub,
  addEventListener: noop,
  createElement: () => ({ set innerHTML(v){}, get value(){return '';} }),
}, { get(t,k){ return (k in t) ? t[k] : noop; } });

const sandbox = {
  window: {}, document: documentStub, navigator: { userAgent: '' },
  speechSynthesis: null, setTimeout: noop, console,
};
sandbox.window.speechSynthesis = null;
sandbox.window.addEventListener = noop;
sandbox.window.document = documentStub;

vm.createContext(sandbox);
try { vm.runInContext(code, sandbox, { timeout: 10000 }); }
catch (e) { /* function bodies referencing DOM may throw at call time only; data assignments run first */
  console.error('warn: eval note:', e.message); }

const UD = sandbox.UD, RH = sandbox.RH, DH = sandbox.DH, GD = sandbox.GD;
if (!UD || !GD) throw new Error('UD/GD not captured');

fs.mkdirSync('c1_src', { recursive: true });

// vocab: {unit: [{n, de, en, exDe, exEn}]}
const vocab = {}, units = {}, groups = {}, match = {};
for (const u of UD) {
  vocab[u.num] = u.vocab.map(v => ({ n: v.n, de: v.de, type: v.type, en: v.en, exDe: v.exDe, exEn: v.exEn }));
  units[u.num] = { de: u.de, en: u.en };
  groups[u.num] = (u.groups || []).map(g => g.title);
  match[u.num] = (u.match || []).map(x => ({ de: x.de, en: x.en }));
}
const reading = {}, dialogue = {};
for (const k in (RH||{})) reading[k] = RH[k];
for (const k in (DH||{})) dialogue[k] = DH[k];

const grammar = GD.map(g => ({ n: g.n, t: g.t, s: g.s, tag: g.tag }));

const w = (name, obj) => fs.writeFileSync(path.join('c1_src', name), JSON.stringify(obj, null, 1), 'utf8');
w('vocab.json', vocab);
w('units.json', units);
w('groups.json', groups);
w('match.json', match);
w('reading.json', reading);
w('dialogue.json', dialogue);
w('grammar.json', grammar);

// per-unit files so each translation agent reads a small slice
for (const d of ['vocab', 'reading', 'dialogue']) fs.mkdirSync(path.join('c1_src', d), { recursive: true });
for (const u of UD) {
  fs.writeFileSync(path.join('c1_src','vocab',`unit_${u.num}.json`),
    JSON.stringify({ unit: u.num, title_de: u.de, vocab: vocab[u.num], groups: groups[u.num] }, null, 1), 'utf8');
  fs.writeFileSync(path.join('c1_src','reading',`unit_${u.num}.json`),
    JSON.stringify({ unit: u.num, html: reading[u.num] || '' }, null, 1), 'utf8');
  fs.writeFileSync(path.join('c1_src','dialogue',`unit_${u.num}.json`),
    JSON.stringify({ unit: u.num, dialogue: dialogue[u.num] || {} }, null, 1), 'utf8');
}

// counts
let vc = 0; for (const k in vocab) vc += vocab[k].length;
let gc = 0; for (const k in groups) gc += groups[k].length;
let mc = 0; for (const k in match) mc += match[k].length;
console.log(JSON.stringify({
  units: Object.keys(units).length,
  vocab: vc,
  groups: gc,
  match_pairs: mc,
  reading: Object.keys(reading).length,
  dialogue: Object.keys(dialogue).length,
  grammar: grammar.length,
}, null, 2));
