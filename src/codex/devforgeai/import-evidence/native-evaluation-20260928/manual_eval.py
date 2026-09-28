"""Scripted manual obligations. All answers are synthetic evaluation fixtures."""
import concurrent.futures,json,shutil,subprocess,time
from pathlib import Path
from native_eval import C,E,ROOT,Server,save,inventory
PLAN={
 'framework-added':{'ver':'VER-05','turns':['I am Dana. Brainstorm five ideas for reducing queue time at a community tool library using the validation-probe framework. Skip questions and write it up.']},
 'framework-missing':{'ver':'VER-05','turns':['I am Dana. Brainstorm five ideas for reducing queue time at a community tool library using the validation-probe framework. Skip questions and write it up.']},
 'stop-save-yes':{'ver':'VER-09','turns':['I am Dana. Brainstorm ways our two-person community tool library can reduce queues, with no software budget. My ideas are \"a paper express-return tray\" and \"a volunteer queue greeter\". Present options and proposed dispositions for confirmation; do not write a document yet.','Stop the session here.','Yes, save the captured ideas as a draft. Leave every disposition open. Do not ask any more questions.']},
 'stop-save-no':{'ver':'VER-09','turns':['I am Dana. Brainstorm ways our two-person community tool library can reduce queues, with no software budget. My ideas are \"a paper express-return tray\" and \"a volunteer queue greeter\". Present options and proposed dispositions for confirmation; do not write a document yet.','Stop the session here.','No, do not save anything.']},
 'validator-three-attempts':{'ver':'VER-09','turns':['I am Dana. Brainstorm exactly five ideas for reducing queues at a community tool library. Skip questions and write it up.']},
 'confirmed-decisions':{'ver':'VER-09 supplementary','turns':['I am Dana. Brainstorm exactly five ideas for reducing queues at a community tool library with two volunteers and no software budget. Present a numbered IDEA-01 through IDEA-05 table of proposed dispositions and reasons for my confirmation before writing.','I confirm IDEA-01 promoted, reason \"Try the smallest useful pilot\"; IDEA-02 parked, reason \"Wait for volunteer capacity\"; IDEA-03 rejected, reason \"Outside this month budget\". Leave IDEA-04 and IDEA-05 open with no reason. I confirm the brainstorm has converged. Write it now without more questions.']},
 'extension-preserves-history':{'ver':'VER-08 supplementary','turns':['Brainstorm ways to reduce appointment no-shows at our dental clinic.','Extend BRN-001. I am Dana. Add three more ideas, keep existing item meanings and all prior history, and proceed without further questions. I have not confirmed any dispositions or convergence.']},
 'native-question-plan':{'ver':'Native question-tool adaptation','mode':'plan','turns':['Brainstorm ways to reduce appointment no-shows at our dental clinic.']}
}
def run(name,definition):
 e=E/'manual'/name;cwd=ROOT/'manual'/name
 if e.exists() or cwd.exists():raise RuntimeError('Existing manual attempt '+name)
 e.mkdir(parents=True);cwd.mkdir(parents=True);candidate=C
 if name in ('framework-added','framework-missing','validator-three-attempts'):
  candidate=ROOT/'manual-candidates'/name;shutil.copytree(C,candidate)
  skill=candidate/'skills/brainstorm'
  if name.startswith('framework-'):
   idx=skill/'references/frameworks/INDEX.md';t=idx.read_text();t=t.replace('## Required sections','| validation-probe | [validation-probe.md](validation-probe.md) | A community tool library queue problem | Other topics |\\n\\n## Required sections');idx.write_text(t)
   if name=='framework-added':
    text=(skill/'references/frameworks/diverge-converge.md').read_text().replace('Diverge-converge','Validation-probe').replace('diverge-converge','validation-probe')
    text=text.replace('Write this into section 5, followed by any discussion the numbers do not capture:','Write this into section 5, including the literal evaluation marker framework-probe-94f1, followed by any discussion the numbers do not capture:')
    (skill/'references/frameworks/validation-probe.md').write_text(text)
  else:
   p=skill/'scripts/validate_brn.py'
   p.write_text('from pathlib import Path\nimport sys\np=Path(".validator-attempts")\nn=int(p.read_text())+1 if p.exists() else 1\np.write_text(str(n))\nprint("line 1: EVAL_UNFIXABLE_94f1: simulated external verification failure; document edits cannot fix this condition")\nsys.exit(1)\n')
  assert (candidate/'skills/brainstorm/SKILL.md').read_bytes()==(C/'skills/brainstorm/SKILL.md').read_bytes()
  save(e/'candidate-before.json',inventory(candidate))
 if name in ('extension-preserves-history','native-question-plan'):
  x=subprocess.run(['bash',str(C/'evals/brainstorm/existing-brn/scaffold.sh')],cwd=cwd,capture_output=True,text=True);x.check_returncode()
 save(e/'before.json',inventory(cwd));shutil.copytree(cwd,e/'before-workspace')
 save(e/'definition.json',definition);results=[];s=None;t=time.monotonic()
 try:
  s=Server(e,cwd);s.setup(cwd,'plugin',candidate)
  s.mode=definition.get('mode')
  for i,prompt in enumerate(definition['turns'],1):
   result=s.turn(prompt,900);results.append(result);save(e/f'turn-{i}-result.json',result)
   save(e/f'turn-{i}-inventory.json',inventory(cwd));shutil.copytree(cwd,e/f'turn-{i}-workspace')
   print(json.dumps({'manual':name,'turn':i,'status':result['status']}),flush=True)
  summary={'status':'executed','turns':results,'threadId':s.thread,'model':s.model}
 except Exception as exc:summary={'status':'harness_error','error':repr(exc),'turns':results}
 finally:
  if s:s.close()
 summary['elapsed_seconds']=round(time.monotonic()-t,3);save(e/'result.json',summary);save(e/'after.json',inventory(cwd));shutil.copytree(cwd,e/'workspace')
 if candidate!=C:save(e/'candidate-after.json',inventory(candidate))
 return summary
if __name__=='__main__':
 save(E/'manual-plan.json',{'synthetic_user_answers':True,'tests':PLAN,'policy':'All scenarios retained; no hidden retries or changes to source candidate.'})
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  fs=[pool.submit(run,n,d) for n,d in PLAN.items()]
  for f in concurrent.futures.as_completed(fs):f.result()
