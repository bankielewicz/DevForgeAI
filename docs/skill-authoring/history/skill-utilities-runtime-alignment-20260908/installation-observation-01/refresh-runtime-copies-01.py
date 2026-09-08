from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, tempfile, datetime
W=Path('/home/bryan/Projects/DevForge');E=W/'tmp/skill-utilities-approved-continuation-20260908T010546709607Z';M=W/'framework/DevForgeAI'
commit='214dd797d6ec564595fc316dbc1f01916fb2bfd2'
h=lambda b:hashlib.sha256(b).hexdigest()
def files(root):
 result={}
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise RuntimeError('Symlink: '+str(p))
  if p.is_file():result[str(p.relative_to(root))]=p.read_bytes()
 return result
if subprocess.check_output(['git','rev-parse','HEAD'],cwd=M,text=True).strip()!=commit:raise RuntimeError('Canonical main changed')
if (W/'.devforge-install.json').exists():raise RuntimeError('New shared installation inventory needs reconciliation')
source_manifest=M/'docs/skill-authoring/history/skill-utilities-runtime-alignment-20260908/candidate-manifest.json'
if h(source_manifest.read_bytes())!='6974a1a4eddd9acd2354a5d177cc727f3d51ac8e6fa6b3198771e3fade7996fd':raise RuntimeError('Source manifest changed')
expected=json.loads(source_manifest.read_text())['files'];before=json.loads((E/'installed-before-alignment-manifest.json').read_text())['skills']
installer_path=W/'framework/DevForge/scripts/install_framework.py'
installer_hash=h(installer_path.read_bytes())
spec=importlib.util.spec_from_file_location('scoped_integration_installer',installer_path);installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
plans=[]
for previous in before:
 name=previous['skill'];source=M/'providers/codex/plugins/devforgeai/skills'/name;dest=W/'.agents/skills'/name
 all_source=files(source);prefix='providers/codex/plugins/devforgeai/skills/'+name+'/'
 wanted={r['path'][len(prefix):]:r['sha256'] for r in expected if r['path'].startswith(prefix)}
 if {n:h(v) for n,v in all_source.items()}!=wanted:raise RuntimeError('Canonical source differs from reviewed manifest')
 old=files(dest)
 if {n:h(v) for n,v in old.items()}!=previous['files_sha256']:raise RuntimeError('Independent installation change; no writes')
 planned={str(rel):p.read_bytes() for p,rel in installer.runtime_skill_files(source)}
 if set(old)-set(planned):raise RuntimeError('Unexpected removal requires reconciliation')
 for rel in planned:installer.safe_destination(W,str(Path('.agents/skills')/name/rel))
 plans.append((name,source,dest,old,planned))
rows=[]
for name,source,dest,old,planned in plans:
 for rel,data in planned.items():
  p=installer.safe_destination(W,str(Path('.agents/skills')/name/rel))
  if (p.read_bytes() if p.exists() else None)!=old.get(rel):raise RuntimeError('Concurrent destination change')
  p.parent.mkdir(parents=True,exist_ok=True)
  if rel not in old:
   with p.open('xb') as f:f.write(data)
  elif old[rel]!=data:
   fd,tmp=tempfile.mkstemp(prefix='.utility-install-',dir=p.parent)
   try:
    with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    os.chmod(tmp,p.stat().st_mode & 0o777)
    if p.read_bytes()!=old[rel]:raise RuntimeError('Concurrent replacement')
    os.replace(tmp,p)
   finally:
    if os.path.exists(tmp):os.unlink(tmp)
 actual=files(dest)
 if actual!=planned:raise RuntimeError('Post-install mismatch')
 rows.append({'skill':name,'canonical':str(source),'installed':str(dest),'files':len(actual),'files_sha256':{n:h(v) for n,v in actual.items()},'match':True})
result={'schema_version':'devforge.scoped-installation-observation/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_main_commit':commit,'procedure':'Supported installer runtime_skill_files and safe_destination; exact frozen-before checks and scoped generation. No broad provider install, hook/agent config changes or shared inventory rewrite.','installer':{'path':str(installer_path),'sha256':installer_hash},'preserved_before':str(E/'installed-before-alignment-manifest.json'),'skills':rows,'native_activation':'NOT_OBSERVED','native_behavior':'NOT_EVALUATED','receiving_execution':'NOT_RUN'}
p=E/'installation-result-01.json'
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
read=json.loads(p.read_text());assert read==result
print(json.dumps({'record':str(p),'sha256':h(p.read_bytes()),'skills':[{k:r[k] for k in ['skill','files','match']} for r in rows]}))
