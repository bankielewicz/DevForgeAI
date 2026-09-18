import datetime, hashlib, json, os, pathlib, platform, re, shutil, sys
R=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('C:/Projects/DevForgeAI')
def write(p,s):
    p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def save(p,v):write(p,json.dumps(v,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for name in ['AGENTS.md','docs/plan/skill-validator-spec.md','docs/plan/skill-validator-adaptive-enhancement-spec.md']:
    p=ROOT/name;write('inputs/'+p.name,p.read_text(encoding='utf-8'))
for name in ['SKILL.md','scripts/quick_validate.py']:
    p=pathlib.Path('C:/Users/bryan/.codex/skills/.system/skill-creator')/name
    write('inputs/creator-'+p.name,p.read_text(encoding='utf-8'))
for name in ['adaptive-validation.md','rules.md','reporting.md']:
    p=ROOT/'.agents/skills/skill-validator/references'/name
    write('inputs/operational-'+name,p.read_text(encoding='utf-8'))
sources=[]
for p in sorted((R/'inputs').iterdir()):
    sources.append({'source_id':p.stem,'original_path':str(p),'url':'https://learn.chatgpt.com/docs/build-skills' if p.name=='openai-build-skills.md' else None,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':ref(p)['sha256'],'snapshot_path':ref(p)['path'],'sections':['entire document'],'freshness':'live_verified' if p.name=='openai-build-skills.md' else 'snapshot_only'})
save('sources.json',{'schema_version':'1','run_id':R.name,'sources':sources})
catalog=(R/'inputs/operational-adaptive-validation.md').read_text()
rules=[]
for line in catalog.splitlines():
    m=re.match(r'\| (AV-[A-Z][0-9]+) \| (.*?) \| (.*?) \|',line)
    if m:
        rules.append({'rule_id':m[1],'revision':'2026-09-12','title':m[1],'source_references':[ref(R/'inputs/operational-adaptive-validation.md')],'authority_class':'project_policy','applicability':'not_applicable' if m[1].startswith('AV-A') else 'applicable','method':'semantic','expected_observation':m[3],'required':True,'limitation':'Adaptive package execution rules do not apply to this ordinary validator package; its support for adaptive inputs is exercised by regression tests.' if m[1].startswith('AV-A') else m[2]})
save('rule-set.json',{'schema_version':'1','run_id':R.name,'rules':rules})
save('assessment-plan.json',{'scope':'Read-only development skill assessment; validator self-review with held-out subagent trial. No repair or installation.','python':sys.executable,'version':sys.version,'os':platform.platform(),'shell':'PowerShell 7','cwd':str(ROOT),'filesystem':'Windows C: native filesystem','target_digest':json.loads((R/'source-manifest.json').read_text())['package_digest'],'coverage_denominator':'Every Python file under captured source/scripts, including fixture-support custody/build modules; excludes only tests, generated synthetic fixtures and external dependencies. Line and branch separately. No first-party pragma exclusions.','cases':['installed creator check','operational structure','operational package scan','all captured unittest cases','independent helper probes','cold explicit validation','description routing'],'native_implicit_activation':'NOT_RUN: no discovery trial selected; explicit invocation cannot prove discovery','timeouts':{'utilities':120,'regression':600,'cold_agent':600},'retries':'None selected; preserve first attempts.','origin':'Base exact skill_name specification; enhancement document retained as supplemental context; historical build lineage unverified.'})
write('coverage.ini','[run]\nbranch = True\nparallel = True\nsource = '+str(R/'source/scripts')+'\ndata_file = '+str(R/'coverage/.coverage')+'\n[report]\nexclude_lines =\n')
(R/'coverage').mkdir();(R/'instrumentation').mkdir();(R/'temp').mkdir()
write('instrumentation/sitecustomize.py','import coverage\ncoverage.process_startup()\n')
P=R/'trials/cold/project'
(P/'invoice-total/scripts').mkdir(parents=True)
write('trials/cold/project/invoice-total/SKILL.md','---\nname: invoice-total\ndescription: Total a local JSON invoice containing signed integer amounts in cents.\n---\n# Invoice Total\nRun python -B scripts/total.py INPUT from this skill directory. Return its JSON total_cents. Negative line items are credits and reduce the total. Do not edit input files.\n')
write('trials/cold/project/invoice-total/scripts/total.py','import json,sys\nfrom pathlib import Path\ndata=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))\nprint(json.dumps({"total_cents":sum(x for x in data["amounts"] if x>0)}))\n')
write('trials/cold/project/invoice-spec.md','---\nskill_name: invoice-total\n---\n# Invoice Total contract\nInput is a local JSON object with amounts, a list of signed integer cents. Output is one JSON object with total_cents equal to the sum of every amount, including negative credits and zero. Empty input amounts yields zero. No network or input mutation. Deliver the computed total to the user.\n')
save('trials/cold/project/sample.json',{'amounts':[1200,-500,100]})
prompt='Use $skill-validator at '+str(R/'source/SKILL.md')+' to validate the skill at '+str(P/'invoice-total')+' against '+str(P/'invoice-spec.md')+'. Project root: '+str(P)+'. Produce the assessment and any justified revision proposal. Read only the selected validator, this synthetic project, and installed Skill Creator checker as needed. Write only under this synthetic project. Do not repair or install anything. No additional subagents, network calls, or external services. Use dated bundled guidance when needed. Keep the task bounded to 600 seconds and deliver the result paths.'
write('trials/cold/prompt.txt',prompt+'\n')
save('trials/cold/plan.json',{'case_id':'cold-invoice','timeout_seconds':600,'executor':'collaboration cold subagent, fork_turns=none','prompt':ref(R/'trials/cold/prompt.txt'),'inputs':[ref(p) for p in sorted(P.rglob('*')) if p.is_file()],'validator_manifest':ref(R/'source-manifest.json'),'expected':['report delivered','concrete finding: negative credits ignored, observed sample total 1300 vs required 800','revision proposal preserves signed-sum requirement and input preservation','source and spec unchanged','no framework acceptance claim'],'permitted_write_root':str(P),'isolation':'Task scope only; same host tools and filesystem. Not OS enforced isolation.'})
print(str(R))

