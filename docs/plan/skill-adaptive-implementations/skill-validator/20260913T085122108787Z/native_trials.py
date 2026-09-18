"""Reviewed bounded Codex CLI fixtures. No auth/model/config overrides."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from capture import ROOT, RUN, scan

TRIALS = RUN / 'native-trials'
def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2))

def setup():
    TRIALS.mkdir(exist_ok=False)
    project = TRIALS / 'handoff-project'
    (project / 'out').mkdir(parents=True)
    (project / 'docs').mkdir()
    (project / 'docs/requirements.md').write_text('REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\n',encoding='utf-8')
    (project / 'AGENTS.md').write_text('This is a synthetic task-card exercise. Use local terminal tools only. No network, connectors, credential reads, dependency installation, server, application implementation, or writes outside this project. Read only the selected skill and raw inputs.\n',encoding='utf-8')
    schema = {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['schema_version','requirement_id','task','verification'],'properties':{'schema_version':{'const':'task-card-v1'},'requirement_id':{'const':'REQ-7'},'task':{'type':'string','minLength':1},'verification':{'type':'array','minItems':1,'items':{'type':'string','minLength':1}}}}
    save(project/'task-card.schema.json',schema)
    for name,body in [('card-producer','Read docs/requirements.md and task-card.schema.json. Write only out/task-card.json satisfying that schema and describing supplied REQ-7 with an observable verification. Do not implement the endpoint or start a server. Missing input: report failure without a card. Completion is the saved valid card and its path.'),('card-consumer','Read only out/task-card.json and task-card.schema.json. If the card is missing, report missing-input failure without writing a receipt. Otherwise validate the exact closed schema and write only out/receipt.json: {"schema_version":"task-receipt-v1","requirement_id":"REQ-7","status":"ACCEPTED" or "REJECTED","reason":nonempty string}. Valid cards yield ACCEPTED and identify their verification. Missing verification or wrong schema_version yields REJECTED naming the exact invalid field. Do not change the card or implement the endpoint.')]:
        path = project/'skills'/name
        path.mkdir(parents=True)
        (path/'SKILL.md').write_text('---\nname: '+name+'\ndescription: Produce a requirement card.\n---\n'+body+'\n',encoding='utf-8')
    save(TRIALS/'expectations.json',{'VAT-17':{'producer':'closed task-card-v1, REQ-7, nonempty task/verification; only out/task-card.json','consumer':'real unchanged producer output; new task; ACCEPTED identifies verification; only out/receipt.json'},'VAT-19':{'explicit':'actual CLI events/final artifacts; host failure NOT_RUN','implicit':'NOT_RUN unless reliable selection event'},'timeout_seconds':120,'boundary':'Requested workspace-write; host configuration retained, not a proof of OS isolation; external tool use prohibited by fixture scope.'})

def execute(role,scenario=None):
    project = TRIALS/'handoff-project'
    if scenario:
        project = TRIALS/scenario
        if not project.exists():
            shutil.copytree(TRIALS/'handoff-project',project,ignore=shutil.ignore_patterns('out','.trial-output'))
            (project/'out').mkdir()
            card = json.loads((TRIALS/'handoff-project/out/task-card.json').read_bytes())
            if scenario=='negative-version':
                card['schema_version'] = 'task-card-v2'
            elif scenario=='negative-verification':
                del card['verification']
            elif scenario=='optional-absent':
                path = project/'skills/card-consumer/SKILL.md'
                path.write_text(path.read_text().replace('If the card is missing, report missing-input failure without writing a receipt.','If the optional card is missing, write out/receipt.json with schema_version task-receipt-v1, requirement_id REQ-7, status REJECTED and reason OPTIONAL_INPUT_ABSENT.'))
            elif scenario=='changed-contract':
                schema = json.loads((project/'task-card.schema.json').read_bytes())
                schema['properties']['schema_version']['const'] = 'task-card-v2'
                save(project/'producer-card.schema.json',schema)
                path = project/'skills/card-producer/SKILL.md'
                path.write_text(path.read_text().replace('task-card.schema.json','producer-card.schema.json'))
            if scenario not in ('required-absent','optional-absent','changed-contract'):
                save(project/'out/task-card.json',card)
            save(TRIALS/(scenario+'-expectations.json'),{'category':'independent negative consumer input' if scenario.startswith('negative') else 'dependency absence branch','expected_status':'REJECTED' if scenario!='required-absent' else 'no receipt','expected_reason':'schema_version' if scenario=='negative-version' else 'verification' if scenario=='negative-verification' else 'OPTIONAL_INPUT_ABSENT' if scenario=='optional-absent' else 'missing input','permitted_effects':['out/receipt.json'] if scenario!='required-absent' else []})
    if role == 'consumer' and not scenario and not (project/'out/task-card.json').exists():
        save(TRIALS/'consumer-not-run.json',{'status':'NOT_RUN','reason':'Required producer artifact unavailable.'})
        return
    label = (scenario+'-' if scenario else '')+role
    number = len(list(TRIALS.glob(label+'-attempt-*')))+1
    folder = TRIALS/(label+'-attempt-'+str(number).zfill(3))
    folder.mkdir()
    output = project/'.trial-output'/(role+'-'+str(number).zfill(3))
    output.mkdir(parents=True)
    skill = 'card-'+role
    prompt = 'Use $'+skill+' at '+str(project/'skills'/skill/'SKILL.md')+' to complete its local task-card workflow. Allowed product write: '+('out/task-card.json' if role=='producer' else 'out/receipt.json')+'. All other files are read-only; do not use network, external connectors or application services.'
    argv = [shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(output/'final.txt'),'-']
    save(folder/'plan.json',{'argv':argv,'prompt':prompt,'timeout_seconds':120,'before':scan(project),'start':dt.datetime.now(dt.timezone.utc).isoformat()})
    card = (project/'out/task-card.json').read_bytes() if role=='consumer' and (project/'out/task-card.json').exists() else None
    with (folder/'stdout.jsonl').open('wb') as out, (folder/'stderr.txt').open('wb') as err:
        process = subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=project)
        try:
            process.communicate(prompt.encode('utf-8'),timeout=120)
            code,termination = process.returncode,'exited'
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=err,stderr=err,timeout=15)
            process.wait(timeout=15)
            code,termination = None,'timeout-tree-terminated'
    unchanged = None if card is None else (project/'out/task-card.json').read_bytes() == card
    save(folder/'result.json',{'exit_code':code,'termination':termination,'producer_unchanged':unchanged,'after':scan(project),'end':dt.datetime.now(dt.timezone.utc).isoformat()})
    print(json.dumps({'role':role,'exit_code':code,'termination':termination,'evidence':str(folder)}))
    print((folder/'stderr.txt').read_text(encoding='utf-8',errors='replace')[-2500:])

if __name__ == '__main__':
    setup() if sys.argv[1]=='setup' else execute(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
