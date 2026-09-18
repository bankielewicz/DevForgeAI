"""Separate standalone scope following rejected authoring intake; no packet repair."""
from prepare import *
import re

inputs = ROOT / 'inputs'
write(ROOT/'standalone-scope.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'dev','basis':'User explicitly selected target and governing specification independently of packet. Rejected packet never establishes builder readiness.','request_sha256':EXPECTED,'rejection':'authoring contract/request mismatch: target_root slash spelling differs','package_digest':json.loads((ROOT/'source-manifest.json').read_bytes())['package_digest']})
write(ROOT/'capabilities.json',{'platform':platform.platform(),'python':sys.version,'python_executable':sys.executable,'shell':'PowerShell','filesystem':'Windows C: native','codex':shutil.which('codex'),'network_trials':'NOT_AUTHORIZED by selected packet; pending separate current authorization','allowed_effects':['fresh validation evidence','disposable synthetic fixtures'],'prohibited_effects':['target repair','operational changes','plugin','example application','external writes','credentials'],'coverage_denominator':'No first-party executable framework code selected or changed; framework coverage NOT_RUN, no passing percentage.'})
run('python-dependencies',[sys.executable,'-B','-X','utf8','-c','import sys,yaml,importlib.util; print(sys.version); print("PyYAML",yaml.__version__); print("tiktoken",bool(importlib.util.find_spec("tiktoken"))); print("coverage",bool(importlib.util.find_spec("coverage")))'])
run('codex-version',[shutil.which('codex'),'--version'])
run('codex-exec-help',[shutil.which('codex'),'exec','--help'])
rules=[]
spec=(inputs/'06-dev-skill-spec.md').read_text(encoding='utf-8')
for match in re.finditer(r'\*\*(DEV-\d{3}) — ([^*]+)\*\*(.*?)(?=\n\*\*DEV-|\n## |\Z)',spec,re.S):
    rules.append({'rule_id':match[1],'revision':'1','title':match[2],'source_refs':[dict(ref(inputs/'06-dev-skill-spec.md'),source_id='dev-spec',locator=match[1])],'authority_class':'project_policy','applicability':'applicable','method':'semantic','expected_observation':match[0],'required':True,'limitation':'Static contract assessment separated from native behavior.'})
av=(inputs/'09-adaptive-validation.md').read_text(encoding='utf-8')
for line in av.splitlines():
    if not line.startswith('| AV-'): continue
    ident,method,expected=[p.strip() for p in line.strip('|').split('|')][:3]
    na=ident.startswith('AV-A') or ident=='AV-F04'
    rules.append({'rule_id':ident,'revision':'2026-09-12','title':ident,'source_refs':[dict(ref(inputs/'09-adaptive-validation.md'),source_id='av-catalog',locator=ident)],'authority_class':'project_policy','applicability':'not_applicable' if na else 'applicable','method':'behavioral' if ident in ('AV-W01','AV-W02') else 'semantic','expected_observation':expected,'required':True,'limitation':'Ordinary standalone skill; no adaptive contract, set, or optional host metadata.' if na else 'Observations need separate semantic adjudication.'})
assert len(rules)==55
write(ROOT/'rule-set.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'dev','rules':rules})
identity=json.loads((inputs/'input-index.json').read_bytes())
write(ROOT/'sources.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'dev','sources':[{'source_id':'dev-spec' if i==6 else 'av-catalog' if i==9 else f'input-{i}','original_path':row['original_path'],'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sha256':row['snapshot']['sha256'],'snapshot_path':row['snapshot']['path'],'sections':'complete retained input','freshness':'current_local'} for i,row in enumerate(identity)]})
run('structure',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(ROOT/'source')])
run('creator-check',[sys.executable,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(ROOT/'source')])
run('package',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'package','--source',str(ROOT/'source'),'--tokenizer','tiktoken','--encoding','cl100k_base'])
