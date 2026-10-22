HEAD='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
CSS='body{margin:0}img{max-width:100%}[hidden]{display:none!important}\n.back{display:inline-flex;align-items:center;gap:6px;font:600 14px var(--font-body);color:var(--muted);text-decoration:none;justify-self:start}\n.back:hover{color:var(--ink);text-decoration:underline}\n'
BACK='\n  <a class="back" href="../../">← MACC Health Sciences, Dental &amp; EMT</a>'
def wrap(s):
    if s.lstrip().lower().startswith('<!doctype'): return s
    w=s.index('<div class="wrap">'); st=s.rindex('</style>',0,w)
    s=s[:st]+'\n'+CSS+'</style></head><body>'+s[st+len('</style>'):w]+'<div class="wrap">'+BACK+s[w+len('<div class="wrap">'):]
    return HEAD+s.rstrip('\n')+'\n</body>\n</html>\n'
