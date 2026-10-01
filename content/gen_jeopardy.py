import json, random, sys, itertools
sys.path.insert(0,'/home/claude/shared')
from master import PARTS as MP, TERMS
B=json.load(open('/tmp/claude-0/bparts.json')); P=B['parts']
LEXW={e['w'] for e in B['lex']}
DICT=set(w.strip().lower() for w in open('/usr/share/dict/american-english-insane'))
def assemble(ids):
    w=''
    for i,pid in enumerate(ids):
        p=P[pid]; s=p['stem']
        if i>0:
            prev=P[ids[i-1]]
            if prev['type']=='root':
                keep=(p['type']=='root' or s[0] not in 'aeiou') and not p.get('noCV')
                if keep: w+=prev['cv']
            if w and w[-1] in 'aeiou' and w[-1]==s[0]: s=s[1:]
        w+=s
    return w
def bid(l,pid): return 'an' if (pid=='a' and l=='an') else pid
ANS={t[0]:[bid(l,p) for l,p in t[1] if p!='cv'] for t in TERMS}
for w,ids in ANS.items(): assert assemble(ids)==w,(w,assemble(ids))
CATS={
 "It's Inflamed":['gastritis','hepatitis','nephritis','dermatitis','cystitis','laryngitis','phlebitis','encephalitis','glossitis','gingivitis','colitis','pericarditis','gastroenteritis','osteoarthritis'],
 'That Hurts!':['neuralgia','myalgia','cephalalgia','otalgia','odontalgia','arthralgia'],
 'Under the Knife':['appendectomy','tonsillectomy','cholecystectomy','craniotomy','tracheostomy','rhinoplasty','angioplasty'],
 'Blood Work':['leukocyte','erythrocyte','thrombocyte','leukopenia','anemia','hematuria','hypoglycemia','hyperglycemia','cyanosis','thrombosis'],
 'Breathe and Beat':['apnea','tachypnea','dyspnea','bradycardia','tachycardia','hypertension','cardiomegaly'],
 'Study and Scope':['dermatology','neurology','pathology','ophthalmology','bronchoscopy','endoscopy','electrocardiogram'],
 'Grab Bag':['hepatomegaly','lipoma','neuropathy','rhinorrhea','polyuria','dysphagia','hemiplegia','diarrhea','subcutaneous','osteoporosis'],
}
used=set(sum(CATS.values(),[])); assert used=={t[0] for t in TERMS}, set(t[0] for t in TERMS)-used
TERM={t[0]:t for t in TERMS}
JUNKLEN=5
def buildable(tray):
    pre=[i for i in tray if P[i]['type']=='prefix']; roots=[i for i in tray if P[i]['type']=='root']; tails=[i for i in tray if P[i]['type'] in('suffix','ending')]
    out=set()
    rs=[()]+[c for n in (1,2,3) for c in itertools.permutations(roots,n)]
    for p in [None]+pre:
        for r in rs:
            for t in tails+[None]:
                ids=([p] if p else [])+list(r)+([t] if t else [])
                if len(ids)<2: continue
                out.add(assemble(ids))
    return out
FILL=[k for k,v in P.items() if k not in ('dent','tic','graph','i','ae','es','is','us','ix','ices','um','a_s','olig','pro','dia','inter','epi','tension','por','cutane','electr','colon','tonsill')]
rng=random.Random(11)
clues=[]; unknown_all={}
for cat,words in CATS.items():
    for w in words:
        ans=ANS[w]
        sibs=[x for x in words if x!=w]
        best=None
        for attempt in range(400):
            tray=list(dict.fromkeys(ans))
            for s in rng.sample(sibs, min(2,len(sibs))):
                for i in ANS[s]:
                    if i not in tray and len(tray)<8: tray.append(i)
            types=lambda t:[P[i]['type'] for i in t]
            while len(tray)<10:
                need = 'prefix' if types(tray).count('prefix')<2 else ('suffix' if types(tray).count('suffix')<3 else ('root' if types(tray).count('root')<3 else None))
                pool=[i for i in FILL if i not in tray and (need is None or P[i]['type']==need)]
                tray.append(rng.choice(pool))
            words_b=buildable(tray)
            unk=[x for x in words_b if x in DICT and x not in LEXW and len(x)>JUNKLEN]
            # a second correct answer: any other term with the same definition (none in the master list), or an accepted synonym
            score=len(unk)
            if best is None or score<best[0]: best=(score,tray,unk)
            if score==0: break
        score,tray,unk=best
        for u in unk: unknown_all[u]=w
        t=TERM[w]
        lvl={'easy':0,'medium':1,'hard':2}[t[6]]
        clues.append({'cat':cat,'w':w,'clue':t[2][0].upper()+t[2][1:]+'.','ans':ans,'tray':tray,'say':t[3],'kind':t[4],'body':t[5],'rank':lvl*100+len(w)})
json.dump(clues,open('/home/claude/shared/jeop_clues.json','w'))
print('clues',len(clues),'cats',len(CATS))
print('unknown real-word hits left:',len(unknown_all))
for u,w in sorted(unknown_all.items()): print(' ',u,'(tray for',w,')')
