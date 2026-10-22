import subprocess, json, sys
p='/home/claude/meddecode-build/meddecode-build.html'; s=open(p).read()
i=s.index('const PARTS = {};'); c=s.index('const CASES',i); j=s.index('\n];',c)+3
js=s[i:j]+'\nconsole.log(JSON.stringify({parts:PARTS,lex:LEX,cases:CASES.map(c=>({ans:c.ans}))}));'
open('/tmp/claude-0/bx.js','w').write(js)
out=subprocess.run(['node','/tmp/claude-0/bx.js'],capture_output=True,text=True)
if out.returncode: print(out.stderr[:2000]); sys.exit(1)
d=json.loads(out.stdout); json.dump(d,open('/tmp/claude-0/bparts.json','w'))
print('parts',len(d['parts']),'lex',len(d['lex']),'cases',len(d['cases']))
