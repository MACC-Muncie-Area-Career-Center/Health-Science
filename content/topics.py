# Shared "Topic" filter bar (Chapter / Body region / Program) for MedDecode Tiles and Build.
import json, sys
sys.path.insert(0,'/home/claude/shared')
from master import CHAPTERS, REGIONS, PROGRAMS, BOOK

CSS = """
/* Topic filter (chapter, body region, program) */
.topics{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:12px 0 0;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
.topics .tlabel{font:700 12px var(--font-body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.topics label{display:flex;align-items:center;gap:6px;font:600 14px var(--font-body);color:var(--ink);min-width:0}
.topics select{font:500 14px var(--font-body);color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 8px;max-width:100%;min-width:0}
.topics .tnote{font-size:13px;color:var(--muted);flex-basis:100%}
.topics .tbtn{font:600 13px var(--font-body);border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;padding:5px 12px;cursor:pointer}
.topics label.tch select{max-width:min(420px,70vw)}
@media (max-width:560px){ .topics label{flex:1 1 100%} .topics select{flex:1} }
body.mdc-classroom .topics label,body.mdc-classroom .topics select{font-size:18px}
"""

HTML = """
  <div class="topics" id="topics" role="group" aria-label="Topic">
    <span class="tlabel">Topic</span>
    <label class="tch">Chapter <select id="t-ch"></select></label>
    <label>Body region <select id="t-reg"></select></label>
    <label>Program <select id="t-prog"></select></label>
    <button type="button" class="tbtn" id="t-clear">All topics</button>
    <button type="button" class="tbtn" id="t-link">Copy student link</button>
    <span class="tnote" id="t-note"></span>
  </div>
"""

JS = """
/* ---------- Topic filter: chapter (Acquiring Medical Language), body region, CTE program ---------- */
const MDT = (function(){
  const CH = %s, REG = %s, PROG = %s, BOOK = %s;
  const st = {ch:'', reg:'', prog:''};
  try { const q = new URLSearchParams(location.search);
    if (CH[q.get('ch')]) st.ch = q.get('ch');
    if (REG.includes(q.get('region'))) st.reg = q.get('region');
    if (PROG.includes(q.get('program'))) st.prog = q.get('program'); } catch(e){}
  let onChange = ()=>{};
  const $t = id => document.getElementById(id);
  function match(it){
    return (!st.ch || (it.ch||[]).includes(+st.ch)) && (!st.reg || (it.reg||[]).includes(st.reg)) && (!st.prog || (it.prog||[]).includes(st.prog));
  }
  function active(){ return !!(st.ch || st.reg || st.prog); }
  function label(){
    const a = [];
    if (st.ch) a.push('Chapter '+st.ch+': '+CH[st.ch]);
    if (st.reg) a.push(st.reg);
    if (st.prog) a.push(st.prog);
    return a.join(' · ');
  }
  function link(){
    const p = new URLSearchParams();
    if (st.ch) p.set('ch', st.ch); if (st.reg) p.set('region', st.reg); if (st.prog) p.set('program', st.prog);
    return location.origin + location.pathname + (p.toString() ? '?'+p : '');
  }
  function sync(){ $t('t-ch').value = st.ch; $t('t-reg').value = st.reg; $t('t-prog').value = st.prog; $t('t-clear').hidden = !active(); }
  function note(t){ $t('t-note').textContent = t; }
  function mount(cb){
    onChange = cb;
    $t('t-ch').innerHTML = '<option value="">All chapters</option>' + Object.entries(CH).map(([n,t])=>`<option value="${n}">Ch ${n} · ${t}</option>`).join('');
    $t('t-reg').innerHTML = '<option value="">All regions</option>' + REG.map(r=>`<option>${r}</option>`).join('');
    $t('t-prog').innerHTML = '<option value="">All programs</option>' + PROG.map(r=>`<option>${r}</option>`).join('');
    $t('t-ch').title = 'Chapters follow ' + BOOK;
    $t('t-ch').addEventListener('change', e=>{ st.ch = e.target.value; sync(); onChange(); });
    $t('t-reg').addEventListener('change', e=>{ st.reg = e.target.value; sync(); onChange(); });
    $t('t-prog').addEventListener('change', e=>{ st.prog = e.target.value; sync(); onChange(); });
    $t('t-clear').addEventListener('click', ()=>{ st.ch = st.reg = st.prog = ''; sync(); onChange(); });
    $t('t-link').addEventListener('click', ()=>{
      const url = link(), b = $t('t-link');
      const done = ok=>{ b.textContent = ok ? 'Link copied' : 'Copy failed'; setTimeout(()=>b.textContent='Copy student link', 1600); };
      try { navigator.clipboard.writeText(url).then(()=>done(true), ()=>{ note('Student link: '+url); }); } catch(e){ note('Student link: '+url); }
    });
    sync();
  }
  return {st, match, active, label, mount, note};
})();
""" % (json.dumps({str(k):v for k,v in CHAPTERS.items()}), json.dumps(REGIONS), json.dumps(PROGRAMS), json.dumps(BOOK))
