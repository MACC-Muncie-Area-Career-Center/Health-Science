import re, sys
MOD = open('/home/claude/shared/md-classroom.js').read()
def inject(s):
    # (re)insert the shared module as its own script, just before the game's main script
    s = re.sub(r'<script id="mdc">.*?</script>\n', '', s, flags=re.S)
    i = s.index('<script>\n(function(){')
    return s[:i] + '<script id="mdc">\n' + MOD + '\n</script>\n' + s[i:]
def rep(s, a, b, name):
    if b in s: return s  # already patched
    assert a in s, f'{name}: missing anchor {a[:60]!r}'
    return s.replace(a, b, 1)
def css(s, block, name):
    if '/* classroom-mode overrides */' in s: return s
    return rep(s, '</style>', '/* classroom-mode overrides */\n' + block + '\n</style>', name)

# ---------- Tiles ----------
f='/home/claude/meddecode-tiles/meddecode-tiles.html'; s=open(f).read()
if 'MDC.classroom)?Math.max(64' not in s: s=rep(s,"unit = Math.max(38, Math.min(64, Math.floor((w-14)/8)));","unit = Math.max(38, Math.min((window.MDC&&MDC.classroom)?Math.max(64, Math.floor((window.innerHeight-170)/10)):64, Math.floor((w-14)/8)));",'tiles')
s=rep(s,"    showMatch(pr);\n    refreshTiles(); renderStats();",
"""    showMatch(pr);
    if (window.MDC){ MDC.play(true,{label:`${pr.a.text} = ${pr.b.text}`}); MDC.define({term:pr.a.text, say:pr.say, def:pr.explain, kind:pr.set, parts:(pr.parts||[]).map(([f,m])=>({form:f,m})), note:'Also see: '+pr.examples.join(', ')}); }
    refreshTiles(); renderStats();""",'tiles')
s=rep(s,"    showWrong(first,t);\n","    showWrong(first,t);\n    if (window.MDC) MDC.play(false,{missLabel:'Not a pair'});\n",'tiles')
if "MDC.init({game:'Tiles'" not in s: s=rep(s,"newGame();\n})();","MDC.init({game:'Tiles', onChange:()=>{ renderBoard(); }});\nnewGame();\n})();",'tiles')
s=css(s,"""body.mdc-classroom .main{grid-template-columns:minmax(0,1fr) 420px}
body.mdc-classroom aside.panel h2{font-size:32px}
body.mdc-classroom aside.panel{font-size:18px}
body.mdc-classroom .stats{font-size:17px}
body.mdc-classroom .tile .band{font-size:12px;padding:7px 4px 6px}""",'tiles')
open(f,'w').write(inject(s))

# ---------- Sort ----------
f='/home/claude/meddecode-sort/meddecode-sort.html'; s=open(f).read()
s=rep(s,"    setFeedback(binId!==main?'warn':'good', msg, it);\n    render(); flash(binId,'good');",
"""    setFeedback(binId!==main?'warn':'good', msg, it);
    render(); flash(binId,'good');
    if (window.MDC){ MDC.play(true,{label:`${it.img?'Picture: '+it.t:it.t} → ${bin.name}`}); MDC.define({term:it.img?('Picture: '+it.t):it.t, say:it.say, def:it.n, kind:bin.name, note:binId!==main?(it.alt||''):''}); }""",'sort')
s=rep(s,"    setFeedback('bad', `<b>Incorrect.</b>","    if (window.MDC) MDC.play(false,{missLabel:'Not '+bin.name});\n    setFeedback('bad', `<b>Incorrect.</b>",'sort')
s=rep(s,"    setFeedback('bad', msg, S.tries[id]>=2 ? it : null);","    if (window.MDC) MDC.play(false,{missLabel:'Not '+bin.name});\n    setFeedback('bad', msg, S.tries[id]>=2 ? it : null);",'sort')
if "MDC.init({game:'Sort'" not in s: s=rep(s,"newRound();\n})();","MDC.init({game:'Sort', onChange:()=>{ render(); }});\nnewRound();\n})();",'sort')
s=css(s,"""body.mdc-classroom .card{min-width:130px;min-height:84px;padding:12px 18px 10px}
body.mdc-classroom .card .t{font-size:25px}
body.mdc-classroom .card .k{font-size:12px}
body.mdc-classroom .card svg{width:64px;height:64px}
body.mdc-classroom .bins{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
body.mdc-classroom .bin{min-height:170px}
body.mdc-classroom .bin .name{font-size:23px}
body.mdc-classroom .bin .def{font-size:15px}
body.mdc-classroom .chip{font-size:17px;padding:6px 10px}
body.mdc-classroom .feedback{font-size:20px}
body.mdc-classroom .question{font-size:26px}""",'sort')
open(f,'w').write(inject(s))

# ---------- Dissect ----------
f='/home/claude/meddecode-dissect/meddecode-dissect.html'; s=open(f).read()
s=rep(s,"return Math.max(18, Math.min(60, Math.floor(w / (n*0.7 + 1))));","return Math.max(18, Math.min((window.MDC&&MDC.classroom)?120:60, Math.floor(w / (n*0.7 + 1))));",'dissect')
s=rep(s,"  if (T.tries>=2) $('show-btn').hidden=false;\n}","  if (T.tries>=2) $('show-btn').hidden=false;\n  if (window.MDC) MDC.play(false,{missLabel:'Not quite: next team, same specimen'});\n}",'dissect')
s=rep(s,"  renderDissection(parts);\n",
"""  renderDissection(parts);
  if (window.MDC){ MDC.play(!shown,{label:'Clean dissection: '+T.term.w, missLabel:'Answer shown'}); MDC.define({term:T.term.w, say:T.term.say, def:T.term.def, parts:parts.filter(p=>p.type!=='cv').map(p=>({form:p.form, m:p.m, type:p.type})), note:T.term.note||''}); }
""",'dissect')
if "MDC.init({game:'Dissect'" not in s: s=rep(s,"newRound();\n})();","MDC.init({game:'Dissect', onChange:()=>{ if (T) renderWord(); }});\nnewRound();\n})();",'dissect')
s=css(s,"""body.mdc-classroom .mat{padding:60px 16px 54px}
body.mdc-classroom .task h2{font-size:28px}
body.mdc-classroom .feedback{font-size:20px}
body.mdc-classroom .part .form{font-size:28px}
body.mdc-classroom .part .mean{font-size:18px}
body.mdc-classroom .equals{font-size:22px}
body.mdc-classroom .equals b{font-size:28px}
body.mdc-classroom .statusbar{font-size:17px}""",'dissect')
open(f,'w').write(inject(s))

# ---------- Build ----------
f='/home/claude/meddecode-build/meddecode-build.html'; s=open(f).read()
s=rep(s,"  if (key===target || alts.includes(key)){ C.builtAlt = key!==target ? LEX_BY_KEY[key] : null; succeed(false); return; }",
"  if (key===target || alts.includes(key)){ C.builtAlt = key!==target ? LEX_BY_KEY[key] : null; succeed(false); if (window.MDC){ const e=LEX_BY_KEY[target]; MDC.play(true,{label:'Built: '+e.w}); } return; }",'build')
s=rep(s,"  } else if (C.checks>=3) $('giveup-btn').hidden=false;\n  setFeedback(cls, html);\n}",
"  } else if (C.checks>=3) $('giveup-btn').hidden=false;\n  setFeedback(cls, html);\n  if (window.MDC){ MDC.play(false,{missLabel: entry ? 'Real word, but not the answer' : 'Not a recognized term'}); if (entry) MDC.define({term:entry.w, def:entry.def, kind:entry.kind, parts:C.rack.map(id=>({form:PARTS[id].disp, m:PARTS[id].m, type:PARTS[id].type})), note:'A real term, but not the answer to this case.'}); }\n}",'build')
s=rep(s,"  renderFile();\n  $('check-btn').hidden=true;",
"""  renderFile();
  if (window.MDC){ if (revealed) MDC.play(false,{missLabel:'Answer shown'}); const e=LEX_BY_KEY[C.cs.ans.join('+')]; MDC.define({term:e.w, say:C.cs.say, def:e.def, kind:C.cs.kind, parts:C.cs.ans.map(id=>({form:PARTS[id].disp, m:PARTS[id].m, type:PARTS[id].type})), note:'Body part affected: '+C.cs.body}); }
  $('check-btn').hidden=true;""",'build')
if "MDC.init({game:'Build'" not in s: s=rep(s,"newRound();\n})();","MDC.init({game:'Build', onChange:()=>{ if (C) render(); }});\nnewRound();\n})();",'build')
s=css(s,"""body.mdc-classroom .case p{font-size:23px}
body.mdc-classroom .tile{min-width:118px;min-height:96px;padding:20px 16px 16px}
body.mdc-classroom .tile .t{font-size:27px}
body.mdc-classroom .tile .m{font-size:14px;max-width:150px}
body.mdc-classroom .tile .k{font-size:10.5px}
body.mdc-classroom .rack{min-height:130px}
body.mdc-classroom .assembled .word{font-size:46px}
body.mdc-classroom .readout{font-size:18px}
body.mdc-classroom .feedback{font-size:20px}
body.mdc-classroom .statusbar{font-size:17px}""",'build')
open(f,'w').write(inject(s))

# ---------- Encounter ----------
f='/home/claude/meddecode-encounter/meddecode-encounter.html'; s=open(f).read()
s=rep(s,"  const repeat = E.asked.includes(id);\n","  const repeat = E.asked.includes(id);\n  const keysBefore = E.sc.key.filter(k=>keyHit(k)).length;\n",'enc')
s=rep(s,"  $('suggest').innerHTML='';\n  renderAll();\n",
"""  $('suggest').innerHTML='';
  renderAll();
  if (window.MDC){
    const gained = E.sc.key.filter(k=>keyHit(k)).length > keysBefore;
    MDC.play(gained,{label:'Key question found', missLabel:repeat?'Already asked':'Useful, but not a key question'});
    if (newF.length){ const f=newF.find(x=>x.red)||newF[0]; MDC.define({term:f.t, def:f.d, kind:sc.name, note:'In plain words: '+f.lay}); }
  }
""",'enc')
s=rep(s,"    $('end-why').innerHTML =","    if (window.MDC) MDC.play(!!o[1],{mult:3, label:'Best decision', missLabel:'Not the best decision'});\n    $('end-why').innerHTML =",'enc')
s=rep(s,"    box.querySelector('.cw').innerHTML =","    if (window.MDC){ MDC.play(ok,{label:'Chart term: '+ans, missLabel:'Not the right term'}); MDC.define({term:ans, def:why, kind:'Chart it'}); }\n    box.querySelector('.cw').innerHTML =",'enc')
if "MDC.init({game:'Encounter'" not in s: s=rep(s,"renderSetup(); applyMode(); renderPicker();","MDC.init({game:'Encounter', onChange:()=>{ if (E && !E.done) renderAll(); }});\nrenderSetup(); applyMode(); renderPicker();",'enc')
s=css(s,"""body.mdc-classroom .msg{font-size:20px;max-width:80%}
body.mdc-classroom .msg .by{font-size:12px}
body.mdc-classroom .transcript{max-height:52vh}
body.mdc-classroom .pt-card .name{font-size:26px}
body.mdc-classroom .pt-card .scene{font-size:17px}
body.mdc-classroom .findings li{font-size:18px}
body.mdc-classroom .findings .def{font-size:15px}
body.mdc-classroom .vitals b{font-size:21px}
body.mdc-classroom .ask-row select,body.mdc-classroom .ask-row input[type=text]{font-size:19px;padding:12px}
body.mdc-classroom .actions .btn{font-size:17px;padding:10px 14px}
body.mdc-classroom .opt{font-size:19px;padding:14px 16px}
body.mdc-classroom .wrapup h2{font-size:30px}
body.mdc-classroom .scard h3{font-size:23px}""",'enc')
open(f,'w').write(inject(s))
print('patched all five')

# ---------- Say It (generated; just refresh the shared module) ----------
f='/home/claude/meddecode-sayit/meddecode-sayit.html'; s=open(f).read(); open(f,'w').write(inject(s))
# ---------- Daily 10 (generated; just refresh the shared module) ----------
f='/home/claude/meddecode-daily10/meddecode-daily10.html'; s=open(f).read(); open(f,'w').write(inject(s))
# ---------- Decode the Unknown (generated; just refresh the shared module) ----------
f='/home/claude/meddecode-unknown/meddecode-unknown.html'; s=open(f).read(); open(f,'w').write(inject(s))
# ---------- Body Map (generated; just refresh the shared module) ----------
f='/home/claude/meddecode-bodymap/meddecode-bodymap.html'; s=open(f).read(); open(f,'w').write(inject(s))
