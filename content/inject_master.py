# Copies generated master-list content into Tiles, Dissect and Sort.
import json, re
J = lambda o: json.dumps(o, ensure_ascii=False)
G = '/home/claude/'
pairs = json.load(open('/home/claude/shared/tiles_pairs.json'))
diss = json.load(open('/home/claude/shared/dissect_terms.json'))
sorti = json.load(open('/home/claude/shared/sort_items.json'))

# Tiles
p = G+'meddecode-tiles/meddecode-tiles.html'; s = open(p).read()
s = re.sub(r'const ALL_PAIRS = \[.*?\];\n', lambda m: 'const ALL_PAIRS = '+J(pairs)+';\n', s, count=1, flags=re.S)
open(p,'w').write(s)

# Dissect: keep the hand-written terms, regenerate the block after the marker
MK = '  // Added from the MedDecode master list\n'
p = G+'meddecode-dissect/meddecode-dissect.html'; s = open(p).read()
i = s.index(MK); j = s.index('\n];', i)
hand = set(re.findall(r"\{w:'([^']+)'", s[:i]))
lines = []
for d in diss:
    if d['w'] in hand: continue
    ps = ','.join(f"CV({J(x['t'])})" if x['type']=='cv' else f"P({J(x['t'])},'{x['type']}',{J(x['m'])},{J(x['form'])})" for x in d['parts'])
    note = f", note:{J(d['note'])}" if d['note'] else ''
    lines.append(f"  {{w:{J(d['w'])}, lvl:'{d['lvl']}', def:{J(d['def'])}, say:{J(d['say'])},\n   parts:[{ps}]{note}, ch:{J(d['ch'])}}}")
s = s[:i] + MK + ',\n'.join(lines) + s[j:]
open(p,'w').write(s)
print('dissect: hand', len(hand), 'from master', len(lines))

# Sort
p = G+'meddecode-sort/meddecode-sort.html'; s = open(p).read()
i = s.index(MK); j = s.index('\n];', i)
hand = set(re.findall(r"\{t:'([^']+)'", s[:i]))
lines = []
for it in sorti:
    if it['t'] in hand: continue
    extra = f", c:'{it['c']}'" if it.get('c') else ''
    say = f", say:{J(it['say'])}" if it.get('say') else ''
    lines.append(f"  {{t:{J(it['t'])}, k:'{it['k']}'{extra}, n:{J(it['n'])}{say}, ch:{J(it.get('ch',[1]))}}}")
s = s[:i] + MK + ',\n'.join(lines) + s[j:]
open(p,'w').write(s)
print('sort: hand', len(hand), 'from master', len(lines))
