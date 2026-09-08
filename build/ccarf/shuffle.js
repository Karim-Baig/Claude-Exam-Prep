/* Build-time transform.
   Authoring convention: the correct option is always written FIRST (c:0),
   which keeps the source readable and the per-option rationales aligned.
   This script redistributes the correct answer evenly across A/B/C/D using a
   fixed seed, so the published bank has no positional tell and the shuffle is
   reproducible across rebuilds (important: saved answers reference an index). */
const fs = require("fs");

const src = fs.readFileSync(".dat.js", "utf8");
const R = new Function(src + "\n;return {QB,CARDS};")();
const QB = R.QB, CARDS = R.CARDS;

function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0;
  let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t;
  return ((t^t>>>14)>>>0)/4294967296; }; }
const rnd = mulberry32(20260908);

// balanced target positions: equal counts of 0,1,2,3, then shuffled
const pos = QB.map((_,n)=> n % 4);
for(let i=pos.length-1;i>0;i--){ const j=(rnd()*(i+1))|0; [pos[i],pos[j]]=[pos[j],pos[i]]; }

/* ---- verified documentation notes -------------------------------------
   Applied where the published exam blueprint / third-party study guides
   diverge from Anthropic's current official documentation. The question
   keeps the exam-aligned framing (so it prepares you for the real item)
   and carries a note stating what the docs actually say.               */
const DOC_NOTES = [
  { test: /PostToolUse/,
    note: "<strong>Verified against Anthropic docs.</strong> The blueprint describes <code>PostToolUse</code> as the place to normalise, redact or trim tool results before the model sees them, and that is the answer the exam expects. Anthropic's current hooks reference says otherwise: <code>PostToolUse</code> fires <em>after</em> the tool has run, supports only a top-level <code>decision: \"block\"</code> with a <code>reason</code> shown to Claude, and cannot rewrite the result &mdash; <code>updatedInput</code> is documented only for <code>PreToolUse</code> and <code>PermissionRequest</code>. In production, do this normalisation inside the tool or MCP server. <code>PreToolUse</code> blocking and argument rewriting are fully confirmed." },
  { test: /<code>Task<\/code>|\bTask tool\b|\\"Task\\"/,
    note: "<strong>Naming note.</strong> The blueprint calls the subagent-spawning tool <code>Task</code>, which is what the exam will use. In current Claude Code it was renamed to the <code>Agent</code> tool (<code>Task</code> was the name up to v2.1.62). The mechanics are unchanged: it must be in the spawning agent's tool list, and several calls in one turn run concurrently." },
  { test: /allowed-tools/,
    note: "<strong>Verified against Anthropic docs.</strong> In <em>skill and command</em> frontmatter, <code>allowed-tools</code> <strong>pre-approves</strong> tools for that turn so they skip the permission prompt &mdash; it does not restrict, and unlisted tools stay callable. <code>disallowed-tools</code> is the field that removes tools from the pool. The opposite naming applies to <em>subagents</em>, where <code>tools</code> (Agent SDK: <code>allowedTools</code>) <em>is</em> an allowlist and does restrict." }
];
function docNote(obj){
  const hay = [obj.q, obj.ask, obj.a && obj.a.join(" "), obj.w && obj.w.join(" "), obj.e, obj.k].filter(Boolean).join(" ");
  const hits = DOC_NOTES.filter(d => d.test.test(hay)).map(d => d.note);
  return hits.length ? hits.join("<br><br>") : null;
}
QB.forEach(q => { const nt = docNote(q); if(nt && !q.n) q.n = nt; });

QB.forEach((q,n)=>{
  const c = q.c;
  const correct = {o:q.a[c], w:q.w[c]};
  const others = q.a.map((o,ix)=>({o, w:q.w[ix]})).filter((_,ix)=>ix!==c);
  for(let i=others.length-1;i>0;i--){ const j=(rnd()*(i+1))|0; [others[i],others[j]]=[others[j],others[i]]; }
  const target = pos[n];
  const slots = new Array(4);
  slots[target] = correct;
  let k=0;
  for(let s=0;s<4;s++) if(s!==target) slots[s] = others[k++];
  q.a = slots.map(x=>x.o);
  q.w = slots.map(x=>x.w);
  q.c = target;
  q.i = n + 1;                       // renumber contiguously
});
CARDS.forEach((c,n)=>{ c.i = "c" + (n+1); });

fs.writeFileSync(".qb_final.js",
  "const QB=" + JSON.stringify(QB) + ";\nconst CARDS=" + JSON.stringify(CARDS) + ";\n");

const key = {}; QB.forEach(q=> key[q.c]=(key[q.c]||0)+1);
const dom = {}; QB.forEach(q=> dom[q.d]=(dom[q.d]||0)+1);
const tsk = {}; QB.forEach(q=> tsk[q.t]=(tsk[q.t]||0)+1);
console.log("Answer key : A=" + (key[0]||0) + " B=" + (key[1]||0) + " C=" + (key[2]||0) + " D=" + (key[3]||0));
console.log("Per domain : " + JSON.stringify(dom));
console.log("Per task   : " + Object.keys(tsk).sort().map(k=>k+":"+tsk[k]).join("  "));
