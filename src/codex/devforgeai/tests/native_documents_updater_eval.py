"""Native Documents Updater evaluation using ephemeral Codex app-server threads.
Requires an already authenticated Codex CLI; never installs the plugin.
"""
import concurrent.futures, datetime, hashlib, json, queue, shutil, subprocess, sys, threading, time, tomllib
from pathlib import Path
PACKAGE = Path(__file__).resolve().parents[1]
EXE = shutil.which("codex") or str(Path.home()/".local/bin/codex")
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def inventory(root):
 return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}
class Server:
 def __init__(self,e,cwd):
  self.e=e;e.mkdir(parents=True,exist_ok=True);self.raw=(e/'protocol.jsonl').open('w');self.err=(e/'stderr.log').open('w');self.lock=threading.Lock();self.q=queue.Queue();self.events=[];self.n=0
  cp=Path.home()/'.codex/config.toml';config=tomllib.loads(cp.read_text()) if cp.exists() else {}
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
 def setup(self,cwd,arm,candidate=None):
  roots=[str(candidate/'skills')] if arm=='plugin' else []
  self.rpc('skills/extraRoots/set',{'extraRoots':roots})
  catalog=self.rpc('skills/list',{'cwds':[str(cwd)],'forceReload':True});save(self.e/'skills-list.json',catalog)
  entries=[s for d in catalog.get('data',[]) for s in d.get('skills',[])]
  selected=[s for s in entries if str(candidate/'skills') in str(s.get('path',''))]
  if arm=='plugin' and not any(s.get('name','').split(':')[-1]=='documents-updater' for s in selected):raise RuntimeError('Candidate documents-updater absent from native skills/list')
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

def git_state(cwd):
    result = {}
    for key, cmd in {
        "status": ["status", "--porcelain=v1", "--untracked-files=all"],
        "head": ["rev-parse", "--verify", "HEAD"],
        "index": ["ls-files", "--stage", "-z"],
        "refs": ["for-each-ref", "--format=%(refname) %(objectname)"],
    }.items():
        r = subprocess.run(["git", *cmd], cwd=cwd, capture_output=True, text=True)
        result[key] = {"exit": r.returncode, "output": r.stdout}
    return result

def trial(case, arm, repeat, evidence, candidate, plan_hash, stage):
    import tempfile
    identity = f"{case}--{arm}--{repeat}"
    e = evidence / stage / identity
    e.mkdir(parents=True, exist_ok=False)
    parent = Path(tempfile.mkdtemp(prefix="dfai-du-eval-"))
    cwd = parent / "project"
    cwd.mkdir()
    # Every trial gets a unique parent: no sibling trial artifacts are exposed.
    local = parent / "devforgeai"
    if arm == "plugin":
        shutil.copytree(candidate, local)
    case_dir = PACKAGE / "evals/documents-updater" / case
    prompt = (case_dir / "prompt.md").read_text().split("---", 2)[2].strip()
    (e / "prompt.md").write_text(prompt + "\n")
    r = subprocess.run(["bash", str(case_dir / "scaffold.sh")], cwd=cwd,
                       capture_output=True, text=True)
    save(e / "scaffold.json", {"exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
    before = inventory(cwd)
    save(e / "before.json", before)
    save(e / "git-before.json", git_state(cwd))
    shutil.copytree(cwd, e / "before-workspace", ignore=shutil.ignore_patterns(".git"))
    s = None
    start = time.monotonic()
    try:
        r.check_returncode()
        s = Server(e, cwd)
        s.setup(cwd, arm, local)
        result = s.turn(prompt, timeout=1200)
        result.update(threadId=s.thread, model=s.model)
    except Exception as exc:
        result = {"status": "harness_error", "error": repr(exc)}
    finally:
        if s:
            s.close()
    result.update(case=case, arm=arm, repeat=repeat, workspace=str(cwd),
                  elapsed_seconds=round(time.monotonic()-start, 3), plan_sha256=plan_hash)
    save(e / "result.json", result)
    save(e / "after.json", inventory(cwd))
    save(e / "git-after.json", git_state(cwd))
    shutil.copytree(cwd, e / "workspace", ignore=shutil.ignore_patterns(".git"))
    print(json.dumps({"trial": identity, "status": result["status"],
                      "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--stage", choices=["smoke", "matrix"], required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    stage = args.stage
    cases = sorted(p.name for p in (PACKAGE/"evals/documents-updater").iterdir() if p.is_dir())
    if stage == "smoke":
        cases = ["updates-readme-and-changelog", "asks-for-unknown-baseline"]
    repeats = range(1, 4) if stage == "matrix" else range(1, 2)
    arms = ("plugin", "baseline") if stage == "matrix" else ("plugin",)
    tasks = [(c, a, n) for n in repeats for c in cases for a in arms]
    candidate = evidence / "candidate"
    if not candidate.exists():
        shutil.copytree(PACKAGE/".codex-plugin", candidate/".codex-plugin")
        shutil.copytree(PACKAGE/"skills/documents-updater", candidate/"skills/documents-updater")
    expected = inventory(candidate)
    actual = {k: hashlib.sha256((PACKAGE/k).read_bytes()).hexdigest() for k in expected}
    if actual != expected:
        raise RuntimeError("Candidate bytes changed; use a new evidence directory")
    rows = [{"path": p, "sha256": h} for p, h in expected.items()]
    digest = hashlib.sha256("".join(f"{r['path']}\0{r['sha256']}\n" for r in rows).encode()).hexdigest()
    plan = {
        "candidate_sha256": digest, "candidate_files": rows,
        "codex_version": subprocess.check_output([EXE, "--version"], text=True).strip(),
        "mandatory": [f"VER-{i:02}" for i in range(1,13)],
        "manual_owner_cases": {"VER-10":"NOT_RUN", "VER-11":"NOT_RUN", "VER-12":"NOT_RUN"},
        "threshold": 0.8,
        "score": "Mean of source regex/file_exists and independently assessed semantic graders; skill activation excluded from score and checked separately. Report all grader passes and strict full-contract trial counts too. Each of three plugin runs must reach threshold; threshold never waives a failed obligation.",
        "isolation": "Unique temp parent per trial; ephemeral app-server, memories and other skills/plugins/MCP disabled. Not an OS-hermetic boundary.",
        "source_suite": inventory(PACKAGE/"evals/documents-updater"),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "grader_sha256": hashlib.sha256((PACKAGE/"tests/grade_documents_updater_eval.py").read_bytes()).hexdigest(),
        "trials": [{"case":c,"arm":a,"repeat":n,"status":"NOT_RUN"} for c,a,n in tasks],
    }
    pp = evidence / (stage+"-plan.json")
    if pp.exists():
        raise RuntimeError("Plan already exists; retain earlier attempts and use a fresh stage/evidence path")
    save(pp,plan)
    plan_hash = hashlib.sha256(pp.read_bytes()).hexdigest()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(trial,c,a,n,evidence,candidate,plan_hash,stage) for c,a,n in tasks]
        for f in concurrent.futures.as_completed(futures):
            f.result()

if __name__ == "__main__":
    main()
