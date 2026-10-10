import os,sys,re,collections,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cw,remap
A='/home/user/eu4-antebellum-modpack'
files=subprocess.run(['git','-c','core.quotepath=false','ls-files','-m','-o','--exclude-standard'],cwd=A,capture_output=True,text=True).stdout.split('\n')
cnt=collections.Counter(); ex={}
def walk(t,nodes,path,rel):
    for n in nodes:
        v=t[n.vstart:n.vend] if n.kind=='value' else ''
        if remap.oor(n.key) and n.kind!='bare' and (path[-1:] not in (['random_list'],)):
            cnt[('KEY',path[-1] if path else '')]+=1; ex.setdefault(('KEY',path[-1] if path else ''),(rel,n.key))
        if n.kind=='value' and remap.oor(v) and n.key not in ('duration','factor','days','months','id','start','historical_score','add_treasury','treasury','time','years','value','amount','DURATION','build_cost','sailors','add_sailors','galley','heavy_ship','total_development','governing_capacity','advisor_exists','chance','weight','base','cost','order','chance_amount'):
            cnt[('VAL',n.key)]+=1; ex.setdefault(('VAL',n.key),(rel,v))
        if n.kind=='block': walk(t,cw.children(t,n),path+[n.key],rel)
for rel in files:
    if rel.endswith('.txt') and rel.split('/')[0] in('common','decisions','events','missions'):
        t=open(os.path.join(A,rel),'rb').read().decode('latin-1')
        walk(t,cw.parse(t),[],rel)
for k,v in cnt.most_common(40): print(k,v,ex[k])
