# Builds the MedDecode Word List page from the master list.
import json, sys
sys.path.insert(0,'/home/claude/shared')
import master as M
from topics import CSS as TCSS, HTML as THTML, JS as TJS

TYPE = {'prefix':'prefix','root':'root','suffix':'suffix'}
terms=[]
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    tg=M.term_tags(t)
    bd=[]
    for l,pid in parts:
        if pid=='cv': bd.append([l,'cv','',''])
        else:
            f,typ,m,*_ = M.PARTS[pid]; bd.append([l,typ,f,m])
    terms.append({'w':w,'d':d,'say':say,'k':kind,'lvl':lvl,'bd':bd,'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],
                  'src':'book' if w in getattr(M,'GLOSSARY_CH12',set()) else '', 'syn':[x for x in getattr(M,'SYN_OF',{}).get(w,[]) if x!=w]})
parts=[]
for pid,(f,typ,m,say,sysn,tile,ck) in M.PARTS.items():
    if m in ('noun ending',): continue
    tg=M.part_tags(pid)
    used=[t[0] for t in M.TERMS if any(p==pid for _,p in t[1])]
    parts.append({'w':f,'d':m,'say':say,'k':typ,'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'ex':used[:8],'n':len(used)})
phr=[{'w':p['t'],'d':p['d'],'say':p['say'] or '','k':'phrase','ch':p['ch'],'reg':['Abdomen and pelvis'],'prog':['EMT','CNA','CCMA'],'src':'book'} for p in M.PHRASES]
DATA={'terms':sorted(terms,key=lambda x:x['w']),'parts':sorted(parts,key=lambda x:x['w'].strip('-').lower()),'phrases':sorted(phr,key=lambda x:x['w'])}

HTML = r'''<title>MedDecode Word List</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
/* Layout: a reference book page. Search and topic filters on top, tabs for terms / word parts / phrases, then one entry per row:
   the term, its pronunciation, its word parts as colored chips, the meaning, and its chapter and program tags. Same tokens as the MedDecode games. */
:root{
  --bg:#e9eeec; --surface:#f7f9f8; --ink:#16262b; --muted:#5b6d70; --line:#cdd7d5; --chip:#e1e8e6;
  --accent:#0f7a73; --accent-ink:#ffffff; --focus:#e08a00;
  --prefix:#6a4bb3; --root:#0f7a73; --suffix:#b4531f; --cv:#6c7b7d;
  --font-display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --font-body:"Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --font-mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54; --cv:#9aaeac; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54; --cv:#9aaeac; color-scheme:dark }
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:15px;line-height:1.45}
.wrap{max-width:1020px;margin:0 auto;padding-inline:16px;padding-block:18px 56px;display:grid;gap:14px}
.wrap > *{min-width:0}
header.top{display:grid;gap:6px}
.brand h1{font-family:var(--font-display);font-weight:800;font-size:clamp(28px,4vw,40px);letter-spacing:-.02em;margin:0;line-height:1;text-wrap:balance}
.brand h1 span{color:var(--accent)}
.brand p{margin:4px 0 0;color:var(--muted);max-width:68ch}
.searchrow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.search{flex:1 1 280px;min-width:0;display:flex;align-items:center;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:4px 6px 4px 12px}
.search input{flex:1;min-width:0;border:0;background:transparent;color:var(--ink);font:500 17px var(--font-body);padding:8px 0;outline:none}
.search:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}
.search svg{flex:none;color:var(--muted)}
.clearx{border:0;background:transparent;color:var(--muted);font:700 18px var(--font-body);cursor:pointer;padding:4px 8px;border-radius:8px}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--surface)}
.seg button{border:0;background:transparent;color:var(--ink);font:600 14px var(--font-body);padding:7px 13px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.seg button .n{font:600 11px var(--font-mono);opacity:.7;margin-left:4px;font-variant-numeric:tabular-nums}
select.sortsel{font:500 14px var(--font-body);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:8px 12px}
button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.status{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;justify-content:space-between;font-size:14px;color:var(--muted)}
.status b{color:var(--ink);font-variant-numeric:tabular-nums}
.legend{display:flex;flex-wrap:wrap;gap:10px;font-size:12.5px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.letters{display:flex;flex-wrap:wrap;gap:2px}
.letters a{font:600 13px var(--font-mono);color:var(--accent);text-decoration:none;padding:2px 6px;border-radius:6px}
.letters a:hover{background:var(--chip)}
.letters span{font:600 13px var(--font-mono);color:var(--line);padding:2px 6px}
.list{display:grid;gap:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.lh{font:800 18px var(--font-display);color:var(--accent);padding:10px 16px 4px;background:var(--bg);border-top:1px solid var(--line)}
.lh:first-child{border-top:0}
.entry{display:grid;grid-template-columns:minmax(0,15rem) minmax(0,1fr);gap:4px 20px;padding:12px 16px;border-top:1px solid var(--line)}
.lh + .entry{border-top:0}
@media (max-width:640px){.entry{grid-template-columns:minmax(0,1fr)}}
.head{display:grid;gap:3px;align-content:start;min-width:0}
.word{font:700 19px/1.15 var(--font-display);overflow-wrap:anywhere}
.word mark{background:color-mix(in srgb,var(--focus) 35%,transparent);color:inherit;border-radius:3px}
.sayrow{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.say{font:13px var(--font-mono);color:var(--muted)}
.hear{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:999px;padding:1px 9px;font:600 12px var(--font-body);cursor:pointer}
.body{display:grid;gap:6px;min-width:0}
.parts{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.p{display:inline-flex;align-items:baseline;gap:5px;font-size:13px;border-radius:7px;padding:2px 8px;background:var(--chip);border-left:4px solid var(--pc)}
.p b{font:600 13.5px var(--font-mono);color:var(--pc)}
.p.cv{--pc:var(--cv);padding:2px 6px}
.p.cv b{color:var(--muted)}
.p[data-t="prefix"]{--pc:var(--prefix)} .p[data-t="root"]{--pc:var(--root)} .p[data-t="suffix"]{--pc:var(--suffix)}
.plus{color:var(--muted);font-size:12px}
.def{font-size:15.5px;max-width:68ch}
.meta{display:flex;flex-wrap:wrap;gap:4px 6px;font-size:12px}
.tag{border:1px solid var(--line);border-radius:999px;padding:1px 8px;color:var(--muted);white-space:nowrap}
.tag.kind{color:var(--ink);font-weight:700}
.tag.book{border-style:dashed}
.ex{font-size:13px;color:var(--muted)}
.ex button{border:0;background:none;padding:0;color:var(--accent);font:inherit;cursor:pointer;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px}
.syn{font-size:13px;color:var(--muted)}
.empty{padding:28px 16px;text-align:center;color:var(--muted)}
.more{display:flex;justify-content:center;padding:12px}
.btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 14px var(--font-body);padding:8px 16px;border-radius:10px;cursor:pointer}
details.about{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 16px}
details.about summary{cursor:pointer;font-weight:700}
details.about p{margin:8px 0 0;color:var(--muted);max-width:80ch}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
''' + TCSS + r'''
</style>

<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Med<span>Decode</span> Word List</h1>
      <p>Every term, word part and phrase used in the MedDecode games, with its pronunciation, its parts and what it means. Search, or narrow the list by chapter, body region or program.</p>
    </div>
  </header>

  <div class="searchrow">
    <label class="search" for="q">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search a term, part or meaning" autocomplete="off" spellcheck="false" aria-label="Search the word list">
      <button type="button" class="clearx" id="q-clear" aria-label="Clear search" hidden>×</button>
    </label>
    <div class="seg" role="group" aria-label="What to list" id="tabs">
      <button type="button" data-tab="terms" aria-pressed="true">Terms<span class="n" id="n-terms"></span></button>
      <button type="button" data-tab="parts" aria-pressed="false">Word parts<span class="n" id="n-parts"></span></button>
      <button type="button" data-tab="phrases" aria-pressed="false">Phrases<span class="n" id="n-phrases"></span></button>
    </div>
    <select class="sortsel" id="sort" aria-label="Order">
      <option value="az">A to Z</option>
      <option value="ch">By chapter</option>
    </select>
  </div>
''' + THTML + r'''
  <div class="status"><span id="count"></span>
    <span class="legend" aria-hidden="true"><span><i style="background:var(--prefix)"></i>Prefix</span><span><i style="background:var(--root)"></i>Root</span><span><i style="background:var(--suffix)"></i>Suffix</span><span><i style="background:var(--cv)"></i>Combining vowel</span></span>
  </div>
  <nav class="letters" id="letters" aria-label="Jump to letter"></nav>
  <section class="list" id="list" aria-live="polite"></section>
  <div class="more" id="more-wrap" hidden><button type="button" class="btn" id="more">Show more</button></div>

  <details class="about">
    <summary>About this list (for instructors)</summary>
    <p>This page is built from the MedDecode master list, the same list that feeds Tiles, Dissect, Sort and Build. When terms are added or corrected, this page updates with the games.</p>
    <p><b>Chapters</b> follow <i>Acquiring Medical Language</i> (Jones and Cavanagh, McGraw Hill Education, 3rd edition). Entries marked <b>from the Ch 12 word list</b> are words from the book's chapter quick reference; their definitions, word parts and pronunciations were written for MedDecode, not copied from the book.</p>
    <p><b>Programs</b> and <b>body regions</b> are first drafts. All entries are drafts until instructors approve them in the content spreadsheet.</p>
  </details>
</div>

<script>
(function(){
const DATA = ''' + json.dumps(DATA, ensure_ascii=False, separators=(',',':')) + r''';
''' + TJS + r'''
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const CHN = %CHN%;
let tab = 'terms', limit = 150;
try { const h = location.hash.slice(1); if (DATA[h]) tab = h; } catch(e){}
try { const s = localStorage.getItem('mdwl-sort'); if (s) $('sort').value = s; } catch(e){}

function norm(s){ return String(s).toLowerCase().replace(/[^a-z0-9 ]/g,''); }
function hay(it){
  if (!it._h) it._h = norm([it.w, it.d, (it.bd||[]).map(p=>p[2]+' '+p[3]).join(' '), (it.syn||[]).join(' ')].join(' '));
  return it._h;
}
function matches(it, q){
  if (!MDT.match(it)) return false;
  if (!q) return true;
  return q.split(' ').filter(Boolean).every(t=>hay(it).includes(t));
}
function score(it, q){
  const w = norm(it.w);
  if (!q) return 0;
  if (w===q) return 0; if (w.startsWith(q)) return 1; if (w.includes(q)) return 2;
  if ((it.bd||[]).some(p=>norm(p[3]).includes(q))) return 3; if (norm(it.d).startsWith(q)) return 4; return 5;
}
function hl(word, q){
  if (!q) return esc(word);
  const i = word.toLowerCase().indexOf(q);
  if (i<0) return esc(word);
  return esc(word.slice(0,i))+'<mark>'+esc(word.slice(i,i+q.length))+'</mark>'+esc(word.slice(i+q.length));
}
function speak(text){
  try { const u = new SpeechSynthesisUtterance(text.replace(/[\/-]/g,' ')); u.rate = .85; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch(e){}
}
const canSpeak = 'speechSynthesis' in window;
function chTag(it){ return it.ch.map(c=>`<span class="tag" title="${esc(CHN[c])}">Ch ${c}</span>`).join(''); }
function entryHTML(it, q){
  const hear = canSpeak ? `<button type="button" class="hear" data-say="${esc(it.k==='prefix'||it.k==='root'||it.k==='suffix' ? it.w.split(',')[0].replace('/o','o').replace('/i','i') : it.w)}" aria-label="Hear ${esc(it.w)}">▶ Hear it</button>` : '';
  const head = `<div class="head"><span class="word">${hl(it.w,q)}</span><span class="sayrow">${it.say?`<span class="say">${esc(it.say)}</span>`:''}${hear}</span></div>`;
  let body = '';
  if (it.bd){
    const chips = it.bd.map(p=> p[1]==='cv' ? `<span class="p cv" data-t="cv" title="combining vowel"><b>${esc(p[0])}</b></span>` : `<span class="p" data-t="${p[1]}" title="${esc(p[1])}"><b>${esc(p[2])}</b>${esc(p[3])}</span>`).join('<span class="plus">+</span>');
    body += `<div class="parts" aria-label="Word parts">${chips}</div>`;
  }
  body += `<div class="def">${esc(it.d)}</div>`;
  if (it.syn && it.syn.length) body += `<div class="syn">Same meaning: ${it.syn.map(s=>`<b>${esc(s)}</b>`).join(', ')}</div>`;
  if (it.ex) body += `<div class="ex">${it.n ? `Used in ${it.n} term${it.n===1?'':'s'}: ${it.ex.map(e=>`<button type="button" data-find="${esc(e)}">${esc(e)}</button>`).join(', ')}${it.n>it.ex.length?'…':''}` : 'Not used in a term yet.'}</div>`;
  const kind = it.k==='phrase' ? '' : `<span class="tag kind">${esc(it.k)}</span>`;
  body += `<div class="meta">${kind}${chTag(it)}${(it.reg||[]).map(r=>`<span class="tag">${esc(r)}</span>`).join('')}<span class="tag">${it.prog.length===4?'All programs':esc(it.prog.join(' · '))}</span>${it.src==='book'?'<span class="tag book">from the Ch 12 word list</span>':''}</div>`;
  return `<article class="entry" id="${it._id}">${head}<div class="body">${body}</div></article>`;
}
function firstLetter(it){ const c = it.w.replace(/^[-\s]+/,'')[0]; return c ? c.toUpperCase() : '#'; }
function render(){
  const q = norm($('q').value).trim();
  $('q-clear').hidden = !$('q').value;
  ['terms','parts','phrases'].forEach(k=>{ $('n-'+k).textContent = DATA[k].filter(it=>matches(it,q)).length; });
  document.querySelectorAll('#tabs [data-tab]').forEach(b=>b.setAttribute('aria-pressed', b.dataset.tab===tab));
  let items = DATA[tab].filter(it=>matches(it,q));
  const byCh = $('sort').value==='ch';
  items.forEach((it,i)=>it._id=tab+'-'+i);
  if (q) items.sort((a,b)=>score(a,q)-score(b,q) || a.w.localeCompare(b.w));
  else if (byCh) items.sort((a,b)=>a.ch[0]-b.ch[0] || a.w.replace(/^-/,'').localeCompare(b.w.replace(/^-/,'')));
  const label = {terms:'term',parts:'word part',phrases:'phrase'}[tab];
  $('count').innerHTML = `<b>${items.length}</b> ${label}${items.length===1?'':'s'}${MDT.active()?' · '+esc(MDT.label()):''}${q?` matching “${esc($('q').value.trim())}”`:''}`;
  const shown = items.slice(0, limit);
  let html = '', last = null;
  shown.forEach(it=>{
    const g = q ? null : (byCh ? 'Chapter '+it.ch[0]+': '+CHN[it.ch[0]] : firstLetter(it));
    if (g!==null && g!==last){ html += `<div class="lh" id="${byCh?'ch'+it.ch[0]:'l-'+g}">${esc(g)}</div>`; last = g; }
    html += entryHTML(it, q);
  });
  $('list').innerHTML = html || `<div class="empty">No ${label}s match. Try a shorter search, or choose “All topics”.</div>`;
  $('more-wrap').hidden = items.length <= limit;
  $('more').textContent = `Show all ${items.length}`;
  // letter bar (A–Z view only)
  if (!q && !byCh){
    const have = new Set(items.map(firstLetter));
    $('letters').innerHTML = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(L=> have.has(L) ? `<a href="#l-${L}" data-l="${L}">${L}</a>` : `<span aria-hidden="true">${L}</span>`).join('');
    $('letters').hidden = false;
  } else $('letters').hidden = true;
  MDT.note(MDT.active() ? 'Showing only entries tagged with this topic.' : 'Choose a chapter, body region or program to narrow the list.');
}
$('list').addEventListener('click', e=>{
  const h = e.target.closest('[data-say]'); if (h){ speak(h.dataset.say); return; }
  const f = e.target.closest('[data-find]'); if (f){ $('q').value = f.dataset.find; tab='terms'; limit=150; render(); window.scrollTo({top:0,behavior:'smooth'}); }
});
$('letters').addEventListener('click', e=>{
  const a = e.target.closest('[data-l]'); if (!a) return; e.preventDefault();
  const id = 'l-'+a.dataset.l;
  if (!document.getElementById(id)){ limit = 100000; render(); }
  const el = document.getElementById(id); if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
});
let t=null;
$('q').addEventListener('input', ()=>{ clearTimeout(t); t=setTimeout(()=>{ limit=150; render(); }, 120); });
$('q-clear').addEventListener('click', ()=>{ $('q').value=''; limit=150; render(); $('q').focus(); });
$('tabs').addEventListener('click', e=>{ const b=e.target.closest('[data-tab]'); if (!b) return; tab=b.dataset.tab; limit=150; render(); });
$('sort').addEventListener('change', ()=>{ try{ localStorage.setItem('mdwl-sort', $('sort').value); }catch(e){} limit=150; render(); });
$('more').addEventListener('click', ()=>{ limit = 100000; render(); });
MDT.mount(()=>{ limit=150; render(); });
render();
})();
</script>
'''.replace('%CHN%', json.dumps({str(k):v for k,v in M.CHAPTERS.items()}))
open('/home/claude/meddecode-wordlist/meddecode-wordlist.html','w').write(HTML)
print('terms',len(DATA['terms']),'parts',len(DATA['parts']),'phrases',len(DATA['phrases']),'bytes',len(HTML))
