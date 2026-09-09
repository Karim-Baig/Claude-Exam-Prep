#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
OUT="../../Claude Certified Architect - Foundations.html"

cat part2_meta.js qb_head.js qb_b*.js cards_head.js cards_b*.js part5_app.js part6_exam.js > .syn.js
node --check .syn.js && echo "JS syntax  : OK"
cat part2_meta.js qb_head.js qb_b*.js cards_head.js cards_b*.js > .dat.js

node -e '
  const fs=require("fs");
  const r=new Function(fs.readFileSync(".dat.js","utf8")+"\n;return {QB,CARDS,TASKS,DOMAINS,SCEN};")();
  let dup=0,bad=0; const ids=new Set();
  r.QB.forEach(q=>{ if(ids.has(q.i)){dup++;console.log("  DUP id "+q.i);} ids.add(q.i);
    if(!q.a||q.a.length!==4||q.c==null||!q.e||!q.k||!q.w||q.w.length!==4||!r.TASKS[q.t]||!r.SCEN[q.s]||!r.DOMAINS[q.d]){bad++;console.log("  BAD q"+q.i);}
    if(q.c!==0){bad++;console.log("  q"+q.i+" not authored with correct option first");} });
  const ci=new Set(); r.CARDS.forEach(c=>{ if(ci.has(c.i)){dup++;console.log("  DUP card "+c.i);} ci.add(c.i);
    if(!c.q||!c.a||!r.DOMAINS[c.d]){bad++;console.log("  BAD card "+c.i);} });
  console.log("Integrity  : "+r.QB.length+" questions | "+r.CARDS.length+" cards | "+dup+" dup | "+bad+" malformed");
  // exam simulator: blueprint weights must total 100 and seat exactly 60
  const N=60, ds=Object.keys(r.DOMAINS);
  const wsum=ds.reduce((a,d)=>a+r.DOMAINS[d].w,0);
  const raw=ds.map(d=>({d,x:r.DOMAINS[d].w/100*N})); const q={}; let used=0;
  raw.forEach(x=>{q[x.d]=Math.floor(x.x); used+=q[x.d];});
  raw.map(x=>({d:x.d,f:x.x-Math.floor(x.x)})).sort((a,b)=>b.f-a.f).slice(0,N-used).forEach(x=>q[x.d]++);
  const seats=ds.reduce((a,d)=>a+q[d],0);
  ds.forEach(d=>{ const have=r.QB.filter(x=>String(x.d)===String(d)).length;
    if(have<q[d]){bad++;console.log("  D"+d+" needs "+q[d]+" exam seats, bank has "+have);} });
  console.log("Exam paper : weights "+wsum+"% | seats "+seats+"/"+N+" ("+ds.map(d=>"D"+d+":"+q[d]).join(" ")+")");
  if(wsum!==100||seats!==N){console.log("  exam quota does not resolve to "+N);process.exit(1);}
  if(dup||bad) process.exit(1);
'
node shuffle.js
cat part1_head.html part2_meta.js .qb_final.js part5_app.js part6_exam.js part9_tail.html > "$OUT"
rm -f .syn.js .dat.js .qb_final.js
echo "Built      : $OUT  ($(du -h "$OUT" | cut -f1))"
