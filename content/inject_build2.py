# Copies Jeopardy clues, synonym answers and topic tags into MedDecode Build (keeps the case tags already in the page).
import json, sys, re
sys.path.insert(0,'/home/claude/shared')
import master as M
clues = json.load(open('/home/claude/shared/jeop_clues.json'))
p = '/home/claude/meddecode-build/meddecode-build.html'; s = open(p).read()
TAGS = json.loads(re.search(r'const TOPIC_TAGS = (\{.*?\});\n', s).group(1))
ALT = json.loads(re.search(r'const JEOP_ALT = (\{.*?\});\n', s).group(1))
TERM = {t[0]:t for t in M.TERMS}
for cl in clues: TAGS['+'.join(cl['ans'])] = M.term_tags(TERM[cl['w']])
for w, alts in json.load(open('/home/claude/shared/jeop_syn_alt.json')).items():
    ALT.setdefault(w, []); [ALT[w].append(a) for a in alts if a not in ALT[w]]
s = re.sub(r'const JEOP = \[.*?\];\n', lambda m: 'const JEOP = '+json.dumps(clues, ensure_ascii=False)+';\n', s, count=1, flags=re.S)
s = re.sub(r'const JEOP_ALT = \{.*?\};\n', lambda m: 'const JEOP_ALT = '+json.dumps(ALT)+';\n', s, count=1)
s = re.sub(r'const TOPIC_TAGS = \{.*?\};\n', lambda m: 'const TOPIC_TAGS = '+json.dumps(TAGS)+';\n', s, count=1)
open(p,'w').write(s); print('clues', len(clues), 'alts', len(ALT), 'tags', len(TAGS))
