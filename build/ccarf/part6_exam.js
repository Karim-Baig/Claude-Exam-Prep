/* ============================================================
   EXAM SIMULATOR
   60 questions / 120 minutes, drawn to the published blueprint
   weights, with 4 scenarios sampled from the pool of 8.
   ============================================================ */
const EX_N    = 60;
const EX_MIN  = 120;
const EX_PASS = 720;
const EX_SCEN = 4;            /* scenarios drawn from the pool of 8 */

/* seats per domain, largest-remainder so the paper is exactly EX_N */
function examQuota(){
  const raw = Object.keys(DOMAINS).map(d=>({d, x: DOMAINS[d].w/100*EX_N}));
  const q = {}; let used = 0;
  raw.forEach(r=>{ q[r.d]=Math.floor(r.x); used+=q[r.d]; });
  raw.map(r=>({d:r.d, f:r.x-Math.floor(r.x)}))
     .sort((a,b)=>b.f-a.f)
     .slice(0, EX_N-used)
     .forEach(r=> q[r.d]++);
  return q;
}

function shuf(a){ for(let i=a.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;[a[i],a[j]]=[a[j],a[i]];} return a; }

function buildPaper(){
  const pool   = Object.keys(SCEN).filter(k=>k!=="GEN");
  const picked = shuf(pool.slice()).slice(0, EX_SCEN);
  const ok     = new Set(picked.concat(["GEN"]));
  const used   = S.exUsed || (S.exUsed = {});
  const quota  = examQuota();
  const ids    = [];

  for(const d in quota){
    let cand = QB.filter(q=>String(q.d)===String(d) && ok.has(q.s));
    if(cand.length < quota[d]) cand = QB.filter(q=>String(q.d)===String(d));
    /* prefer questions not served in a previous sitting */
    const fresh = shuf(cand.filter(q=>!used[q.i]));
    const stale = shuf(cand.filter(q=> used[q.i]));
    fresh.concat(stale).slice(0, quota[d]).forEach(q=> ids.push(q.i));
  }
  return {ids: shuf(ids), scen: picked};
}

function examStart(){
  const p = buildPaper();
  S.exam = {ids:p.ids, scen:p.scen, ans:{}, flag:{}, cur:0,
            t0:Date.now(), dur:EX_MIN*60000, done:false};
  save(); renderExam();
}

const exQ    = id => QB.find(q=>q.i===id);
const exLeft = () => Math.max(0, S.exam.t0 + S.exam.dur - Date.now());
function hhmmss(ms){
  const s = Math.floor(ms/1000);
  return [Math.floor(s/3600), Math.floor(s/60)%60, s%60]
    .map(n=>String(n).padStart(2,"0")).join(":");
}

let EXTIMER = null;
function examStopClock(){ clearInterval(EXTIMER); EXTIMER=null; }
function examTick(){
  const el = $("#exClock");
  if(!el || !S.exam || S.exam.done){ examStopClock(); return; }
  const ms = exLeft();
  el.textContent = hhmmss(ms);
  el.className = "clock" + (ms<=5*60000 ? " crit" : (ms<=15*60000 ? " warn" : ""));
  if(ms<=0){ examStopClock(); examSubmit(true); }
}

/* ---------- router entry ---------- */
function renderExam(){
  examStopClock();
  const e = S.exam;
  if(!e)          return examIntro();
  if(e.done)      return examResults();
  if(exLeft()<=0) return examSubmit(true);
  examRun();
}

/* ---------- intro ---------- */
function examIntro(){
  const hist = S.exams || [];
  const best = hist.length ? Math.max.apply(null, hist.map(h=>h.score)) : null;
  const q = examQuota();
  $("#v-exam").innerHTML = `
  <div class="card" style="margin-bottom:16px">
    <h3>Exam Simulator</h3>
    <p class="sub">A full mock under real conditions: <strong>${EX_N} questions</strong>,
      <strong>${EX_MIN} minutes</strong>, no feedback until you submit. Scored 100&ndash;1000,
      pass at <strong>${EX_PASS}</strong>. Each sitting draws <strong>${EX_SCEN} scenarios</strong>
      from the pool of 8, as the real exam does, and weights the paper to the blueprint:</p>
    <table class="tbl" style="margin:14px 0">
      ${Object.keys(DOMAINS).map(d=>`<tr>
        <td><span class="pill d${d}">D${d}</span> ${DOMAINS[d].n}</td>
        <td style="text-align:right;color:var(--tx2)">${DOMAINS[d].w}%</td>
        <td style="text-align:right"><strong>${q[d]} questions</strong></td></tr>`).join("")}
    </table>
    <p class="sub">Questions you have not been served in a previous sitting are preferred, so
      repeat attempts stay useful. Answers feed Weak Areas once you submit. The clock runs on
      wall time &mdash; closing the tab does not pause it, and your paper is restored if you reload.</p>
    <div class="row" style="margin-top:14px">
      <button class="btn" id="exGo">Start ${EX_N}-question exam</button>
      ${hist.length?`<button class="btn ghost" id="exHist">Past attempts (${hist.length})</button>`:""}
    </div>
  </div>
  ${best!==null?`<div class="card"><h3>Best score so far</h3>
    <div class="scorebig" style="color:${best>=EX_PASS?"var(--ok)":"var(--bad)"}">${best}</div>
    <p class="sub">across ${hist.length} sitting${hist.length>1?"s":""}</p></div>`:""}`;

  $("#exGo").onclick = examStart;
  if($("#exHist")) $("#exHist").onclick = examHistory;
}

/* ---------- the paper ---------- */
function examRun(){
  const e = S.exam;
  $("#v-exam").innerHTML = `
    <div class="exambar">
      <div><div class="clock" id="exClock">${hhmmss(exLeft())}</div>
        <div class="meta">time remaining</div></div>
      <div><div id="exDone" style="font-weight:700;font-size:17px">${Object.keys(e.ans).length}<span style="color:var(--tx3)">/${EX_N}</span></div>
        <div class="meta">answered</div></div>
      <div><div id="exFlagN" style="font-weight:700;font-size:17px;color:var(--warn)">${Object.keys(e.flag).length}</div>
        <div class="meta">flagged</div></div>
      <div class="sp"></div>
      <button class="btn ghost" id="exQuit">Abandon</button>
      <button class="btn" id="exEnd">Submit exam</button>
    </div>
    <div id="exSlot"></div>
    <div class="card" style="margin-top:16px">
      <h3>Question navigator</h3>
      <div class="palette" id="exPal"></div>
      <div class="legend">
        <span><i style="background:var(--accdim);border-color:var(--acc)"></i>answered</span>
        <span><i style="background:var(--bg3)"></i>not answered</span>
        <span><i style="background:var(--bg3);border-color:var(--warn)"></i>flagged</span>
      </div>
    </div>`;

  $("#exEnd").onclick  = examConfirmSubmit;
  $("#exQuit").onclick = ()=>{
    if(confirm("Abandon this exam? Your answers will be discarded and nothing is recorded.")){
      examStopClock(); delete S.exam; save(); renderExam();
    }
  };
  exDraw();
  EXTIMER = setInterval(examTick, 1000);
}

function exPalette(){
  const e = S.exam, pal = $("#exPal"); if(!pal) return;
  pal.innerHTML = e.ids.map((id,n)=>{
    const c = ["pcell"];
    if(e.ans[id]!=null) c.push("done");
    if(e.flag[id])      c.push("flag");
    if(n===e.cur)       c.push("cur");
    return `<button class="${c.join(" ")}" data-n="${n}">${n+1}</button>`;
  }).join("");
  $$("#exPal .pcell").forEach(b=> b.onclick = ()=>{ S.exam.cur=+b.dataset.n; save(); exDraw(); });
}

function exCounts(){
  const e = S.exam;
  if($("#exDone"))  $("#exDone").innerHTML  = `${Object.keys(e.ans).length}<span style="color:var(--tx3)">/${EX_N}</span>`;
  if($("#exFlagN")) $("#exFlagN").textContent = Object.keys(e.flag).length;
}

function exDraw(){
  const e = S.exam, q = exQ(e.ids[e.cur]);
  if(!q){ toast("Question missing from bank"); return; }
  const sc = SCEN[q.s] || SCEN.GEN;
  const pick = e.ans[q.i];
  $("#exSlot").innerHTML = `
    <div class="card">
      <div class="qhead">
        <span class="qnum">Question ${e.cur+1} of ${EX_N}</span>
        ${q.s!=="GEN"?`<span class="pill">${sc.n}</span>`:""}
        <button class="star ${e.flag[q.i]?"on":""}" id="exFlag" title="Flag for review (F)">${e.flag[q.i]?"★":"☆"}</button>
      </div>
      ${q.s!=="GEN"?`<div class="scen"><div class="t">Scenario &mdash; ${sc.n}</div><div class="b">${sc.b}</div></div>`:""}
      <div class="stem">${q.q}</div>
      <div class="ask">${q.ask||"Which approach is most effective?"}</div>
      <div class="opts" id="exOpts">
        ${q.a.map((o,ix)=>`<button class="opt ${pick===ix?"picked":""}" data-ix="${ix}"><span class="k">${KEYS[ix]}</span><span class="ot">${o}</span></button>`).join("")}
      </div>
      <div class="qfoot">
        <button class="btn ghost" id="exPrev" ${e.cur===0?"disabled":""}>&larr; Previous</button>
        <button class="btn" id="exNext">${e.cur===EX_N-1?"Go to first unanswered":"Next &rarr;"}</button>
        <button class="btn ghost" id="exClear" ${pick==null?"disabled":""}>Clear answer</button>
        <span class="sp" style="font-size:12px;color:var(--tx3)">Keys: <kbd>A</kbd>&ndash;<kbd>D</kbd> answer &middot; <kbd>&rarr;</kbd> next &middot; <kbd>F</kbd> flag</span>
      </div>
    </div>`;

  $$("#exOpts .opt").forEach(b=> b.onclick = ()=>{
    S.exam.ans[q.i] = +b.dataset.ix; save();
    $$("#exOpts .opt").forEach(x=> x.classList.toggle("picked", x===b));
    $("#exClear").disabled = false;
    exPalette(); exCounts();
  });
  $("#exPrev").onclick = ()=>{ if(S.exam.cur>0){ S.exam.cur--; save(); exDraw(); } };
  $("#exNext").onclick = ()=>{
    if(S.exam.cur < EX_N-1){ S.exam.cur++; save(); exDraw(); }
    else{
      const n = S.exam.ids.findIndex(id=>S.exam.ans[id]==null);
      if(n<0) examConfirmSubmit();
      else { S.exam.cur=n; save(); exDraw(); toast("Jumped to first unanswered"); }
    }
  };
  $("#exClear").onclick = ()=>{ delete S.exam.ans[q.i]; save(); exDraw(); exCounts(); };
  $("#exFlag").onclick  = ()=>{
    if(S.exam.flag[q.i]) delete S.exam.flag[q.i]; else S.exam.flag[q.i]=1;
    save(); exDraw(); exCounts();
  };
  exPalette();
}

function examConfirmSubmit(){
  const e = S.exam, un = e.ids.filter(id=>e.ans[id]==null).length;
  const msg = un
    ? un+" question"+(un>1?"s are":" is")+" unanswered. There is no guessing penalty — "
      + "unanswered questions simply score zero.\n\nSubmit anyway?"
    : "Submit your exam for scoring?";
  if(confirm(msg)) examSubmit(false);
}

/* ---------- scoring ---------- */
function examSubmit(auto){
  examStopClock();
  const e = S.exam; if(!e || e.done) return;
  const dom = {}; Object.keys(DOMAINS).forEach(d=> dom[d]={ok:0,total:0});
  let ok = 0;
  S.exUsed = S.exUsed || {};

  e.ids.forEach(id=>{
    const q = exQ(id); if(!q) return;
    const pick  = e.ans[id];
    const right = pick===q.c;
    if(right) ok++;
    dom[q.d].total++; if(right) dom[q.d].ok++;
    S.exUsed[id] = 1;
    if(pick!=null){                      /* feed Weak Areas */
      const r = S.seen[id] || {n:0};
      S.seen[id] = {a:pick, ok:right, n:r.n+1};
    }
  });

  const acc = ok/EX_N;
  e.done  = true;
  e.score = scaled(acc);
  e.ok    = ok;
  e.dom   = dom;
  e.secs  = Math.round(Math.min(e.dur, Date.now()-e.t0)/1000);
  e.auto  = !!auto;
  (S.exams = S.exams || []).push({ts:Date.now(), score:e.score, ok:ok,
                                  total:EX_N, secs:e.secs, auto:!!auto});
  markDay(); save();
  if(auto) toast("Time expired — exam submitted automatically");
  examResults();
}

function examResults(){
  const e = S.exam, pass = e.score>=EX_PASS;
  const mins = Math.floor(e.secs/60), secs = e.secs%60;
  $("#v-exam").innerHTML = `
  <div class="card" style="margin-bottom:16px;text-align:center">
    <p class="sub" style="margin-bottom:4px">Scaled score</p>
    <div class="scorebig" style="color:${pass?"var(--ok)":"var(--bad)"}">${e.score}</div>
    <div class="verdict ${pass?"pass":"fail"}">${pass?"PASS":"BELOW PASS LINE"}</div>
    <div class="gauge">
      <i style="width:${((e.score-100)/900*100).toFixed(1)}%;background:${pass?"var(--ok)":"var(--bad)"}"></i>
      <span class="cut" style="left:${((EX_PASS-100)/900*100).toFixed(1)}%"></span>
    </div>
    <p class="sub" style="font-size:12px">100 &nbsp;&middot;&nbsp; pass mark ${EX_PASS} &nbsp;&middot;&nbsp; 1000</p>
    <p class="sub" style="margin-top:12px"><strong>${e.ok}/${EX_N}</strong> correct
      (${(e.ok/EX_N*100).toFixed(1)}%) &nbsp;&middot;&nbsp; ${mins}m ${secs}s used of ${EX_MIN}m
      ${e.auto?` &nbsp;&middot;&nbsp; <span style="color:var(--warn)">auto-submitted on time-out</span>`:""}</p>
  </div>

  <div class="card" style="margin-bottom:16px">
    <h3>By domain</h3>
    <p class="sub" style="margin-bottom:14px">Where the marks went on this paper.</p>
    ${Object.keys(DOMAINS).map(d=>{
      const b=e.dom[d], a=b.total?b.ok/b.total:0;
      return `<div class="dombar">
        <div class="nm">${DOMAINS[d].n}</div>
        <div class="tr"><i style="width:${(a*100).toFixed(1)}%;background:${DOMAINS[d].c}"></i></div>
        <div class="vl">${b.total?(a*100).toFixed(0)+"%":"&mdash;"} <span style="color:var(--tx3)">${b.ok}/${b.total}</span></div>
      </div>`;
    }).join("")}
  </div>

  <div class="card" style="margin-bottom:16px">
    <h3>Scenarios on this paper</h3>
    <div class="row" style="margin-top:6px">${e.scen.map(k=>`<span class="pill">${SCEN[k].n}</span>`).join("")}</div>
    <p class="sub" style="margin-top:10px">The real exam draws ${EX_SCEN} of 8. A new sitting draws again.</p>
  </div>

  <div class="card" style="margin-bottom:16px">
    <h3>Question review</h3>
    <p class="sub" style="margin-bottom:10px">Click any question to read the full explanation.</p>
    <div class="palette" style="margin-bottom:14px">
      ${e.ids.map((id,n)=>{ const q=exQ(id);
        return `<button class="pcell ${e.ans[id]===q.c?"ok":"no"}" data-rev="${n}">${n+1}</button>`; }).join("")}
    </div>
    <div class="legend">
      <span><i style="background:var(--okdim);border-color:var(--ok)"></i>correct</span>
      <span><i style="background:var(--baddim);border-color:var(--bad)"></i>incorrect or unanswered</span>
    </div>
    <div id="exRev" style="margin-top:14px"></div>
  </div>

  <div class="card">
    <div class="row">
      <button class="btn" id="exAgain">Start a new exam</button>
      <button class="btn ghost" id="exWrong">Practise what I missed</button>
      <button class="btn ghost" id="exHist2">Past attempts (${(S.exams||[]).length})</button>
    </div>
  </div>`;

  $$("[data-rev]").forEach(b=> b.onclick = ()=> exReview(+b.dataset.rev));
  $("#exAgain").onclick = ()=>{
    if(confirm("Start a fresh exam? This result stays in your history.")){
      delete S.exam; save(); examStart();
    }
  };
  $("#exHist2").onclick = examHistory;
  $("#exWrong").onclick = ()=>{
    const miss = e.ids.filter(id=> e.ans[id]!==exQ(id).c);
    if(!miss.length){ toast("Nothing missed — full marks"); return; }
    S.stars = S.stars || {}; miss.forEach(id=> S.stars[id]=1);
    S.filters = Object.assign({}, S.filters, {d:"",t:"",s:"",mode:"starred",shuffle:false});
    save(); toast(miss.length+" missed questions bookmarked"); go("practice");
  };
}

function exReview(n){
  const e = S.exam, id = e.ids[n], q = exQ(id);
  const pick = e.ans[id], right = pick===q.c;
  const sc = SCEN[q.s] || SCEN.GEN;
  $("#exRev").innerHTML = `
    <div class="card" style="background:var(--bg3)">
      <div class="qhead">
        <span class="qnum">Question ${n+1}</span>
        <span class="pill d${q.d}">D${q.d} &middot; ${DOMAINS[q.d].n}</span>
        <span class="pill">${q.t} ${esc(TASKS[q.t]||"")}</span>
      </div>
      ${q.s!=="GEN"?`<div class="scen"><div class="t">Scenario &mdash; ${sc.n}</div><div class="b">${sc.b}</div></div>`:""}
      <div class="stem">${q.q}</div>
      <div class="ask">${q.ask||"Which approach is most effective?"}</div>
      <div class="opts">
        ${q.a.map((o,ix)=>`<div class="opt locked ${ix===q.c?"correct":(ix===pick?"wrong":"")}"><span class="k">${KEYS[ix]}</span><span class="ot">${o}${q.w&&q.w[ix]?`<span class="why"><strong>${ix===q.c?"Correct:":"Why not "+KEYS[ix]+":"}</strong> ${q.w[ix]}</span>`:""}</span></div>`).join("")}
      </div>
      <div class="exp ${right?"good":"bad"}">
        <div class="hd">${pick==null ? "Not answered &mdash; the answer is "+KEYS[q.c]
                        : (right ? "Correct &mdash; "+KEYS[q.c]
                                 : "Incorrect &mdash; the answer is "+KEYS[q.c])}</div>
        <div class="bd">
          <p>${q.e}</p>
          ${q.k?`<div class="anchor"><div class="t">Concept to lock in</div><div class="b">${q.k}</div></div>`:""}
          ${q.n?`<div class="anchor docnote"><div class="t">Documentation check</div><div class="b">${q.n}</div></div>`:""}
        </div>
      </div>
    </div>`;
  $("#exRev").scrollIntoView({behavior:"smooth", block:"nearest"});
}

function examHistory(){
  const h = (S.exams||[]).slice().reverse();
  $("#v-exam").innerHTML = `
  <div class="card">
    <h3>Past attempts</h3>
    <p class="sub" style="margin-bottom:12px">${h.length} sitting${h.length===1?"":"s"} recorded in this browser.</p>
    ${h.length ? h.map(r=>`<div class="examrow">
        <span class="ix">${new Date(r.ts).toISOString().slice(0,10)}</span>
        <span class="mk" style="color:${r.score>=EX_PASS?"var(--ok)":"var(--bad)"}">${r.score>=EX_PASS?"✓":"✗"}</span>
        <span class="tx"><strong>${r.score}</strong> &nbsp; ${r.ok}/${r.total} correct &nbsp;&middot;&nbsp; ${Math.floor(r.secs/60)}m${r.auto?" &middot; timed out":""}</span>
      </div>`).join("") : `<p class="sub">No attempts recorded yet.</p>`}
    <div class="row" style="margin-top:16px">
      <button class="btn ghost" id="exBack">Back</button>
      ${h.length?`<button class="btn ghost" id="exClr" style="color:var(--bad);border-color:var(--bad)">Clear history</button>`:""}
    </div>
  </div>`;
  $("#exBack").onclick = renderExam;
  if($("#exClr")) $("#exClr").onclick = ()=>{
    if(confirm("Delete all recorded exam attempts?")){ S.exams=[]; save(); examHistory(); }
  };
}

/* keyboard, exam view only */
document.addEventListener("keydown", ev=>{
  if(!$("#v-exam").classList.contains("on")) return;
  if(/input|select|textarea/i.test(ev.target.tagName)) return;
  const e = S.exam; if(!e || e.done) return;
  const q = exQ(e.ids[e.cur]); if(!q) return;
  const k = ev.key.toUpperCase();
  if(KEYS.indexOf(k)>-1 && KEYS.indexOf(k)<q.a.length){
    const b = $$("#exOpts .opt")[KEYS.indexOf(k)]; if(b){ b.click(); ev.preventDefault(); }
  } else if(/^[1-4]$/.test(k)){
    const b = $$("#exOpts .opt")[+k-1]; if(b){ b.click(); ev.preventDefault(); }
  } else if(ev.key==="ArrowRight"){ const b=$("#exNext"); if(b){ b.click(); ev.preventDefault(); } }
  else if(ev.key==="ArrowLeft"){ const b=$("#exPrev"); if(b){ b.click(); ev.preventDefault(); } }
  else if(k==="F"){ const b=$("#exFlag"); if(b) b.click(); }
});
