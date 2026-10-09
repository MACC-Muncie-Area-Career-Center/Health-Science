# Builds "MedDecode the Unknown" (decode unfamiliar textbook terms from their word parts) from the master list.
import json, sys, re
sys.path.insert(0,'/home/claude/shared')
import master as M
from topics import CSS as TCSS, HTML as THTML, JS as TJS
MOD = open('/home/claude/shared/md-classroom.js').read()
D10 = open('/home/claude/shared/gen_daily10.py').read()
BASECSS = D10[D10.index(':root{'):D10.index('/* Today strip')]

grp = {}
for i,g in enumerate(M.SYN_GROUPS):
    for w in g: grp[w] = i
words=[]
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    bd = []
    for letters,pid in parts:
        if pid=='cv': continue
        P = M.PARTS[pid]
        bd.append([P[0], P[1], P[2], min(M.part_tags(pid)['ch']), pid])
    if len(bd) < 2: continue
    tg = M.term_tags(t)
    words.append({'w':w,'d':d,'od':re.sub(r'\s*\((as in|same as)[^)]*\)','',d),'say':say,'k':kind,'sys':sysn,'sp':[l for l,_ in parts],'st':['cv' if p=='cv' else M.PARTS[p][1] for _,p in parts],
                  'bd':bd,'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':grp.get(w,-1)})

HTML = r'''<title>MedDecode the Unknown</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
/* Layout: a "case file" per word. The unfamiliar term sits at the top; below it a ladder of clues that cost points
   (split it, then each part's meaning, read from the end), then four meanings to choose from. Same tokens as the other games. */
''' + BASECSS + r'''
.statusbar{display:flex;flex-wrap:wrap;gap:6px 18px;font-family:var(--font-mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.statusbar b{color:var(--ink);font-weight:600}
.setrow{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
.setrow label{display:flex;align-items:center;gap:6px;font:600 14px var(--font-body);min-width:0}
.setrow select{font:500 14px var(--font-body);color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 8px;max-width:100%;min-width:0}
.setrow .tlabel{font:700 12px var(--font-body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.setrow .note{font-size:13px;color:var(--muted);flex-basis:100%}
@media (max-width:560px){ .setrow label{flex:1 1 100%} .setrow select{flex:1} }

.card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px clamp(14px,3vw,28px) 22px;display:grid;gap:14px}
.card .top{display:flex;flex-wrap:wrap;gap:6px 12px;justify-content:space-between;align-items:baseline}
.tag{font:600 11px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.worth{font:700 12px var(--font-mono);border-radius:999px;padding:3px 10px;background:var(--accent);color:var(--accent-ink)}
.worth.low{background:var(--chip);color:var(--ink)}
.unk{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}
.term{font:800 clamp(34px,6.5vw,60px)/1.02 var(--font-display);letter-spacing:-.015em;overflow-wrap:anywhere;margin:0;display:flex;flex-wrap:wrap;align-items:baseline}
.term .sg{border-radius:0;padding:0}
.term.split .sg{border-bottom:5px solid var(--pc);padding:0 2px}
.term.split .sg + .sg{margin-left:10px}
.term .sg[data-t="prefix"]{--pc:var(--prefix)} .term .sg[data-t="root"]{--pc:var(--root)} .term .sg[data-t="suffix"]{--pc:var(--suffix)} .term .sg[data-t="cv"]{--pc:var(--line);color:var(--muted)}
.ask{margin:0;color:var(--muted);font-weight:700}
.clues{display:grid;gap:8px;border-top:1px dashed var(--line);padding-top:12px}
.clues h2{margin:0;font:700 13px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.clist{display:grid;gap:6px;margin:0;padding:0;list-style:none}
.clist li{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;background:var(--bg);border-radius:10px;padding:8px 12px;border-left:4px solid var(--pc,var(--line))}
.clist li[data-t="prefix"]{--pc:var(--prefix)} .clist li[data-t="root"]{--pc:var(--root)} .clist li[data-t="suffix"]{--pc:var(--suffix)}
.clist b{font:700 15px var(--font-mono);color:var(--pc,var(--ink))}
.clist .m{font-size:16px;font-weight:700}
.clist .kn{font:600 11px var(--font-mono);letter-spacing:.05em;text-transform:uppercase;color:var(--good);background:var(--good-bg);border-radius:999px;padding:2px 8px}
.clist .ty{font:600 11px var(--font-mono);letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:8px}
.opt{display:flex;gap:10px;align-items:flex-start;text-align:left;border:2px solid var(--line);background:var(--bg);color:var(--ink);font:600 16px/1.3 var(--font-body);padding:12px 14px;border-radius:12px;cursor:pointer;min-height:56px}
.opt .k{flex:none;display:inline-grid;place-items:center;width:24px;height:24px;border-radius:6px;background:var(--chip);font:700 12px var(--font-mono);color:var(--muted)}
.opt:hover:not(:disabled){border-color:var(--ink)}
.opt.right{border-color:var(--good);background:var(--good-bg);color:var(--good)}
.opt.wrong{border-color:var(--bad);background:var(--bad-bg);color:var(--bad)}
.opt:disabled{cursor:default}
.opt:disabled:not(.right):not(.wrong){opacity:.55}
.guess{border:2px dashed var(--line);border-radius:12px;padding:14px;display:grid;gap:8px;justify-items:start}
.guess p{margin:0;color:var(--muted)}
.fb{border-radius:12px;padding:12px 14px;display:grid;gap:10px}
.fb.good{background:var(--good-bg)} .fb.bad{background:var(--bad-bg)}
.fb .h{font-weight:700} .fb.good .h{color:var(--good)} .fb.bad .h{color:var(--bad)}
.fb .w{font:800 22px var(--font-display)} .fb .say{font:600 15px var(--font-mono);color:var(--muted);margin-left:8px}
.read{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.read .p{display:inline-flex;align-items:baseline;gap:5px;font-size:14px;border-radius:7px;padding:3px 9px;background:var(--surface);border-left:4px solid var(--pc)}
.read .p b{font:700 14px var(--font-mono);color:var(--pc)}
.read .p[data-t="prefix"]{--pc:var(--prefix)} .read .p[data-t="root"]{--pc:var(--root)} .read .p[data-t="suffix"]{--pc:var(--suffix)}
.read .ar{color:var(--muted);font:700 14px var(--font-mono)}
.fb .lbl{font:700 11px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.also{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px}
.also span b{font-family:var(--font-mono)}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px;display:grid;gap:14px}
.panel h2{font:800 26px var(--font-display);margin:0}
.panel h3{font:700 13px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.bigs{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.bigs div{background:var(--bg);border-radius:10px;padding:10px 12px}
.bigs b{display:block;font:800 26px var(--font-display);font-variant-numeric:tabular-nums}
.bigs span{font-size:12.5px;color:var(--muted)}
.rlist{margin:0;padding:0;list-style:none;display:grid;gap:4px}
.rlist li{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.rlist .mk{font:700 13px var(--font-mono);width:18px;flex:none}
.rlist .mk.ok{color:var(--good)} .rlist .mk.no{color:var(--bad)}
.rlist .d{color:var(--muted);font-size:14px}
.rlist .c{font:600 12px var(--font-mono);color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips span{font-size:14px;background:var(--bg);border-radius:8px;padding:4px 10px}
.chips b{font-family:var(--font-mono)}
details.about{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px 16px}
details.about summary{cursor:pointer;font-weight:700}
details.about p{margin:8px 0 0;color:var(--muted);max-width:80ch}
body.mdc-classroom .term{font-size:clamp(52px,7vw,92px)}
body.mdc-classroom .opt{font-size:24px;padding:18px;min-height:80px}
body.mdc-classroom .clist .m{font-size:24px} body.mdc-classroom .clist b{font-size:22px}
''' + TCSS + r'''
</style>

<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Med<span>Decode</span> the Unknown</h1>
      <p>Every word here is one you may not have learned yet. Work out what it means from its parts. Each clue costs a point, so try before you peek.</p>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="Choices">
        <button type="button" id="c-show" aria-pressed="true">Show choices</button>
        <button type="button" id="c-guess" aria-pressed="false">Guess first</button>
      </div>
      <button type="button" class="btn" id="new-btn">New round</button>
    </div>
  </header>
''' + THTML + r'''
  <div class="setrow" role="group" aria-label="What students have covered">
    <span class="tlabel">Covered so far</span>
    <label>Chapters <select id="thru"></select></label>
    <span class="note" id="thru-note"></span>
  </div>
  <div class="statusbar" aria-live="polite">
    <span>Word <b id="s-word">1/10</b></span>
    <span>Points <b id="s-pts">0</b></span>
    <span>No-clue decodes <b id="s-clean">0</b></span>
  </div>

  <article class="card" id="card" aria-live="polite"></article>
  <section class="panel" id="results" hidden></section>

  <details class="about">
    <summary>How Decode the Unknown works (for instructors)</summary>
    <p><b>The skill.</b> Students meet a term they may not have studied and work out its meaning from its parts, the way they will on the job. Every term is from <i>Acquiring Medical Language</i>; meanings, splits and pronunciations are written by MedDecode.</p>
    <p><b>Clues cost points.</b> A word is worth 5 points with no clues. Clue 1 splits the word into its parts. The next clues give each part's meaning, starting from the end of the word (the suffix usually says what kind of word it is), then the prefix, then the roots. A correct answer earns 5 minus the clues used (at least 1).</p>
    <p><b>The wrong choices share parts with the answer</b> (for <i>gastritis</i>: stomach pain, inflammation of the colon), so students have to decode every part, not just spot one.</p>
    <p><b>Covered so far.</b> Set this to the chapters your class has finished, then press <b>Copy student link</b>. Words then come from chapters the class hasn't reached yet, and any part already covered is marked <b>You know this</b>. On the MedDecode site, words a student hasn't met in Daily 10 are chosen first.</p>
    <p><b>Guess first</b> hides the four choices until the student (or the class) has said a guess out loud. It turns on automatically in Classroom mode. With Team mode on, each word is one team's turn, worth the same points as solo play.</p>
  </details>
</div>

<script>
(function(){
const WORDS = ''' + json.dumps(words, ensure_ascii=False, separators=(',',':')) + r''';
const CHAP = ''' + json.dumps({str(k):v for k,v in M.CHAPTERS.items()}) + r''';
''' + TJS + r'''
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ROUND = 10, MAXPTS = 5;
const norm = s => String(s).toLowerCase().replace(/[^a-z]/g,'');
function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function balanced(arr){
  const g={}; arr.forEach(it=>{ const k=it.ch[Math.floor(Math.random()*it.ch.length)]; (g[k]=g[k]||[]).push(it); });
  const lists=Object.values(g).map(l=>shuffle(l.slice())); const out=[];
  while (lists.some(l=>l.length)){ shuffle(lists).forEach(l=>{ if (l.length) out.push(l.pop()); }); }
  return out;
}
const sameMeaning = (a,b) => (a.g>=0 && a.g===b.g) || norm(a.d)===norm(b.d);

/* Words this student has already met in Daily 10 (same site only). */
let seenD10 = {};
try { const s = JSON.parse(localStorage.getItem('md-daily10-v1')||'null'); if (s && s.box) seenD10 = s.box; } catch(e){}

/* ---------- Voice ---------- */
const canSpeak = 'speechSynthesis' in window;
let voice = null;
function pickVoice(){ try { const vs = speechSynthesis.getVoices(); voice = vs.find(v=>/^en[-_]US/i.test(v.lang) && /natural|google|samantha|aria|jenny/i.test(v.name)) || vs.find(v=>/^en[-_]US/i.test(v.lang)) || vs.find(v=>/^en/i.test(v.lang)) || null; } catch(e){} }
if (canSpeak){ pickVoice(); try { speechSynthesis.onvoiceschanged = pickVoice; } catch(e){} }
function speak(text, rate){ if (!canSpeak) return; try { const u = new SpeechSynthesisUtterance(text); u.rate = rate||.85; if (voice) u.voice = voice; u.lang='en-US'; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch(e){} }

/* ---------- Covered-so-far setting ---------- */
let thru = 0, guessFirst = false, R = null;
try { const q = +new URLSearchParams(location.search).get('through'); if (q>=1 && q<=12) thru = q; } catch(e){}
window.MDT_EXTRA = () => ({through: thru ? String(thru) : ''});
$('thru').innerHTML = '<option value="0">Not set (all words)</option>' + Object.keys(CHAP).map(Number).filter(n=>n<13).map(n=>`<option value="${n}">${n===1?'Chapter 1':'Chapters 1–'+n}</option>`).join('');
$('thru').value = String(thru);
$('thru').addEventListener('change', e=>{ thru = +e.target.value; newRound(); });
const known = p => thru && p[3] <= thru;

/* ---------- Round ---------- */
function pickRound(){
  let note = '';
  let pool = WORDS.filter(w=>MDT.match(w));
  if (MDT.active() && !pool.length){ pool = WORDS.slice(); note = `No terms match ${MDT.label()} yet, so this round uses all topics. `; }
  let p2 = pool;
  if (thru){
    p2 = pool.filter(w=>w.ch.every(c=>c>thru) && w.bd.some(known));
    const withRoot = p2.filter(w=>w.bd.some(p=>p[1]==='root' && known(p)));
    if (withRoot.length >= ROUND) p2 = withRoot;
    if (!p2.length){ p2 = pool; $('thru-note').textContent = `No words in this topic come from chapters after ${thru}, so this round uses the whole topic.`; }
    else $('thru-note').textContent = `Words come from chapters ${thru+1}–13, the ones your class hasn't reached. Parts from Chapters 1–${thru} are marked "You know this".`;
  } else $('thru-note').textContent = 'Set this to the chapters your class has finished, and words will come from the chapters ahead.';
  const fresh = p2.filter(w=>!seenD10[w.w]), met = p2.filter(w=>seenD10[w.w]);
  const words = balanced(fresh).concat(balanced(met)).slice(0, ROUND);
  MDT.note(note + (MDT.active() ? `${MDT.label()}: ${p2.length} word${p2.length===1?'':'s'} to decode.` : `All topics: ${p2.length} words to decode.`));
  return words;
}
function newRound(){
  const words = pickRound();
  R = {words, i:0, pts:0, clean:0, log:[]};
  $('results').hidden = true; $('card').hidden = false;
  loadWord();
}
function distractors(w){
  const ids = new Set(w.bd.map(p=>p[4]));
  const share = shuffle(WORDS.filter(x=>x.w!==w.w && !sameMeaning(x,w) && x.bd.some(p=>ids.has(p[4]))));
  // prefer one sharing the suffix and one sharing a root
  const suf = w.bd.filter(p=>p[1]==='suffix').map(p=>p[4]), roots = w.bd.filter(p=>p[1]!=='suffix').map(p=>p[4]);
  const out = [];
  const add = x => { if (x && out.length<3 && !out.some(o=>o.w===x.w || sameMeaning(o,x))) out.push(x); };
  add(share.find(x=>x.bd.some(p=>roots.includes(p[4]))));
  add(share.find(x=>x.bd.some(p=>suf.includes(p[4]))));
  share.forEach(add);
  shuffle(WORDS.filter(x=>x.w!==w.w && !sameMeaning(x,w) && x.sys===w.sys)).forEach(add);
  shuffle(WORDS.filter(x=>x.w!==w.w && !sameMeaning(x,w))).forEach(add);
  return out;
}
/* Reading order: suffix first, then prefix, then roots left to right. */
function readOrder(w){ return w.bd.filter(p=>p[1]==='suffix').concat(w.bd.filter(p=>p[1]==='prefix'), w.bd.filter(p=>p[1]==='root')); }
const segTypes = w => w.st;

/* ---------- One word ---------- */
let W = null;
function loadWord(){
  const w = R.words[R.i];
  W = {w, clues:0, done:false, order:readOrder(w), opts:shuffle([w].concat(distractors(w))), shown:!guessFirst};
  renderCard();
  renderStatus();
  if (window.MDC) MDC.hideDef();
}
function worth(){ return Math.max(1, MAXPTS - W.clues); }
function renderStatus(){
  $('s-word').textContent = `${Math.min(R.i+1,R.words.length)}/${R.words.length}`;
  $('s-pts').textContent = R.pts; $('s-clean').textContent = R.clean;
}
function termHTML(w, split){
  const types = segTypes(w);
  return `<h2 class="term${split?' split':''}" aria-label="${esc(w.w)}">${w.sp.map((s,i)=>`<span class="sg" data-t="${split?types[i]:''}">${esc(s)}</span>`).join('')}</h2>`;
}
function nextClueLabel(){
  if (W.clues===0) return 'Clue: split it into parts';
  const p = W.order[W.clues-1]; if (!p) return '';
  return `Clue: what does ${p[1]==='suffix'?'the ending':p[1]==='prefix'?'the beginning':'the root'} ${p[0]} mean?`;
}
function cluesHTML(){
  if (!W.clues) return '';
  const items = W.order.slice(0, W.clues-1).map(p=>`<li data-t="${p[1]}"><b>${esc(p[0])}</b><span class="ty">${esc(p[1])}</span><span class="m">${esc(p[2])}</span>${known(p)?'<span class="kn">You know this</span>':''}</li>`).join('');
  const parts = `<li><span class="m">${W.w.bd.length} parts: ${W.w.bd.map(p=>`<b style="color:var(--${p[1]})">${esc(p[0])}</b>`).join(' + ')}</span></li>`;
  return parts + items;
}
function renderCard(){
  const w = W.w, maxClues = 1 + W.order.length;
  const pill = seenD10[w.w] ? '' : '<span class="tag">New to you</span>';
  $('card').innerHTML = `
    <div class="top"><span class="tag">Word ${R.i+1} of ${R.words.length} · Ch ${w.ch.join(', ')} · ${esc(w.k)}</span><span class="worth${W.clues?' low':''}" id="worth">Worth ${worth()} pt${worth()===1?'':'s'}</span></div>
    <div class="unk">${termHTML(w, W.clues>0)}</div>
    <div class="row">${canSpeak?'<button type="button" class="btn" id="hear">▶ Hear it</button>':''}${pill}</div>
    <section class="clues" id="clues">
      <h2>Clues (each costs 1 point)</h2>
      <ul class="clist" id="clist">${cluesHTML()}</ul>
      <div class="row"><button type="button" class="btn" id="clue" ${W.clues>=maxClues||W.done?'hidden':''}>${esc(nextClueLabel())}</button></div>
    </section>
    <p class="ask">What does it mean?</p>
    <div id="choices">${W.shown ? optsHTML() : `<div class="guess"><p>Say your guess out loud first, or write it down. Then show the choices.</p><button type="button" class="btn primary" id="reveal">I have a guess: show choices</button></div>`}</div>
    <div id="fb"></div>`;
  const h = $('hear'); if (h) h.addEventListener('click', ()=>speak(w.w));
  $('clue').addEventListener('click', ()=>{ if (W.done) return; W.clues++; renderCard(); const c=$('clue'); if (c && !c.hidden) c.focus(); });
  const rv = $('reveal'); if (rv) rv.addEventListener('click', ()=>{ W.shown = true; renderCard(); });
  bindOpts();
}
function optsHTML(){
  return `<div class="opts" id="opts">${W.opts.map((o,i)=>`<button type="button" class="opt" data-w="${esc(o.w)}"><span class="k">${i+1}</span><span>${esc(o.od)}</span></button>`).join('')}</div>`;
}
function bindOpts(){
  const o = $('opts'); if (!o) return;
  o.addEventListener('click', e=>{ const b = e.target.closest('.opt'); if (!b || b.disabled || W.done) return; answer(b); });
}
function answer(b){
  const w = W.w, ok = b.dataset.w === w.w;
  W.done = true;
  document.querySelectorAll('#opts .opt').forEach(x=>{ x.disabled = true; if (x.dataset.w===w.w) x.classList.add('right'); });
  if (!ok) b.classList.add('wrong');
  $('clue').hidden = true;
  const pts = ok ? worth() : 0;
  R.pts += pts; if (ok && !W.clues) R.clean++;
  const chosen = WORDS.find(x=>x.w===b.dataset.w);
  R.log.push({w:w.w, ok, clues:W.clues, pts, chose: ok?null:chosen.w});
  const ro = W.order;
  const read = ro.map((p,i)=>`<span class="p" data-t="${p[1]}"><b>${esc(p[0])}</b>${esc(p[2])}</span>${i<ro.length-1?'<span class="ar">→</span>':''}`).join('');
  const ids = new Set(w.bd.map(p=>p[4]));
  const also = w.bd.map(p=>{ const ex = WORDS.filter(x=>x.w!==w.w && x.bd.some(q=>q[4]===p[4])).slice(0,3).map(x=>x.w); return ex.length ? `<span><b style="color:var(--${p[1]})">${esc(p[0])}</b> also in ${ex.map(esc).join(', ')}</span>` : ''; }).join('');
  let why = '';
  if (!ok){
    const diff = chosen.bd.filter(p=>!ids.has(p[4])).map(p=>`${p[0]} (${p[2]})`);
    why = `You chose the meaning of <b>${esc(chosen.w)}</b>${diff.length?`, which uses ${diff.map(esc).join(' + ')}`:''}.`;
  }
  $('fb').innerHTML = `<div class="fb ${ok?'good':'bad'}">
    <div class="h">${ok ? (W.clues ? `Decoded with ${W.clues} clue${W.clues===1?'':'s'}: +${pts}` : `Decoded with no clues: +${pts}`) : 'Not quite.'} ${why}</div>
    <div><span class="w">${esc(w.w)}</span><span class="say">${esc(w.say)}</span></div>
    <div class="lbl">Read it from the end</div>
    <div class="read">${read}</div>
    <div><b>Meaning:</b> ${esc(w.d)}</div>
    ${also?`<div class="lbl">Where else these parts show up</div><div class="also">${also}</div>`:''}
    <div class="row">${canSpeak?'<button type="button" class="btn" id="fb-hear">▶ Hear it</button>':''}<button type="button" class="btn primary" id="next">${R.i<R.words.length-1?'Next word →':'See results →'}</button></div>
  </div>`;
  // show the full split now
  document.querySelector('#card .unk').innerHTML = termHTML(w, true);
  const fh = $('fb-hear'); if (fh) fh.addEventListener('click', ()=>speak(w.w));
  $('next').addEventListener('click', ()=>{ if (R.i < R.words.length-1){ R.i++; loadWord(); window.scrollTo({top:Math.max(0,$('card').offsetTop-12), behavior:'smooth'}); } else finish(); });
  $('next').focus({preventScroll:true});
  $('fb').scrollIntoView({block:'nearest', behavior:'smooth'});
  if (window.MDC){ MDC.play(ok, {points:pts, label:w.w, missLabel:'No points: '+w.w}); MDC.define({term:w.w, say:w.say, def:w.d, kind:'Decoded', parts:w.bd.map(p=>({form:p[0], m:p[2], type:p[1]}))}); }
  renderStatus();
}
function finish(){
  $('card').hidden = true;
  const P = $('results'); P.hidden = false;
  const n = R.words.length, right = R.log.filter(l=>l.ok).length, max = n*MAXPTS;
  const avg = (R.log.reduce((a,l)=>a+l.clues,0)/n).toFixed(1);
  const review = {};
  R.log.forEach(l=>{ if (!l.ok || l.clues>1){ const w = R.words.find(x=>x.w===l.w); readOrder(w).slice(0, l.ok ? Math.max(0,l.clues-1) : 9).forEach(p=>{ review[p[4]] = p; }); } });
  const rv = Object.values(review);
  P.innerHTML = `<h2>${R.pts>=max*.8?'Expert decoder!':R.pts>=max*.55?'Solid decoding':'Keep decoding'}</h2>
    <div class="bigs">
      <div><b>${R.pts}/${max}</b><span>Points</span></div>
      <div><b>${right}/${n}</b><span>Decoded correctly</span></div>
      <div><b>${R.clean}</b><span>With no clues</span></div>
      <div><b>${avg}</b><span>Clues per word</span></div>
    </div>
    <ul class="rlist">${R.log.map(l=>{ const w = R.words.find(x=>x.w===l.w); return `<li><span class="mk ${l.ok?'ok':'no'}">${l.ok?'✓':'✗'}</span><b>${esc(w.w)}</b><span class="d">${esc(w.d)}</span><span class="c">${l.clues} clue${l.clues===1?'':'s'} · +${l.pts}</span></li>`; }).join('')}</ul>
    ${rv.length?`<h3>Word parts to review</h3><div class="chips">${rv.map(p=>`<span><b style="color:var(--${p[1]})">${esc(p[0])}</b> ${esc(p[2])}</span>`).join('')}</div>`:''}
    <div class="row"><button type="button" class="btn primary" id="again">New round</button></div>`;
  $('again').addEventListener('click', newRound);
  renderStatus();
  P.scrollIntoView({behavior:'smooth', block:'start'});
}

/* ---------- Controls ---------- */
function setGuess(g){ guessFirst = g; $('c-show').setAttribute('aria-pressed', !g); $('c-guess').setAttribute('aria-pressed', g); if (W && !W.done){ W.shown = !g; renderCard(); } }
$('c-show').addEventListener('click', ()=>setGuess(false));
$('c-guess').addEventListener('click', ()=>setGuess(true));
$('new-btn').addEventListener('click', newRound);
document.addEventListener('keydown', e=>{
  if (e.target.closest && e.target.closest('input,textarea,select')) return;
  if (/^[1-4]$/.test(e.key)){ const b = document.querySelectorAll('#opts .opt')[+e.key-1]; if (b && !b.disabled) b.click(); }
});
MDC.init({game:'Decode the Unknown', onChange:()=>{}});
MDT.mount(()=>newRound());
if (window.MDC && MDC.classroom) setGuess(true);
newRound();
})();
</script>
'''
i = HTML.index('<script>\n(function(){')
HTML = HTML[:i] + '<script id="mdc">\n' + MOD + '\n</script>\n' + HTML[i:]
import os; os.makedirs('/home/claude/meddecode-unknown', exist_ok=True)
open('/home/claude/meddecode-unknown/meddecode-unknown.html','w').write(HTML)
print('words', len(words), 'bytes', len(HTML))
