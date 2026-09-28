from pathlib import Path
import sys, tempfile, json, shutil, time
e=Path('src/codex/devforgeai/import-evidence/native-evaluation-20260928');sys.path.insert(0,str(e))
from native_eval import E,C,Server,save,inventory
name='hands-off-to-prd--baseline--3';out=E/'isolation-controls'/name;assert not out.exists();out.mkdir(parents=True)
root=Path(tempfile.mkdtemp(prefix='devforgeai-baseline-'));cwd=root/'project';cwd.mkdir()
prompt=(C/'evals/brainstorm/hands-off-to-prd/prompt.md').read_text().split('---',2)[2].strip()
save(out/'purpose.json',{'original_trial':name,'reason':'Final audit found sibling filename exposure in this baseline trial; retain original and run a control in a unique empty directory tree with no candidate copy.'})
(out/'prompt.md').write_text(prompt+'\n');save(out/'before.json',inventory(cwd))
s=None;t=time.monotonic()
try:
 s=Server(out,cwd);s.setup(cwd,'baseline');r=s.turn(prompt,900);r.update({'threadId':s.thread,'model':s.model})
except Exception as exc:r={'status':'harness_error','error':repr(exc)}
finally:
 if s:s.close()
r.update({'case':'hands-off-to-prd','arm':'baseline','repeat':3,'elapsed_seconds':round(time.monotonic()-t,3),'workspace':str(cwd)})
save(out/'result.json',r);save(out/'after.json',inventory(cwd));shutil.copytree(cwd,out/'workspace')
print(json.dumps({'control':name,'status':r['status'],'elapsed_seconds':r['elapsed_seconds']}),flush=True)
