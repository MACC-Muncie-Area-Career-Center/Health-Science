# Builds MedDecode Daily 10 (spaced-repetition daily review) from the master list.
import json, re, sys
sys.path.insert(0,'/home/claude/shared')
import master as M
from topics import CSS as TCSS, HTML as THTML, JS as TJS
MOD = open('/home/claude/shared/md-classroom.js').read()

grp = {}
for i,g in enumerate(M.SYN_GROUPS):
    for w in g: grp[w] = i
words=[]
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    tg = M.term_tags(t)
    bd = [[M.PARTS[p][0], M.PARTS[p][1], M.PARTS[p][2]] for _,p in parts if p!='cv']
    words.append({'w':w,'d':d,'say':say,'bd':bd,'k':kind,'sys':sysn,'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':grp.get(w,-1)})
# Phrases, unsplittable words and abbreviations (Oct 2026)
_have = {x['w'] for x in words}
for ph in M.PHRASES:
    if ph['t'] in _have: continue
    tg = M.phrase_tags(ph); _have.add(ph['t'])
    words.append({'w':ph['t'],'d':ph['d'],'say':ph['say'] or '','bd':[],'k':ph['kind'],'sys':M._CH_SYS.get(tg['ch'][0],'General'),'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':grp.get(ph['t'],-1)})
import re as _re
for a in M.ABBREVIATIONS:
    ab, full, typ, how, chs = a
    if ab in _have: continue
    tg = M.abbrev_tags(a); _have.add(ab)
    m = _re.sub(r'\s*\(.*?\)', '', full).split(';')[0].strip()
    words.append({'w':ab,'d':m,'say':'','bd':[],'k':'abbreviation','sys':'Abbreviations','ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':-1})
seen=set(); parts=[]
for form,typ,mean,*_ in M.PARTS.values():
    k=(typ,mean.lower())
    if k in seen: continue
    seen.add(k); parts.append([form,typ,mean])

HTML = r'''<title>MedDecode Daily 10</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
/* Layout: a daily card stack. A progress strip (streak, today's 10 as dots), one question card at a time,
   then a results card and "My progress" (Leitner boxes). Same tokens as the other MedDecode games. */
:root{
  --bg:#e9eeec; --surface:#f7f9f8; --ink:#16262b; --muted:#5b6d70; --line:#cdd7d5; --chip:#e1e8e6;
  --accent:#0f7a73; --accent-ink:#ffffff; --focus:#e08a00;
  --good:#1f7a3d; --bad:#b3261e; --good-bg:#e3f2e7; --bad-bg:#f9e4e2; --warn:#8a5a00; --warn-bg:#fbefd0;
  --prefix:#6a4bb3; --root:#0f7a73; --suffix:#b4531f;
  --b1:#c2410c; --b2:#b7791f; --b3:#3f8f6b; --b4:#0f7a73; --b5:#4b5fb3;
  --font-display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --font-body:"Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --font-mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --good:#6fd08e; --bad:#ff8a80; --good-bg:#16301f; --bad-bg:#3a1a18; --warn:#ffcf70; --warn-bg:#3a2e12;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54;
  --b1:#ff8a5c; --b2:#f2c14e; --b3:#6fd08e; --b4:#3cc2b6; --b5:#8fa2ff; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --good:#6fd08e; --bad:#ff8a80; --good-bg:#16301f; --bad-bg:#3a1a18; --warn:#ffcf70; --warn-bg:#3a2e12;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54;
  --b1:#ff8a5c; --b2:#f2c14e; --b3:#6fd08e; --b4:#3cc2b6; --b5:#8fa2ff; color-scheme:dark }
*{box-sizing:border-box}
[hidden]{display:none!important}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:15px;line-height:1.45}
.wrap{max-width:860px;margin:0 auto;padding-inline:16px;padding-block:18px 56px;display:grid;gap:16px}
.wrap > *{min-width:0}
header.top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px}
.brand h1{font-family:var(--font-display);font-weight:800;font-size:clamp(26px,4vw,36px);letter-spacing:-.02em;margin:0;line-height:1}
.brand h1 span{color:var(--accent)}
.brand p{margin:6px 0 0;color:var(--muted);max-width:60ch}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--surface)}
.seg button{border:0;background:transparent;color:var(--ink);font:600 14px var(--font-body);padding:7px 13px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 15px var(--font-body);padding:9px 16px;border-radius:10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.btn:hover{border-color:var(--ink)}
.btn.primary{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.btn.danger{color:var(--bad);border-color:var(--bad)}
.btn:disabled{opacity:.45;cursor:not-allowed}
button:focus-visible,select:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--focus);outline-offset:2px}

/* Today strip: streak + ten dots */
.strip{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:center;justify-content:space-between;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 14px}
.streak{display:flex;align-items:baseline;gap:8px}
.streak b{font:800 30px/1 var(--font-display);font-variant-numeric:tabular-nums;color:var(--accent)}
.streak span{font-size:13px;color:var(--muted)}
.dots{display:flex;gap:6px;flex-wrap:wrap}
.dots i{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);background:transparent;display:block}
.dots i.cur{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}
.dots i.ok{background:var(--good);border-color:var(--good)}
.dots i.no{background:var(--bad);border-color:var(--bad)}
.dots i.fix{background:var(--warn);border-color:var(--warn)}
.mix{font:600 12.5px var(--font-mono);color:var(--muted)}
.mix b{color:var(--ink)}

.card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px clamp(14px,3vw,28px) 22px;display:grid;gap:14px}
.card .top{display:flex;flex-wrap:wrap;gap:6px 12px;justify-content:space-between;align-items:baseline}
.tag{font:600 11px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pill{display:inline-block;font:700 11px var(--font-mono);letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:3px 9px;background:var(--chip);color:var(--ink)}
.pill.new{background:var(--accent);color:var(--accent-ink)}
.prompt{font:800 clamp(28px,5vw,46px)/1.05 var(--font-display);letter-spacing:-.015em;overflow-wrap:anywhere;margin:0}
.prompt.def{font:700 clamp(20px,3vw,27px)/1.25 var(--font-body);letter-spacing:0}
.prompt mark{background:transparent;color:var(--accent);text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:5px}
.ask{margin:0;color:var(--muted);font-weight:700}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:8px}
.opt{display:flex;gap:10px;align-items:flex-start;text-align:left;border:2px solid var(--line);background:var(--bg);color:var(--ink);font:600 16px/1.3 var(--font-body);padding:12px 14px;border-radius:12px;cursor:pointer;min-height:56px}
.opt .k{flex:none;display:inline-grid;place-items:center;width:24px;height:24px;border-radius:6px;background:var(--chip);font:700 12px var(--font-mono);color:var(--muted)}
.opt:hover:not(:disabled){border-color:var(--ink)}
.opt.term{font:700 19px var(--font-mono)}
.opt.right{border-color:var(--good);background:var(--good-bg);color:var(--good)}
.opt.wrong{border-color:var(--bad);background:var(--bad-bg);color:var(--bad)}
.opt:disabled{cursor:default}
.opt:disabled:not(.right):not(.wrong){opacity:.55}
.spell{display:flex;flex-wrap:wrap;gap:8px}
.spell input{flex:1 1 240px;min-width:0;font:600 20px var(--font-mono);padding:10px 12px;border:2px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink)}
.spell input.right{border-color:var(--good)} .spell input.wrong{border-color:var(--bad)}
.hint{margin:0;color:var(--muted);font-size:14px}
.listen{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.fb{border-radius:12px;padding:12px 14px;display:grid;gap:8px}
.fb.good{background:var(--good-bg)} .fb.bad{background:var(--bad-bg)}
.fb .h{font-weight:700} .fb.good .h{color:var(--good)} .fb.bad .h{color:var(--bad)}
.fb .w{font:800 22px var(--font-display)} .fb .say{font:600 15px var(--font-mono);color:var(--muted);margin-left:8px}
.fb .moved{font-size:13px;color:var(--muted)}
.parts{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.p{display:inline-flex;align-items:baseline;gap:5px;font-size:13px;border-radius:7px;padding:2px 8px;background:var(--surface);border-left:4px solid var(--pc)}
.p b{font:600 13.5px var(--font-mono);color:var(--pc)}
.p[data-t="prefix"]{--pc:var(--prefix)} .p[data-t="root"]{--pc:var(--root)} .p[data-t="suffix"]{--pc:var(--suffix)}
.plus{color:var(--muted);font-size:12px}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px;display:grid;gap:14px}
.panel h2{font:800 26px var(--font-display);margin:0}
.panel h3{font:700 13px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.bigs{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.bigs div{background:var(--bg);border-radius:10px;padding:10px 12px}
.bigs b{display:block;font:800 26px var(--font-display);font-variant-numeric:tabular-nums}
.bigs span{font-size:12.5px;color:var(--muted)}
.done-card{border:2px solid var(--accent);border-radius:14px;padding:12px 14px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:baseline;justify-content:space-between}
.done-card b{font:800 20px var(--font-display)}
.done-card span{font:600 13px var(--font-mono);color:var(--muted)}
.rlist{margin:0;padding:0;list-style:none;display:grid;gap:4px}
.rlist li{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.rlist .m{font:700 13px var(--font-mono);width:18px;flex:none}
.rlist .m.ok{color:var(--good)} .rlist .m.no{color:var(--bad)}
.rlist .d{color:var(--muted);font-size:14px}
.boxes{display:grid;gap:6px}
.bx{display:grid;grid-template-columns:minmax(110px,150px) minmax(0,1fr) 44px;gap:10px;align-items:center;font-size:14px}
.bx .bar{height:14px;border-radius:7px;background:var(--bg);overflow:hidden}
.bx .bar i{display:block;height:100%;background:var(--c)}
.bx .n{font:600 13px var(--font-mono);text-align:right;font-variant-numeric:tabular-nums}
.cal{display:flex;gap:5px;flex-wrap:wrap}
.cal i{width:22px;height:22px;border-radius:6px;background:var(--bg);border:1px solid var(--line);display:grid;place-items:center;font:600 10px var(--font-mono);color:var(--muted);font-style:normal}
.cal i.on{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.cal i.today{outline:2px solid var(--focus);outline-offset:1px}
.msg{border-radius:10px;padding:10px 12px;font-size:14.5px}
.msg.warn{background:var(--warn-bg);color:var(--warn)}
.msg.plain{background:var(--bg)}
textarea{width:100%;min-height:70px;font:13px var(--font-mono);border:1px solid var(--line);border-radius:10px;padding:8px;background:var(--bg);color:var(--ink)}
details.about,details.more{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px 16px}
details.about summary,details.more summary{cursor:pointer;font-weight:700}
details.about p{margin:8px 0 0;color:var(--muted);max-width:80ch}
details.more > div{display:grid;gap:10px;margin-top:10px}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
body.mdc-classroom .prompt{font-size:clamp(44px,6vw,76px)}
body.mdc-classroom .prompt.def{font-size:clamp(28px,3.4vw,40px)}
body.mdc-classroom .opt{font-size:24px;padding:18px;min-height:80px}
body.mdc-classroom .opt.term{font-size:28px}
''' + TCSS + r'''
</style>

<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Med<span>Decode</span> Daily 10</h1>
      <p>Ten quick questions a day. Words you miss come back sooner; words you know come back later, until they stick.</p>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="Mode">
        <button type="button" id="m-me" aria-pressed="true">My Daily 10</button>
        <button type="button" id="m-class" aria-pressed="false">Class warm-up</button>
      </div>
    </div>
  </header>
''' + THTML + r'''
  <div class="strip" aria-live="polite">
    <div class="streak"><b id="s-streak">0</b><span id="s-streak-l">day streak</span></div>
    <div class="dots" id="dots" aria-label="Today's questions"></div>
    <div class="mix" id="s-mix"></div>
  </div>
  <div id="storemsg"></div>

  <article class="card" id="card" aria-live="polite"></article>
  <section class="panel" id="results" hidden></section>

  <section class="panel" id="progress">
    <h3>My progress</h3>
    <div class="bigs" id="p-bigs"></div>
    <div class="boxes" id="p-boxes"></div>
    <h3>Last 14 days</h3>
    <div class="cal" id="p-cal"></div>
  </section>

  <details class="more" id="more">
    <summary>Move or reset my progress</summary>
    <div>
      <p class="hint">Progress is saved only in this browser on this device. To continue on another device, copy your progress code here and paste it there.</p>
      <div class="row"><button type="button" class="btn" id="code-copy">Copy my progress code</button><span class="hint" id="code-msg"></span></div>
      <textarea id="code-in" aria-label="Paste a progress code" placeholder="Paste a progress code from another device"></textarea>
      <div class="row"><button type="button" class="btn" id="code-load">Load this code</button></div>
      <div class="row"><button type="button" class="btn danger" id="reset">Reset my progress</button><span class="hint" id="reset-msg"></span></div>
    </div>
  </details>

  <details class="about">
    <summary>How Daily 10 works (for instructors)</summary>
    <p><b>Spaced review.</b> Each word sits in one of five boxes. A correct answer moves it up a box and pushes its next review further out (1, 2, 4, 7, then 14 days). A miss sends it back to box 1, so it returns tomorrow. Each day's 10 starts with the words that are due, then adds new words from the chosen topic, dealt evenly across chapters.</p>
    <p><b>Question types get harder as a word moves up:</b> new words ask for the meaning or a word part; middle boxes ask students to pick the term from its definition or from hearing it; top boxes ask them to spell it. Missed words come back once at the end of the set as a quick fix (that second try doesn't change the box).</p>
    <p><b>Topics.</b> Pick a chapter, body region or program and press <b>Copy student link</b> to post a focused link in Schoology. New words then come from that topic; words that are due for review still appear from any topic.</p>
    <p><b>Privacy.</b> Progress is stored only in the student's browser on that device. Nothing is sent anywhere. For credit, students can screenshot the "Daily 10 complete" card with the date and score. Students who switch devices can use the progress code to carry their boxes over.</p>
    <p><b>Class warm-up</b> is for the classroom screen: 10 questions from the chosen topic, no saved progress. With Team mode on, each answer is one team's play.</p>
  </details>
</div>

<script>
(function(){
const WORDS = ''' + json.dumps(words, ensure_ascii=False, separators=(',',':')) + r''';
const PARTS = ''' + json.dumps(parts, ensure_ascii=False, separators=(',',':')) + r''';
''' + TJS + r'''
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const N = 10, MAX_DUE = 7, KEY = 'md-daily10-v1';
const INTERVAL = [0,1,2,4,7,14];
const BOXNAME = ['', 'Learning', 'Practicing', 'Getting it', 'Strong', 'Mastered'];
const BYW = Object.fromEntries(WORDS.map(w=>[w.w,w]));

/* ---------- Dates (local) ---------- */
const pad = n => String(n).padStart(2,'0');
const dkey = d => `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const today = () => dkey(new Date());
function addDays(k, n){ const [y,m,d] = k.split('-').map(Number); return dkey(new Date(y, m-1, d+n)); }
const prettyDate = k => { const [y,m,d] = k.split('-').map(Number); return new Date(y,m-1,d).toLocaleDateString(undefined,{weekday:'short', month:'short', day:'numeric', year:'numeric'}); };

/* ---------- Storage (per browser; works without it) ---------- */
let canStore = true;
function blank(){ return {v:1, box:{}, days:{}, cur:null}; }
let S = blank();
try { const raw = localStorage.getItem(KEY); if (raw){ const s = JSON.parse(raw); if (s && s.box && s.days) S = Object.assign(blank(), s); } localStorage.setItem(KEY+'-t','1'); localStorage.removeItem(KEY+'-t'); }
catch(e){ canStore = false; }
function save(){ if (!canStore) return; try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e){ canStore = false; showStoreMsg(); } }
function showStoreMsg(){ $('storemsg').innerHTML = canStore ? '' : '<div class="msg warn">This browser isn\'t letting MedDecode save progress (private window or blocked site data). Today\'s 10 still works, but your boxes and streak won\'t be remembered.</div>'; }

/* ---------- Helpers ---------- */
function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function balanced(arr){
  const g={}; arr.forEach(it=>{ const k=it.ch[Math.floor(Math.random()*it.ch.length)]; (g[k]=g[k]||[]).push(it); });
  const lists=Object.values(g).map(l=>shuffle(l.slice())); const out=[];
  while (lists.some(l=>l.length)){ shuffle(lists).forEach(l=>{ if (l.length) out.push(l.pop()); }); }
  return out;
}
const norm = s => String(s).toLowerCase().replace(/[^a-z]/g,'');
function lev(a,b){ const m=a.length,n=b.length,d=Array.from({length:m+1},(_,i)=>[i]); for(let j=1;j<=n;j++) d[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++) d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]===b[j-1]?0:1)); return d[m][n]; }
const sameMeaning = (a,b) => (a.g>=0 && a.g===b.g) || norm(a.d)===norm(b.d);

/* ---------- Voice ---------- */
const canSpeak = 'speechSynthesis' in window;
let voice = null;
function pickVoice(){ try { const vs = speechSynthesis.getVoices(); voice = vs.find(v=>/^en[-_]US/i.test(v.lang) && /natural|google|samantha|aria|jenny/i.test(v.name)) || vs.find(v=>/^en[-_]US/i.test(v.lang)) || vs.find(v=>/^en/i.test(v.lang)) || null; } catch(e){} }
if (canSpeak){ pickVoice(); try { speechSynthesis.onvoiceschanged = pickVoice; } catch(e){} }
function speak(text, rate){ if (!canSpeak) return; try { const u = new SpeechSynthesisUtterance(text); u.rate = rate||.85; if (voice) u.voice = voice; u.lang='en-US'; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch(e){} }

/* ---------- Building a day's set ---------- */
let mode = 'me', R = null;
function poolNew(){
  let pool = WORDS.filter(w=>MDT.match(w)), note = '';
  if (MDT.active() && !pool.length){ pool = WORDS.slice(); note = `No terms match ${MDT.label()} yet, so new words come from all topics.`; }
  return {pool, note};
}
function buildSet(){
  const t = today(), {pool, note} = poolNew();
  const due = Object.entries(S.box).filter(([w,b])=>BYW[w] && b.due<=t)
    .sort((a,b)=> (MDT.match(BYW[b[0]])-MDT.match(BYW[a[0]])) || a[1].due.localeCompare(b[1].due) || a[1].b-b[1].b).map(e=>e[0]);
  const ids = due.slice(0, MAX_DUE);
  const fresh = balanced(pool.filter(w=>!S.box[w.w])).map(w=>w.w);
  while (ids.length<N && fresh.length) ids.push(fresh.shift());
  for (const w of due.slice(MAX_DUE)) { if (ids.length>=N) break; ids.push(w); }
  if (ids.length<N){ // everything seen: pull the weakest words that aren't due yet
    const rest = Object.entries(S.box).filter(([w])=>BYW[w] && !ids.includes(w) && MDT.match(BYW[w])).sort((a,b)=>a[1].b-b[1].b || a[1].due.localeCompare(b[1].due)).map(e=>e[0]);
    while (ids.length<N && rest.length) ids.push(rest.shift());
  }
  const nDue = Math.min(due.length, ids.filter(w=>S.box[w] && S.box[w].due<=t).length);
  MDT.note(note || (MDT.active() ? `${MDT.label()}: new words come from this topic. Words due for review appear from any topic.` : `All topics: ${WORDS.length} words. Choose a chapter, body region or program to focus new words.`));
  return {date:t, ids:shuffle(ids), qs:{}, i:0, ans:[], fix:[], fi:0, nDue, phase:'main'};
}
function buildWarmup(){
  const {pool, note} = poolNew();
  MDT.note(note || (MDT.active() ? `${MDT.label()}: ${pool.length} words.` : `All topics: ${WORDS.length} words.`));
  return {date:today(), ids:balanced(pool).slice(0,N).map(w=>w.w), qs:{}, i:0, ans:[], fix:[], fi:0, nDue:0, phase:'main', warm:true};
}

/* ---------- Questions ---------- */
function typeFor(w, fix){
  if (fix) return 'def2term';
  const b = (S.box[w.w]||{}).b || 0;
  const hasPart = w.bd.length>1;
  if (mode==='class') return pickOne(['term2def','def2term', hasPart?'part':'term2def']);
  if (b<=1) return pickOne(hasPart ? ['term2def','term2def','part'] : ['term2def']);
  if (b===2) return pickOne(canSpeak ? ['def2term','hear', hasPart?'part':'def2term'] : ['def2term', hasPart?'part':'def2term']);
  return pickOne(canSpeak ? ['spell','spell','hear','def2term'] : ['spell','spell','def2term']);
}
const pickOne = a => a[Math.floor(Math.random()*a.length)];
function distractWords(w, n){
  const near = shuffle(WORDS.filter(x=>x.w!==w.w && !sameMeaning(x,w) && (x.sys===w.sys || x.k===w.k)));
  const far = shuffle(WORDS.filter(x=>x.w!==w.w && !sameMeaning(x,w)));
  const out = [];
  for (const x of near.concat(far)){ if (out.length>=n) break; if (!out.some(o=>o.w===x.w || sameMeaning(o,x))) out.push(x); }
  return out;
}
function makeQ(word, fix){
  const w = BYW[word], type = typeFor(w, fix);
  const q = {w:word, type};
  if (type==='term2def'){ q.opts = shuffle([w.d].concat(distractWords(w,3).map(x=>x.d))); q.ans = w.d; }
  else if (type==='def2term' || type==='hear'){ q.opts = shuffle([w.w].concat(distractWords(w,3).map(x=>x.w))); q.ans = w.w; }
  else if (type==='part'){
    const cand = w.bd.filter(p=>p[2] && p[2].length<60);
    const p = cand[Math.floor(Math.random()*cand.length)] || w.bd[0];
    const others = shuffle(PARTS.filter(x=>x[1]===p[1] && norm(x[2])!==norm(p[2]) && !w.bd.some(y=>norm(y[2])===norm(x[2])))).slice(0,3);
    q.part = p; q.opts = shuffle([p[2]].concat(others.map(x=>x[2]))); q.ans = p[2];
  }
  else { q.ans = w.w; }
  return q;
}

/* ---------- Render ---------- */
function partsHTML(w){ return w.bd.map(p=>`<span class="p" data-t="${p[1]}"><b>${esc(p[0])}</b>${esc(p[2])}</span>`).join('<span class="plus">+</span>'); }
function highlight(word, form){
  const f = form.replace(/[-\s]/g,'').split(',')[0];
  const i = f ? word.toLowerCase().indexOf(f.toLowerCase()) : -1;
  return i<0 ? esc(word) : esc(word.slice(0,i)) + '<mark>' + esc(word.slice(i,i+f.length)) + '</mark>' + esc(word.slice(i+f.length));
}
function curWord(){ return R.phase==='fix' ? R.fix[R.fi] : R.ids[R.i]; }
function curQ(){
  const k = (R.phase==='fix'?'f:':'') + curWord();
  if (!R.qs[k]) { R.qs[k] = makeQ(curWord(), R.phase==='fix'); persist(); }
  return R.qs[k];
}
function persist(){ if (mode==='me'){ S.cur = R; save(); } }

function renderStrip(){
  const st = streak();
  $('s-streak').textContent = st.n; 
  const dots = [];
  for (let i=0;i<R.ids.length;i++){
    const a = R.ans[i];
    const fixed = a===false && R.fixed && R.fixed[R.ids[i]];
    dots.push(`<i class="${a===true?'ok':a===false?(fixed?'fix':'no'):(R.phase==='main'&&i===R.i?'cur':'')}" title="Question ${i+1}"></i>`);
  }
  $('dots').innerHTML = dots.join('');
  const nNew = R.ids.filter(w=>!R.wasSeen || !R.wasSeen[w]).length;
  $('s-mix').innerHTML = R.warm ? '<b>Class warm-up</b> · not saved' : `<b>${R.ids.length - nNew}</b> review · <b>${nNew}</b> new`;
}

function render(){
  if (R.phase==='done'){ $('card').hidden = true; showResults(); renderStrip(); renderProgress(); return; }
  $('card').hidden = false; $('results').hidden = true;
  const q = curQ(), w = BYW[q.w];
  const isFix = R.phase==='fix';
  const b = (S.box[w.w]||{}).b || 0;
  const label = isFix ? `Quick fix ${R.fi+1} of ${R.fix.length}` : `Question ${R.i+1} of ${R.ids.length}`;
  const pill = isFix ? '<span class="pill">Second try</span>' : R.warm ? '' : (b && R.wasSeen && R.wasSeen[w.w]) ? `<span class="pill">Review · ${BOXNAME[b]}</span>` : '<span class="pill new">New word</span>';
  let body = '';
  const optBtns = (cls)=>`<div class="opts" id="opts">${q.opts.map((o,i)=>`<button type="button" class="opt ${cls}" data-v="${esc(o)}"><span class="k">${i+1}</span><span>${esc(o)}</span></button>`).join('')}</div>`;
  if (q.type==='term2def'){
    body = `<p class="ask">What does this term mean?</p><h2 class="prompt">${esc(w.w)}</h2>
      <div class="listen">${canSpeak?'<button type="button" class="btn" id="hear">▶ Hear it</button>':''}</div>${optBtns('')}`;
  } else if (q.type==='def2term'){
    body = `<p class="ask">Which term matches this definition?</p><h2 class="prompt def">${esc(w.d)}</h2>${optBtns('term')}`;
  } else if (q.type==='hear'){
    body = `<p class="ask">Listen, then choose the word you heard.</p>
      <div class="listen"><button type="button" class="btn primary" id="hear">▶ Play the word</button><button type="button" class="btn" id="slow">Slow</button></div>${optBtns('term')}`;
  } else if (q.type==='part'){
    body = `<p class="ask">In this term, what does the marked ${esc(q.part[1])} <b style="font-family:var(--font-mono)">${esc(q.part[0])}</b> mean?</p><h2 class="prompt">${highlight(w.w, q.part[0])}</h2>${optBtns('')}`;
  } else {
    body = `<p class="ask">Spell the term that matches this definition.</p><h2 class="prompt def">${esc(w.d)}</h2>
      <form class="spell" id="spell" autocomplete="off"><input id="sp-in" aria-label="Your spelling" spellcheck="false" autocapitalize="off" autocorrect="off" placeholder="Type the term"><button type="submit" class="btn primary">Check</button></form>
      <div class="row"><button type="button" class="btn" id="sp-hint">Hint</button>${canSpeak?'<button type="button" class="btn" id="hear">▶ Hear it</button>':''}</div><p class="hint" id="sp-h" hidden></p>`;
  }
  $('card').innerHTML = `<div class="top"><span class="tag">${label}</span>${pill}</div>${body}<div id="fb"></div>`;
  bind(q, w);
  renderStrip();
  if (q.type==='hear') setTimeout(()=>speak(w.w,.85), 250);
  if (window.MDC) MDC.hideDef();
}

function bind(q, w){
  const h = $('hear'); if (h) h.addEventListener('click', ()=>speak(w.w,.85));
  const sl = $('slow'); if (sl) sl.addEventListener('click', ()=>speak(w.w,.55));
  const o = $('opts');
  if (o) o.addEventListener('click', e=>{ const b = e.target.closest('.opt'); if (!b || b.disabled) return; answerMC(q, w, b); });
  const f = $('spell');
  if (f){
    f.addEventListener('submit', e=>{ e.preventDefault(); const v = $('sp-in').value.trim(); if (!v) return; answerSpell(q, w, v); });
    $('sp-hint').addEventListener('click', ()=>{ const el=$('sp-h'); el.hidden=false; el.innerHTML = `Starts with <b>${esc(w.w[0])}</b>, ${w.w.length} letters. Parts: ${w.bd.map(p=>esc(p[2])).join(' + ')}`; q.hinted = true; });
    setTimeout(()=>{ try { if (!('ontouchstart' in window)) $('sp-in').focus(); } catch(e){} }, 50);
  }
}
function answerMC(q, w, b){
  const ok = b.dataset.v === q.ans;
  document.querySelectorAll('#opts .opt').forEach(x=>{ x.disabled = true; if (x.dataset.v===q.ans) x.classList.add('right'); });
  if (!ok) b.classList.add('wrong');
  record(ok, w, ok ? '' : `You chose “${esc(b.dataset.v)}”.`);
}
function answerSpell(q, w, v){
  const d = lev(norm(v), norm(w.w));
  const ok = d===0 || (d===1 && w.w.length>=7);
  const inp = $('sp-in'); inp.disabled = true; inp.classList.add(ok?'right':'wrong');
  document.querySelector('#spell button').disabled = true; $('sp-hint').disabled = true;
  record(ok, w, d===0 ? '' : ok ? `Almost: one letter off. Check the spelling: <b>${esc(w.w)}</b>.` : `You wrote “${esc(v)}”.`);
}

function record(ok, w, extra){
  let moved = '';
  if (R.phase==='fix'){
    R.fixed = R.fixed || {}; if (ok) R.fixed[w.w] = true;
  } else {
    R.ans[R.i] = ok;
    if (!R.warm){
      const prev = S.box[w.w];
      const nb = ok ? Math.min(5, (prev ? prev.b : 1) + 1) : 1;
      S.box[w.w] = {b:nb, due:addDays(today(), INTERVAL[nb]), n:(prev?prev.n:0)+1, r:(prev?prev.r:0)+(ok?1:0)};
      const days = INTERVAL[nb];
      moved = ok ? `Moved to box ${nb} (${BOXNAME[nb]}). Next review in ${days} day${days===1?'':'s'}.` : `Back to box 1. It returns tomorrow${R.phase==='main'?' and once more at the end of today\'s set':''}.`;
    }
  }
  const last = R.phase==='fix' ? R.fi>=R.fix.length-1 : R.i>=R.ids.length-1;
  const missed = R.phase==='main' ? R.ids.filter((x,i)=>R.ans[i]===false) : [];
  const nextLabel = !last ? 'Next →' : (R.phase==='main' && missed.length && !R.warm) ? `Quick fix: ${missed.length} missed →` : 'See results →';
  $('fb').innerHTML = `<div class="fb ${ok?'good':'bad'}">
    <div class="h">${ok?'Correct!':'Not quite.'} ${extra||''}</div>
    <div><span class="w">${esc(w.w)}</span><span class="say">${esc(w.say)}</span></div>
    <div>${esc(w.d)}</div>
    ${w.bd.length?`<div class="parts">${partsHTML(w)}</div>`:''}
    ${moved?`<div class="moved">${moved}</div>`:''}
    <div class="row">${canSpeak?'<button type="button" class="btn" id="fb-hear">▶ Hear it</button>':''}<button type="button" class="btn primary" id="next">${nextLabel}</button></div>
  </div>`;
  const fh = $('fb-hear'); if (fh) fh.addEventListener('click', ()=>speak(w.w,.85));
  $('next').addEventListener('click', advance);
  $('next').focus({preventScroll:true});
  $('fb').scrollIntoView({block:'nearest', behavior:'smooth'});
  if (window.MDC){
    if (R.phase==='main') MDC.play(ok, {label:w.w, missLabel:'No points: '+w.w});
    MDC.define({term:w.w, say:w.say, def:w.d, kind:'Daily 10', parts:w.bd.map(p=>({form:p[0], m:p[2], type:p[1]}))});
  }
  persist(); renderStrip(); renderProgress();
}
function advance(){
  if (R.phase==='main'){
    if (R.i < R.ids.length-1){ R.i++; }
    else {
      R.fix = R.warm ? [] : R.ids.filter((x,i)=>R.ans[i]===false);
      if (R.fix.length){ R.phase = 'fix'; R.fi = 0; }
      else finishDay();
    }
  } else if (R.phase==='fix'){
    if (R.fi < R.fix.length-1) R.fi++; else finishDay();
  }
  persist(); render();
  window.scrollTo({top:Math.max(0,$('card').offsetTop-12), behavior:'smooth'});
}
function finishDay(){
  R.phase = 'done';
  const score = R.ans.filter(Boolean).length;
  if (!R.warm && !R.bonus){ const prev = S.days[R.date]; if (!prev) S.days[R.date] = {s:score, n:R.ids.length}; }
}

/* ---------- Results and progress ---------- */
function streak(){
  let n = 0, k = today();
  if (!S.days[k]) k = addDays(k, -1);
  while (S.days[k]){ n++; k = addDays(k, -1); }
  return {n};
}
function showResults(){
  const score = R.ans.filter(Boolean).length, n = R.ids.length;
  const P = $('results'); P.hidden = false;
  const tomorrow = Object.values(S.box).filter(b=>b.due<=addDays(today(),1)).length;
  const fixedN = R.fixed ? Object.keys(R.fixed).length : 0;
  const head = R.warm ? 'Warm-up complete' : R.bonus ? 'Bonus round complete' : score>=9 ? 'Excellent work!' : score>=7 ? 'Nice work!' : score>=5 ? 'Good effort' : 'Keep at it';
  P.innerHTML = `<h2>${head}</h2>
    ${R.warm ? '' : `<div class="done-card"><b>Daily 10 complete${R.bonus?' (bonus)':''} · ${score}/${n}</b><span>${esc(prettyDate(R.date))} · ${streak().n}-day streak</span></div>`}
    <div class="bigs">
      <div><b>${score}/${n}</b><span>Right the first time</span></div>
      ${R.warm?'':`<div><b>${fixedN}/${R.fix.length}</b><span>Fixed on the second try</span></div>
      <div><b>${tomorrow}</b><span>Words due by tomorrow</span></div>`}
    </div>
    <ul class="rlist">${R.ids.map((x,i)=>{ const w = BYW[x]; return `<li><span class="m ${R.ans[i]?'ok':'no'}">${R.ans[i]?'✓':'✗'}</span><b>${esc(w.w)}</b><span class="d">${esc(w.d)}</span></li>`; }).join('')}</ul>
    <div class="row">
      ${R.warm ? '<button type="button" class="btn primary" id="again">Another warm-up</button>' : `<button type="button" class="btn primary" id="bonus">Bonus 10 (new words)</button>`}
      <span class="hint">${R.warm ? 'Class warm-ups are not saved.' : 'Come back tomorrow for your next Daily 10.'}</span>
    </div>`;
  const a = $('again'); if (a) a.addEventListener('click', ()=>{ R = buildWarmup(); render(); });
  const bo = $('bonus'); if (bo) bo.addEventListener('click', ()=>{ startSet(true); });
}
function renderProgress(){
  const counts = [0,0,0,0,0,0];
  Object.entries(S.box).forEach(([w,b])=>{ if (BYW[w]) counts[b.b]++; });
  const seen = counts.reduce((a,b)=>a+b,0), total = WORDS.length;
  const due = Object.values(S.box).filter(b=>b.due<=today()).length;
  const daysDone = Object.keys(S.days).length;
  $('p-bigs').innerHTML = `<div><b>${seen}</b><span>of ${total} words started</span></div><div><b>${counts[5]}</b><span>Mastered (box 5)</span></div><div><b>${daysDone}</b><span>Days completed</span></div><div><b>${due}</b><span>Due now</span></div>`;
  const max = Math.max(1, ...counts.slice(1));
  const row = (name, n, c)=>`<div class="bx" style="--c:${c}"><span>${name}</span><span class="bar"><i style="width:${(n/max*100).toFixed(1)}%"></i></span><span class="n">${n}</span></div>`;
  $('p-boxes').innerHTML = [1,2,3,4,5].map(b=>row(`${b} · ${BOXNAME[b]}`, counts[b], `var(--b${b})`)).join('');
  const cells = []; for (let i=13;i>=0;i--){ const k = addDays(today(), -i); const d = S.days[k]; cells.push(`<i class="${d?'on':''}${i===0?' today':''}" title="${esc(prettyDate(k))}${d?`: ${d.s}/${d.n}`:''}">${+k.slice(8)}</i>`); }
  $('p-cal').innerHTML = cells.join('');
}

/* ---------- Start ---------- */
function startSet(bonus){
  if (mode==='class'){ R = buildWarmup(); render(); return; }
  const t = today();
  if (!bonus && S.cur && S.cur.date===t && !S.cur.warm && S.cur.ids && S.cur.ids.length){ R = S.cur; }
  else if (!bonus && S.days[t]){ R = S.cur && S.cur.date===t ? S.cur : null; if (!R){ R = buildSet(); R.phase='done'; R.ans = R.ids.map(()=>true); } }
  else {
    if (bonus){ // bonus: unseen words from the topic, else the weakest seen words
      const {pool} = poolNew(); const fresh = balanced(pool.filter(w=>!S.box[w.w])).map(w=>w.w);
      const weak = Object.entries(S.box).filter(([w])=>BYW[w]&&MDT.match(BYW[w])).sort((a,b)=>a[1].b-b[1].b).map(e=>e[0]);
      const ids = fresh.slice(0,N); while (ids.length<N && weak.length){ const x=weak.shift(); if (!ids.includes(x)) ids.push(x); }
      R = {date:t, ids:shuffle(ids), qs:{}, i:0, ans:[], fix:[], fi:0, nDue:0, phase:'main', bonus:true};
    } else R = buildSet();
    R.wasSeen = Object.fromEntries(R.ids.map(w=>[w, !!S.box[w]]));
  }
  persist(); render();
}
function setMode(m){
  mode = m; $('m-me').setAttribute('aria-pressed', m==='me'); $('m-class').setAttribute('aria-pressed', m==='class');
  $('progress').hidden = m==='class'; $('more').hidden = m==='class';
  startSet();
}
$('m-me').addEventListener('click', ()=>setMode('me'));
$('m-class').addEventListener('click', ()=>setMode('class'));
document.addEventListener('keydown', e=>{
  if (e.target.closest && e.target.closest('input,textarea,select')) return;
  if (/^[1-4]$/.test(e.key)){ const b = document.querySelectorAll('#opts .opt')[+e.key-1]; if (b && !b.disabled) b.click(); }
});

/* Progress code: lets a student carry boxes to another device. */
$('code-copy').addEventListener('click', ()=>{
  const code = 'MD10:' + btoa(unescape(encodeURIComponent(JSON.stringify({box:S.box, days:S.days}))));
  const done = ok=>{ $('code-msg').textContent = ok ? 'Copied. Paste it on your other device.' : 'Copy failed. Select and copy the code below.'; if (!ok) $('code-in').value = code; };
  try { navigator.clipboard.writeText(code).then(()=>done(true), ()=>done(false)); } catch(e){ done(false); }
});
$('code-load').addEventListener('click', ()=>{
  const v = $('code-in').value.trim();
  try {
    if (!v.startsWith('MD10:')) throw 0;
    const d = JSON.parse(decodeURIComponent(escape(atob(v.slice(5)))));
    if (!d || typeof d.box!=='object' || typeof d.days!=='object') throw 0;
    Object.entries(d.box).forEach(([w,b])=>{ const c = S.box[w]; if (BYW[w] && b && b.b && (!c || c.n < b.n)) S.box[w] = b; });
    Object.entries(d.days).forEach(([k,x])=>{ if (!S.days[k]) S.days[k] = x; });
    save(); renderProgress(); renderStrip(); $('code-msg').textContent = 'Progress loaded and merged.'; $('code-in').value = '';
  } catch(e){ $('code-msg').textContent = 'That code didn\'t work. Copy the whole code, starting with MD10:'; }
});
let resetArm = null;
$('reset').addEventListener('click', ()=>{
  if (!resetArm){ $('reset').textContent = 'Tap again to erase all progress'; $('reset-msg').textContent = 'This can\'t be undone.'; resetArm = setTimeout(()=>{ resetArm=null; $('reset').textContent='Reset my progress'; $('reset-msg').textContent=''; }, 4000); return; }
  clearTimeout(resetArm); resetArm = null; S = blank(); save(); $('reset').textContent='Reset my progress'; $('reset-msg').textContent='Progress erased.'; renderProgress(); startSet();
});

MDC.init({game:'Daily 10', onChange:()=>{}});
MDT.mount(()=>{ if (mode==='class') startSet(); else if (R && R.phase==='main' && R.i===0 && !R.ans.length){ S.cur = null; startSet(); } else MDT.note(`${MDT.active()?MDT.label():'All topics'}: applies to your next set of new words.`); });
showStoreMsg();
renderProgress();
if (window.MDC && (MDC.classroom || MDC.teams)) setMode('class'); else startSet();
})();
</script>
'''
i = HTML.index('<script>\n(function(){')
HTML = HTML[:i] + '<script id="mdc">\n' + MOD + '\n</script>\n' + HTML[i:]
import os; os.makedirs('/home/claude/meddecode-daily10', exist_ok=True)
open('/home/claude/meddecode-daily10/meddecode-daily10.html','w').write(HTML)
print('words', len(words), 'parts', len(parts), 'bytes', len(HTML))
