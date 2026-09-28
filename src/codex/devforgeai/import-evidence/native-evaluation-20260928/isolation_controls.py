"""Fresh framework controls after sibling filename exposure; originals remain scored."""
from pathlib import Path
import concurrent.futures,json,shutil,tempfile,time
from native_eval import C,E,Server,save,inventory
def run(n):
 e=E/'isolation-controls'/f'uses-named-framework--plugin--{n}'
 assert not e.exists();e.mkdir(parents=True)
 root=Path(tempfile.mkdtemp(prefix='devforgeai-framework-'))
 cwd=root/'project';cwd.mkdir();candidate=root/'plugin';shutil.copytree(C,candidate)
 prompt=(C/'evals/brainstorm/uses-named-framework/prompt.md').read_text().split('---',2)[2].strip()
 (e/'prompt.md').write_text(prompt+'\n')
 save(e/'before.json',inventory(cwd));save(e/'candidate-before.json',inventory(candidate))
 save(e/'purpose.json',{'original_trial':f'uses-named-framework--plugin--{n}','reason':'Original trial listed sibling BRN filenames. This control uses a unique parent containing only its own project and exact candidate copy. Original trial is retained; frozen matrix denominator is unchanged.'})
 s=None;t=time.monotonic()
 try:
  s=Server(e,cwd);s.setup(cwd,'plugin',candidate);r=s.turn(prompt,900);r.update({'threadId':s.thread,'model':s.model})
 except Exception as exc:r={'status':'harness_error','error':repr(exc)}
 finally:
  if s:s.close()
 r.update({'case':'uses-named-framework','arm':'plugin','repeat':n,'elapsed_seconds':round(time.monotonic()-t,3),'workspace':str(cwd)})
 save(e/'result.json',r);save(e/'after.json',inventory(cwd));save(e/'candidate-after.json',inventory(candidate));shutil.copytree(cwd,e/'workspace')
 print(json.dumps({'control':n,'status':r['status'],'elapsed_seconds':r['elapsed_seconds']}),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for f in [pool.submit(run,n) for n in [2,3]]:f.result()
