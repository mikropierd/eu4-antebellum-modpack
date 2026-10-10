import os,re,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cw
A='/home/user/eu4-antebellum-modpack'
changed=subprocess.run(['git','-c','core.quotepath=false','status','--short'],cwd=A,capture_output=True,text=True).stdout.split('\n')
bad=0; oor=0
def strip_comments(t):
    return re.sub(r'#[^\n]*','',re.sub(r'"[^"\n]*"','""',t))
for l in changed:
    if not l.strip(): continue
    rel=l[3:].strip('"')
    p=os.path.join(A,rel)
    if os.path.isdir(p):
        continue
    if rel.endswith(('.txt','.gui','.gfx')) and rel.split('/')[0] in ('common','decisions','events','missions','interface','customizable_localization'):
        t=open(p,'rb').read().decode('latin-1'); s=strip_comments(t)
        if s.count('{')!=s.count('}'): bad+=1; print('UNBALANCED',rel,s.count('{'),s.count('}'))
print('unbalanced:',bad)
