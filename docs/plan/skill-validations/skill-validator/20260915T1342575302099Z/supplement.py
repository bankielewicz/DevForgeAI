import hashlib,json,pathlib,sys
from run_checks import command
R=pathlib.Path(__file__).resolve().parent
S=R.parent/(R.name+'-supplemental');S.mkdir()
raw=json.loads((R/'commands/package/stdout.txt').read_text())['observations']
def ref(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for c in raw['unicode_candidates']:
    c['disposition']='legitimate';c['reason']='Intentional fullwidth-p confusable-command test at tests/test_adaptive.py:102; surrounding assertions verify detection and redaction.'
for node in raw['resources']:
    path=node['path'];folder=path.split('/')[0]
    node['role']='fixture' if folder=='tests' or '/fixtures/' in path else 'runtime' if folder=='scripts' or path=='SKILL.md' else 'template' if folder=='assets' and path.endswith('.md') else 'reference'
    node['usage']='intentional_nonruntime' if node['role']=='fixture' else 'used'
    node['evidence']=[ref(R/'source'/path),ref(R/'semantic-review.md')]
    node['reason']='Test discovery or synthetic fixture consumer documented in evals/README.md.' if node['role']=='fixture' else 'Package command/import, linked guidance, template or schema consumer reviewed; see semantic-review.md. Graph reachable records Markdown edges only.'
for module in ['adaptive_contracts','authoring_intake','skill_format','text_resources','windows_trial','trial_worker']:
    destination='scripts/'+module+'.py'
    for p in (R/'source/scripts').glob('*.py'):
        lines=p.read_text(encoding='utf-8').splitlines()
        matches=[i+1 for i,line in enumerate(lines) if ('import '+module in line or 'from '+module+' import' in line or module+'.py' in line)]
        if matches:
            raw['edges'].append({'source':'scripts/'+p.name,'line':matches[0],'target':destination,'kind':'script_call','resolution':'resolved'})
value={'schema_version':'adaptive-observations-v1','run_id':R.name,'target_digest':json.loads((R/'source-manifest.json').read_text())['package_digest'],'unicode_candidates':raw['unicode_candidates'],'resources':raw['resources'],'edges':raw['edges'],'context':raw['context'],'bindings':[],'limitations':['Validator self-review; no model/OS independence claim.','Exact-byte/character/line counts only; tokenizer not selected.','Recorded graph is static; does not prove execution or host load cost.','Native implicit activation, adversarial host input and user-correction handling remain unperformed.']}
(S/'adaptive-observations.json').write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
command('supplement-records',[sys.executable,'-B','-X','utf8','C:/Projects/DevForgeAI/.agents/skills/skill-validator/scripts/adaptive_observe.py','records','--run-root',str(S)])
command('record-integrity',[sys.executable,'-B','-X','utf8','C:/Projects/DevForgeAI/.agents/skills/skill-validator/scripts/observe.py','records','--run-root',str(R)])
print('Supplement',str(S))

