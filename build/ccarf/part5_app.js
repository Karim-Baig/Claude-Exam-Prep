/* ============================================================
   Application engine
   ============================================================ */
const $  = (s,r)=> (r||document).querySelector(s);
const $$ = (s,r)=> Array.from((r||document).querySelectorAll(s));
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const KEYS = ["A","B","C","D","E"];
const LS = "ccarf_v1";

/* ---------- persisted state ---------- */
let S = {seen:{}, stars:{}, srs:{}, theme:"dark", days:{}, filters:{}};
try{ Object.assign(S, JSON.parse(localStorage.getItem(LS)||"{}")); }catch(e){}
const save = () => { try{ localStorage.setItem(LS, JSON.stringify(S)); }catch(e){} };

document.documentElement.dataset.theme = S.theme || "dark";
$("#themeBtn").onclick = () => {
  S.theme = document.documentElement.dataset.theme = (S.theme==="dark"?"light":"dark");
  save();
};

let TOAST;
function toast(msg){
  const t=$("#toast"); t.textContent=msg; t.classList.add("on");
  clearTimeout(TOAST); TOAST=setTimeout(()=>t.classList.remove("on"),1800);
}

/* ---------- derived stats ---------- */
const rec = id => S.seen[id];
function stats(list){
  let a=0,c=0;
  (list||QB).forEach(q=>{ const r=rec(q.i); if(r){a++; if(r.ok)c++;} });
  return {ans:a, ok:c, acc: a? c/a : 0, total:(list||QB).length};
}
function byDomain(){
  const m={};
  for(const d in DOMAINS) m[d]={ans:0,ok:0,total:0};
  QB.forEach(q=>{ const b=m[q.d]; if(!b)return; b.total++; const r=rec(q.i); if(r){b.ans++; if(r.ok)b.ok++;} });
  return m;
}
function byTask(){
  const m={};
  QB.forEach(q=>{ (m[q.t] = m[q.t] || {ans:0,ok:0,total:0,d:q.d}).total++;
    const r=rec(q.i); if(r){m[q.t].ans++; if(r.ok)m[q.t].ok++;} });
  return m;
}
const scaled = acc => Math.round(100 + acc*900);
function markDay(){
  const k = new Date().toISOString().slice(0,10);
  S.days[k] = (S.days[k]||0)+1;
}
function streak(){
  let n=0, d=new Date();
  for(;;){ const k=d.toISOString().slice(0,10); if(S.days[k]){n++; d.setDate(d.getDate()-1);} else break; }
  return n;
}

/* ---------- router ---------- */
const VIEWS = {dash:renderDash, practice:renderPractice, weak:renderWeak, cards:renderCards, search:renderSearch, ref:renderRef};
function go(v){
  $$("nav button").forEach(b=>b.classList.toggle("on", b.dataset.v===v));
  $$(".view").forEach(s=>s.classList.toggle("on", s.id==="v-"+v));
  VIEWS[v]();
  window.scrollTo({top:0,behavior:"instant"});
}
$$("nav button").forEach(b=> b.onclick = ()=> go(b.dataset.v));

/* ============================================================
   DASHBOARD
   ============================================================ */
function renderDash(){
  const st = stats(), dm = byDomain();
  const starred = Object.keys(S.stars).length;
  const missed  = QB.filter(q=>{const r=rec(q.i); return r && !r.ok;}).length;
  const est = scaled(st.acc);
  const ready = st.ans<40 ? "&mdash;" : (est>=720 ? "On track" : "Not yet");
  const readyC = st.ans<40 ? "var(--tx3)" : (est>=720 ? "var(--ok)" : "var(--bad)");

  $("#v-dash").innerHTML = `
  <div class="stats">
    <div class="stat"><div class="n">${QB.length}</div><div class="l">Questions in bank</div></div>
    <div class="stat"><div class="n">${st.ans}</div><div class="l">Answered</div>
      <div class="bar"><i style="width:${(st.ans/Math.max(QB.length,1)*100).toFixed(1)}%"></i></div></div>
    <div class="stat"><div class="n">${st.ans?(st.acc*100).toFixed(1)+"%":"&mdash;"}</div><div class="l">Accuracy</div>
      <div class="bar"><i style="width:${(st.acc*100).toFixed(1)}%;background:${st.acc>=.689?"var(--ok)":"var(--bad)"}"></i></div></div>
    <div class="stat"><div class="n" style="color:${readyC}">${st.ans<40?"&mdash;":est}</div><div class="l">Est. scaled score</div></div>
    <div class="stat"><div class="n" style="color:${readyC};font-size:20px;padding-top:5px">${ready}</div><div class="l">Pass line 720</div></div>
    <div class="stat"><div class="n">${streak()}</div><div class="l">Day streak</div></div>
  </div>

  <div class="card" style="margin-bottom:16px">
    <h3>Performance by exam domain</h3>
    <p class="sub" style="margin-bottom:14px">Bar shows your accuracy. The percentage in brackets is that domain's weight on the real 60-question exam.</p>
    ${Object.keys(DOMAINS).map(d=>{
      const b=dm[d], acc=b.ans?b.ok/b.ans:0;
      return `<div class="dombar">
        <div class="nm">${DOMAINS[d].n} <span style="color:var(--tx3);font-weight:500">(${DOMAINS[d].w}%)</span></div>
        <div class="tr"><i style="width:${(acc*100).toFixed(1)}%;background:${DOMAINS[d].c}"></i></div>
        <div class="vl">${b.ans?(acc*100).toFixed(0)+"%":"&mdash;"} <span style="color:var(--tx3)">${b.ans}/${b.total}</span></div>
      </div>`;
    }).join("")}
  </div>

  <div class="card" style="margin-bottom:16px">
    <h3>Jump straight in</h3>
    <div class="row" style="margin-top:6px">
      <button class="btn" data-jump="unseen">Continue &mdash; new questions</button>
      <button class="btn ghost" data-jump="missed">Redo missed (${missed})</button>
      <button class="btn ghost" data-jump="starred">Bookmarked (${starred})</button>
      <button class="btn ghost" data-jump="weak">Drill my weakest tasks</button>
      <button class="btn ghost" data-jump="cards">Concept flashcards</button>
    </div>
  </div>

  <div class="card">
    <h3>Your data</h3>
    <p class="sub">Progress lives in this browser's localStorage only. Export before clearing browser data or moving machines.</p>
    <div class="row">
      <button class="btn ghost" id="expBtn">Export progress</button>
      <button class="btn ghost" id="impBtn">Import progress</button>
      <button class="btn ghost" id="rstBtn" style="color:var(--bad);border-color:var(--bad)">Reset all progress</button>
      <input type="file" id="impFile" accept="application/json" hidden>
    </div>
  </div>`;

  $$("[data-jump]").forEach(b=> b.onclick = ()=>{
    const j=b.dataset.jump;
    if(j==="cards") return go("cards");
    if(j==="weak")  return go("weak");
    S.filters = {d:"", t:"", s:"", mode:j, shuffle:true}; save();
    go("practice");
  });
  $("#expBtn").onclick = ()=>{
    const blob = new Blob([JSON.stringify(S)],{type:"application/json"});
    const a=document.createElement("a");
    a.href=URL.createObjectURL(blob); a.download="ccarf-progress-"+new Date().toISOString().slice(0,10)+".json"; a.click();
    toast("Progress exported");
  };
  $("#impBtn").onclick = ()=> $("#impFile").click();
  $("#impFile").onchange = e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=()=>{ try{ Object.assign(S, JSON.parse(r.result)); save(); toast("Progress imported"); renderDash(); }
                   catch(x){ toast("Could not read that file"); } };
    r.readAsText(f);
  };
  $("#rstBtn").onclick = ()=>{
    if(confirm("Erase all answers, bookmarks and flashcard scheduling? This cannot be undone.")){
      S={seen:{},stars:{},srs:{},theme:S.theme,days:{},filters:{}}; save(); renderDash(); toast("Progress reset");
    }
  };
}

/* ============================================================
   PRACTICE
   ============================================================ */
let POOL=[], PIDX=0, PICK=null, SHOWN=false;

function buildPool(){
  const f = S.filters||{};
  let p = QB.filter(q =>
      (!f.d || String(q.d)===String(f.d)) &&
      (!f.t || q.t===f.t) &&
      (!f.s || q.s===f.s) &&
      (!f.tasks || f.tasks.includes(q.t)));
  if(f.mode==="unseen")  p = p.filter(q=>!rec(q.i));
  if(f.mode==="missed")  p = p.filter(q=>{const r=rec(q.i); return r && !r.ok;});
  if(f.mode==="starred") p = p.filter(q=>S.stars[q.i]);
  if(f.shuffle){ for(let i=p.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;[p[i],p[j]]=[p[j],p[i]];} }
  return p;
}

function renderPractice(){
  const f = S.filters = Object.assign({d:"",t:"",s:"",mode:"all",shuffle:true}, S.filters);
  const taskOpts = Object.keys(TASKS).filter(t=>!f.d || t.startsWith(f.d+"."));
  $("#v-practice").innerHTML = `
    <div class="card" style="margin-bottom:16px">
      <div class="row" style="align-items:flex-end;gap:12px">
        <label class="fl">Domain<select id="fD">
          <option value="">All domains</option>
          ${Object.keys(DOMAINS).map(d=>`<option value="${d}" ${f.d==d?"selected":""}>${d}. ${DOMAINS[d].n} (${DOMAINS[d].w}%)</option>`).join("")}
        </select></label>
        <label class="fl">Task<select id="fT">
          <option value="">All tasks</option>
          ${taskOpts.map(t=>`<option value="${t}" ${f.t===t?"selected":""}>${t} &mdash; ${TASKS[t]}</option>`).join("")}
        </select></label>
        <label class="fl">Scenario<select id="fS">
          <option value="">All scenarios</option>
          ${Object.keys(SCEN).map(k=>`<option value="${k}" ${f.s===k?"selected":""}>${SCEN[k].n}</option>`).join("")}
        </select></label>
        <label class="fl">Set<select id="fM">
          <option value="all"     ${f.mode==="all"?"selected":""}>Everything</option>
          <option value="unseen"  ${f.mode==="unseen"?"selected":""}>Not yet answered</option>
          <option value="missed"  ${f.mode==="missed"?"selected":""}>Previously missed</option>
          <option value="starred" ${f.mode==="starred"?"selected":""}>Bookmarked</option>
        </select></label>
        <label class="fl">Order<select id="fO">
          <option value="1" ${f.shuffle?"selected":""}>Shuffled</option>
          <option value="0" ${!f.shuffle?"selected":""}>Sequential</option>
        </select></label>
        <button class="btn" id="fGo">Apply</button>
      </div>
    </div>
    <div id="qslot"></div>`;

  $("#fD").onchange = e=>{ f.d=e.target.value; f.t=""; save(); renderPractice(); };
  ["fT","fS","fM","fO"].forEach(id=> $("#"+id).onchange = e=>{
    if(id==="fT") f.t=e.target.value;
    if(id==="fS") f.s=e.target.value;
    if(id==="fM") f.mode=e.target.value;
    if(id==="fO") f.shuffle = e.target.value==="1";
    save();
  });
  $("#fGo").onclick = ()=>{ POOL=buildPool(); PIDX=0; drawQ(); };

  POOL = buildPool(); PIDX = 0; drawQ();
}

function drawQ(){
  const slot=$("#qslot");
  if(!POOL.length){
    slot.innerHTML = `<div class="card empty">No questions match that filter.<br><br>
      <button class="btn ghost" onclick="S.filters={d:'',t:'',s:'',mode:'all',shuffle:true};save();renderPractice()">Reset filters</button></div>`;
    return;
  }
  PIDX = Math.max(0, Math.min(PIDX, POOL.length-1));
  const q = POOL[PIDX];
  PICK=null; SHOWN=false;
  const sc = SCEN[q.s]||SCEN.GEN;
  slot.innerHTML = `
    <div class="card">
      <div class="qhead">
        <span class="qnum">Question ${PIDX+1} of ${POOL.length}</span>
        <span class="pill d${q.d}">D${q.d} &middot; ${DOMAINS[q.d].n}</span>
        <span class="pill">${q.t} ${esc(TASKS[q.t]||"")}</span>
        <span class="pill">${"●".repeat(q.diff||2)}</span>
        <button class="star ${S.stars[q.i]?"on":""}" id="starB" title="Bookmark (S)">${S.stars[q.i]?"★":"☆"}</button>
      </div>
      ${q.s!=="GEN" ? `<div class="scen"><div class="t">Scenario &mdash; ${sc.n}</div><div class="b">${sc.b}</div></div>`:""}
      <div class="stem">${q.q}</div>
      <div class="ask">${q.ask||"Which approach is most effective?"}</div>
      <div class="opts" id="opts">
        ${q.a.map((o,ix)=>`<button class="opt" data-ix="${ix}"><span class="k">${KEYS[ix]}</span><span class="ot">${o}</span></button>`).join("")}
      </div>
      <div id="expslot"></div>
      <div class="qfoot">
        <button class="btn ghost" id="prevB">&larr; Previous</button>
        <button class="btn" id="nextB">Next &rarr;</button>
        <button class="btn ghost" id="revealB">Reveal answer</button>
        <span class="sp" style="font-size:12px;color:var(--tx3)">Keys: <kbd>A</kbd>&ndash;<kbd>D</kbd> answer &middot; <kbd>&rarr;</kbd> next &middot; <kbd>S</kbd> bookmark</span>
      </div>
    </div>`;

  $$("#opts .opt").forEach(b=> b.onclick = ()=> answer(q, +b.dataset.ix));
  $("#prevB").onclick = ()=>{ PIDX--; drawQ(); };
  $("#nextB").onclick = ()=>{ PIDX++; if(PIDX>=POOL.length){PIDX=POOL.length-1; toast("End of this set");} drawQ(); };
  $("#revealB").onclick = ()=> answer(q, -1);
  $("#starB").onclick = ()=>{
    if(S.stars[q.i]) delete S.stars[q.i]; else S.stars[q.i]=1;
    save(); $("#starB").classList.toggle("on",!!S.stars[q.i]);
    $("#starB").textContent = S.stars[q.i]?"★":"☆";
  };
}

function answer(q, ix){
  if(SHOWN) return;
  SHOWN=true; PICK=ix;
  const ok = ix===q.c;
  if(ix>=0){
    const r = S.seen[q.i] || {n:0};
    S.seen[q.i] = {a:ix, ok:ok, n:r.n+1};
    markDay(); save();
  }
  $$("#opts .opt").forEach(b=>{
    const i=+b.dataset.ix;
    b.classList.add("locked");
    if(i===q.c) b.classList.add("correct");
    else if(i===ix) b.classList.add("wrong");
    if(q.w && q.w[i]) b.querySelector(".ot").insertAdjacentHTML("beforeend",
      `<span class="why"><strong>${i===q.c?"Correct:":"Why not "+KEYS[i]+":"}</strong> ${q.w[i]}</span>`);
  });
  $("#expslot").innerHTML = `
    <div class="exp ${ix<0?"":(ok?"good":"bad")}">
      <div class="hd">${ix<0?"Answer &mdash; "+KEYS[q.c]:(ok?"Correct &mdash; "+KEYS[q.c]:"Incorrect &mdash; the answer is "+KEYS[q.c])}</div>
      <div class="bd">
        <p>${q.e}</p>
        ${q.k?`<div class="anchor"><div class="t">Concept to lock in</div><div class="b">${q.k}</div></div>`:""}
        ${q.n?`<div class="anchor docnote"><div class="t">Documentation check</div><div class="b">${q.n}</div></div>`:""}
      </div>
    </div>`;
  $("#revealB").disabled = true;
}

document.addEventListener("keydown", e=>{
  if(!$("#v-practice").classList.contains("on")) return;
  if(/input|select|textarea/i.test(e.target.tagName)) return;
  const q = POOL[PIDX]; if(!q) return;
  const k = e.key.toUpperCase();
  if(!SHOWN && KEYS.indexOf(k)>-1 && KEYS.indexOf(k)<q.a.length){ answer(q, KEYS.indexOf(k)); e.preventDefault(); }
  else if(!SHOWN && /^[1-4]$/.test(k)){ answer(q, +k-1); e.preventDefault(); }
  else if(e.key==="ArrowRight"||e.key==="Enter"){ $("#nextB")&&$("#nextB").click(); e.preventDefault(); }
  else if(e.key==="ArrowLeft"){ $("#prevB")&&$("#prevB").click(); e.preventDefault(); }
  else if(k==="S"){ $("#starB")&&$("#starB").click(); }
});

/* ============================================================
   WEAK AREAS
   ============================================================ */
function renderWeak(){
  const t = byTask();
  const rows = Object.keys(t).map(k=>({k, ...t[k], acc: t[k].ans? t[k].ok/t[k].ans : null}))
                .sort((a,b)=>{
                  if(a.acc===null && b.acc===null) return a.k.localeCompare(b.k);
                  if(a.acc===null) return 1; if(b.acc===null) return -1;
                  return a.acc-b.acc;
                });
  const weakKeys = rows.filter(r=>r.acc!==null && r.acc<0.7 && r.ans>=3).map(r=>r.k);
  $("#v-weak").innerHTML = `
    <h2>Weak areas</h2>
    <p class="sub">Accuracy per blueprint task statement, worst first. A task is flagged weak below 70% (the pass line sits at roughly 69% raw). Tasks you have not attempted at least 3 times are not yet judged.</p>
    <div class="card" style="margin-bottom:16px">
      <div class="row">
        <button class="btn" id="drillB" ${weakKeys.length?"":"disabled"}>Drill ${weakKeys.length} weak task${weakKeys.length===1?"":"s"}</button>
        <button class="btn ghost" id="drillMissed">Redo every missed question</button>
      </div>
    </div>
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Task</th><th>Domain</th><th style="text-align:right">Answered</th><th style="text-align:right">Accuracy</th><th></th></tr></thead>
        <tbody>${rows.map(r=>{
          const col = r.acc===null?"var(--tx3)":(r.acc>=.8?"var(--ok)":r.acc>=.7?"var(--warn)":"var(--bad)");
          return `<tr>
            <td><strong>${r.k}</strong> &nbsp;${esc(TASKS[r.k]||"")}</td>
            <td><span class="pill d${r.d}">D${r.d}</span></td>
            <td style="text-align:right;color:var(--tx2)">${r.ans}/${r.total}</td>
            <td class="acc" style="text-align:right;color:${col}">${r.acc===null?"&mdash;":(r.acc*100).toFixed(0)+"%"}</td>
            <td style="text-align:right"><button class="btn ghost" style="padding:5px 10px;font-size:12px" data-dt="${r.k}">Practice</button></td>
          </tr>`;}).join("")}</tbody>
      </table>
    </div>`;
  $("#drillB").onclick = ()=>{ S.filters={d:"",t:"",s:"",mode:"all",shuffle:true,tasks:weakKeys}; save(); go("practice"); };
  $("#drillMissed").onclick = ()=>{ S.filters={d:"",t:"",s:"",mode:"missed",shuffle:true}; save(); go("practice"); };
  $$("[data-dt]").forEach(b=> b.onclick = ()=>{
    S.filters={d:"",t:b.dataset.dt,s:"",mode:"all",shuffle:true}; save(); go("practice"); });
}

/* ============================================================
   FLASHCARDS  (Leitner boxes 0-4)
   ============================================================ */
let FDECK=[], FIDX=0, FFLIP=false;
const IVL=[0,1,3,7,21];

function dueCards(){
  const now=Date.now();
  return CARDS.filter(c=>{ const r=S.srs[c.i]; return !r || r.due<=now; });
}
function renderCards(){
  const due = dueCards();
  const boxes=[0,0,0,0,0];
  CARDS.forEach(c=>{ const r=S.srs[c.i]; boxes[r?r.box:0]++; });
  $("#v-cards").innerHTML = `
    <h2>Concept flashcards</h2>
    <p class="sub">The decision rules, comparisons and hard facts behind the questions. Cards you rate poorly come back sooner (Leitner intervals: 1, 3, 7, 21 days).</p>
    <div class="stats">
      <div class="stat"><div class="n">${CARDS.length}</div><div class="l">Cards</div></div>
      <div class="stat"><div class="n" style="color:var(--acc)">${due.length}</div><div class="l">Due now</div></div>
      <div class="stat"><div class="n" style="color:var(--ok)">${boxes[4]}</div><div class="l">Mastered</div></div>
      <div class="stat"><div class="n">${boxes[0]}</div><div class="l">New / relearning</div></div>
    </div>
    <div class="row" style="margin-bottom:14px">
      <label class="fl" style="flex-direction:row;align-items:center;gap:8px">Filter
        <select id="cD"><option value="">All domains</option>
        ${Object.keys(DOMAINS).map(d=>`<option value="${d}">${d}. ${DOMAINS[d].n}</option>`).join("")}</select></label>
      <button class="btn" id="cStart">Study due cards</button>
      <button class="btn ghost" id="cAll">Study all (shuffled)</button>
    </div>
    <div id="cslot"></div>`;
  $("#cStart").onclick = ()=>{ FDECK = filterC(dueCards()); shuf(FDECK); FIDX=0; drawC(); };
  $("#cAll").onclick   = ()=>{ FDECK = filterC(CARDS.slice()); shuf(FDECK); FIDX=0; drawC(); };
  function filterC(l){ const d=$("#cD").value; return d? l.filter(c=>String(c.d)===d) : l; }
  FDECK = filterC(due); shuf(FDECK); FIDX=0; drawC();
}
function shuf(a){ for(let i=a.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;[a[i],a[j]]=[a[j],a[i]];} }
function drawC(){
  const slot=$("#cslot");
  if(!FDECK.length){ slot.innerHTML=`<div class="card empty">Nothing due. Use <em>Study all</em> to review ahead.</div>`; return; }
  if(FIDX>=FDECK.length){ slot.innerHTML=`<div class="card empty">Deck finished. ${FDECK.length} cards reviewed.</div>`; renderCardsStats(); return; }
  const c=FDECK[FIDX]; FFLIP=false;
  slot.innerHTML=`
    <div class="card fcard" id="fc">
      <div style="position:absolute;top:12px;left:16px" class="pill d${c.d}">D${c.d} &middot; ${c.t||""}</div>
      <div style="position:absolute;top:12px;right:16px;font-size:11px;color:var(--tx3)">${FIDX+1} / ${FDECK.length}</div>
      <div class="q">${c.q}</div>
      <div class="a" id="fa" hidden>${c.a}</div>
      <div class="hint" id="fh">Click, or press Space, to reveal</div>
    </div>
    <div class="srs" id="srsbtns" hidden>
      <button data-g="0">Again<br><span style="font-weight:400;font-size:11px;color:var(--tx3)">&lt;1 day</span></button>
      <button data-g="1">Hard<br><span style="font-weight:400;font-size:11px;color:var(--tx3)">1 day</span></button>
      <button data-g="2">Good<br><span style="font-weight:400;font-size:11px;color:var(--tx3)">step up</span></button>
      <button data-g="3">Easy<br><span style="font-weight:400;font-size:11px;color:var(--tx3)">21 days</span></button>
    </div>`;
  $("#fc").onclick = flip;
  $$("#srsbtns button").forEach(b=> b.onclick = ()=> grade(c, +b.dataset.g));
}
function flip(){
  if(FFLIP) return; FFLIP=true;
  $("#fa").hidden=false; $("#fh").hidden=true; $("#srsbtns").hidden=false;
}
function grade(c,g){
  const r=S.srs[c.i]||{box:0};
  let box = g===0?0 : g===1?Math.max(1,r.box) : g===2?Math.min(4,r.box+1) : 4;
  S.srs[c.i]={box, due: Date.now() + IVL[box]*864e5};
  markDay(); save(); FIDX++; drawC();
}
function renderCardsStats(){}
document.addEventListener("keydown", e=>{
  if(!$("#v-cards").classList.contains("on")) return;
  if(/input|select/i.test(e.target.tagName)) return;
  if(e.code==="Space"){ e.preventDefault(); if(!FFLIP) flip(); }
  else if(FFLIP && /^[1-4]$/.test(e.key)){ const b=$(`#srsbtns button[data-g="${+e.key-1}"]`); b&&b.click(); }
});

/* ============================================================
   SEARCH
   ============================================================ */
function renderSearch(){
  $("#v-search").innerHTML=`
    <h2>Search the bank</h2>
    <p class="sub">Full-text across every stem, option, explanation and concept anchor. Useful for chasing a single idea &mdash; try <code>tool_choice</code>, <code>fork_session</code>, <code>isRetryable</code>, <code>lost in the middle</code>.</p>
    <div class="card" style="margin-bottom:16px">
      <input type="search" id="sq" placeholder="Search 1,500+ questions and explanations&hellip;" style="width:100%;padding:12px 14px;font-size:15px">
      <div style="margin-top:8px;font-size:12px;color:var(--tx3)" id="scount"></div>
    </div>
    <div id="sres"></div>`;
  const inp=$("#sq"); inp.focus();
  inp.oninput = ()=>{
    const t=inp.value.trim();
    if(t.length<2){ $("#sres").innerHTML=""; $("#scount").textContent=""; return; }
    const rx = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"i");
    const hits = QB.filter(q=> rx.test(q.q)||rx.test(q.e)||rx.test(q.k||"")||q.a.some(o=>rx.test(o))).slice(0,120);
    $("#scount").textContent = `${hits.length}${hits.length===120?"+":""} match${hits.length===1?"":"es"}`;
    $("#sres").innerHTML = hits.map(q=>`
      <div class="searchhit" data-qi="${q.i}">
        <div style="margin-bottom:6px"><span class="pill d${q.d}">D${q.d}</span> <span class="pill">${q.t}</span></div>
        <div class="s">${q.q.replace(/<[^>]+>/g,"").slice(0,240).replace(rx,m=>"<mark>"+m+"</mark>")}&hellip;</div>
      </div>`).join("");
    $$("[data-qi]").forEach(el=> el.onclick = ()=>{
      const q = QB.find(x=>x.i===+el.dataset.qi);
      POOL=[q]; PIDX=0; go("practice"); setTimeout(()=>{ POOL=[q]; PIDX=0; drawQ(); },0);
    });
  };
}

/* ============================================================
   BLUEPRINT REFERENCE
   ============================================================ */
function renderRef(){
  $("#v-ref").innerHTML=`
  <h2>Exam blueprint &amp; scenario pool</h2>
  <p class="sub">What the CCAR-F actually tests, and how this bank maps onto it.</p>
  <div class="card reftbl" style="margin-bottom:16px">
    <h3>Format</h3>
    <table class="tbl">
      <tr><td><strong>Exam code</strong></td><td>CCAR-F &mdash; Claude Certified Architect, Foundations</td></tr>
      <tr><td><strong>Questions</strong></td><td>60, single-answer multiple choice (1 correct of 4)</td></tr>
      <tr><td><strong>Time</strong></td><td>120 minutes (2 minutes per question)</td></tr>
      <tr><td><strong>Scoring</strong></td><td>Scaled 100&ndash;1000; <strong>pass at 720</strong>; no penalty for guessing &mdash; answer everything</td></tr>
      <tr><td><strong>Scenarios</strong></td><td>4 drawn at random from a pool of 8; questions hang off those scenarios</td></tr>
      <tr><td><strong>Delivery</strong></td><td>Pearson VUE, online-proctored or test centre</td></tr>
      <tr><td><strong>Validity</strong></td><td>12 months</td></tr>
    </table>
    <h4>Domain weights</h4>
    <table class="tbl">
      ${Object.keys(DOMAINS).map(d=>`<tr><td><span class="pill d${d}">D${d}</span> ${DOMAINS[d].n}</td>
        <td style="text-align:right"><strong>${DOMAINS[d].w}%</strong></td>
        <td style="text-align:right;color:var(--tx2)">&asymp;${Math.round(DOMAINS[d].w*0.6)} questions</td></tr>`).join("")}
    </table>
  </div>
  <div class="card reftbl" style="margin-bottom:16px">
    <h3>Task statements</h3>
    ${Object.keys(DOMAINS).map(d=>`<h4>Domain ${d} &mdash; ${DOMAINS[d].n} (${DOMAINS[d].w}%)</h4>
      <ul>${Object.keys(TASKS).filter(t=>t.startsWith(d+".")).map(t=>`<li><strong>${t}</strong> ${esc(TASKS[t])}</li>`).join("")}</ul>`).join("")}
  </div>
  <div class="card reftbl">
    <h3>Scenario pool</h3>
    ${Object.keys(SCEN).filter(k=>k!=="GEN").map(k=>`<h4>${SCEN[k].n}</h4><p style="font-size:13.5px;color:var(--tx2);line-height:1.7">${SCEN[k].b}</p>`).join("")}
  </div>`;
}

/* ---------- boot ---------- */
QB.forEach((q,ix)=>{ if(q.i==null) q.i=ix+1; });
renderDash();
