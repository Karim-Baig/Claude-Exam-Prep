// Full-bank integrity + quality report. Run from qbank_work: node verify.js
const fs = require('fs');
const path = require('path');
const HTML = path.join(__dirname, '..', 'claude-foundations-exam.html');
const html = fs.readFileSync(HTML, 'utf8');
const QB = [];
eval([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1])
      .filter(s => s.includes('QB.push')).join('\n'));

const LTR = ['A', 'B', 'C', 'D'];
const W = { D1:33.1, D2:16.8, D3:14.7, D4:11.0, D5:10.6, D6:8.1, D7:3.1, D8:2.6 };
const DN = { D1:'Applications & Integration', D2:'Model Selection & Optimization',
             D3:'Agents & Workflows', D4:'Prompt & Context Engineering',
             D5:'Tools & MCP', D6:'Security & Safety', D7:'Claude Code',
             D8:'Evaluation, Testing & Debugging' };

console.log('=== BANK ===');
console.log('Questions:', QB.length, '  File:', (fs.statSync(HTML).size/1048576).toFixed(2)+' MB');

const byDom = {}; QB.forEach(q => byDom[q.d] = (byDom[q.d]||0) + 1);
console.log('\nDomain                                have   actual   target   delta');
Object.keys(W).forEach(d => {
  const c = byDom[d]||0, act = c/QB.length*100;
  console.log(`${d} ${DN[d].padEnd(31)} ${String(c).padStart(4)} ${act.toFixed(1).padStart(7)}% ${String(W[d]).padStart(7)}% ${(act-W[d]>=0?'+':'')+(act-W[d]).toFixed(1)}`);
});

const t = {S:0,R:0}; QB.forEach(q => t[q.t]++);
const f = {}; QB.forEach(q => f[q.f] = (f[q.f]||0)+1);
console.log('\nStyle:', (t.S/QB.length*100).toFixed(0)+'% scenario /', (t.R/QB.length*100).toFixed(0)+'% recall   (target 70/30)');
console.log('Difficulty:  E', f.E, ' M', f.M, ' H', f.H,
            ` (${(f.E/QB.length*100).toFixed(0)}/${(f.M/QB.length*100).toFixed(0)}/${(f.H/QB.length*100).toFixed(0)})`);
console.log('Sub-skills:', new Set(QB.map(q => q.s)).size);
console.log('With why-others-fail:', QB.filter(q => q.w).length + '/' + QB.length);

// ---- integrity ----
let bad = 0;
QB.forEach(q => {
  const p = [];
  if (!q.q || !q.e) p.push('text');
  if (!Array.isArray(q.o) || q.o.length !== 4) p.push('options');
  if (typeof q.a !== 'number' || q.a < 0 || q.a > 3) p.push('answer');
  if (!W[q.d]) p.push('domain');
  if (p.length) { console.log('  BAD #' + q.id + ': ' + p.join(',')); bad++; }
});
const ids = QB.map(q => q.id);
const dupIds = ids.filter((v, i) => ids.indexOf(v) !== i);
console.log('\nIntegrity errors:', bad, '| duplicate ids:', dupIds.length);

// ---- runtime option shuffle: distribution + letter-remap correctness ----
function remap(text, o2n) {
  if (!text) return text;
  const ph = L => ' ' + o2n[LTR.indexOf(L)] + ' ';
  return text
    .replace(/\b([A-D]), ([A-D]),? and ([A-D])\b/g, (m,a,b,c) => ph(a)+', '+ph(b)+', and '+ph(c))
    .replace(/\b([A-D])\/([A-D])\/([A-D])\b/g, (m,a,b,c) => ph(a)+'/'+ph(b)+'/'+ph(c))
    .replace(/\b([A-D])\/([A-D])\b/g, (m,a,b) => ph(a)+'/'+ph(b))
    .replace(/([Oo]ption )([A-D])\b/g, (m,p,L) => p+ph(L))
    .replace(/\b([A-D])(?=\s*—)/g, (m,L) => ph(L))
    .replace(/ (\d) /g, (m,n) => LTR[+n]);
}
function prep(q) {
  const idx = [...q.o.keys()];
  let s = (q.id * 2654435761) % 4294967296;
  const rnd = () => { s = (s*1103515245+12345) % 2147483648; return s/2147483648; };
  for (let k = idx.length-1; k > 0; k--) { const j = Math.floor(rnd()*(k+1)); [idx[k],idx[j]]=[idx[j],idx[k]]; }
  const o2n = {}; idx.forEach((o,n) => o2n[o] = n);
  return { ans: idx.indexOf(q.a), w: remap(q.w, o2n), e: remap(q.e, o2n) };
}
const post = {}; let collide = 0, leftover = 0, refsChecked = 0;
QB.forEach(q => {
  const P = prep(q);
  post[P.ans] = (post[P.ans]||0) + 1;
  [...(P.w||'').matchAll(/\b([A-D])(?=\s*—)/g)].forEach(m => {
    refsChecked++;
    if (LTR.indexOf(m[1]) === P.ans) { collide++; }
  });
  if (/ \d /.test(P.e) || / \d /.test(P.w||'')) leftover++;
});
console.log('\nAuthored answer index :', [0,1,2,3].map(k => QB.filter(q=>q.a===k).length).join(' / '));
console.log('After engine shuffle  :', [0,1,2,3].map(k => post[k]||0).join(' / '));
console.log('Letter refs checked:', refsChecked, '| refs hitting correct answer:', collide, '(must be 0)');
console.log('Unresolved placeholders:', leftover, '(must be 0)');

// ---- stale-fact sweep ----
const STALE = [
  [/x-request-id/i, 'x-request-id (should be request-id)'],
  [/\(w\s*[×x]\s*h\)\s*\/\s*750/i, 'obsolete /750 image formula'],
  [/-latest\b/, '-latest alias (does not exist)'],
];
// A stale term is legitimate when used as a distractor or explicitly corrected;
// it is only an error when it appears in the CORRECT option, or is asserted in
// the explanation with no correcting language nearby.
const CORRECTED = /not\b|no\s|does not exist|doesn't exist|obsolete|no longer|removed|deprecated|is gone|is wrong|wrong here|wrong spelling|misconception|assume|trap|instead|rather than|superseded|never/i;
let stale = 0, traps = 0;
STALE.push([/tasks\/result/, 'tasks/result (does not exist)']);
QB.forEach(q => {
  STALE.forEach(([re, label]) => {
    const inCorrect = re.test(q.o[q.a]);
    const inExp = re.test(q.e + ' ' + (q.w || ''));
    const inDistractor = q.o.some((o, k) => k !== q.a && re.test(o));
    if (inCorrect) { console.log('  ERROR #' + q.id + ': ' + label + ' is the KEYED ANSWER'); stale++; return; }
    if (inExp) {
      // does the sentence mentioning it also correct it?
      const sents = (q.e + ' ' + (q.w || '')).split(/(?<=[.!?])\s+/).filter(s => re.test(s));
      if (!sents.some(s => CORRECTED.test(s))) {
        console.log('  ERROR #' + q.id + ': ' + label + ' asserted without correction'); stale++; return;
      }
    }
    if (inDistractor || inExp) traps++;
  });
});
console.log('\nStale-fact ERRORS:', stale, ' | deliberate traps (correct usage):', traps);

// ---- exam simulator weighting sanity ----
let want = {}, tot = 0;
Object.keys(W).forEach(k => { want[k] = Math.round(W[k]/100*53); tot += want[k]; });
console.log('53-question exam sample would draw:',
  Object.keys(want).map(k => k+':'+want[k]).join(' '), '=', tot);
const short = Object.keys(want).filter(k => (byDom[k]||0) < want[k]);
console.log('Domains with too few questions to fill an exam:', short.length ? short.join(',') : 'none');

console.log('\n' + (bad === 0 && dupIds.length === 0 && collide === 0 && leftover === 0 && stale === 0
  ? 'ALL CHECKS PASSED' : 'CHECKS FAILED — see above'));
