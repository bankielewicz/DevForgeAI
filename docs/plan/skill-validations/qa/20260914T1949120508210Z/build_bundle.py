"""Seal an explicitly partial evaluation bundle without manufacturing native runs."""
from bootstrap import ROOT, write, run
from prepare_trials import ref
import ast
import importlib.metadata
import json
from pathlib import Path
import sys

vectors=[]
def literal(node):
    if isinstance(node, ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='dict' and not node.args:
        return {x.arg:literal(x.value) for x in node.keywords}
    return ast.literal_eval(node)
# Literal expected assertions existed and failed before grader implementation.
tree=ast.parse((ROOT/'evaluation/test_graders.py').read_text(encoding='utf-8'))
for node in ast.walk(tree):
    if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):
        for call in ast.walk(node):
            if isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute) and call.func.attr=='assertEqual' and isinstance(call.args[0],ast.Call) and isinstance(call.args[0].func,ast.Name):
                inner=call.args[0]
                try:
                    args=[literal(x) for x in inner.args]
                    kwargs={x.arg:literal(x.value) for x in inner.keywords}
                    expected=literal(call.args[1])
                except ValueError:
                    continue
                vectors.append(dict(id='CTRL-'+node.name,function=inner.func.id,args=args,kwargs=kwargs,expected=expected))
write(ROOT/'evaluation/fixtures.json',vectors)
write(ROOT/'evaluation/expected-results.json',{v['id']:v['expected'] for v in vectors})
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['schema_version','case_id','kind','required','result','expected','observed','reason','evidence'],'properties':{'schema_version':{'const':'qa-eval-result-v1'},'case_id':{'type':'string','minLength':1},'kind':{'enum':['grader-control','skill-scenario']},'required':{'type':'boolean'},'result':{'enum':['PASS','FAIL','NOT_RUN','ERROR']},'expected':{},'observed':{},'reason':{'type':'string','minLength':1},'evidence':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['path','sha256'],'properties':{'path':{'type':'string'},'sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}}}}
write(ROOT/'inputs/evaluation-result.schema.json',schema)
write(ROOT/'evaluation/runtime.json',{'python':sys.version,'executable':sys.executable,'dependencies':{'stdlib':'required','PyYAML':importlib.metadata.version('PyYAML'),'coverage':importlib.metadata.version('coverage'),'jsonschema':importlib.metadata.version('jsonschema')},'native':'Codex CLI 0.154.0, inherited gpt-6-astra high; no model override','network':'Native CLI existing authenticated model transport only; fixtures have no network effects. No credentials copied.','coverage_denominator':'evaluation/graders.py only; runner/bootstrap/native harness excluded from this focused grader measurement and explicitly unmeasured. No framework executable code in target.','scope':'Three concrete cold project fixtures; 42 scenario obligations retained. Full native variants and complete deterministic report/evidence grading remain incomplete.'})
manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
items=[ROOT/'evaluation'/x for x in ['graders.py','test_graders.py','runner.py','fixtures.json','expected-results.json','runtime.json']]
items += [ROOT/'inputs/evaluation-result.schema.json',ROOT/'case-catalog.json',ROOT/'rule-set.json',ROOT/'source-manifest.json',ROOT/'native_trial.py',ROOT/'focused_batch.py']
items += [ROOT/'source'/row['path'] for row in manifest['files']]
items += [ROOT/row['snapshot_path'] for row in json.loads((ROOT/'input-bindings.json').read_bytes())]
for cid in ['QPV-01','QPV-02','QPV-06']:
    case=ROOT/'trials'/cid
    items += [case/'prompt.txt',case/'plan.json',case/'before.json']
    items += [case/'project'/r['path'] for r in json.loads((case/'before.json').read_bytes())['files']]
    items += list(case.glob('attempt-*'))
write(ROOT/'evaluation/bundle-manifest.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'qa','package_digest':manifest['package_digest'],'inputs':[ref(x) for x in sorted(set(items))],'scope':'Partial campaign; presence of bundle is not completed evaluation.'})
print('Sealed',len(set(items)),'inputs and',len(vectors),'independent controls')
