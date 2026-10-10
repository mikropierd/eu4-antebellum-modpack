import os,sys,re,collections,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cw
A='/home/user/eu4-antebellum-modpack'; V='/home/user/Victorum-Enhanced'
def series(root,files):
    out=[]
    for rel in files:
        t=open(os.path.join(root,rel),'rb').read().decode('latin-1')
        for n in cw.parse(t):
            if n.kind!='block': continue
            slot=cw.get_scalar(t,n,'slot')
            pot=[c for c in cw.children(t,n) if c.key=='potential' and c.kind=='block']
            tags=set()
            if pot:
                ptxt=t[pot[0].bstart:pot[0].bend]
                tags=set(re.findall(r'\btag\s*=\s*([A-Z0-9]{3})\b',ptxt))|set(re.findall(r'\boriginal_tag\s*=\s*([A-Z0-9]{3})\b',ptxt))
            out.append((rel,n.key,slot,tags))
    return out
head=subprocess.run(['git','ls-tree','-r','--name-only','HEAD','missions'],cwd=A,capture_output=True,text=True).stdout.split()
af=[f for f in head if f.endswith('.txt') and not os.path.exists(os.path.join(V,f))]
vf=[os.path.relpath(os.path.join(r,f),V) for r,_,fs in os.walk(V+'/missions') for f in fs if f.endswith('.txt')]
vs=series(V,vf); as_=series(A,af)
byv=collections.defaultdict(list)
for rel,k,slot,tags in vs:
    for t in tags: byv[(t,slot)].append((rel,k))
n=0
for rel,k,slot,tags in as_:
    hit=[(t,byv[(t,slot)]) for t in tags if (t,slot) in byv]
    if hit:
        n+=1; print(rel,k,'slot',slot,'<->',[(t,[x[1] for x in v][:3]) for t,v in hit])
print(n,len(as_))
