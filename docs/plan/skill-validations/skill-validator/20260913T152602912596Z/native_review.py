"""Actual CLI trials, existing config/auth/model; no bypass flags."""
import json
import os
from pathlib import Path
import shutil
import sys
from qa_harness import RUN, ROOT, TARGET, execute, inventory, save, sha

NATIVE=RUN/'trials/native'
SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['schema_version','requirement_id','task','verification'],'properties':{'schema_version':{'const':'task-card-v1'},'requirement_id':{'const':'REQ-7'},'task':{'type':'string','minLength':1},'verification':{'type':'array','minItems':1,'items':{'type':'string','minLength':1}}}}

def text(path,content):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding='utf-8')

def setup():
    NATIVE.mkdir(parents=True,exist_ok=False)
    for scenario in ('handoff','changed-producer','negative-verification','required-absent','optional-absent','full-validator','implicit'):
        p=NATIVE/scenario
        (p/'.trial-output').mkdir(parents=True)
        (p/'out').mkdir()
        text(p/'AGENTS.md','Synthetic QA fixture. Local files only; no external connectors, network requests, credential inspection, installation, configuration changes, servers, or writes outside this fixture. Use the selected skill and task only. Reports may be created only when the current task explicitly authorizes them.\n')
        text(p/'docs/requirements.md','REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.\n')
        save(p/'task-card.schema.json',SCHEMA)
        text(p/'skills/card-producer/SKILL.md','---\nname: card-producer\ndescription: Turn the supplied local requirement into a schema-bound JSON task card.\n---\nRead docs/requirements.md and producer-card.schema.json if present, otherwise task-card.schema.json. Write only out/task-card.json satisfying that schema and describing REQ-7 with an observable verification. On missing input report failure without a card. Do not implement application code or run a server. Deliver the saved card path.\n')
        optional=scenario=='optional-absent'
        text(p/'skills/card-consumer/SKILL.md','---\nname: card-consumer\ndescription: Validate an existing local task card and return a receipt.\n---\nRead out/task-card.json and task-card.schema.json. Preserve the card bytes. '+('When the optional card is absent write a REJECTED receipt with reason OPTIONAL_INPUT_ABSENT.' if optional else 'When the required card is absent report missing-input failure and write no receipt.')+' Otherwise validate the closed schema. Write only out/receipt.json, closed fields schema_version task-receipt-v1, requirement_id REQ-7, status ACCEPTED or REJECTED, nonempty reason. ACCEPTED identifies the card verification; invalid cards yield REJECTED naming each invalid field. Do not implement the endpoint.\n')
        if scenario=='changed-producer':
            changed=json.loads(json.dumps(SCHEMA)); changed['properties']['schema_version']['const']='task-card-v2'
            save(p/'producer-card.schema.json',changed)
        if scenario=='negative-verification':
            save(p/'out/task-card.json',{'schema_version':'task-card-v1','requirement_id':'REQ-7','task':'Document the health endpoint'})
        if scenario in ('full-validator','implicit'):
            inventory(TARGET,p/'.agents/skills/skill-validator')
            text(p/'candidate/brief-note/SKILL.md','---\nname: brief-note\ndescription: Summarize supplied notes in exactly three short bullets. Use for note summaries; exclude implementation and deployment.\n---\nRead the supplied notes. Return exactly three bullets faithful to the notes. If no notes were supplied, ask for them. Do not write files or contact services.\n')
            text(p/'candidate-spec.md','---\nskill_name: brief-note\n---\nAssess this ordinary instruction-only note summarizer. It must return three factual bullets from notes, request missing notes, and create no files or external effects. No adaptive descriptor, runtime binding, scripts, tokenizer or installation is required.\n')
    save(NATIVE/'expectations.json',{'timeout_seconds':120,'producer':'Only card output; exact schema and REQ-7 with observable verification','consumer':'Fresh task uses unchanged real producer bytes; ACCEPTED identifies verification; v2 and missing verification REJECTED field named','required-absent':'No receipt; missing input failure','optional-absent':'REJECTED OPTIONAL_INPUT_ABSENT','full-validator':'Complete bounded report or honest INCOMPLETE; original candidate unchanged','implicit':'Selection signal required; resemblance does not prove activation','effects_boundary':'Actual workspace-write CLI with inherited config; prompt and manifest checks are not OS isolation proof'})

def run(scenario,role,attempt):
    p=NATIVE/scenario
    if role=='consumer' and scenario in ('handoff','changed-producer') and not (p/'out/task-card.json').exists():
        save(NATIVE/(scenario+'-consumer-not-run.json'),{'result':'NOT_RUN','reason':'Required producer artifact absent'})
        return
    if role in ('producer','consumer'):
        prompt=f'Use $card-{role} at {p / "skills" / ("card-"+role) / "SKILL.md"} to complete its local task-card workflow. Allowed product write: out/'+('task-card.json' if role=='producer' else 'receipt.json')+'. All other inputs are read-only. Deliver the artifact path or concrete failure.'
    else:
        invoke=('Use $skill-validator at '+str(p/'.agents/skills/skill-validator/SKILL.md')+'. ') if scenario=='full-validator' else ''
        prompt=invoke+'Validate candidate/brief-note against candidate-spec.md in this synthetic project. Complete a proportionate ordinary-skill assessment and retain evidence under docs/plan/skill-validations. The target and specification are read-only. Only local bounded tests and assessment evidence writes inside this fixture are authorized. Do not install, repair, invoke builder, or use external services.'
    name=f'native-{scenario}-{role}-{attempt}'
    before=inventory(p)
    save(NATIVE/(name+'-before.json'),before)
    card=(p/'out/task-card.json').read_bytes() if role=='consumer' and (p/'out/task-card.json').exists() else None
    record=execute(name,[shutil.which('codex'),'exec','--cd',str(p),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(p/'.trial-output'/(name+'.txt')),'-'],cwd=p,stdin=prompt)
    after=inventory(p)
    old={x['path']:x for x in before['files']}; new={x['path']:x for x in after['files']}
    save(NATIVE/(name+'-effects.json'),{'before_digest':before['package_digest'],'after':after,'changed':[x for x in old.keys()|new.keys() if old.get(x)!=new.get(x)],'producer_artifact_unchanged':card is None or card==(p/'out/task-card.json').read_bytes(),'result':record})

if __name__=='__main__':
    setup() if sys.argv[1]=='setup' else run(*sys.argv[1:])
