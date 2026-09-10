#!/usr/bin/env python3
"""
Inject the "10 Things to Know" rail into an existing exam bank HTML file.

    python build/tenthings/inject.py <bank.html> <content.json> [--key NAME]

The three older banks (Associate, Architect Foundations, Developer) were each built by
a different pipeline and each has a different layout: one is a flex column with its own
filter sidebar, one is a plain block `main`, one is a CSS grid. Rather than restructure
three working apps, the rail is injected as a **fixed-position panel** that owns no
space in the host layout, plus one rule that pads `body` while it is open.

Everything is namespaced under `#tt10` / `.tt10-*`, and the panel reads its colours from
the host page at runtime, so it follows whatever theme the bank is already in.

Idempotent: re-running replaces the previous injection rather than stacking.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

START = "<!--TT10:START-->"
END = "<!--TT10:END-->"

CSS = """
#tt10,#tt10 *{box-sizing:border-box}
#tt10{
  position:fixed;left:0;top:0;bottom:0;width:340px;z-index:99000;
  display:flex;flex-direction:column;
  background:var(--tt10-bg,#161a21);color:var(--tt10-fg,#e7eaf0);
  border-right:1px solid var(--tt10-bd,#2b3240);
  font:14px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  transform:translateX(-100%);transition:transform .18s ease;
  box-shadow:0 0 40px rgba(0,0,0,.28);
}
html[data-tt10="open"] #tt10{transform:none}
html[data-tt10="open"] body{padding-left:340px}
#tt10-scrim{
  position:fixed;inset:0;z-index:98999;background:rgba(0,0,0,.45);
  opacity:0;pointer-events:none;transition:opacity .18s ease;
}
#tt10-hd{padding:14px 15px 12px;border-bottom:1px solid var(--tt10-bd,#2b3240);flex:none}
#tt10-hd h2{
  margin:0;font-size:12.5px;letter-spacing:.6px;text-transform:uppercase;
  color:var(--tt10-acc,#d97757);font-weight:700;
}
#tt10-hd p{margin:3px 0 0;font-size:11.5px;opacity:.62}
#tt10-pick{
  width:100%;margin-top:11px;padding:7px 9px;border-radius:7px;font:inherit;font-size:12.5px;
  background:var(--tt10-bg2,rgba(127,127,127,.14));color:inherit;
  border:1px solid var(--tt10-bd,#2b3240);
}
#tt10-body{overflow-y:auto;padding:9px;flex:1}
.tt10-c{
  border:1px solid var(--tt10-bd,#2b3240);border-radius:9px;margin-bottom:7px;
  background:var(--tt10-bg2,rgba(127,127,127,.09));overflow:hidden;
}
.tt10-c>button{
  width:100%;display:flex;gap:9px;align-items:flex-start;padding:10px 11px;text-align:left;
  background:none;border:0;cursor:pointer;color:inherit;font:inherit;
}
.tt10-c>button:hover{background:rgba(127,127,127,.12)}
.tt10-n{
  flex:none;width:19px;height:19px;border-radius:5px;margin-top:1px;
  background:var(--tt10-accbg,rgba(217,119,87,.16));color:var(--tt10-acc,#d97757);
  font-size:11px;font-weight:700;display:grid;place-items:center;
}
.tt10-t{font-size:13px;font-weight:600;line-height:1.4}
.tt10-c.on .tt10-t{color:var(--tt10-acc,#d97757)}
.tt10-b{padding:0 11px 11px 39px;font-size:12.5px;line-height:1.62;opacity:.86;display:none}
.tt10-c.on .tt10-b{display:block}
.tt10-note{
  margin-top:9px;padding:8px 10px;border-left:2px solid var(--tt10-acc,#d97757);
  background:var(--tt10-accbg,rgba(217,119,87,.13));border-radius:0 6px 6px 0;
  font-size:12px;opacity:1;
}
.tt10-note b{
  display:block;margin-bottom:2px;font-size:10.5px;letter-spacing:.5px;
  text-transform:uppercase;color:var(--tt10-acc,#d97757);
}
#tt10-btn{
  cursor:pointer;font:inherit;font-size:12.5px;padding:6px 11px;border-radius:8px;
  background:var(--tt10-bg2,rgba(127,127,127,.14));color:inherit;
  border:1px solid var(--tt10-bd,#2b3240);
}
#tt10-btn:hover{border-color:var(--tt10-acc,#d97757)}
#tt10-btn.tt10-float{position:fixed;left:12px;bottom:12px;z-index:98000}
#tt10-x{
  position:absolute;right:9px;top:11px;cursor:pointer;border:0;background:none;
  color:inherit;opacity:.5;font-size:19px;line-height:1;padding:2px 6px;
}
#tt10-x:hover{opacity:1}
@media(max-width:1100px){
  html[data-tt10="open"] body{padding-left:0}
  html[data-tt10="open"] #tt10-scrim{opacity:1;pointer-events:auto}
}
@media print{#tt10,#tt10-scrim,#tt10-btn{display:none}}
"""

JS = r"""
(function(){
  var DATA = __TT10_DATA__, KEY = __TT10_KEY__;
  if(!DATA || !Object.keys(DATA).length) return;
  var H = document.documentElement, sections = Object.keys(DATA);

  var rail = document.createElement('aside');
  rail.id = 'tt10';
  rail.innerHTML =
    '<div id="tt10-hd">'
  +   '<button id="tt10-x" title="Close" aria-label="Close">&times;</button>'
  +   '<h2>10 Things to Know</h2>'
  +   '<p>Key concepts, what they mean, and how they are tested.</p>'
  +   '<select id="tt10-pick"></select>'
  + '</div><div id="tt10-body"></div>';
  var scrim = document.createElement('div');
  scrim.id = 'tt10-scrim';
  document.body.appendChild(scrim);
  document.body.appendChild(rail);

  var pick = rail.querySelector('#tt10-pick');
  var body = rail.querySelector('#tt10-body');
  pick.innerHTML = sections.map(function(s){
    return '<option value="'+esc(s)+'">'+esc(s)+'</option>'; }).join('');

  function esc(s){ return String(s==null?'':s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function md(s){
    var code=[], t=esc(s);
    t=t.replace(/`([^`]+)`/g,function(m,c){code.push(c);return '\u0001'+(code.length-1)+'\u0001';});
    t=t.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
    t=t.replace(/\u0001(\d+)\u0001/g,function(m,i){return '<code>'+code[+i]+'</code>';});
    return t.replace(/\n/g,'<br>');
  }
  function draw(){
    var list = DATA[pick.value] || [];
    body.innerHTML = list.map(function(c,i){
      return '<div class="tt10-c"><button type="button"><span class="tt10-n">'+(i+1)+'</span>'
        +'<span class="tt10-t">'+esc(c.title)+'</span></button>'
        +'<div class="tt10-b">'+md(c.desc)
        +(c.note?'<div class="tt10-note"><b>Note</b>'+md(c.note)+'</div>':'')
        +'</div></div>';
    }).join('');
    body.scrollTop = 0;
  }
  body.addEventListener('click', function(e){
    var c = e.target.closest ? e.target.closest('.tt10-c') : null;
    if(c) c.classList.toggle('on');
  });
  pick.addEventListener('change', function(){ draw(); save(); });

  function open(v){
    H.setAttribute('data-tt10', v ? 'open' : 'shut');
    if(btn) btn.setAttribute('aria-expanded', v ? 'true' : 'false');
    save();
  }
  function save(){
    try{ localStorage.setItem(KEY, JSON.stringify(
      {open: H.getAttribute('data-tt10')==='open', sec: pick.value})); }catch(e){}
  }

  // The rail borrows the host page's own colours, so it follows whatever theme the
  // bank is in without needing to know how that bank implements theming.
  function paint(){
    var cs = getComputedStyle(document.body), s = rail.style;
    s.setProperty('--tt10-bg', cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)'
      ? cs.backgroundColor : (getComputedStyle(H).backgroundColor || '#161a21'));
    s.setProperty('--tt10-fg', cs.color || '#e7eaf0');
    var dark = luma(s.getPropertyValue('--tt10-bg')) < 128;
    s.setProperty('--tt10-bd', dark ? 'rgba(255,255,255,.14)' : 'rgba(0,0,0,.14)');
    s.setProperty('--tt10-bg2', dark ? 'rgba(255,255,255,.05)' : 'rgba(0,0,0,.04)');
    s.setProperty('--tt10-acc', dark ? '#e08d70' : '#b8542f');
    s.setProperty('--tt10-accbg', dark ? 'rgba(224,141,112,.15)' : 'rgba(184,84,47,.10)');
  }
  function luma(c){
    var m = /(\d+)[,\s]+(\d+)[,\s]+(\d+)/.exec(c||''); if(!m) return 0;
    return 0.299*+m[1] + 0.587*+m[2] + 0.114*+m[3];
  }

  // Put the toggle in the host header if there is one; otherwise float it.
  var btn = document.createElement('button');
  btn.id = 'tt10-btn'; btn.type = 'button';
  btn.setAttribute('aria-controls','tt10');
  btn.innerHTML = '&#9776; 10 Things';
  var host = document.querySelector('header nav') || document.querySelector('header')
          || document.querySelector('#app > header');
  if(host) host.appendChild(btn); else { btn.classList.add('tt10-float'); document.body.appendChild(btn); }
  btn.addEventListener('click', function(){ open(H.getAttribute('data-tt10')!=='open'); });
  rail.querySelector('#tt10-x').addEventListener('click', function(){ open(false); });
  scrim.addEventListener('click', function(){ open(false); });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && H.getAttribute('data-tt10')==='open') open(false);
  });

  var saved = {};
  try{ saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }catch(e){}
  if(saved.sec && DATA[saved.sec]) pick.value = saved.sec;
  draw();
  paint();
  new MutationObserver(paint).observe(H, {attributes:true, attributeFilter:['class','data-theme','style']});
  new MutationObserver(paint).observe(document.body, {attributes:true, attributeFilter:['class','data-theme','style']});
  open(saved.open !== undefined ? !!saved.open : window.innerWidth >= 1400);
})();
"""


def strip_previous(html: str) -> str:
    return re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)


def main() -> int:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    target, content = Path(sys.argv[1]), Path(sys.argv[2])
    storage_key = "tt10." + (sys.argv[sys.argv.index("--key") + 1]
                             if "--key" in sys.argv else target.stem.replace(" ", "_"))

    if not target.exists():
        sys.exit(f"!! no such bank: {target}")
    if not content.exists():
        sys.exit(f"!! no such content file: {content}")

    data = json.loads(content.read_text(encoding="utf-8-sig"))
    bad = {k: len(v) for k, v in data.items() if not isinstance(v, list) or len(v) != 10}
    if bad:
        sys.exit(f"!! every section must hold exactly 10 concepts; got {bad}")
    for sec, items in data.items():
        for i, c in enumerate(items):
            for f in ("title", "desc", "note"):
                if not str(c.get(f, "")).strip():
                    sys.exit(f"!! {sec}[{i}] is missing '{f}'")

    html = strip_previous(target.read_text(encoding="utf-8"))
    if "</body>" not in html:
        sys.exit("!! target has no </body> to inject before")

    payload = (json.dumps(data, ensure_ascii=False, separators=(",", ":"))
               .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    js = JS.replace("__TT10_DATA__", payload).replace("__TT10_KEY__", json.dumps(storage_key))
    block = f"{START}\n<style>{CSS}</style>\n<script>{js}</script>\n{END}\n"

    html = html.replace("</body>", block + "</body>", 1)
    target.write_text(html, encoding="utf-8")

    n = sum(len(v) for v in data.values())
    print(f"-> {target.name}")
    print(f"   {len(data)} sections, {n} concepts, storage key {storage_key!r}")
    print(f"   {target.stat().st_size/1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
