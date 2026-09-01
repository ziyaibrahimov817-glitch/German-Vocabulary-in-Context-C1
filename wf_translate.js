export const meta = {
  name: 'c1-translate',
  description: 'Translate C1 German learning content into target languages (agents read per-unit source, write per-unit translation JSON)',
  phases: [
    { title: 'Vocab' },
    { title: 'Reading' },
    { title: 'Dialogue' },
    { title: 'Titles' },
  ],
};

// args: { jobs:[{lang,name,native,types}, ...] }  OR a single {lang,name,native,types}
// robust: args may arrive as a JSON string
const A = (typeof args === 'string') ? JSON.parse(args) : args;
if (!A || (!A.jobs && !A.lang)) throw new Error('bad args: ' + JSON.stringify(args));
const JOBS = A.jobs ? A.jobs : [{ lang: A.lang, name: A.name, native: A.native, types: A.types }];
for (const J of JOBS) if (!J.lang || !J.name) throw new Error('job missing lang/name: ' + JSON.stringify(J));
const UNITS = Array.from({ length: 26 }, (_, i) => i + 1);

function mkRules(NAME, NATIVE) {
  return `You are a professional ${NAME} (${NATIVE}) translator localizing a German C1 vocabulary-learning app.
GERMAN is the source/learning language and must NEVER be translated away - you translate the *meanings and example translations* INTO ${NAME}.
Rules:
- Translate FROM the German (fields de / exDe) as the authoritative source; the English fields (en / exEn) are only a cross-check.
- Use natural, idiomatic ${NAME} at C1 (advanced) register. Preserve nuance; do not paraphrase loosely.
- Use the correct native script/orthography for ${NAME}. No transliteration into Latin unless that IS the language's script.
- Output PLAIN text only (no HTML tags, no HTML entities). Do not include the German or English in your output values.
- Keep proper nouns/technical terms accurate; keep any numbers.`;
}

const VOCAB_SCHEMA = {
  type: 'object',
  properties: {
    unit: { type: 'integer' },
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          n: { type: 'integer' },
          m: { type: 'string', description: 'meaning translation' },
          e: { type: 'string', description: 'example-sentence translation' },
        },
        required: ['n', 'm', 'e'], additionalProperties: false,
      },
    },
  },
  required: ['unit', 'items'], additionalProperties: false,
};

function vocabUnit(J, u) {
  return agent(
    `${mkRules(J.name, J.native)}

TASK: Read the file c1_src/vocab/unit_${u}.json. It has a "vocab" array; each entry has n, de, type, en, exDe, exEn.
For every entry produce:
 - m = the ${J.name} translation of the word meaning (translate the German "de", using article/type and "en" as cross-check)
 - e = the ${J.name} translation of the example sentence "exDe"
Then WRITE the result to c1_tr/${J.lang}/vocab/unit_${u}.json as JSON of shape {"<n>":{"m":"...","e":"..."}, ...} (keys are item numbers as strings), covering ALL entries. Create directories as needed.
Also return the structured object (unit, items[]).`,
    { label: `${J.lang}:vocab:u${u}`, phase: 'Vocab', schema: VOCAB_SCHEMA, agentType: 'general-purpose', model: 'sonnet' }
  );
}

function readingUnit(J, u) {
  return agent(
    `${mkRules(J.name, J.native)}

TASK: Read c1_src/reading/unit_${u}.json (field "html" is a German reading passage as HTML, with inline English translations inside <span> elements).
Produce a ${J.name} version of the SAME HTML: keep every HTML tag and the GERMAN text exactly as-is, but replace the ENGLISH translation text (e.g. inside <span>...</span> after an em dash, and any English gloss) with an accurate ${J.name} translation. Do not translate the German. Keep structure/tags identical.
WRITE the resulting HTML string to c1_tr/${J.lang}/reading/unit_${u}.json as JSON {"html":"<...>"}. Return {"unit":${u},"ok":true}.`,
    { label: `${J.lang}:reading:u${u}`, phase: 'Reading', agentType: 'general-purpose', model: 'sonnet' }
  );
}

function dialogueUnit(J, u) {
  return agent(
    `${mkRules(J.name, J.native)}

TASK: Read c1_src/dialogue/unit_${u}.json (field "dialogue" is an object {i: introHTML, box: dialogueHTML}; German with inline English).
Produce a ${J.name} version keeping all HTML tags and the GERMAN text exactly, replacing only the ENGLISH translation text with ${J.name}.
WRITE to c1_tr/${J.lang}/dialogue/unit_${u}.json as JSON {"i":"<...>","box":"<...>"}. Return {"unit":${u},"ok":true}.`,
    { label: `${J.lang}:dialogue:u${u}`, phase: 'Dialogue', agentType: 'general-purpose', model: 'sonnet' }
  );
}

function titles(J) {
  return agent(
    `${mkRules(J.name, J.native)}

TASK: Read three files: c1_src/units.json ({unit:{de,en}}), c1_src/groups.json ({unit:[titles...]}), c1_src/grammar.json ([{n,t,s,tag}]).
Translate into ${J.name}:
 - each unit title (translate the German "de", "en" is cross-check) -> units[unit]
 - each group title (English section headings) -> groups[unit] = [..same order/length..]
 - each grammar lesson: t (title), s (subtitle), tag -> grammar[n] = {t,s,tag}
WRITE one file c1_tr/${J.lang}/titles.json as JSON: {"units":{"1":"...",...},"groups":{"1":["...",...],...},"grammar":{"1":{"t":"...","s":"...","tag":"..."},...}}.
Return {"ok":true}.`,
    { label: `${J.lang}:titles`, phase: 'Titles', agentType: 'general-purpose', model: 'sonnet' }
  );
}

// Build one flat task list across all jobs so the global concurrency cap paces everything.
const tasks = [];
for (const J of JOBS) {
  const types = J.types || ['vocab', 'reading', 'dialogue', 'titles'];
  const us = (J.units && J.units.length) ? J.units : UNITS;   // per-job unit subset
  if (types.includes('vocab'))    for (const u of us) tasks.push(() => vocabUnit(J, u));
  if (types.includes('reading'))  for (const u of us) tasks.push(() => readingUnit(J, u));
  if (types.includes('dialogue')) for (const u of us) tasks.push(() => dialogueUnit(J, u));
  if (types.includes('titles'))   tasks.push(() => titles(J));
}
log(`Translating ${JOBS.length} language(s), ${tasks.length} agent tasks`);
const results = await parallel(tasks);
const ok = results.filter(Boolean).length;
log(`Completed ${ok}/${tasks.length} tasks`);
return { jobs: JOBS.map(j => j.lang), tasks: tasks.length, ok };
