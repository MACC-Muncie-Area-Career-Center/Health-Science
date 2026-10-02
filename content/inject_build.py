# Copies Jeopardy clues, synonym answers and topic tags into MedDecode Build.
import json,sys,re
sys.path.insert(0,'/home/claude/shared')
import build_tags as BT, master as M
B=json.load(open('/tmp/claude-0/bparts.json'))
clues=json.load(open('/home/claude/shared/jeop_clues.json'))
OVR={'myocarditis':{'ch':[9],'reg':['Chest']},'vertebrae':{'reg':['Back and spine']},'bronchi':{'reg':['Chest']}}
TAGS={}
for cs in B['cases']:
    w=BT.word_of(cs['ans']); t=dict(BT.tags_for_word(w,cs['ans'])); t.update(OVR.get(w,{}))
    TAGS['+'.join(cs['ans'])]={'ch':t['ch'],'reg':t['reg'],'prog':t['prog']}
TERM={t[0]:t for t in M.TERMS}
for cl in clues: TAGS['+'.join(cl['ans'])]=M.term_tags(TERM[cl['w']])
ALT={"gastroenteritis":[["enter","gastr","itis"]],"cardiomyopathy":[["my","cardi","pathy"]],"thrombocytopenia":[["thromb","penia"]],
     "postpartum":[["post","part","al"]],"intradermal":[["intra","derm","ic"]]}
for w,alts in json.load(open('/home/claude/shared/jeop_syn_alt.json')).items():
    ALT.setdefault(w,[]); [ALT[w].append(a) for a in alts if a not in ALT[w]]
p='/home/claude/meddecode-build/meddecode-build.html'; s=open(p).read()
s=re.sub(r'const JEOP = \[.*?\];\n', lambda m:'const JEOP = '+json.dumps(clues,ensure_ascii=False)+';\n', s, count=1, flags=re.S)
s=re.sub(r'const JEOP_ALT = \{.*?\};\n', lambda m:'const JEOP_ALT = '+json.dumps(ALT)+';\n', s, count=1)
s=re.sub(r'const TOPIC_TAGS = \{.*?\};\n', lambda m:'const TOPIC_TAGS = '+json.dumps(TAGS)+';\n', s, count=1)
open(p,'w').write(s); print('clues',len(clues),'alts',len(ALT),'tags',len(TAGS))
