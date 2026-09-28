"""Native evaluation controller. Never installs or changes the source candidate."""
import concurrent.futures,datetime,hashlib,json,queue,shutil,subprocess,sys,threading,time,tomllib
from pathlib import Path
E=Path(__file__).resolve().parent
ROOT=Path('/tmp/devforgeai-codex-eval-20260928')
C=ROOT/'candidate'
EXE='/home/bryan/.local/bin/codex'
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def inventory(root):
 return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}
class Server:
 def __init__(self,e,cwd):
  self.e=e;e.mkdir(parents=True,exist_ok=True);self.raw=(e/'protocol.jsonl').open('w');self.err=(e/'stderr.log').open('w');self.lock=threading.Lock();self.q=queue.Queue();self.events=[];self.n=0
  cp=Path('/home/bryan/.codex/config.toml');config=tomllib.loads(cp.read_text()) if cp.exists() else {}
  args=[EXE,'app-server','--listen','stdio://','-c','features.memories=false']
  for key in ['mcp_servers','plugins']:
   for name in config.get(key,{}):args+=['-c',key+'.'+name+'.enabled=false']
  save(e/'launch.json',{'argv':args,'cwd':str(cwd)})
  self.p=subprocess.Popen(args,cwd=cwd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1,start_new_session=True)
  threading.Thread(target=self.read,daemon=True).start()
  self.rpc('initialize',{'clientInfo':{'name':'devforgeai_eval','title':'DevForgeAI Native Evaluation','version':'1.0.0'},'capabilities':{'experimentalApi':True}})
  self.send({'method':'initialized','params':{}})
 def record(self,d,o):
  with self.lock:
   self.raw.write(json.dumps({'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'direction':d,'message':o})+'\n');self.raw.flush()
 def read(self):
  for line in self.p.stdout:
   try:o=json.loads(line)
   except ValueError:o={'unparsed_stdout':line}
   self.record('server',o);self.q.put(o)
  self.q.put({'process_exited':self.p.poll()})
 def send(self,o):
  self.record('client',o);self.p.stdin.write(json.dumps(o)+'\n');self.p.stdin.flush()
 def next(self,t=60):
  o=self.q.get(timeout=t);self.events.append(o)
  if 'process_exited' in o:raise RuntimeError('app-server exited: '+str(o))
  return o
 def rpc(self,method,params,timeout=60):
  self.n+=1;i=self.n;self.send({'method':method,'id':i,'params':params});deadline=time.monotonic()+timeout
  while time.monotonic()<deadline:
   o=self.next(max(.1,deadline-time.monotonic()))
   if o.get('id')==i and 'method' not in o:
    if 'error' in o:raise RuntimeError(method+': '+json.dumps(o['error']))
    return o.get('result')
  raise TimeoutError(method)
 def setup(self,cwd,arm,candidate=C):
  roots=[str(candidate/'skills')] if arm=='plugin' else []
  self.rpc('skills/extraRoots/set',{'extraRoots':roots})
  catalog=self.rpc('skills/list',{'cwds':[str(cwd)],'forceReload':True});save(self.e/'skills-list.json',catalog)
  entries=[s for d in catalog.get('data',[]) for s in d.get('skills',[])]
  selected=[s for s in entries if str(candidate/'skills') in str(s.get('path',''))]
  if arm=='plugin' and not any(s.get('name','').split(':')[-1]=='brainstorm' for s in selected):raise RuntimeError('Candidate brainstorm absent from native skills/list')
  other=[{'path':s['path'],'enabled':False} for s in entries if s not in selected]
  config={'skills.config':other,'features.memories':False}
  started=self.rpc('thread/start',{'cwd':str(cwd),'ephemeral':True,'sandbox':'workspace-write','approvalPolicy':'never','config':config})
  save(self.e/'thread-start.json',started);self.thread=started['thread']['id'];self.model=started.get('model');self.started=started
 def turn(self,prompt,timeout=900,question_answer=None):
  params={'threadId':self.thread,'input':[{'type':'text','text':prompt}]}
  if getattr(self,'mode',None):params['collaborationMode']={'mode':self.mode,'settings':{'model':self.model,'reasoning_effort':'high','developer_instructions':None}}
  start=self.rpc('turn/start',params)
  tid=start['turn']['id'];deadline=time.monotonic()+timeout;questions=[];result=None
  while time.monotonic()<deadline:
   o=self.next(max(.1,deadline-time.monotonic()))
   if 'id' in o and 'method' in o:
    if o['method']=='item/tool/requestUserInput':
     questions.append(o)
     if question_answer is None:
      result={'status':'awaiting_input','turnId':tid,'questions':questions};self.rpc('turn/interrupt',{'threadId':self.thread,'turnId':tid});break
     self.send({'id':o['id'],'result':{'answers':question_answer(o['params'])}})
    else:
     result={'status':'blocked_server_request','request':o,'turnId':tid};self.rpc('turn/interrupt',{'threadId':self.thread,'turnId':tid});break
   if o.get('method')=='turn/completed' and o['params']['turn']['id']==tid:
    result=o['params']['turn'];break
  if result is None:
   self.rpc('turn/interrupt',{'threadId':self.thread,'turnId':tid});result={'status':'timeout','turnId':tid}
  return result
 def close(self):
  if self.p.poll() is None:
   self.p.terminate()
   try:self.p.wait(timeout=10)
   except subprocess.TimeoutExpired:self.p.kill();self.p.wait(timeout=5)
  self.err.close();self.raw.close()
def trial(case,arm,repeat,stage='runs'):
 identity=f'{case}--{arm}--{repeat}';e=E/stage/identity;cwd=ROOT/stage/identity
 if e.exists() or cwd.exists():raise RuntimeError('Attempt already exists: '+identity)
 e.mkdir(parents=True);cwd.mkdir(parents=True);cd=C/'evals/brainstorm'/case
 full=(cd/'prompt.md').read_text();prompt=full.split('---',2)[2].strip();(e/'prompt.md').write_text(prompt+'\n')
 if (cd/'scaffold.sh').exists():
  x=subprocess.run(['bash',str(cd/'scaffold.sh')],cwd=cwd,capture_output=True,text=True);save(e/'scaffold.json',{'returncode':x.returncode,'stdout':x.stdout,'stderr':x.stderr});x.check_returncode()
 save(e/'before.json',inventory(cwd));s=None;t=time.monotonic()
 try:
  s=Server(e,cwd);s.setup(cwd,arm)
  result=s.turn(prompt,300 if case in ('asks-for-topic','ignores-unrelated-request') else 900)
  result.update({'threadId':s.thread,'model':s.model})
 except Exception as exc:result={'status':'harness_error','error':repr(exc)}
 finally:
  if s:s.close()
 result.update({'case':case,'arm':arm,'repeat':repeat,'elapsed_seconds':round(time.monotonic()-t,3),'workspace':str(cwd)})
 save(e/'result.json',result);save(e/'after.json',inventory(cwd));shutil.copytree(cwd,e/'workspace',dirs_exist_ok=True)
 print(json.dumps({'trial':identity,'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],'error':result.get('error')}),flush=True);return result
if __name__=='__main__':
 if sys.argv[1]=='preflight':trial('asks-for-topic','plugin',int(sys.argv[2]),'preflight')
 elif sys.argv[1]=='matrix':
  cases=sorted(p.parent.name for p in (C/'evals/brainstorm').glob('*/prompt.md'))
  tasks=[(c,a,n) for n in range(1,4) for c in cases for a in ('plugin','baseline')]
  save(E/'matrix.json',{'mandatory_VER':[f'VER-{i:02}' for i in range(1,11)],'case_threshold':.8,'scoring':'mean of three binary trial scores; each trial requires all applicable graders','trials':[{'case':c,'arm':a,'repeat':n,'status':'NOT_RUN'} for c,a,n in tasks]})
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   futures=[pool.submit(trial,*t) for t in tasks]
   for f in concurrent.futures.as_completed(futures):f.result()
