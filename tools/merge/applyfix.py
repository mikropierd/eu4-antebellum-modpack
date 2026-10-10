import sys,os,re,subprocess,glob,json,tempfile
repo=sys.argv[1]; dry=len(sys.argv)>2 and sys.argv[2]=='dry'
R='/home/user/'+repo
res={'applied':[],'already':[],'missing':[],'conflict':[]}
def run(args,inp):
    return subprocess.run(args,cwd=R,input=inp,capture_output=True,text=True,errors='replace')
for p in sorted(glob.glob('/home/user/grotaclasBugfixes/patches/*.patch')):
    txt=open(p,encoding='utf-8',errors='replace').read()
    parts=re.split(r'(?m)^(?=diff --git )',txt)
    head,secs=parts[0],parts[1:]
    if secs:
        # strip trailing signature from last section
        secs[-1]=re.sub(r'(?ms)^-- \n[\d.]+\n?$','',secs[-1])
    name=os.path.basename(p)
    for s in secs:
        first=s.split('\n',1)[0]; f=first[len('diff --git a/'):].split(' b/')[-1]
        newfile='new file mode' in s
        deleted='deleted file mode' in s
        if not newfile and not os.path.exists(os.path.join(R,f)):
            res['missing'].append((name,f)); continue
        if newfile and os.path.exists(os.path.join(R,f)):
            res['conflict'].append((name,f,'new file exists')); continue
        if s.count('\n@@')==0 and 'Binary' in s:
            res['conflict'].append((name,f,'binary')); continue
        r=run(['patch','-p1','-l','-F0','--forward','--dry-run','--no-backup-if-mismatch'],s)
        if r.returncode==0:
            if not dry: run(['patch','-p1','-l','-F0','--forward','--no-backup-if-mismatch'],s)
            res['applied'].append((name,f)); continue
        rr=run(['patch','-p1','-l','-R','--dry-run','--no-backup-if-mismatch'],s)
        if rr.returncode==0: res['already'].append((name,f))
        else: res['conflict'].append((name,f,'hunk mismatch'))
json.dump(res,open(f'{S}/fix_{repo}.json' if False else f'/tmp/claude-0/-home-user/1f71c29d-3371-549a-adfe-f028567f4302/scratchpad/fix_{repo}.json','w'),indent=1)
print({k:len(v) for k,v in res.items()})
