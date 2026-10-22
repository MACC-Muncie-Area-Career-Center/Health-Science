# Refreshes the word data in MedDecode Translator from the master list (terms and phrases a chart note can use).
import json, re, sys
sys.path.insert(0,'/home/claude/shared')
import master as M
SLOT = {'condition':'dx','symptom':'cc','sign':'exam','test':'test','procedure':'plan','specialist':'ref','medication':'med','instrument':'tool'}
grp = {w:i for i,g in enumerate(M.SYN_GROUPS) for w in g}
MALE = ('prostat','erect','testi','testic','penis','penile','scrot','sperm','semen','semin','circumcis','vasectom','orchi','epididym')
words = []
for t in M.TERMS:
    w,parts,d,say,kind,sysn,lvl = t
    if kind not in SLOT: continue
    tg = M.term_tags(t)
    words.append({'w':w,'d':d,'say':say,'k':kind,'s':SLOT[kind],'sys':sysn,
                  'bd':[[M.PARTS[p][0],M.PARTS[p][1],M.PARTS[p][2]] for _,p in parts if p!='cv'],
                  'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':grp.get(w,-1)})
have = {x['w'] for x in words}
for ph in M.PHRASES:
    if ph['kind'] not in SLOT or ph['t'] in have: continue
    tg = M.phrase_tags(ph); low = (ph['t']+' '+ph['d']).lower()
    sysn = M._CH_SYS.get(tg['ch'][0], 'General')
    if 12 in tg['ch'] and any(k in low for k in MALE): sysn = 'Male reproductive'
    words.append({'w':ph['t'],'d':ph['d'],'say':ph['say'] or '','k':ph['kind'],'s':SLOT[ph['kind']],'sys':sysn,'bd':[],
                  'ch':tg['ch'],'reg':tg['reg'],'prog':tg['prog'],'g':grp.get(ph['t'],-1)})
p = '/home/claude/meddecode-translator/meddecode-translator.html'; s = open(p).read()
s = re.sub(r'const WORDS = \[.*?\];\n', lambda m: 'const WORDS = '+json.dumps(words, ensure_ascii=False)+';\n', s, count=1, flags=re.S)
open(p,'w').write(s)
print('translator words', len(words))
