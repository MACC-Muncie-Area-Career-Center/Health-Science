# Builds MedDecode Body Map (where word roots live on the body) from the master list.
import json, sys
sys.path.insert(0,'/home/claude/shared')
import master as M
import bodymap_spots as B
import bodyfig as F
from topics import CSS as TCSS, HTML as THTML, JS as TJS
MOD = open('/home/claude/shared/md-classroom.js').read()
D10 = open('/home/claude/shared/gen_daily10.py').read()
BASECSS = D10[D10.index(':root{'):D10.index('/* Today strip')]

# roots used anywhere on the map
mapped = []
for s in B.SPOTS: mapped += s[4]
for t in B.TRAY: mapped += t[2]
mapped = list(dict.fromkeys(mapped))
ROOTS = {}
for pid in mapped:
    form,typ,mean,say,sysn,tile,ck = M.PARTS[pid]
    ROOTS[pid] = {'f':form,'m':mean,'ch':M.part_tags(pid)['ch']}
TERMS = []
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    ids = [p for _,p in parts if p in ROOTS]
    if not ids: continue
    tg = M.term_tags(t)
    TERMS.append({'w':w,'d':d,'say':say,'r':list(dict.fromkeys(ids)),
                  'bd':[[M.PARTS[p][0],M.PARTS[p][1],M.PARTS[p][2]] for _,p in parts if p!='cv'],
                  'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog']})
SPOTS = [{'id':i,'n':n,'l':l,'r':r,'x':x} for i,n,l,c,r,svg,x in B.SPOTS] + [{'id':i,'n':n,'l':'tray','r':r} for i,n,r in B.TRAY]

def sil(sex, lid):
    P = F.PIECES[sex]
    if lid=='outside':
        fill = ''.join(f'<path d="{P[k]}"/>' for k in ('legs','arm','torso','neck','head'))
        return (f'<g class="sil" aria-hidden="true">{fill}</g>')
    return f'<g class="sil ghost" aria-hidden="true"><path d="{F.OUTLINE[sex]}"/></g>'

def hits(i, sex):
    h = B.HITS.get(i, [])
    if isinstance(h, dict): h = h[sex]
    return ''.join(f'<circle class="hit" cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in h)

def spot_g(i,n,c,shape,sex):
    return f'<g class="spot" data-id="{i}" data-c="{c}" tabindex="0" role="button" aria-label="{n}"><title>{n}</title>{shape}{hits(i,sex)}</g>'

def layer_svg(lid):
    parts = []
    for sex in ('f','m'):
        g = [sil(sex, lid)]
        if lid in ('bones','repro'): g.append(f'<path class="pelvis" d="{F.PELVIS[sex]}" aria-hidden="true"/>')
        if lid=='repro': g.append(B.REPRO_CONTEXT[sex])
        for i,n,l,c,r,shape,x in B.SPOTS:
            if l!=lid or (x and x!=sex): continue
            if isinstance(shape, dict): g.append(spot_g(i,n,c,shape[sex],sex))
            elif x or isinstance(B.HITS.get(i), dict): g.append(spot_g(i,n,c,shape,sex))
        if lid=='outside':
            g.append(f'<g class="outline" aria-hidden="true"><path d="{F.OUTLINE[sex]}"/>{F.DETAILS[sex]}</g>')
        parts.append(f'<g data-sex="{sex}">' + ''.join(g) + '</g>')
    for i,n,l,c,r,shape,x in B.SPOTS:   # spots drawn the same on both figures
        if l==lid and not x and not isinstance(shape, dict) and not isinstance(B.HITS.get(i), dict):
            parts.append(spot_g(i,n,c,shape,'m'))
    return f'<g class="layer" data-layer="{lid}" hidden>' + ''.join(parts) + '</g>'

SVG = ('<svg id="map" viewBox="0 0 400 820" data-fig="f" role="group" aria-label="Body map">' + B.CLIPS
       + ''.join(layer_svg(l) for l,_ in B.LAYERS) + '</svg>')
VIEWS = {l: B.ZOOM.get(l, B.VIEW) for l,_ in B.LAYERS}
TABS = ''.join(f'<button type="button" data-layer="{l}" aria-pressed="false">{n}</button>' for l,n in B.LAYERS)
TRAYB = ''.join(f'<button type="button" class="chip spot" data-id="{i}">{n}</button>' for i,n,r in B.TRAY)

HTML = r'''<title>MedDecode Body Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
/* Layout: the body drawing on the left (layer tabs above, a "throughout the body" tray below),
   and a panel on the right that explains what was tapped or asks the next question. */
''' + BASECSS + r'''
:root{ --body:#d5dfdc; --body-edge:#9fb1ad; --ghost:#e6ecea;
  --c-skin:#c9d6d2; --c-sense:#5b7fd1; --c-resp:#4aa3c7; --c-oral:#d07a9a; --c-nerv:#9a7bd6; --c-lymph:#7fb35a; --c-endo:#d9a43c;
  --c-card:#cf4b4b; --c-dig:#d98a4b; --c-uri:#c6a33a; --c-bone:#b9b1a0; --c-repro:#c46fb0; }
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){ --body:#2c3b3e; --body-edge:#4d6064; --ghost:#1d2a2d; --c-skin:#3a4c50; --c-bone:#8a8474; }}
:root[data-theme="dark"]{ --body:#2c3b3e; --body-edge:#4d6064; --ghost:#1d2a2d; --c-skin:#3a4c50; --c-bone:#8a8474; }
.statusbar{display:flex;flex-wrap:wrap;gap:6px 18px;font-family:var(--font-mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.statusbar b{color:var(--ink);font-weight:600}
.wrap{max-width:1120px}
.stage{display:grid;grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:16px;align-items:start}
@media (max-width:820px){ .stage{grid-template-columns:minmax(0,1fr)} .side{order:-1} }
.mapcol{display:grid;gap:10px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:12px}
.layers{display:flex;flex-wrap:wrap;gap:4px}
.layers button{border:1px solid var(--line);background:var(--bg);color:var(--ink);font:600 14px var(--font-body);padding:7px 12px;border-radius:999px;cursor:pointer}
.layers button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.layers button.hint{box-shadow:0 0 0 3px var(--focus)}
#map{width:100%;max-width:420px;height:auto;display:block;margin:0 auto;touch-action:manipulation}
@media (max-width:820px){ #map{max-height:70vh} }
.sil path{fill:var(--body);stroke:none}
.sil.ghost path{fill:var(--ghost);stroke:var(--body-edge);stroke-width:1.5;stroke-dasharray:5 4;vector-effect:non-scaling-stroke}
.outline{pointer-events:none}
.outline path,.outline circle{fill:none;stroke:var(--body-edge);stroke-width:1.1;vector-effect:non-scaling-stroke}
.outline path:first-child{stroke:var(--ink);stroke-opacity:.55;stroke-width:1.6}
.pelvis{fill:none;stroke:var(--body-edge);stroke-width:2;stroke-dasharray:3 3;pointer-events:none;vector-effect:non-scaling-stroke}
#map[data-fig="f"] [data-sex="m"], #map[data-fig="m"] [data-sex="f"]{display:none}
.figs{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.figs .lab{font:700 12px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ctx text{font:700 15px var(--font-mono);fill:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.ctx text.small{font:600 5.5px var(--font-body);text-transform:none;letter-spacing:0}
.ctx .organ-ctx{fill:none;stroke:var(--body-edge);stroke-dasharray:4 3;stroke-width:1.6;vector-effect:non-scaling-stroke}
.ctx .tube-ctx{fill:none;stroke:var(--body-edge);stroke-dasharray:2 1.5;stroke-width:2.5}
g.spot{cursor:pointer;outline:none}
g.spot > *{fill:var(--sc);stroke:var(--edge,rgba(0,0,0,.25));stroke-width:1.2;transition:fill .15s, stroke .15s, opacity .15s}
g.spot > :not(.tube){vector-effect:non-scaling-stroke}
g.spot > .tube{fill:none;stroke:var(--sc);stroke-linecap:round}
g.spot[data-c="skin"] > *{fill:var(--body);stroke:none}
g.spot[data-c="skin"] > .tube{stroke:var(--body)}
g.spot[data-c="skin"]{--sc:var(--body)}
g.spot[data-c="sense"]{--sc:var(--c-sense)} g.spot[data-c="resp"]{--sc:var(--c-resp)} g.spot[data-c="oral"]{--sc:var(--c-oral)}
g.spot[data-c="nerv"]{--sc:var(--c-nerv)} g.spot[data-c="lymph"]{--sc:var(--c-lymph)} g.spot[data-c="endo"]{--sc:var(--c-endo)}
g.spot[data-c="card"]{--sc:var(--c-card)} g.spot[data-c="dig"]{--sc:var(--c-dig)} g.spot[data-c="uri"]{--sc:var(--c-uri)}
g.spot[data-c="bone"]{--sc:var(--c-bone)} g.spot[data-c="repro"]{--sc:var(--c-repro)}
g.spot:hover > *, g.spot:focus-visible > *{stroke:var(--ink);stroke-width:2.5;stroke-dasharray:none}
g.spot:hover > .tube, g.spot:focus-visible > .tube{stroke:var(--ink)}
#map g.spot.sel > *{fill:var(--accent);stroke:var(--ink);stroke-width:2.5;stroke-dasharray:none}
#map g.spot.sel > .tube{stroke:var(--accent)}
#map g.spot.ok > *{fill:var(--good);stroke:var(--good);stroke-dasharray:none} #map g.spot.ok > .tube{stroke:var(--good)}
#map g.spot.no > *{fill:var(--bad);stroke:var(--bad);stroke-dasharray:none} #map g.spot.no > .tube{stroke:var(--bad)}
#map g.spot.glow > *{fill:var(--focus);stroke:var(--ink);stroke-width:3;stroke-dasharray:none;animation:pulse 1.2s ease-in-out infinite}
#map g.spot.glow > .tube{stroke:var(--focus)}
@keyframes pulse{50%{opacity:.55}}
g.spot > .hit{fill:transparent!important;stroke:none!important;animation:none!important}
.trayw{display:grid;gap:6px}
.trayw h3{margin:0;font:700 12px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.tray{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--line);background:var(--bg);color:var(--ink);font:600 13.5px var(--font-body);padding:6px 11px;border-radius:999px;cursor:pointer}
.chip:hover{border-color:var(--ink)}
.chip.sel{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.chip.ok{background:var(--good);border-color:var(--good);color:#fff}
.chip.no{background:var(--bad);border-color:var(--bad);color:#fff}
.chip.glow{background:var(--focus);border-color:var(--focus);color:#1b1300}

.side{display:grid;gap:12px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px;display:grid;gap:12px}
.panel h2{font:800 clamp(24px,3.4vw,34px)/1.1 var(--font-display);margin:0;letter-spacing:-.01em}
.panel h3{font:700 13px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.tag{font:600 11px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.roots{display:flex;flex-wrap:wrap;gap:6px}
.root{display:inline-flex;align-items:baseline;gap:6px;background:var(--bg);border-radius:8px;padding:5px 10px;border-left:4px solid var(--root)}
.root b{font:700 16px var(--font-mono);color:var(--root)}
.tlist{margin:0;padding:0;list-style:none;display:grid;gap:6px}
.tlist li{background:var(--bg);border-radius:10px;padding:8px 12px;display:grid;gap:2px}
.tlist .w{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
.tlist .w b{font:700 16px var(--font-body)}
.tlist .say{font:600 13px var(--font-mono);color:var(--muted)}
.tlist .d{font-size:14px;color:var(--muted)}
.hearbtn{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;font:600 12px var(--font-body);padding:2px 9px;cursor:pointer}
.hint{margin:0;color:var(--muted);font-size:14px}
.spotlist{display:flex;flex-wrap:wrap;gap:6px}
.prompt{font:800 clamp(34px,5.6vw,56px)/1 var(--font-mono);letter-spacing:-.01em;color:var(--accent);margin:0;overflow-wrap:anywhere}
.prompt.term{font-family:var(--font-display);color:var(--ink)}
.ask{margin:0;font-weight:700;color:var(--muted)}
.opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.opt{border:2px solid var(--line);background:var(--bg);color:var(--ink);font:700 19px var(--font-mono);padding:12px;border-radius:12px;cursor:pointer;display:flex;gap:8px;align-items:center}
.opt .k{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:6px;background:var(--chip);font:700 12px var(--font-mono);color:var(--muted)}
.opt.right{border-color:var(--good);background:var(--good-bg);color:var(--good)}
.opt.wrong{border-color:var(--bad);background:var(--bad-bg);color:var(--bad)}
.opt:disabled{cursor:default}
.fb{border-radius:12px;padding:12px 14px;display:grid;gap:8px}
.fb.good{background:var(--good-bg)} .fb.bad{background:var(--bad-bg)}
.fb .h{font-weight:700} .fb.good .h{color:var(--good)} .fb.bad .h{color:var(--bad)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.bigs{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px}
.bigs div{background:var(--bg);border-radius:10px;padding:10px 12px}
.bigs b{display:block;font:800 26px var(--font-display);font-variant-numeric:tabular-nums}
.bigs span{font-size:12.5px;color:var(--muted)}
.rlist{margin:0;padding:0;list-style:none;display:grid;gap:4px}
.rlist li{display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
.rlist .mk{font:700 13px var(--font-mono);width:16px} .rlist .mk.ok{color:var(--good)} .rlist .mk.no{color:var(--bad)}
.rlist .d{color:var(--muted);font-size:14px}
details.about{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px 16px}
details.about summary{cursor:pointer;font-weight:700}
details.about p{margin:8px 0 0;color:var(--muted);max-width:80ch}
@media (prefers-reduced-motion: reduce){ g.spot.glow > *{animation:none} g.spot > *{transition:none} }
body.mdc-classroom .stage{grid-template-columns:minmax(0,560px) minmax(0,1fr)}
body.mdc-classroom #map{max-width:560px}
body.mdc-classroom .prompt{font-size:clamp(56px,6vw,90px)}
body.mdc-classroom .opt{font-size:28px;padding:18px}
body.mdc-classroom .chip,body.mdc-classroom .layers button{font-size:18px;padding:9px 15px}
''' + TCSS + r'''
</style>

<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Med<span>Decode</span> Body Map</h1>
      <p>See where word roots live on the body. Explore by tapping, then test yourself: find the root on the body, find where a term's problem is, or name the part that lights up.</p>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="Mode">
        <button type="button" data-mode="explore" aria-pressed="true">Explore</button>
        <button type="button" data-mode="root" aria-pressed="false">Find the root</button>
        <button type="button" data-mode="term" aria-pressed="false">Where's the problem?</button>
        <button type="button" data-mode="name" aria-pressed="false">Name it</button>
      </div>
    </div>
  </header>
''' + THTML + r'''
  <div class="statusbar" id="status" aria-live="polite" hidden>
    <span>Question <b id="s-q">1/10</b></span>
    <span>Correct <b id="s-ok">0</b></span>
    <span>First-tap streak <b id="s-st">0</b></span>
  </div>
  <div class="stage">
    <div class="mapcol">
      <div class="figs"><span class="lab">Figure</span><div class="seg" role="group" aria-label="Figure"><button type="button" data-fig-btn="f" aria-pressed="true">Female</button><button type="button" data-fig-btn="m" aria-pressed="false">Male</button></div></div>
      <div class="layers" role="group" aria-label="Layer">''' + TABS + r'''</div>
      ''' + SVG + r'''
      <div class="trayw"><h3>Throughout the body</h3><div class="tray" id="tray">''' + TRAYB + r'''</div></div>
    </div>
    <div class="side">
      <section class="panel" id="panel" aria-live="polite"></section>
    </div>
  </div>
  <details class="about">
    <summary>How Body Map works (for instructors)</summary>
    <p><b>Explore</b> shows each place's roots and every MedDecode term built from them (filtered by the Topic bar), with pronunciation. Layers keep overlapping organs apart: Outside, Organs, Urinary, Bones and Reproductive. Skin, muscle, blood, nerves and other tissues found all over the body are in the "Throughout the body" tray.</p>
    <p><b>Find the root</b> shows a root (nephr/o) and students tap where it lives. <b>Where's the problem?</b> shows a term (pyelonephritis) and students tap the body part it's about. <b>Name it</b> lights up a place and students choose its root. In the two "find" modes the map switches to the right layer for each question; a wrong tap shows what was tapped and where the answer is.</p>
    <p>Roots that describe colors, actions or conditions (cyan/o, phag/o, lith/o) aren't places, so they aren't on the map; they appear in the other games. The figures are simplified drawings for locating organs, not an anatomy reference.</p>
    <p><b>Female and male figures.</b> Students switch with the Figure buttons (the choice is remembered on that device; <code>?figure=male</code> or <code>?figure=female</code> in a link sets it). The figures differ in body shape, pelvis, urethra length and reproductive organs. The Reproductive layer zooms in on the pelvis. In quiz rounds the map switches to the figure that has the answer (for example, the male figure for orchi/o) and says so. Use the Chapter filter to leave reproductive terms out of quiz rounds.</p>
    <p><b>Team mode:</b> each question is one team's turn; a correct first tap earns the points.</p>
  </details>
</div>

<script>
(function(){
const SPOTS = ''' + json.dumps(SPOTS, ensure_ascii=False, separators=(',',':')) + r''';
const ROOTS = ''' + json.dumps(ROOTS, ensure_ascii=False, separators=(',',':')) + r''';
const TERMS = ''' + json.dumps(TERMS, ensure_ascii=False, separators=(',',':')) + r''';
''' + TJS + r'''
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const BYID = Object.fromEntries(SPOTS.map(s=>[s.id,s]));
const VIEWS = ''' + json.dumps(VIEWS) + r''';
const ROUND = 10;
function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function balanced(arr){
  const g={}; arr.forEach(it=>{ const k=it.ch[Math.floor(Math.random()*it.ch.length)]; (g[k]=g[k]||[]).push(it); });
  const lists=Object.values(g).map(l=>shuffle(l.slice())); const out=[];
  while (lists.some(l=>l.length)){ shuffle(lists).forEach(l=>{ if (l.length) out.push(l.pop()); }); }
  return out;
}
const spotsOfRoot = pid => SPOTS.filter(s=>s.r.includes(pid));
const termsOfSpot = s => TERMS.filter(t=>t.r.some(r=>s.r.includes(r)));

/* ---------- Voice ---------- */
const canSpeak = 'speechSynthesis' in window;
let voice = null;
function pickVoice(){ try { const vs = speechSynthesis.getVoices(); voice = vs.find(v=>/^en[-_]US/i.test(v.lang) && /natural|google|samantha|aria|jenny/i.test(v.name)) || vs.find(v=>/^en[-_]US/i.test(v.lang)) || vs.find(v=>/^en/i.test(v.lang)) || null; } catch(e){} }
if (canSpeak){ pickVoice(); try { speechSynthesis.onvoiceschanged = pickVoice; } catch(e){} }
function speak(text, rate){ if (!canSpeak) return; try { const u = new SpeechSynthesisUtterance(text); u.rate = rate||.85; if (voice) u.voice = voice; u.lang='en-US'; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch(e){} }

/* ---------- Map state ---------- */
let layer = 'outside', mode = 'explore', R = null, Q = null, fig = 'f';
try { const v = localStorage.getItem('md-bodymap-fig'); if (v==='m' || v==='f') fig = v; } catch(e){}
try { const q = new URLSearchParams(location.search).get('figure'); if (q==='male') fig = 'm'; if (q==='female') fig = 'f'; } catch(e){}
const avail = s => !s.x || s.x===fig;
const figName = x => x==='m' ? 'male' : 'female';
function setFig(x, user){
  fig = x; $('map').setAttribute('data-fig', x);
  document.querySelectorAll('[data-fig-btn]').forEach(b=>b.setAttribute('aria-pressed', b.dataset.figBtn===x));
  if (user){ try { localStorage.setItem('md-bodymap-fig', x); } catch(e){} }
}
document.querySelectorAll('[data-fig-btn]').forEach(b=>b.addEventListener('click', ()=>{ setFig(b.dataset.figBtn, true); if (mode==='explore') exploreHome(); }));
function setLayer(l){
  layer = l; $('map').setAttribute('viewBox', VIEWS[l]);
  document.querySelectorAll('.layer').forEach(g=>g.toggleAttribute('hidden', g.dataset.layer!==l));
  document.querySelectorAll('.layers button').forEach(b=>{ b.setAttribute('aria-pressed', b.dataset.layer===l); b.classList.remove('hint'); });
}
function els(id){ return [...document.querySelectorAll(`.spot[data-id="${id}"]`)]; }
function clearMarks(){ document.querySelectorAll('.spot').forEach(e=>e.classList.remove('sel','ok','no','glow')); }
document.querySelectorAll('.layers button').forEach(b=>b.addEventListener('click', ()=>{ setLayer(b.dataset.layer); if (mode==='explore') exploreHome(); }));
document.querySelectorAll('.spot').forEach(e=>{
  e.addEventListener('click', ()=>tap(e.dataset.id));
  e.addEventListener('keydown', ev=>{ if (ev.key==='Enter' || ev.key===' '){ ev.preventDefault(); tap(e.dataset.id); } });
});
function tap(id){ if (mode==='explore') explore(id); else if (mode==='root' || mode==='term') answerTap(id); }
const layerName = l => ({outside:'Outside', organs:'Organs', urinary:'Urinary', bones:'Bones', repro:'Reproductive', tray:'Throughout the body'})[l];
function showSpot(id){ const s = BYID[id]; if (s.x && s.x!==fig) setFig(s.x); if (s.l!=='tray' && s.l!==layer) setLayer(s.l); }

/* ---------- Explore ---------- */
function rootsHTML(s){ return `<div class="roots">${s.r.map(r=>`<span class="root"><b>${esc(ROOTS[r].f)}</b>${esc(ROOTS[r].m)}</span>`).join('')}</div>`; }
function exploreHome(){
  clearMarks();
  const here = SPOTS.filter(s=>s.l===layer && avail(s));
  $('panel').innerHTML = `<span class="tag">Explore · ${esc(layerName(layer))} layer</span>
    <h2>Tap any part of the body</h2>
    <p class="hint">Or choose from the list. Switch layers above the drawing to see organs, the urinary tract, bones and reproductive organs. Skin, muscle, blood and nerves are in "Throughout the body".</p>
    <div class="spotlist">${here.map(s=>`<button type="button" class="chip" data-go="${s.id}">${esc(s.n)}</button>`).join('')}</div>`;
  $('panel').querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click', ()=>explore(b.dataset.go)));
}
function explore(id){
  const s = BYID[id]; showSpot(id); clearMarks(); els(id).forEach(e=>e.classList.add('sel'));
  const all = termsOfSpot(s), list = all.filter(t=>MDT.match(t));
  const shown = list.slice(0, 14);
  $('panel').innerHTML = `<span class="tag">${esc(layerName(s.l))}</span>
    <h2>${esc(s.n)}</h2>
    <h3>Word roots</h3>${rootsHTML(s)}
    <h3>Terms built from ${s.r.length>1?'these roots':'this root'} (${list.length}${MDT.active()?` in ${esc(MDT.label())}`:''})</h3>
    ${shown.length ? `<ul class="tlist">${shown.map(t=>`<li><span class="w"><b>${esc(t.w)}</b><span class="say">${esc(t.say)}</span>${canSpeak?`<button type="button" class="hearbtn" data-say="${esc(t.w)}">▶ Hear</button>`:''}</span><span class="d">${esc(t.d)}</span></li>`).join('')}</ul>` : `<p class="hint">${all.length ? 'No terms with these roots in this topic yet. Choose "All topics" to see them all.' : 'No MedDecode terms use this root yet.'}</p>`}
    ${list.length>shown.length?`<button type="button" class="btn" id="more">Show all ${list.length}</button>`:''}
    <div class="row"><button type="button" class="btn" id="back">← All places on this layer</button></div>`;
  bindHear();
  const m = $('more'); if (m) m.addEventListener('click', ()=>{ $('panel').querySelector('.tlist').innerHTML = list.map(t=>`<li><span class="w"><b>${esc(t.w)}</b><span class="say">${esc(t.say)}</span>${canSpeak?`<button type="button" class="hearbtn" data-say="${esc(t.w)}">▶ Hear</button>`:''}</span><span class="d">${esc(t.d)}</span></li>`).join(''); m.remove(); bindHear(); });
  $('back').addEventListener('click', exploreHome);
  if (window.innerWidth<=820) $('panel').scrollIntoView({block:'start', behavior:'smooth'});
  if (window.MDC){ MDC.define({term:s.n, def:s.r.map(x=>`${ROOTS[x].f} = ${ROOTS[x].m}`).join(' · '), kind:'Body Map', parts:s.r.map(x=>({form:ROOTS[x].f, m:ROOTS[x].m, type:'root'}))}); }
}
function bindHear(){ $('panel').querySelectorAll('[data-say]').forEach(b=>b.onclick = ()=>speak(b.dataset.say)); }

/* ---------- Quiz rounds ---------- */
function rootPool(){
  return Object.keys(ROOTS).filter(pid=>{ const ts = TERMS.filter(t=>t.r.includes(pid)); return MDT.active() ? ts.some(t=>MDT.match(t)) : true; })
    .map(pid=>({pid, ch:ROOTS[pid].ch}));
}
function newRound(){
  clearMarks();
  let note = '', items;
  if (mode==='term'){
    let pool = TERMS.filter(t=>MDT.match(t));
    if (!pool.length){ pool = TERMS.slice(); note = `No terms match ${MDT.label()} yet, so this round uses all topics. `; }
    // one term per place where possible, so a round visits different parts of the body
    const seen = new Set(); items = [];
    for (const t of balanced(pool)){ const k = t.r.join(); if (seen.has(k)) continue; seen.add(k); items.push({t}); if (items.length>=ROUND) break; }
    MDT.note(note + `${MDT.active()?MDT.label():'All topics'}: ${pool.length} terms with a place on the map.`);
  } else {
    let pool = rootPool();
    if (!pool.length){ pool = Object.keys(ROOTS).map(pid=>({pid, ch:ROOTS[pid].ch})); note = `No roots match ${MDT.label()} yet, so this round uses all topics. `; }
    if (mode==='name'){ // one root per place
      const seen = new Set(); items = [];
      for (const it of balanced(pool)){ const s = spotsOfRoot(it.pid)[0]; if (seen.has(s.id)) continue; seen.add(s.id); items.push({pid:it.pid, spot:s.id}); if (items.length>=ROUND) break; }
    } else items = balanced(pool).slice(0, ROUND).map(it=>({pid:it.pid}));
    MDT.note(note + `${MDT.active()?MDT.label():'All topics'}: ${pool.length} roots on the map.`);
  }
  R = {items, i:0, ok:0, streak:0, best:0, log:[]};
  $('status').hidden = false;
  loadQ();
}
function answersFor(it){
  if (mode==='term') return SPOTS.filter(s=>s.r.some(r=>it.t.r.includes(r))).map(s=>s.id);
  return spotsOfRoot(it.pid).map(s=>s.id);
}
function loadQ(){
  clearMarks();
  const it = R.items[R.i];
  const ans = answersFor(it).sort((a,b)=>avail(BYID[b])-avail(BYID[a]));
  Q = {it, tries:0, done:false, ans};
  const first = BYID[Q.ans[0]];
  if (mode==='root' || mode==='term'){
    let switched = false;
    if (first.x && first.x!==fig){ setFig(first.x); switched = true; }
    if (first.l!=='tray') setLayer(first.l);
    const lay = first.l==='tray' ? 'in the "Throughout the body" tray' : `on the ${switched?`<b>${figName(fig)}</b> figure's `:''}${layerName(first.l)} layer`;
    if (mode==='root'){
      $('panel').innerHTML = `<span class="tag">Find the root · ${R.i+1} of ${R.items.length}</span>
        <p class="ask">Tap where this root lives:</p><h2 class="prompt">${esc(ROOTS[it.pid].f)}</h2>
        <p class="hint">Look ${lay}.</p><div id="fb"></div>`;
    } else {
      $('panel').innerHTML = `<span class="tag">Where's the problem? · ${R.i+1} of ${R.items.length}</span>
        <p class="ask">Tap the part of the body this term is about:</p><h2 class="prompt term">${esc(it.t.w)}</h2>
        <div class="row">${canSpeak?'<button type="button" class="btn" id="hear">▶ Hear it</button>':''}</div>
        <p class="hint">Look ${lay}.</p><div id="fb"></div>`;
      const h = $('hear'); if (h) h.addEventListener('click', ()=>speak(it.t.w));
    }
  } else { // name it
    const s = BYID[it.spot]; showSpot(s.id); els(s.id).forEach(e=>e.classList.add('glow'));
    const others = shuffle(Object.keys(ROOTS).filter(p=>!s.r.includes(p) && ROOTS[p].m!==ROOTS[it.pid].m)).slice(0,3);
    Q.opts = shuffle([it.pid].concat(others));
    $('panel').innerHTML = `<span class="tag">Name it · ${R.i+1} of ${R.items.length}</span>
      <p class="ask">Which root names the part that's lit up${s.l==='tray'?' in the tray':''}?</p>
      <div class="opts" id="opts">${Q.opts.map((p,i)=>`<button type="button" class="opt" data-p="${p}"><span class="k">${i+1}</span>${esc(ROOTS[p].f)}</button>`).join('')}</div><div id="fb"></div>`;
    $('opts').addEventListener('click', e=>{ const b = e.target.closest('.opt'); if (b && !b.disabled) answerName(b); });
  }
  renderStatus();
  if (window.MDC) MDC.hideDef();
}
function renderStatus(){ $('s-q').textContent = `${Math.min(R.i+1,R.items.length)}/${R.items.length}`; $('s-ok').textContent = R.ok; $('s-st').textContent = R.streak; }
function answerTap(id){
  if (!Q || Q.done) return;
  Q.tries++;
  const ok = Q.ans.includes(id);
  if (!ok && Q.tries<2){
    els(id).forEach(e=>e.classList.add('no'));
    const s = BYID[id];
    $('fb').innerHTML = `<div class="fb bad"><div class="h">That's the ${esc(s.n.toLowerCase())} (${s.r.map(r=>esc(ROOTS[r].f)).join(', ')}). Try once more.</div></div>`;
    setTimeout(()=>els(id).forEach(e=>e.classList.remove('no')), 900);
    return;
  }
  finishQ(ok, id);
}
function answerName(b){
  const ok = b.dataset.p === Q.it.pid;
  document.querySelectorAll('#opts .opt').forEach(x=>{ x.disabled = true; if (x.dataset.p===Q.it.pid) x.classList.add('right'); });
  if (!ok) b.classList.add('wrong');
  Q.tries = 1; finishQ(ok, null, b.dataset.p);
}
function finishQ(ok, tapped, picked){
  Q.done = true; clearMarks();
  Q.ans.forEach(a=>els(a).forEach(e=>e.classList.add('ok')));
  if (tapped && !ok) els(tapped).forEach(e=>e.classList.add('no'));
  const first = ok && Q.tries===1;
  if (ok) R.ok++;
  if (first){ R.streak++; R.best = Math.max(R.best, R.streak); } else R.streak = 0;
  const it = Q.it, spot = BYID[Q.ans[0]];
  R.log.push({label: mode==='term' ? it.t.w : ROOTS[it.pid].f, ok, first, where: Q.ans.map(a=>BYID[a].n).join(' / ')});
  let body = '';
  if (mode==='term'){
    const t = it.t;
    body = `<div><b>${esc(t.w)}</b> <span style="font-family:var(--font-mono);color:var(--muted)">${esc(t.say)}</span></div><div>${esc(t.d)}</div>
      <div class="roots">${t.bd.map(p=>`<span class="root" style="--root:var(--${p[1]})"><b>${esc(p[0])}</b>${esc(p[2])}</span>`).join('')}</div>`;
  } else {
    const p = ROOTS[it.pid];
    const ex = TERMS.filter(t=>t.r.includes(it.pid)).slice(0,3).map(t=>t.w);
    body = `<div><b style="font-family:var(--font-mono);font-size:18px">${esc(p.f)}</b> means <b>${esc(p.m)}</b>.</div>${ex.length?`<div class="hint">Used in ${ex.map(esc).join(', ')}.</div>`:''}
      ${picked && !ok ? `<div class="hint">${esc(ROOTS[picked].f)} means ${esc(ROOTS[picked].m)}${spotsOfRoot(picked)[0]?`, the ${esc(spotsOfRoot(picked)[0].n.toLowerCase())}`:''}.</div>`:''}`;
  }
  const where = Q.ans.map(a=>esc(BYID[a].n.toLowerCase())).join(' or the ');
  const msg = ok ? (first ? `Correct: the ${where}.` : `Got it on the second tap: the ${where}.`) : `It's the ${where}${spot.l==='tray'?' (in the "Throughout the body" tray)':` (${layerName(spot.l)} layer)`}.`;
  $('fb').innerHTML = `<div class="fb ${ok?'good':'bad'}"><div class="h">${msg}</div>${body}
    <div class="row">${mode==='term'&&canSpeak?'<button type="button" class="btn" id="fb-hear">▶ Hear it</button>':''}<button type="button" class="btn primary" id="next">${R.i<R.items.length-1?'Next →':'See results →'}</button></div></div>`;
  const fh = $('fb-hear'); if (fh) fh.addEventListener('click', ()=>speak(it.t.w));
  $('next').addEventListener('click', ()=>{ if (R.i<R.items.length-1){ R.i++; loadQ(); } else results(); });
  $('next').focus({preventScroll:true});
  if (window.innerWidth<=820) $('fb').scrollIntoView({block:'nearest', behavior:'smooth'});
  if (window.MDC){
    MDC.play(first, {label: R.log[R.log.length-1].label, missLabel:'No points this time'});
    if (mode==='term') MDC.define({term:it.t.w, say:it.t.say, def:it.t.d, kind:'Body Map', parts:it.t.bd.map(p=>({form:p[0], m:p[2], type:p[1]}))});
    else MDC.define({term:ROOTS[it.pid].f, def:ROOTS[it.pid].m, kind:'Body Map', parts:[]});
  }
  renderStatus();
}
function results(){
  clearMarks();
  const n = R.items.length, first = R.log.filter(l=>l.first).length;
  $('panel').innerHTML = `<h2>${first>=9?'You know your way around the body!':first>=6?'Good map reading':'Keep exploring'}</h2>
    <div class="bigs"><div><b>${first}/${n}</b><span>Right on the first try</span></div><div><b>${R.ok}/${n}</b><span>Right in the end</span></div><div><b>${R.best}</b><span>Best streak</span></div></div>
    <ul class="rlist">${R.log.map(l=>`<li><span class="mk ${l.first?'ok':'no'}">${l.first?'✓':'✗'}</span><b>${esc(l.label)}</b><span class="d">${esc(l.where)}</span></li>`).join('')}</ul>
    <div class="row"><button type="button" class="btn primary" id="again">New round</button><button type="button" class="btn" id="toexp">Explore the map</button></div>`;
  $('again').addEventListener('click', newRound);
  $('toexp').addEventListener('click', ()=>setMode('explore'));
}

/* ---------- Controls ---------- */
function setMode(m){
  mode = m;
  document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed', b.dataset.mode===m));
  if (m==='explore'){ $('status').hidden = true; MDT.note(MDT.active() ? `${MDT.label()}: term lists show this topic only.` : 'All topics. Choose a chapter, body region or program to focus the term lists and quiz rounds.'); exploreHome(); }
  else newRound();
}
document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click', ()=>setMode(b.dataset.mode)));
document.addEventListener('keydown', e=>{
  if (e.target.closest && e.target.closest('input,textarea,select')) return;
  if (mode==='name' && /^[1-4]$/.test(e.key)){ const b = document.querySelectorAll('#opts .opt')[+e.key-1]; if (b && !b.disabled) b.click(); }
});
MDC.init({game:'Body Map', onChange:()=>{}});
MDT.mount(()=>setMode(mode));
setFig(fig);
setLayer('outside');
setMode('explore');
})();
</script>
'''
i = HTML.index('<script>\n(function(){')
HTML = HTML[:i] + '<script id="mdc">\n' + MOD + '\n</script>\n' + HTML[i:]
import os; os.makedirs('/home/claude/meddecode-bodymap', exist_ok=True)
open('/home/claude/meddecode-bodymap/meddecode-bodymap.html','w').write(HTML)
print('spots', len(SPOTS), 'roots', len(ROOTS), 'terms', len(TERMS), 'bytes', len(HTML))
