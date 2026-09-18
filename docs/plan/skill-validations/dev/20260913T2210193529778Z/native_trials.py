"""Bounded native dev trials using the inspected existing execution harness.

Only local synthetic fixture writes and the existing authenticated model connection
are authorized. No trust bypass, model/provider override, installation or repair.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

RUN=Path(__file__).resolve().parent
PROJECT=RUN.parents[4]
PRIOR=RUN.parent/'20260913T2136389781471Z'
HARNESS=PROJECT/'docs/plan/skill-validations/skill-validator/20260913T152602912596Z'
sys.path.insert(0,str(HARNESS))
import qa_harness as h
h.RUN=RUN
sys.path.insert(0,str(PROJECT/'.agents/skills/skill-validator/scripts'))
import observe

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n' if not isinstance(value,str) else value)

def setup():
    assert observe.make_manifest(PROJECT/'src/agents/skills/dev')['package_digest']=='7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae'
    receipt=json.loads((PRIOR/'FINAL-RECEIPT.json').read_bytes())
    for key in ('bundle_manifest','artifact_ledger','report','checks'):
        ref=receipt[key]; assert h.sha((PRIOR/ref['path']).read_bytes())==ref['sha256']
    for row in json.loads((PRIOR/'artifact-ledger.json').read_bytes())['files']:
        assert h.sha((PRIOR/row['path']).read_bytes())==row['sha256'],row['path']
    refs=json.loads((PRIOR/'inputs/input-index.json').read_bytes())
    for row in refs: assert h.sha(observe.read_stable(observe.safe_path(row['original_path'])))==row['snapshot']['sha256']
    save(RUN/'authorization.json',{'source':'User answered yes to authorization of cold Codex CLI trials using the existing authenticated model connection, product changes limited to disposable local fixtures.','timestamp_recorded':h.now(),'permission_changes':['Existing model connection authorized'],'unchanged_restrictions':['no target/operational repair','no installation','no plugins','no example application','no product network or credential inspection','no external writes'],'prior_run':str(PRIOR),'prior_receipt_sha256':h.sha((PRIOR/'FINAL-RECEIPT.json').read_bytes()),'input_readback':'MATCH','packet_intake':'prior REJECTED result retained; not repaired'})
    inp=RUN/'inputs'; inp.mkdir()
    shutil.copyfile(HARNESS/'qa_harness.py',inp/'qa_harness.py')
    shutil.copyfile(PRIOR/'bundle/scenarios.jsonl',inp/'prior-scenarios.jsonl')
    shutil.copyfile(PRIOR/'inputs/06-dev-skill-spec.md',inp/'dev-skill-spec.md')
    shutil.copyfile(PRIOR/'rule-set.json',inp/'rule-set.json')
    shutil.copyfile(PRIOR/'assessment/semantic-observations.json',inp/'prior-semantic-observations.json')
    shutil.copyfile(PRIOR/'FINAL-RECEIPT.json',inp/'prior-final-receipt.json')
    cases=[json.loads(line) for line in (inp/'prior-scenarios.jsonl').read_text(encoding='utf-8').splitlines()]
    plans=[]
    for case in cases:
        cid=case['case_id']
        if cid in ('DV-15','DV-16'): continue
        variants=['python','javascript'] if cid=='DV-03' else [None]
        for variant in variants:
            name=cid+('-'+variant if variant else '')
            base=RUN/'trials'/name
            if cid=='DV-18':
                project=base/'project space Ω $literal'
                fixture=PRIOR/'bundle/fixtures'/cid/'project space Ω $literal'
            else:
                project=base/'project'
                fixture=PRIOR/'bundle/fixtures'/cid
                if variant: fixture=fixture/variant
            before=h.inventory(fixture,project)
            h.inventory(RUN/'source',project/'trial-skill/dev')
            (project/'.trial-output').mkdir()
            selected=['spec.md']
            if cid=='DV-02': selected+=['consumer.md']
            if cid=='DV-06': selected+=['conflict.md']
            if cid=='DV-18': selected=['spec [input] Ω.md']
            scope='plan only' if cid=='DV-14' else 'analyze supplied synthetic QA evidence only' if cid=='DV-11' else 'resume selected checkpoint.json' if cid=='DV-13' else 'implement through applicable QA'
            evidence='custom receipts/' if cid=='DV-17' else 'evidence/'
            prompt=f'Use $dev at {project / "trial-skill/dev/SKILL.md"}. Selected disposable project: {project}. Selected specification documents: {json.dumps(selected,ensure_ascii=False)}. Requested scope: {scope}. Evidence destination: {evidence}. Read the raw local inputs. All product changes must remain in this disposable project. The trial-skill package, specification inputs and unrelated sentinel are read-only. No product network, credential inspection, installation, external connectors or external writes. Do not use earlier conversation history or memories. Deliver the resulting artifacts or precise remaining gap.'
            plan=dict(case,trial_id=name,permitted_write_root=str(project),task_prompt=prompt,fixture_origin=str(fixture),fixture_manifest=before,selected_specs=selected,authorization=str(RUN/'authorization.json'),timeout_seconds=120)
            save(base/'plan.json',plan)
            save(base/'prompt.txt',prompt)
            plans.append({'trial_id':name,'case_id':cid,'project':str(project),'plan':str(base/'plan.json'),'prompt_sha256':h.sha(prompt.encode())})
    save(RUN/'native-plan.json',{'run_id':RUN.name,'trials':plans,'case_count':18,'native_attempt_count':len(plans),'retained_cases':{'DV-15':'prior deterministic PASS after unchanged-byte readback','DV-16':'accepted authoring handoff prerequisite still rejected; product QA sub-observation may use DV-01/09 results'},'timeout_seconds':120,'retry_policy':'No automatic retries of completed/timeout attempts; host-start failures retain attempts and any sandbox escalation is separately authorized by host approval.','cold_isolation':'Fresh CLI process per case; shared inherited config and repository instructions may affect behavior. Before/after fixture readbacks are observations, not OS isolation proof.'})
    print('SETUP',len(plans),'native projects',flush=True)

def trial(name,attempt):
    base=RUN/'trials'/name
    plan=json.loads((base/'plan.json').read_bytes()); project=Path(plan['permitted_write_root'])
    prompt=(base/'prompt.txt').read_text(encoding='utf-8')
    saved=base/('attempt-'+attempt); saved.mkdir(exist_ok=False)
    save(saved/'before.json',h.inventory(project))
    cmd=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output'/('final-'+attempt+'.txt')),'-']
    record=h.execute(name+'-'+attempt,cmd,cwd=project,stdin=prompt,timeout=120)
    after=h.inventory(project)
    save(saved/'after.json',after)
    before=json.loads((saved/'before.json').read_bytes()); old={r['path']:r for r in before['files']}; new={r['path']:r for r in after['files']}
    changes=[p for p in sorted(old.keys()|new.keys()) if old.get(p)!=new.get(p)]
    immutable=['trial-skill/','spec.md','consumer.md','conflict.md','spec [input] Ω.md','unrelated.txt']
    save(saved/'effects.json',{'changed_paths':changes,'immutable_changes':[p for p in changes if any(p==x or p.startswith(x) for x in immutable)],'exclusions':after['exclusions'],'command_receipt':str(RUN/'commands'/(name+'-'+attempt)/'command.json')})
    save(saved/'result.json',record)
    print('COMPLETED',name,attempt,record['termination'],record.get('exit_status'),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='setup': setup()
    elif sys.argv[1]=='batch':
        # Each cold task owns a distinct fixture and retains its own receipts.
        # Limit concurrent model sessions to two; cases do not share outputs.
        import concurrent.futures
        plans=json.loads((RUN/'native-plan.json').read_bytes())['trials']
        names=[p['trial_id'] for p in plans if p['trial_id']!='DV-01']
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures={pool.submit(trial,name,'001'):name for name in names}
            for future in concurrent.futures.as_completed(futures):
                future.result()
    else: trial(*sys.argv[1:])
