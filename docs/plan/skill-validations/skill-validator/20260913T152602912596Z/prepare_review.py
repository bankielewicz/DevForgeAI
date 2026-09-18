"""Pin independent contract expectations and inspect code without importing it."""
import ast
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import sys
from qa_harness import RUN, ROOT, TARGET, LOADED, PRIOR, save, sha, now

save(RUN/'setup-attempt-001.json', {'status':'PARTIAL', 'error':'PackageNotFoundError: yaml; module distribution name is PyYAML', 'effects':'contract and bounded source captures complete; environment write not completed', 'retry':'prepare_review.py environment-only continuation; no input capture overwritten'})
save(RUN/'environment.json', {'time_utc':now(),'platform':platform.platform(),'python':sys.version,'executable':sys.executable,'codex':shutil.which('codex'),'packages':{n: next((d.version for d in importlib.metadata.distributions() if d.metadata['Name'].lower() == n.lower()),None) for n in ['PyYAML','coverage','tiktoken','jsonschema']},'loaded_evaluator':str(LOADED),'development_target':str(TARGET),'self_review':'Loaded and target bytes identical; helper results are self-review. External probes have separate fixture code and specification-derived expectations.'})
auth = '''# Authorization and scope
Validator-only QA requested for exact development skill-validator; reported 75 files and d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1.
Both selected specification hashes verified before dependent assessment. Read-only companion and previous implementation evidence. Assessment and bounded synthetic testing only; no production/package/operational repairs, installation, dependency downloads, builder workflow invocation, hooks, remote publication, or Rust changes.
All work products are below this fresh UTC run. Synthetic executions use declared trials roots; TEMP/TMP/TMPDIR point inside this run. Existing regression tests may invoke companion Python helpers only on their own synthetic temporary fixtures as part of the explicitly requested suite; this is not invoking the builder skill.
No real binding is created or captured. Synthetic identities remain only in synthetic operational binding files. Existing CLI model/auth retained; no sandbox, approval, or hook-trust bypass.
Early discovery commands and the failed first environment metadata read are retained in the conversation tool transcript, not reconstructed as raw output here. Subsequent executions have exact retained command receipts.
'''
(RUN/'authorization.md').write_text(auth,encoding='utf-8')
obligations=[]
spec=RUN/'inputs/skill-validator-adaptive-enhancement-spec.md'
for n,line in enumerate(spec.read_text(encoding='utf-8').splitlines(),1):
    if line.startswith('| VA-') or line.startswith('| VAT-') or line.startswith('| AV-'):
        cells=[x.strip() for x in line.strip('|').split('|')]
        obligations.append({'id':cells[0],'specification':str(spec),'line':n,'exact_obligation':line,'required':True,'applicability':'applicable','planned_method':'independent terminal fixtures plus source and semantic review; native cases conditional on capability','expected_before_execution':cells[-1], 'result':'NOT_RUN'})
save(RUN/'expectations-before-execution.json',obligations)
audit=[]
for package in ('target','companion','loaded-evaluator'):
    manifest=json.loads((RUN/(package+'-before.json')).read_text(encoding='utf-8'))
    for row in manifest['files']:
        p=RUN/'inputs'/package/row['path']
        entry={'package':package,**row}
        if p.suffix=='.py':
            tree=ast.parse(p.read_bytes(),filename=str(p))
            entry['imports']=[{'line':n.lineno,'text':ast.unparse(n)} for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
            entry['definitions']=[{'line':n.lineno,'end':n.end_lineno,'name':n.name} for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
            entry['effects']=[{'line':n.lineno,'text':ast.unparse(n)} for n in ast.walk(tree) if isinstance(n,ast.Call) and any(t in ast.unparse(n.func) for t in ('subprocess','write','unlink','remove','rmtree','mkdir','copy','rename','replace','exec','eval','open','import_module','TemporaryDirectory'))]
        elif p.suffix=='.json':
            entry['json_parsed']=True
            value=json.loads(p.read_bytes())
            entry['top_level']=list(value) if type(value)==dict else type(value).__name__
        audit.append(entry)
save(RUN/'source-inspection.json',audit)
ancestors=set()
for p in [TARGET,LOADED,ROOT/'src/agents/skills/skill-builder',PRIOR,RUN]:
    ancestors.update([p,*[x for x in p.parents if x==ROOT or ROOT in x.parents]])
agents=[]
for p in sorted(ancestors):
    if (p/'AGENTS.md').is_file():
        data=(p/'AGENTS.md').read_bytes()
        name='AGENTS-'+sha(str(p).encode())[:8]+'.md'
        (RUN/'inputs'/name).write_bytes(data)
        agents.append({'path':str(p/'AGENTS.md'),'capture':name,'sha256':sha(data)})
save(RUN/'applicable-instructions.json',agents)
checker=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
(RUN/'inputs/quick_validate.py').write_bytes(checker.read_bytes())
save(RUN/'checker-identity.json',{'path':str(checker),'sha256':sha(checker.read_bytes()),'scope':'limited structural check only'})
print('Pinned',len(obligations),'obligations; inspected',len(audit),'source entries; instructions',agents)
