# Builds MedDecode Say It (pronunciation practice) from the master list.
import json, re, sys
sys.path.insert(0,'/home/claude/shared')
import master as M
from topics import CSS as TCSS, HTML as THTML, JS as TJS
MOD = open('/home/claude/shared/md-classroom.js').read()

words=[]
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    syl = [s for s in re.split(r'[-\s]+', say) if s]
    stress = [i for i,s in enumerate(syl) if s.isupper() and len(s)>1]
    if len(stress)!=1 or len(syl)<2: continue
    tg = M.term_tags(t)
    bd = [[M.PARTS[p][0], M.PARTS[p][1], M.PARTS[p][2]] for _,p in parts if p!='cv']
    words.append({'w':w,'d':d,'say':say,'syl':[s.lower() for s in syl],'st':stress[0],'bd':bd,'k':kind,'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog']})

HTML = r'''<title>MedDecode Say It</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>
/* Layout: one word at a time on a "speaking card": the term, its meaning, its syllables as tappable beats,
   then three steps down the card: find the stress, listen, say it. Same tokens as the other MedDecode games. */
:root{
  --bg:#e9eeec; --surface:#f7f9f8; --ink:#16262b; --muted:#5b6d70; --line:#cdd7d5; --chip:#e1e8e6;
  --accent:#0f7a73; --accent-ink:#ffffff; --focus:#e08a00;
  --good:#1f7a3d; --bad:#b3261e; --good-bg:#e3f2e7; --bad-bg:#f9e4e2; --warn:#8a5a00; --warn-bg:#fbefd0;
  --prefix:#6a4bb3; --root:#0f7a73; --suffix:#b4531f; --beat:#fffdf6; --beat-edge:#d9cfb5;
  --font-display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --font-body:"Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --font-mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --good:#6fd08e; --bad:#ff8a80; --good-bg:#16301f; --bad-bg:#3a1a18; --warn:#ffcf70; --warn-bg:#3a2e12;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54; --beat:#1e2a2c; --beat-edge:#3a4a4c; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#0f1719; --surface:#172225; --ink:#e4ecea; --muted:#9aaeac; --line:#2b3a3d; --chip:#203034;
  --accent:#3cc2b6; --accent-ink:#06201e; --focus:#ffb84d;
  --good:#6fd08e; --bad:#ff8a80; --good-bg:#16301f; --bad-bg:#3a1a18; --warn:#ffcf70; --warn-bg:#3a2e12;
  --prefix:#a78bea; --root:#3cc2b6; --suffix:#e58a54; --beat:#1e2a2c; --beat-edge:#3a4a4c; color-scheme:dark }
*{box-sizing:border-box}
[hidden]{display:none!important}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:15px;line-height:1.45}
.wrap{max-width:980px;margin:0 auto;padding-inline:16px;padding-block:18px 56px;display:grid;gap:16px}
.wrap > *{min-width:0}
header.top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px}
.brand h1{font-family:var(--font-display);font-weight:800;font-size:clamp(26px,4vw,36px);letter-spacing:-.02em;margin:0;line-height:1}
.brand h1 span{color:var(--accent)}
.brand p{margin:6px 0 0;color:var(--muted);max-width:62ch}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--surface)}
.seg button{border:0;background:transparent;color:var(--ink);font:600 14px var(--font-body);padding:7px 13px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 15px var(--font-body);padding:9px 16px;border-radius:10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.btn:hover{border-color:var(--ink)}
.btn.primary{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.btn.rec{background:var(--bad);color:#fff;border-color:var(--bad)}
.btn:disabled{opacity:.45;cursor:not-allowed}
button:focus-visible,select:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.statusbar{display:flex;flex-wrap:wrap;gap:6px 18px;font-family:var(--font-mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.statusbar b{color:var(--ink);font-weight:600}

.card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px clamp(14px,3vw,28px) 22px;display:grid;gap:16px}
.card .top{display:flex;flex-wrap:wrap;gap:6px 12px;justify-content:space-between;align-items:baseline}
.tag{font:600 11px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.term{font:800 clamp(34px,6vw,58px)/1.02 var(--font-display);letter-spacing:-.015em;overflow-wrap:anywhere;margin:0}
.def{font-size:17px;max-width:62ch;margin:-6px 0 0}
.parts{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.p{display:inline-flex;align-items:baseline;gap:5px;font-size:13px;border-radius:7px;padding:2px 8px;background:var(--chip);border-left:4px solid var(--pc)}
.p b{font:600 13.5px var(--font-mono);color:var(--pc)}
.p[data-t="prefix"]{--pc:var(--prefix)} .p[data-t="root"]{--pc:var(--root)} .p[data-t="suffix"]{--pc:var(--suffix)}
.plus{color:var(--muted);font-size:12px}

.step{display:grid;gap:10px;border-top:1px dashed var(--line);padding-top:14px}
.step h2{margin:0;font:700 13px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);display:flex;gap:8px;align-items:center}
.step h2 .n{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--ink);color:var(--bg);font-size:12px;letter-spacing:0}
.step.done h2 .n{background:var(--good)}
.step p.hint{margin:0;color:var(--muted);font-size:14px;max-width:62ch}

/* Syllable beats: one tile per spoken beat; the stressed beat is taller once found. */
.beats{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}
.beat{min-width:64px;padding:12px 14px 10px;border-radius:12px;background:var(--beat);border:2px solid var(--beat-edge);color:var(--ink);
  font:600 clamp(20px,3vw,28px)/1 var(--font-mono);cursor:pointer;transition:transform .15s ease, background .15s ease, border-color .15s ease;display:grid;justify-items:center;gap:6px}
.beat .dot{width:8px;height:8px;border-radius:50%;background:var(--beat-edge)}
.beat:hover{transform:translateY(-2px)}
.beat.on{border-color:var(--accent)}
.beat.stress{background:var(--accent);border-color:var(--accent);color:var(--accent-ink);padding-top:22px;font-size:clamp(24px,3.6vw,34px);text-transform:uppercase}
.beat.stress .dot{background:var(--accent-ink);width:12px;height:12px}
.beat.miss{border-color:var(--bad);animation:shake .35s ease}
.beat.playing{outline:3px solid var(--focus);outline-offset:2px}
.beats.locked .beat{cursor:default}
@keyframes shake{0%,100%{translate:0}25%{translate:-5px}75%{translate:5px}}
.say-line{font:600 16px var(--font-mono);color:var(--muted)}
.say-line b{color:var(--accent)}

.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.msg{border-radius:10px;padding:10px 12px;font-size:15px}
.msg.good{background:var(--good-bg);color:var(--good)}
.msg.bad{background:var(--bad-bg);color:var(--bad)}
.msg.warn{background:var(--warn-bg);color:var(--warn)}
.msg.plain{background:var(--bg)}
.reps{display:flex;gap:8px;flex-wrap:wrap}
.rep{border:2px dashed var(--line);border-radius:12px;padding:8px 14px;font:600 14px var(--font-body);background:transparent;color:var(--muted);cursor:pointer}
.rep.done{border-style:solid;border-color:var(--good);color:var(--good);background:var(--good-bg)}
.rate{display:flex;flex-wrap:wrap;gap:8px}
.rate button{flex:1 1 140px;border:2px solid var(--line);background:var(--bg);color:var(--ink);font:700 15px var(--font-body);padding:12px;border-radius:12px;cursor:pointer}
.rate button[data-r="2"]{border-color:var(--good)} .rate button[data-r="1"]{border-color:var(--warn)} .rate button[data-r="0"]{border-color:var(--bad)}
.rate button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.level{width:160px;height:10px;border-radius:5px;background:var(--line);overflow:hidden}
.level i{display:block;height:100%;width:0;background:var(--bad);transition:width .08s linear}

/* Class echo: one huge word for the room to repeat together. */
.echo{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:clamp(18px,4vw,40px);display:grid;gap:18px;justify-items:center;text-align:center}
.echo .term{font-size:clamp(44px,9vw,110px)}
.echo .beats{justify-content:center}
.echo .cue{font:800 clamp(20px,3vw,30px) var(--font-display);color:var(--accent);min-height:1.3em}
.echo .def{margin:0;font-size:clamp(17px,2vw,24px)}

.results{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px;display:grid;gap:14px}
.results h2{font:800 26px var(--font-display);margin:0}
.bigs{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px}
.bigs div{background:var(--bg);border-radius:10px;padding:10px 12px}
.bigs b{display:block;font:800 26px var(--font-display);font-variant-numeric:tabular-nums}
.bigs span{font-size:12.5px;color:var(--muted)}
.rlist{margin:0;padding-left:18px;display:grid;gap:4px}
details.about{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px 16px}
details.about summary{cursor:pointer;font-weight:700}
details.about p{margin:8px 0 0;color:var(--muted);max-width:80ch}
@media (prefers-reduced-motion: reduce){.beat,.level i{transition:none}.beat.miss{animation:none}}
/* classroom-mode overrides */
body.mdc-classroom .term{font-size:clamp(48px,7vw,84px)}
body.mdc-classroom .beat{font-size:36px;min-width:90px;padding:16px 18px 14px}
body.mdc-classroom .beat.stress{font-size:44px;padding-top:28px}
body.mdc-classroom .def{font-size:22px}
body.mdc-classroom .btn{font-size:18px}
''' + TCSS + r'''
</style>

<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Med<span>Decode</span> Say It</h1>
      <p>Practice saying medical terms out loud. Find the stressed beat, listen to the model, then say it yourself and compare.</p>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="Mode">
        <button type="button" id="m-practice" aria-pressed="true">Practice</button>
        <button type="button" id="m-echo" aria-pressed="false">Class echo</button>
      </div>
      <div class="seg" role="group" aria-label="Word length" id="len-seg">
        <button type="button" data-len="short" aria-pressed="false">Short</button>
        <button type="button" data-len="medium" aria-pressed="false">Medium</button>
        <button type="button" data-len="long" aria-pressed="false">Long</button>
        <button type="button" data-len="mixed" aria-pressed="true">Mixed</button>
      </div>
      <button type="button" class="btn" id="new-btn">New round</button>
    </div>
  </header>
''' + THTML + r'''
  <div class="statusbar" aria-live="polite">
    <span>Word <b id="s-word">1/10</b></span>
    <span>Stress found first try <b id="s-stress">0</b></span>
    <span>Nailed it <b id="s-nailed">0</b></span>
  </div>

  <section id="practice">
    <article class="card" id="card" aria-live="polite"></article>
  </section>
  <section class="echo" id="echo" hidden aria-live="polite"></section>
  <section class="results" id="results" hidden></section>

  <details class="about">
    <summary>How Say It works (for instructors)</summary>
    <p><b>Beats and stress.</b> Each term is shown in beats from its MedDecode pronunciation (gas-TRY-tis). Students tap the beat that gets the stress before they hear it, which trains the ear for where medical words put their weight. Common patterns: -itis words stress the beat before -itis; -ology and -otomy words stress the beat before -logy or -tomy.</p>
    <p><b>Listening.</b> Hear it and Slow use the device's built-in voice. Computer voices sometimes say medical words imperfectly, so the respelling on the card is the model. Step through plays one beat at a time.</p>
    <p><b>Saying it.</b> On the MedDecode site, Record captures the student's voice in the browser so they can play it back next to the model. Nothing is uploaded or saved; the recording disappears when the next word loads. Where recording isn't allowed, students say the word aloud three times and tap each one. <b>Check my pronunciation</b> is optional and uses the browser's speech recognition; in Chrome, that audio goes to Google. Recognizers often miss medical words, so a miss does not mean the student was wrong.</p>
    <p><b>Class echo</b> is for the classroom screen: each word appears large, plays twice with a pause for the class to repeat, then moves on.</p>
    <p><b>Team mode:</b> finding the stress first try earns half points without ending the turn; the teacher's rating (Nailed it) earns full points and passes the turn.</p>
  </details>
</div>

<script>
(function(){
const WORDS = ''' + json.dumps(words, ensure_ascii=False, separators=(',',':')) + r''';
''' + TJS + r'''
const $ = id => document.getElementById(id);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ROUND = 10;
let mode = 'practice', len = 'mixed', R = null, W = null, echoTimer = null, echoPaused = false, echoGen = 0;

/* ---------- Voice ---------- */
const canSpeak = 'speechSynthesis' in window;
let voice = null;
function pickVoice(){ try { const vs = speechSynthesis.getVoices(); voice = vs.find(v=>/^en[-_]US/i.test(v.lang) && /natural|google|samantha|aria|jenny/i.test(v.name)) || vs.find(v=>/^en[-_]US/i.test(v.lang)) || vs.find(v=>/^en/i.test(v.lang)) || null; } catch(e){} }
if (canSpeak){ pickVoice(); try { speechSynthesis.onvoiceschanged = pickVoice; } catch(e){} }
function speak(text, rate, onend){
  if (!canSpeak){ if (onend) setTimeout(onend, 600); return; }
  try {
    const u = new SpeechSynthesisUtterance(text); u.rate = rate || .9; if (voice) u.voice = voice; u.lang = 'en-US';
    if (onend){ let done = false; const once = ()=>{ if (!done){ done = true; onend(); } };
      u.onend = once; u.onerror = once; setTimeout(once, 1800 + text.length*140/(rate||.9)); }
    speechSynthesis.cancel(); speechSynthesis.speak(u);
  } catch(e){ if (onend) setTimeout(onend, 600); }
}
function stepThrough(beats, word){
  let i = 0;
  const els = [...document.querySelectorAll('#'+beats+' .beat')];
  const next = ()=>{
    els.forEach(e=>e.classList.remove('playing'));
    if (i >= word.syl.length){ setTimeout(()=>speak(word.w, .85), 350); return; }
    els[i] && els[i].classList.add('playing');
    const s = word.syl[i]; i++;
    speak(s, .8, ()=>setTimeout(next, 220));
  };
  next();
}

/* ---------- Word pool ---------- */
const lenOf = w => w.syl.length<=3 ? 'short' : w.syl.length<=5 ? 'medium' : 'long';
function shuffle(a){ for (let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function balanced(arr){
  const g={}; arr.forEach(it=>{ const k=it.ch[Math.floor(Math.random()*it.ch.length)]; (g[k]=g[k]||[]).push(it); });
  const lists=Object.values(g).map(l=>shuffle(l.slice())); const out=[];
  while (lists.some(l=>l.length)){ shuffle(lists).forEach(l=>{ if (l.length) out.push(l.pop()); }); }
  return out;
}
function pickRound(list){
  let note = '';
  let pool = WORDS.filter(w=>MDT.match(w));
  if (MDT.active() && !pool.length){ pool = WORDS.slice(); note = `No terms match ${MDT.label()} yet, so this round uses all topics.`; }
  let p2 = pool.filter(w=>len==='mixed' || lenOf(w)===len);
  if (!p2.length){ p2 = pool; note = (note?note+' ':'') + 'No words of that length match, so this round uses every length.'; }
  const words = list || balanced(p2).slice(0, ROUND);
  if (!note) note = MDT.active() ? `${MDT.label()}: ${p2.length} word${p2.length===1?'':'s'} to practice.` : `All topics: ${WORDS.length} words. Choose a chapter, body region or program to focus the round.`;
  MDT.note(note);
  return words;
}

/* ---------- Practice ---------- */
function newRound(list){
  stopEcho(); stopRec();
  const words = pickRound(list);
  R = {words, i:0, stressFirst:0, nailed:0, log:[]};
  $('results').hidden = true;
  if (mode==='echo'){ $('practice').hidden = true; $('echo').hidden = false; startEcho(); }
  else { $('practice').hidden = false; $('echo').hidden = true; loadWord(); }
  renderStatus();
}
function renderStatus(){
  $('s-word').textContent = `${Math.min(R.i+1, R.words.length)}/${R.words.length}`;
  $('s-stress').textContent = R.stressFirst; $('s-nailed').textContent = R.nailed;
}
function partsHTML(w){ return w.bd.map(p=>`<span class="p" data-t="${p[1]}"><b>${esc(p[0])}</b>${esc(p[2])}</span>`).join('<span class="plus">+</span>'); }
function beatsHTML(w, id, reveal){
  return `<div class="beats${reveal?' locked':''}" id="${id}" role="group" aria-label="Beats">${w.syl.map((s,i)=>`<button type="button" class="beat${reveal && i===w.st?' stress':''}" data-i="${i}" aria-label="Beat ${i+1}: ${esc(s)}"><span>${esc(s)}</span><span class="dot" aria-hidden="true"></span></button>`).join('')}</div>`;
}
function sayLine(w){ return w.syl.map((s,i)=> i===w.st ? `<b>${esc(s.toUpperCase())}</b>` : esc(s)).join('-'); }

function loadWord(){
  stopRec();
  const w = R.words[R.i];
  W = {w, tries:0, found:false, reps:0, rating:null, recUrl:null};
  const recOK = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  $('card').innerHTML = `
    <div class="top"><span class="tag">Word ${R.i+1} of ${R.words.length} · ${w.syl.length} beats</span><span class="tag">Ch ${w.ch.join(', ')} · ${esc(w.k)}</span></div>
    <h2 class="term">${esc(w.w)}</h2>
    <p class="def">${esc(w.d)}</p>
    <div class="parts" aria-label="Word parts">${partsHTML(w)}</div>

    <section class="step" id="st1">
      <h2><span class="n">1</span> Find the stress</h2>
      <p class="hint">Which beat is said loudest and longest? Tap it.</p>
      ${beatsHTML(w,'beats',false)}
      <div id="st1-msg"></div>
    </section>

    <section class="step" id="st2">
      <h2><span class="n">2</span> Listen</h2>
      <div class="say-line" id="sayline">${esc(w.syl.join('-'))}</div>
      <div class="row">
        <button type="button" class="btn primary" id="hear" ${canSpeak?'':'disabled'}>▶ Hear it</button>
        <button type="button" class="btn" id="slow" ${canSpeak?'':'disabled'}>Slow</button>
        <button type="button" class="btn" id="steps" ${canSpeak?'':'disabled'}>Step through the beats</button>
      </div>
      ${canSpeak?'':'<p class="hint">This browser has no built-in voice. Read the respelling out loud instead.</p>'}
    </section>

    <section class="step" id="st3">
      <h2><span class="n">3</span> Say it</h2>
      <p class="hint">Say it three times: slowly by beats, then at normal speed, then as you would to a patient or coworker.</p>
      <div class="reps" id="reps">
        <button type="button" class="rep" data-k="0">1 · Slow</button>
        <button type="button" class="rep" data-k="1">2 · Normal</button>
        <button type="button" class="rep" data-k="2">3 · Like a pro</button>
      </div>
      <div class="row" id="recrow" ${recOK?'':'hidden'}>
        <button type="button" class="btn rec" id="rec">● Record</button>
        <span class="level" aria-hidden="true"><i id="lvl"></i></span>
        <button type="button" class="btn" id="mine" hidden>▶ My try</button>
        <button type="button" class="btn" id="model2" hidden ${canSpeak?'':'disabled'}>▶ Model</button>
      </div>
      <div id="recmsg"></div>
      <div class="row" ${SR?'':'hidden'}><button type="button" class="btn" id="check">Check my pronunciation</button><span class="hint" style="font-size:12.5px;color:var(--muted)">Optional. Uses the browser's speech recognition (in Chrome, audio goes to Google).</span></div>
      <div id="checkmsg"></div>
    </section>

    <section class="step" id="st4">
      <h2><span class="n">4</span> How did it go?</h2>
      <div class="rate" id="rate">
        <button type="button" data-r="2">Nailed it</button>
        <button type="button" data-r="1">Close</button>
        <button type="button" data-r="0">Need more practice</button>
      </div>
      <div class="row"><button type="button" class="btn primary" id="next" disabled>${R.i < R.words.length-1 ? 'Next word →' : 'See results →'}</button></div>
    </section>`;
  bindWord();
  renderStatus();
  if (window.MDC) MDC.hideDef();
}
function bindWord(){
  const w = W.w;
  $('beats').addEventListener('click', e=>{
    const b = e.target.closest('.beat'); if (!b) return;
    const i = +b.dataset.i;
    if (W.found){ speak(w.syl[i], .8); return; }
    W.tries++;
    if (i===w.st){
      W.found = true; const first = W.tries===1; if (first) R.stressFirst++;
      $('beats').classList.add('locked');
      document.querySelectorAll('#beats .beat').forEach(x=>x.classList.toggle('stress', +x.dataset.i===w.st));
      $('sayline').innerHTML = sayLine(w);
      $('st1').classList.add('done');
      $('st1-msg').innerHTML = `<div class="msg good"><b>${first?'Right on the first try.':'Got it.'}</b> The stress falls on <b>${esc(w.syl[w.st].toUpperCase())}</b>: ${sayLine(w)}.</div>`;
      if (window.MDC) MDC.play(first, {mult:.5, keepTurn:true, label:'Found the stress', missLabel:'Stress found, no points'});
      renderStatus();
      speak(w.w, .85);
    } else {
      b.classList.remove('miss'); void b.offsetWidth; b.classList.add('miss');
      if (W.tries>=2){
        $('st1-msg').innerHTML = `<div class="msg warn">Listen for the loudest beat: press <b>Hear it</b>, then tap again.</div>`;
      } else $('st1-msg').innerHTML = `<div class="msg bad">Not that beat. Try another.</div>`;
    }
  });
  $('hear').addEventListener('click', ()=>speak(w.w, .9));
  $('slow').addEventListener('click', ()=>speak(w.w, .55));
  $('steps').addEventListener('click', ()=>stepThrough('beats', w));
  $('reps').addEventListener('click', e=>{ const b=e.target.closest('.rep'); if (!b) return; b.classList.add('done'); W.reps = document.querySelectorAll('#reps .rep.done').length; if (W.reps===3) $('st3').classList.add('done'); });
  const rec = $('rec'); if (rec) rec.addEventListener('click', toggleRec);
  $('mine').addEventListener('click', ()=>{ if (W.recUrl){ const a = new Audio(W.recUrl); a.play().catch(()=>{}); } });
  $('model2').addEventListener('click', ()=>speak(w.w, .9));
  const ck = $('check'); if (ck) ck.addEventListener('click', checkPron);
  $('rate').addEventListener('click', e=>{
    const b = e.target.closest('button[data-r]'); if (!b || W.rating!==null) return;
    W.rating = +b.dataset.r;
    $('rate').querySelectorAll('button').forEach(x=>{ x.setAttribute('aria-pressed', x===b); x.disabled = x!==b; });
    if (W.rating===2) R.nailed++;
    $('st4').classList.add('done');
    R.log.push({w:w.w, rating:W.rating, stressFirst:W.found && W.tries===1, found:W.found});
    if (window.MDC){ MDC.play(W.rating===2, {label:'Nailed it: '+w.w, missLabel: W.rating===1?'Close, no points':'Keep practicing'}); MDC.define({term:w.w, say:w.say, def:w.d, kind:'Say it', parts:w.bd.map(p=>({form:p[0], m:p[2], type:p[1]}))}); }
    $('next').disabled = false; $('next').focus();
    renderStatus();
  });
  $('next').addEventListener('click', ()=>{ if (R.i < R.words.length-1){ R.i++; loadWord(); window.scrollTo({top:$('card').offsetTop-12, behavior:'smooth'}); } else finish(); });
}

/* ---------- Recording (works where the browser allows the microphone) ---------- */
let mr = null, stream = null, chunks = [], raf = null, actx = null;
async function toggleRec(){
  if (mr && mr.state==='recording'){ mr.stop(); return; }
  try {
    stream = await navigator.mediaDevices.getUserMedia({audio:true});
  } catch(e){
    $('recrow').hidden = true;
    $('recmsg').innerHTML = `<div class="msg plain">Recording isn't available here${location.protocol==='file:'?'':' (the browser or this page blocked the microphone)'}. Say the word out loud and tap the three steps above instead. On the MedDecode site, Record lets you hear yourself.</div>`;
    return;
  }
  chunks = [];
  mr = new MediaRecorder(stream);
  mr.ondataavailable = e=>{ if (e.data.size) chunks.push(e.data); };
  mr.onstop = ()=>{
    if (W.recUrl) URL.revokeObjectURL(W.recUrl);
    W.recUrl = URL.createObjectURL(new Blob(chunks, {type: mr.mimeType || 'audio/webm'}));
    stopStream();
    $('rec').textContent = '● Record again'; $('mine').hidden = false; $('model2').hidden = false;
    const a = new Audio(W.recUrl); a.play().catch(()=>{});
    $('reps').querySelectorAll('.rep:not(.done)')[0]?.classList.add('done');
  };
  mr.start(); $('rec').textContent = '■ Stop';
  meter();
  setTimeout(()=>{ if (mr && mr.state==='recording') mr.stop(); }, 6000);
}
function meter(){
  try {
    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    const src = actx.createMediaStreamSource(stream), an = actx.createAnalyser(); an.fftSize = 512; src.connect(an);
    const buf = new Uint8Array(an.fftSize);
    const tick = ()=>{ an.getByteTimeDomainData(buf); let m=0; for (const v of buf) m=Math.max(m, Math.abs(v-128)); const el=$('lvl'); if (el) el.style.width = Math.min(100, m*1.6)+'%'; if (mr && mr.state==='recording') raf = requestAnimationFrame(tick); else if (el) el.style.width='0'; };
    tick();
  } catch(e){}
}
function stopStream(){ if (stream){ stream.getTracks().forEach(t=>t.stop()); stream = null; } if (raf) cancelAnimationFrame(raf); }
function stopRec(){ try { if (mr && mr.state==='recording'){ mr.onstop = null; mr.stop(); } } catch(e){} mr = null; stopStream(); }

/* ---------- Optional speech-recognition check ---------- */
function lev(a,b){ const m=a.length,n=b.length,d=Array.from({length:m+1},(_,i)=>[i]); for(let j=1;j<=n;j++) d[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++) d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]===b[j-1]?0:1)); return d[m][n]; }
function checkPron(){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition; if (!SR) return;
  const w = W.w, out = $('checkmsg');
  let r;
  try { r = new SR(); } catch(e){ out.innerHTML = '<div class="msg plain">Speech recognition is not available in this browser.</div>'; return; }
  r.lang = 'en-US'; r.maxAlternatives = 5; r.interimResults = false;
  out.innerHTML = '<div class="msg plain">Listening… say the word once.</div>';
  r.onresult = e=>{
    const alts = [...e.results[0]].map(a=>a.transcript.toLowerCase().replace(/[^a-z]/g,''));
    const target = w.w.replace(/[^a-z]/g,'');
    const best = alts.map(a=>({a, s:1 - lev(a,target)/Math.max(a.length,target.length)})).sort((x,y)=>y.s-x.s)[0];
    const heard = esc(e.results[0][0].transcript);
    if (best.s>=.85) out.innerHTML = `<div class="msg good"><b>Recognized.</b> It heard “${heard}”.</div>`;
    else if (best.s>=.6) out.innerHTML = `<div class="msg warn"><b>Close.</b> It heard “${heard}”. Recognizers often struggle with medical words, so compare with the model too.</div>`;
    else out.innerHTML = `<div class="msg plain">It heard “${heard}”. That doesn't mean you were wrong: medical words are hard for recognizers. Compare with the model and try once more.</div>`;
  };
  r.onerror = e=>{ out.innerHTML = `<div class="msg plain">${e.error==='not-allowed'||e.error==='service-not-allowed' ? 'The microphone is blocked here, so the check can\'t run.' : 'Nothing was recognized. Try again, a little closer to the microphone.'}</div>`; };
  try { r.start(); } catch(e){}
}

/* ---------- Class echo ---------- */
function startEcho(){ R.i = 0; echoPaused = false; renderEcho(); }
function stopEcho(){ echoGen++; clearTimeout(echoTimer); echoTimer = null; try{ if (canSpeak) speechSynthesis.cancel(); }catch(e){} }
function renderEcho(){
  stopEcho();
  const w = R.words[R.i];
  $('echo').innerHTML = `
    <span class="tag">Word ${R.i+1} of ${R.words.length} · Ch ${w.ch.join(', ')}</span>
    <h2 class="term">${esc(w.w)}</h2>
    ${beatsHTML(w,'ebeats',true)}
    <div class="say-line">${sayLine(w)}</div>
    <p class="def">${esc(w.d)}</p>
    <div class="cue" id="cue">Listen…</div>
    <div class="row" style="justify-content:center">
      <button type="button" class="btn" id="e-prev">← Back</button>
      <button type="button" class="btn" id="e-again">Say it again</button>
      <button type="button" class="btn" id="e-pause">${echoPaused?'Resume':'Pause'}</button>
      <button type="button" class="btn primary" id="e-next">${R.i<R.words.length-1?'Next →':'Finish'}</button>
    </div>`;
  renderStatus();
  $('e-prev').addEventListener('click', ()=>{ if (R.i>0){ R.i--; renderEcho(); } });
  $('e-next').addEventListener('click', ()=>{ if (R.i<R.words.length-1){ R.i++; renderEcho(); } else { stopEcho(); finishEcho(); } });
  $('e-again').addEventListener('click', ()=>{ const p=echoPaused; echoPaused=false; stopEcho(); runEcho(w, true); echoPaused=p; });
  $('e-pause').addEventListener('click', ()=>{ echoPaused = !echoPaused; $('e-pause').textContent = echoPaused?'Resume':'Pause'; if (echoPaused) stopEcho(); else runEcho(w); });
  $('ebeats').addEventListener('click', e=>{ const b=e.target.closest('.beat'); if (b) speak(w.syl[+b.dataset.i], .8); });
  if (window.MDC) MDC.define({term:w.w, say:w.say, def:w.d, kind:'Class echo', parts:w.bd.map(p=>({form:p[0], m:p[2], type:p[1]}))});
  if (!echoPaused) runEcho(w);
}
function runEcho(w, once){
  const gen = echoGen, live = ()=> gen===echoGen && mode==='echo' && !echoPaused;
  const cue = t=>{ if (!live()) return; const c=$('cue'); if (c) c.textContent = t; };
  const speakE = (t, r, cb)=> speak(t, r, ()=>{ if (live() && cb) cb(); });
  const gap = Math.max(2200, w.syl.length*650);
  cue('Listen…');
  speakE(w.w, .8, ()=>{ cue('Your turn: say it together'); echoTimer = setTimeout(()=>{
    if (!live()) return;
    if (once) { cue('Listen…'); speakE(w.w, .9, ()=>cue('Again: all together')); return; }
    cue('Listen again…'); speakE(w.w, .9, ()=>{ cue('Your turn again'); echoTimer = setTimeout(()=>{ if (!live()) return; if (R.i<R.words.length-1){ R.i++; renderEcho(); } else cue('Done. Press Next or Back.'); }, gap); });
  }, gap); });
}
function finishEcho(){
  $('echo').hidden = true;
  const R2 = $('results'); R2.hidden = false;
  R2.innerHTML = `<h2>Class echo complete</h2><p style="margin:0;color:var(--muted)">${R.words.length} words: ${R.words.map(w=>esc(w.w)).join(', ')}.</p><div class="row"><button type="button" class="btn primary" id="again">Another round</button></div>`;
  $('again').addEventListener('click', ()=>newRound());
}

/* ---------- Results ---------- */
function finish(){
  stopRec();
  $('practice').hidden = true;
  const again = R.log.filter(l=>l.rating===0 || l.rating===1 || !l.stressFirst).map(l=>l.w);
  const R2 = $('results'); R2.hidden = false;
  const lab = {2:'Nailed it', 1:'Close', 0:'Need more practice'};
  R2.innerHTML = `<h2>${R.nailed>=8?'Great speaking!':R.nailed>=5?'Good progress':'Keep practicing'}</h2>
    <div class="bigs">
      <div><b>${R.words.length}</b><span>Words practiced</span></div>
      <div><b>${R.stressFirst}/${R.words.length}</b><span>Stress found on the first try</span></div>
      <div><b>${R.nailed}</b><span>Rated "Nailed it"</span></div>
    </div>
    <ul class="rlist">${R.log.map(l=>{ const w = R.words.find(x=>x.w===l.w); return `<li><b>${esc(l.w)}</b> <span style="font-family:var(--font-mono);color:var(--muted)">${sayLine(w)}</span> · ${lab[l.rating]}${l.stressFirst?'':' · stress missed'}</li>`; }).join('')}</ul>
    <div class="row">
      ${again.length ? `<button type="button" class="btn primary" id="redo">Practice these ${again.length} again</button>` : ''}
      <button type="button" class="btn${again.length?'':' primary'}" id="again">New round</button>
    </div>`;
  if ($('redo')) $('redo').addEventListener('click', ()=>newRound(R.words.filter(w=>again.includes(w.w))));
  $('again').addEventListener('click', ()=>newRound());
  renderStatus();
  R2.scrollIntoView({behavior:'smooth', block:'start'});
}

/* ---------- Controls ---------- */
function setMode(m){ mode = m; $('m-practice').setAttribute('aria-pressed', m==='practice'); $('m-echo').setAttribute('aria-pressed', m==='echo'); newRound(); }
$('m-practice').addEventListener('click', ()=>setMode('practice'));
$('m-echo').addEventListener('click', ()=>setMode('echo'));
document.querySelectorAll('[data-len]').forEach(b=>b.addEventListener('click', ()=>{ len = b.dataset.len; document.querySelectorAll('[data-len]').forEach(x=>x.setAttribute('aria-pressed', x===b)); newRound(); }));
$('new-btn').addEventListener('click', ()=>newRound());
MDC.init({game:'Say It', onChange:()=>{}});
MDT.mount(()=>newRound());
newRound();
})();
</script>
'''
i = HTML.index('<script>\n(function(){')
HTML = HTML[:i] + '<script id="mdc">\n' + MOD + '\n</script>\n' + HTML[i:]
open('/home/claude/meddecode-sayit/meddecode-sayit.html','w').write(HTML)
print('words', len(words), 'bytes', len(HTML))
