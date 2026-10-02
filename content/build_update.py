# Adds new master-list word parts and terms to MedDecode Build (PARTS and LEX).
import re, json, sys
sys.path.insert(0,'/home/claude/shared')
from master import PARTS as MP, TERMS
p='/home/claude/meddecode-build/meddecode-build.html'; s=open(p).read()
i=s.index('const PARTS = {};'); j=s.index('const LEX')
have=set(re.findall(r"""part\(["']([^"']+)["']""", s[i:j]))
NOCV={'tic'}
lines=[]
for pid,(form,typ,m,say,sysname,tile,ck) in MP.items():
    if pid in have or pid in ('us','um','is'): continue
    if typ=='prefix':
        stem=form.split('/')[0].rstrip('-').split(',')[0]
        lines.append(f"part({json.dumps(pid)},'prefix',{json.dumps(form)},{json.dumps(stem)},{json.dumps(m)});")
    elif typ=='root':
        stem=form.split('/')[0]
        lines.append(f"part({json.dumps(pid)},'root',{json.dumps(form)},{json.dumps(stem)},{json.dumps(m)},{{\"body\": {json.dumps(m)}}});")
    else:
        stem=form.lstrip('-')
        lines.append(f"part({json.dumps(pid)},'suffix',{json.dumps(form)},{json.dumps(stem)},{json.dumps(m)}{',{noCV:true}' if pid in NOCV else ''});")
if lines:
    k=s.index('// singular and plural endings')
    s=s[:k]+'// added with the Oct 2026 master-list expansion\n'+'\n'.join(lines)+'\n'+s[k:]
print('parts added',len(lines))
# LEX
i=s.index('const LEX = ['); j=s.index('].map(([ids,w,def,kind])',i)
lexw=set(re.findall(r'\[["\'][^"\']*["\'],\s*["\']([^"\']+)["\']', s[i:j]))
def bid(l,pid): return 'an' if (pid=='a' and l=='an') else pid
KIND={'record term':'concept'}
new=[]
for t in TERMS:
    w,parts,d,say,kind,sysname,lvl=t
    if w in lexw: continue
    ids=' '.join(bid(l,pid) for l,pid in parts if pid!='cv')
    new.append('  '+json.dumps([ids,w,d,KIND.get(kind,kind)]))
body=s[i:j].rstrip()
if not body.endswith(','): body+=','
s=s[:i]+body+'\n  // added with the Oct 2026 master-list expansion\n'+',\n'.join(new)+'\n'+s[j:]
open(p,'w').write(s)
print('lex added',len(new))
