import json, random, re, sys
sys.path.insert(0, '/home/claude/shared')
from master import PARTS, TERMS, part_tags, term_tags, SYN_OF

TYPE_NAME = {'prefix':'prefix','root':'root','suffix':'suffix'}
IMAGE_ROOTS = {'cardi':'heart','hepat':'liver','nephr':'kidney','oste':'bone'}

def P(pid):
    form,typ,m,say,sysname,tile,ck = PARTS[pid]
    return dict(id=pid, form=form, type=typ, m=m, say=say, sys=sysname, tile=tile, ck=ck)

# ---------- checks ----------
errors = []
for w,parts,d,say,kind,sysname,lvl in TERMS:
    if ''.join(l for l,_ in parts) != w: errors.append(f'{w}: parts spell {"".join(l for l,_ in parts)}')
    for l,pid in parts:
        if pid!='cv' and pid not in PARTS: errors.append(f'{w}: unknown part {pid}')
words = [t[0] for t in TERMS]
if len(words)!=len(set(words)): errors.append('duplicate terms')
if errors: print('\n'.join(errors)); sys.exit(1)

def term_parts(t):
    return [P(pid) for l,pid in t[1] if pid!='cv']

def examples_for(pid, exclude=None, n=3):
    ex = [t[0] for t in TERMS if any(p==pid for _,p in t[1]) and t[0]!=exclude]
    return ex[:n]

def breakdown(t):
    return ' + '.join(f"{p['form']} ({p['m']})" for p in term_parts(t))

# ---------- Tiles pairs ----------
rng = random.Random(7)
all_meanings = {}
for pid in PARTS: all_meanings.setdefault(PARTS[pid][1],[]).append(PARTS[pid][2])

pairs = []
n = 0
for pid,(form,typ,m,say,sysname,tile,ck) in PARTS.items():
    if not tile: continue
    n += 1
    ex = examples_for(pid)
    if typ=='root' and pid in IMAGE_ROOTS:
        b = {'icon':IMAGE_ROOTS[pid], 'text':m, 'kind':'anatomy'}; sett='Root → Anatomy'
    else:
        b = {'text':m, 'kind':'meaning'}; sett = 'Root → Meaning' if typ=='root' else 'Affix → Meaning'
    explain = f"{form} is {'the combining form' if typ=='root' else 'a '+typ} meaning {m}."
    nudge = (f"Think of a term you know: {ex[0]}." if ex else f"{form} is a {typ}.")
    pairs.append({'id':f'p-{pid}','set':sett,'system':sysname,'a':{'text':form,'kind':typ},'b':b,'say':say,'speak':form.split(',')[0].replace('/o','o').strip('-'),
                  'explain':explain,'examples':ex or [form],'nudge':nudge,'uses':[pid],'ck':ck or ('m:'+m), **part_tags(pid)})
for t in TERMS:
    w,parts,d,say,kind,sysname,lvl = t
    tp = term_parts(t)
    real = [p for p in tp if p['m']]
    correct = ', '.join(f"{p['form']} = {p['m']}" for p in real)
    # two distractors: swap in meanings from other parts of the same type
    opts=set(); tries=0
    while len(opts)<2 and tries<200:
        tries+=1
        fake=[]
        for p in real:
            pool=[PARTS[q][2] for q in PARTS if PARTS[q][1]==p['type'] and PARTS[q][2]!=p['m']]
            fake.append(f"{p['form']} = {rng.choice(pool) if rng.random()<0.7 or len(real)==1 else p['m']}")
        s=', '.join(fake)
        if s!=correct: opts.add(s)
    options=[correct]+sorted(opts); rng.shuffle(options)
    ex=[]
    for p in tp:
        for e in examples_for(p['id'], exclude=w):
            if e not in ex: ex.append(e)
    pairs.append({'id':f't-{w}','set':'Term → Definition','system':sysname,'a':{'text':w,'kind':'term'},'b':{'text':d,'kind':'definition'},'say':say,'speak':w,
                  'explain':f"{breakdown(t)} = {d}.",'parts':[[p['form'],p['m']] for p in real],'examples':ex[:3] or [w],
                  'nudge':f"Break it down: {tp[0]['form']} means {tp[0]['m']}.",
                  'quiz':{'q':'Why do these tiles match?','options':options,'answer':options.index(correct)},
                  'uses':[p['id'] for p in tp],'ck':'t:'+(SYN_OF[w][0] if w in SYN_OF else w), **term_tags(t)})
json.dump(pairs, open('/home/claude/shared/tiles_pairs.json','w'))

# ---------- Dissect terms ----------
diss=[]
for t in TERMS:
    w,parts,d,say,kind,sysname,lvl = t
    seg=[]
    prev=None
    note=''
    for i,(l,pid) in enumerate(parts):
        if pid=='cv': seg.append({'t':l,'type':'cv'}); continue
        p=P(pid); seg.append({'t':l,'type':p['type'],'m':p['m'],'form':p['form']})
    # automatic teaching note for a dropped combining vowel
    for i in range(len(parts)-1):
        a,b=parts[i],parts[i+1]
        if a[1]!='cv' and PARTS[a[1]][1]=='root' and b[1]!='cv' and PARTS[b[1]][1]=='suffix' and b[0][0] in 'aeiou':
            note=f"The o of {PARTS[a[1]][0]} is dropped because {PARTS[b[1]][0]} begins with a vowel."
    lv = lvl if lvl!='easy' else 'easy'
    roots=[p for p in parts if p[1]!='cv' and PARTS[p[1]][1]=='root']
    if len(roots)>=2: lv='hard'
    elif any(p[1]!='cv' and PARTS[p[1]][1]=='prefix' for p in parts): lv='medium'
    else: lv='easy'
    diss.append({'w':w,'lvl':lv,'def':d,'say':say,'parts':seg,'note':note, **term_tags(t)})
json.dump(diss, open('/home/claude/shared/dissect_terms.json','w'))

# ---------- Sort items ----------
CAT = {'condition':'dx','symptom':'sx','sign':'sx','procedure':'tx','test':'test','body part':'body','medication':'tx'}
sort_items=[]
for t in TERMS:
    w,parts,d,say,kind,sysname,lvl = t
    if kind not in CAT: continue
    sort_items.append({'t':w,'k':'term','c':CAT[kind],'n':f"{breakdown(t)}: {d}.",'say':say, **term_tags(t)})
for pid,(form,typ,m,say,sysname,tile,ck) in PARTS.items():
    if typ=='root' and tile and sysname not in ('General',) and pid not in ('glyc','phag','path','crin','phas','psych','men','nat','part','ox','ur','gnos','eti','immun','gynec','hem','scler','lith','orth','hydr','calc','melan','myc','acr'):
        sort_items.append({'t':form,'k':'root','c':'body','n':f"{form} means {m}.",'say':say})
SUF_CAT={'pathy':'dx','rrhea':'sx','plegia':'sx','penia':'dx','ostomy':'tx','osis':'dx','oma':'dx','itis':'dx','ectomy':'tx','otomy':'tx','plasty':'tx','algia':'sx','megaly':'sx','scopy':'test','gram':'test'}
for pid,c in SUF_CAT.items():
    form,typ,m,say,*_ = PARTS[pid]
    sort_items.append({'t':form,'k':'suffix','c':c,'n':f"{form} means {m}.",'say':say})
for pid in ('hemi','a','dia','tachy','brady','hyper','hypo','dys','peri','sub','poly','endo'):
    form,typ,m,say,*_ = PARTS[pid]
    sort_items.append({'t':form,'k':'prefix','n':f"{form} means {m}.",'say':say})
from master import PHRASES
for ph in PHRASES:
    if not ph['c']: continue
    it={'t':ph['t'],'k':'phrase' if ' ' in ph['t'] else 'term','c':ph['c'],'n':ph['d'][0].upper()+ph['d'][1:]+'.','ch':ph['ch'],'reg':['Abdomen and pelvis'],'prog':['EMT','CNA','CCMA']}
    if ph['say']: it['say']=ph['say']
    sort_items.append(it)
json.dump(sort_items, open('/home/claude/shared/sort_items.json','w'))
print(f'tiles pairs: {len(pairs)} ({sum(1 for p in pairs if p["id"].startswith("t-"))} terms) | dissect terms: {len(diss)} | sort items from master: {len(sort_items)}')
