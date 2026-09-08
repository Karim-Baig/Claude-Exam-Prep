#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
OUT="../../CCAR-F_Architect_Question_Bank.html"

cat part2_meta.js qb_head.js qb_b*.js cards_head.js cards_b*.js part5_app.js > .syn.js
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
  if(dup||bad) process.exit(1);
'
node shuffle.js
cat part1_head.html part2_meta.js .qb_final.js part5_app.js part9_tail.html > "$OUT"
rm -f .syn.js .dat.js .qb_final.js
echo "Built      : $OUT  ($(du -h "$OUT" | cut -f1))"
