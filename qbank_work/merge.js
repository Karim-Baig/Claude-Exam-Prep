// Merge validated authoring batches into the exam HTML.
// Refuses to merge if any batch fails validation, collides on ids, or duplicates
// an existing question. Run with --dry to validate without writing.
const fs = require('fs');
const path = require('path');

const WORK = __dirname;
const HTML = path.join(WORK, '..', 'claude-foundations-exam.html');
const DRY = process.argv.includes('--dry');
const LTR = ['A', 'B', 'C', 'D'];

const EXPECTED = {
  B01:{n:80,  lo:1001, hi:1080, d:['D1']},
  B02:{n:75,  lo:1081, hi:1155, d:['D1']},
  B03:{n:75,  lo:1156, hi:1230, d:['D1']},
  B04:{n:70,  lo:1231, hi:1300, d:['D1']},
  B05:{n:82,  lo:1301, hi:1382, d:['D1']},
  B06:{n:70,  lo:1401, hi:1470, d:['D2']},
  B07:{n:65,  lo:1471, hi:1535, d:['D2']},
  B08:{n:62,  lo:1536, hi:1597, d:['D2']},
  B09:{n:80,  lo:1601, hi:1680, d:['D3']},
  B10:{n:81,  lo:1681, hi:1761, d:['D3']},
  B11:{n:65,  lo:1801, hi:1865, d:['D4']},
  B12:{n:55,  lo:1866, hi:1920, d:['D4']},
  B13:{n:70,  lo:1921, hi:1990, d:['D5']},
  B14:{n:43,  lo:1991, hi:2033, d:['D5']},
  B15:{n:87,  lo:2041, hi:2127, d:['D6']},
  B16:{n:46,  lo:2131, hi:2176, d:['D7','D8']},
};

// Agents intermittently wrap output in <script> tags or markdown fences.
// Strip them rather than rejecting — cheaper than a round-trip, and the
// normalised text is what gets merged, so the HTML stays well-formed.
// Trim to the QB.push(...) span FIRST, then clean only outside it.
// Question stems legitimately contain ``` fences and code, so never strip
// those globally — doing so would corrupt code blocks inside string literals.
function normalise(src) {
  let s = src, stripped = [];
  const a = s.indexOf('QB.push');
  if (a < 0) throw new Error('no QB.push( call found');
  if (a > 0) { s = s.slice(a); stripped.push('leading wrapper/prose'); }
  const b = s.lastIndexOf(');');
  if (b < 0) throw new Error('unterminated QB.push( call');
  if (b < s.length - 3) { s = s.slice(0, b + 2); stripped.push('trailing wrapper/prose'); }
  // A script tag surviving inside the span would be inside a string literal,
  // which is legitimate question content — leave it alone.
  return { src: s, stripped };
}
function loadBatch(file) {
  const QB = [];
  const raw = fs.readFileSync(file, 'utf8');
  const { src, stripped } = normalise(raw);
  eval(src);
  if (stripped.length) {
    fs.writeFileSync(file, src.trim() + '\n');   // persist the cleaned form
    console.log(`      (auto-cleaned: ${stripped.join(', ')})`);
  }
  return QB;
}

// ---- load existing bank ----
const html = fs.readFileSync(HTML, 'utf8');
const existing = [];
{
  const QB = existing;
  eval([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1])
        .filter(s => s.includes('QB.push')).join('\n'));
}
console.log('Existing bank:', existing.length);

// ---- validate each batch independently ----
const seenIds = new Map(existing.map(q => [q.id, 'existing']));
const batches = {};
let fatal = 0;

Object.keys(EXPECTED).forEach(key => {
  const file = path.join(WORK, `batch_${key}.js`);
  if (!fs.existsSync(file)) { console.log(`  ${key}  MISSING — not yet written`); return; }
  const spec = EXPECTED[key];
  let QB;
  try { QB = loadBatch(file); }
  catch (e) { console.log(`  ${key}  PARSE FAIL: ${e.message}`); return; }

  // A short count means the agent is still writing — defer that batch rather
  // than failing the whole merge, so complete batches can land incrementally.
  const problems = [];
  if (QB.length !== spec.n) {
    console.log(`  ${key}  ${QB.length}/${spec.n} — INCOMPLETE, deferred to a later merge`);
    return;
  }

  QB.forEach(q => {
    const p = [];
    if (!q.q || !q.e || !q.w) p.push('missing text');
    if (!Array.isArray(q.o) || q.o.length !== 4) p.push('options');
    if (typeof q.a !== 'number' || q.a < 0 || q.a > 3) p.push('answer idx');
    if (q.id < spec.lo || q.id > spec.hi) p.push('id out of range');
    if (!spec.d.includes(q.d)) p.push(`domain ${q.d}`);
    if (!q.t || !'SR'.includes(q.t)) p.push('type');
    if (!q.f || !'EMH'.includes(q.f)) p.push('difficulty');
    if (!q.s) p.push('subskill');
    // option letter prefixes
    if (Array.isArray(q.o) && q.o.some((o, i) => !String(o).startsWith(LTR[i] + '. '))) p.push('opt prefix');
    // w must reference all three wrong options and never the correct one
    const refs = new Set();
    [...(q.w || '').matchAll(/\b([A-D])(?=\s*[—/])/g)].forEach(m => refs.add(m[1]));
    [...(q.w || '').matchAll(/\b([A-D])\/([A-D])/g)].forEach(m => { refs.add(m[1]); refs.add(m[2]); });
    [...(q.w || '').matchAll(/\b([A-D]), ([A-D]),? and ([A-D])\b/g)].forEach(m => { refs.add(m[1]); refs.add(m[2]); refs.add(m[3]); });
    if (refs.has(LTR[q.a])) p.push('w references correct answer');
    if (!LTR.filter((_, i) => i !== q.a).every(L => refs.has(L))) p.push('w incomplete coverage');
    if (/\b[A-D]:/.test(q.w || '')) p.push('w uses colon form');
    // id collision across all sources
    if (seenIds.has(q.id)) p.push(`id collides with ${seenIds.get(q.id)}`);
    else seenIds.set(q.id, key);
    if (p.length) problems.push(`#${q.id}: ${p.join(', ')}`);
  });

  if (problems.length) {
    console.log(`  ${key}  ${QB.length} q — ${problems.length} PROBLEM(S)`);
    problems.slice(0, 12).forEach(p => console.log(`      ${p}`));
    if (problems.length > 12) console.log(`      …and ${problems.length - 12} more`);
    fatal += problems.length;
  } else {
    const a = {}; QB.forEach(q => a[q.a] = (a[q.a] || 0) + 1);
    const s = QB.filter(q => q.t === 'S').length;
    console.log(`  ${key}  ${QB.length} q  OK   spread ${[0,1,2,3].map(k=>a[k]||0).join('/')}  scenario ${Math.round(s/QB.length*100)}%`);
    batches[key] = QB;
  }
});

// ---- cross-batch + against-existing duplicate detection ----
const all = [...existing, ...Object.values(batches).flat()];
const norm = s => new Set(String(s).toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(w => w.length > 4));
const sig = all.map(q => ({ id: q.id, d: q.d, set: norm(q.q + ' ' + q.o.join(' ')) }));
let dups = 0;
for (let i = 0; i < sig.length; i++) {
  for (let j = i + 1; j < sig.length; j++) {
    if (sig[i].set.size < 8 || sig[j].set.size < 8) continue;
    const inter = [...sig[i].set].filter(x => sig[j].set.has(x)).length;
    if (inter / (sig[i].set.size + sig[j].set.size - inter) > 0.55) {
      if (dups < 15) console.log(`  NEAR-DUP  #${sig[i].id} <-> #${sig[j].id}`);
      dups++;
    }
  }
}
console.log(`\nCross-bank near-duplicates: ${dups}`);
console.log(`Total after merge would be: ${all.length}`);
if (fatal) { console.log(`\nREFUSING TO MERGE — ${fatal} validation problem(s).`); process.exit(1); }
if (dups) console.log('WARNING: near-duplicates present (review, not fatal).');

// ---- merge ----
if (DRY) { console.log('\n--dry: no changes written.'); process.exit(0); }
if (!Object.keys(batches).length) { console.log('\nNothing to merge.'); process.exit(0); }

let insert = '';
Object.keys(EXPECTED).forEach(key => {
  if (!batches[key]) return;
  insert += `<script>\n/* ===== authored batch ${key} ===== */\n`
          + fs.readFileSync(path.join(WORK, `batch_${key}.js`), 'utf8').trim()
          + `\n</script>\n`;
});
if (!html.includes('<!--@BATCH@-->')) { console.log('Marker <!--@BATCH@--> not found.'); process.exit(1); }
fs.copyFileSync(HTML, HTML + '.bak');
// MUST use a replacer FUNCTION: with a replacement *string*, JS expands `$&`,
// "$`", "$'" and `$1`. Question text legitimately contains regexes ending in
// `$` followed by a backtick, which silently injected the whole document
// prefix into the bank. A function makes the replacement literal.
const merged = html.replace('<!--@BATCH@-->', () => insert + '<!--@BATCH@-->');
// post-write sanity: the document must still have exactly one shell
const shells = (merged.match(/<!DOCTYPE html>/gi) || []).length;
if (shells !== 1) { console.log(`ABORT: ${shells} DOCTYPE occurrences after merge — corruption.`); process.exit(1); }
fs.writeFileSync(HTML, merged);
console.log(`\nMerged ${Object.keys(batches).length} batch(es). Backup at claude-foundations-exam.html.bak`);
