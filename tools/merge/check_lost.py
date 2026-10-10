import os,re,sys,json,subprocess,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cw
S=os.path.dirname(os.path.abspath(__file__))
V='/home/user/Victorum-Enhanced'; A='/home/user/eu4-antebellum-modpack'
def git_show(rel):
    return subprocess.run(['git','show','HEAD:'+rel],cwd=A,capture_output=True).stdout.decode('latin-1')
tok=re.compile(r"[A-Za-z_][\w.\-']{2,}")
vtok=set()
for d in ['common','decisions','events','missions','interface']:
    for root,_,fs in os.walk(V+'/'+d):
        for f in fs:
            if f.endswith(('.txt','.gui','.gfx')):
                vtok.update(tok.findall(open(os.path.join(root,f),'rb').read().decode('latin-1')))
# A defined identifiers (HEAD)
files=subprocess.run(['git','ls-tree','-r','--name-only','HEAD'],cwd=A,capture_output=True,text=True).stdout.split('\n')
aonly=set()
for rel in files:
    if rel.split('/')[0] in ('common','decisions','events','missions','interface') and rel.endswith(('.txt','.gui','.gfx')):
        t=git_show(rel)
        for nd in cw.parse(t):
            k=nd.key
            if nd.kind=='block' and k not in vtok and len(k)>3 and not k.isdigit(): aonly.add(k)
            if nd.kind=='block':
                for sub in ('id','name'):
                    v=cw.get_scalar(t,nd,sub)
                    if v and v not in vtok and not v.isdigit(): aonly.add(v)
            if nd.kind=='value' and k=='namespace':
                aonly.add(t[nd.vstart:nd.vend])
print('A-only ids',len(aonly))
rep=json.load(open(f'{S}/merge_report.json'))
out=collections.defaultdict(list)
byfile=collections.defaultdict(set)
for f,k in rep['v_won']: byfile[f].add(k)
for f,keys in byfile.items():
    at=git_show(f)
    nt=open(os.path.join(A,f),'rb').read().decode('latin-1')
    for nd in cw.parse(at):
        text=at[nd.start:nd.end]
        found={w for w in tok.findall(text) if w in aonly or (('.' in w) and w.split('.')[0] in aonly)}
        if not found: continue
        missing={w for w in found if w not in nt}
        if missing: out[f].append((nd.key,sorted(missing)[:8]))
json.dump(out,open(f'{S}/lost.json','w'),indent=1)
for f,v in out.items(): print(f,len(v),v[:3])
