import os,sys,re,collections,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cw
A='/home/user/eu4-antebellum-modpack'
files=subprocess.run(['git','-c','core.quotepath=false','ls-files','-m','-o','--exclude-standard'],cwd=A,capture_output=True,text=True).stdout.split('\n')
files+= subprocess.run(['git','-c','core.quotepath=false','ls-files'],cwd=A,capture_output=True,text=True).stdout.split('\n')
files=sorted(set(f for f in files if f))
W={'country_decisions','province_decisions'}
defs=collections.defaultdict(lambda: collections.defaultdict(list))  # dir -> key -> [(file,hash)]
for rel in files:
    parts=rel.split('/')
    if parts[0] not in ('common','decisions','missions','events') or not rel.endswith('.txt'): continue
    if len(parts)<3 and parts[0]=='common': continue
    d='/'.join(parts[:2]) if parts[0]=='common' else parts[0]
    if d in ('common/technologies','common/countries','common/country_tags','common/province_names','common/cultures','common/defines','common/bookmarks','common/history'): continue
    t=open(os.path.join(A,rel),'rb').read().decode('latin-1')
    nodes=cw.parse(t)
    for n in nodes:
        if n.kind!='block': continue
        subs=[(n,n.key)]
        if n.key in W: subs=[(c,c.key) for c in cw.children(t,n) if c.kind=='block']
        for nd,k in subs:
            if parts[0]=='events':
                i=cw.get_scalar(t,nd,'id')
                if not i: continue
                k=i
            if parts[0]=='common' and d.endswith(('on_actions',)): continue
            defs[d][k].append((rel,hash(re.sub(r'\s+','',t[nd.start:nd.end]))))
out=[]
for d,m in defs.items():
    for k,v in m.items():
        fs={f for f,_ in v}
        if len(fs)>1:
            out.append((d,k,sorted(fs)))
print(len(out))
c=collections.Counter(d for d,_,_ in out); print(c.most_common(40))
import json; json.dump(out,open(os.path.dirname(os.path.abspath(__file__))+'/dups.json','w'),indent=1)
