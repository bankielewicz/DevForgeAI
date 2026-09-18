"""Independently reduce retained observations and live byte readback; no target writes."""
import json
from pathlib import Path
from preflight import ROOT, RUN, PACKET, TARGET, capture, sha
from prepare_origin import ORIGIN
from workflow import js, ref, read, now, BUILDER

rows,excluded=capture(TARGET)
assert not excluded
before=read(PACKET/'source-manifest.json')['files']
assert rows==read(RUN/'final-delivery-readback.json')['files']
assert rows==capture(RUN/'published/revision/N')[0]
assert rows==capture(RUN/'published/revision/after')[0]
assert [r['path'] for r in rows]==[r['path'] for r in before]
delta=[r['path'] for r,b in zip(rows,before) if r!=b]
assert delta==['evals/build-manifest.json','references/evidence-format.md']
old=(RUN/'published/revision/B/references/evidence-format.md').read_bytes()
new=(TARGET/'references/evidence-format.md').read_bytes()
assert new==old.replace(b'builder enhancements require the three actual trials in the evaluation reference.',b'builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements).')
assert (TARGET/'evals/build-manifest.json').read_bytes()==(RUN/'published/revision/B/evals/build-manifest.json').read_bytes().replace(sha(old).encode(),sha(new).encode())
manifest=read(TARGET/'evals/build-manifest.json')
assert manifest['artifacts']=={r['path']:r['sha256'] for r in rows if r['path']!='evals/build-manifest.json'}
profiles=[]
for label,base,count in [('adoption',ORIGIN,1),('candidate',RUN,3),('delivered',RUN,3),('published',RUN,3)]:
    path=base/(label+'-results.jsonl')
    records=[json.loads(line) for line in path.read_text().splitlines()]
    cases=base/(label+'-cases.jsonl')
    assert len(records)==count
    for record in records:
        assert record['status']==record['expected']=='PASS' and record['expectation_met'] and record['error'] is None
        assert record['cases_sha256']==sha(cases.read_bytes())
    profiles.append({'label':label,'profile':records[0]['profile'],'records':count,'all_expected_pass':True,'cases':str(cases),'cases_sha256':sha(cases.read_bytes()),'results':str(path),'results_sha256':sha(path.read_bytes())})
commands=[]
for base in [ORIGIN,RUN]:
    for folder in sorted((base/'commands').iterdir()):
        if not folder.is_dir(): continue
        plan=read(folder/'plan.json'); attempt=read(folder/'attempt-001.json')
        assert attempt['exit_code']==plan['expected_exit']==0
        assert sha((folder/'stdout.txt').read_bytes())==attempt['stdout_sha256']
        assert sha((folder/'stderr.txt').read_bytes())==attempt['stderr_sha256']
        for snapshot in plan['input_snapshots']:
            if 'files' in snapshot:
                assert capture(Path(snapshot['snapshot']))[0]==snapshot['files']
            else:
                assert sha(Path(snapshot['snapshot']).read_bytes())==snapshot['sha256']
        commands.append({'plan':str(folder/'plan.json'),'plan_sha256':sha((folder/'plan.json').read_bytes()),'attempt':str(folder/'attempt-001.json'),'attempt_sha256':sha((folder/'attempt-001.json').read_bytes()),'command':plan['command'],'exit_code':attempt['exit_code'],'started':attempt['started'],'finished':attempt['finished']})
assert capture(BUILDER)[0]==capture(ORIGIN/'commands/adoption-plan/inputs/1')[0], 'operational builder changed'
digest=sha(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode())
assert digest=='c9af00b9c81fa0f417fdffcbac6f2b33f3c304b02fca05aff5b3a519fdd60cf3'
out={'schema_version':'1','timestamp':now(),'status':'DELIVERY_VERIFIED_FRESH_VALIDATION_SEPARATE','target':str(TARGET),'target_package_digest':digest,'files':rows,'delta':delta,'profiles':profiles,'command_receipts':commands,'operational_builder':'UNCHANGED','approved_spec_sha256':sha((PACKET/'revision-spec.md').read_bytes()),'approved_manifest_sha256':sha((PACKET/'source-manifest.json').read_bytes()),'independent_delta_review':ref(RUN,RUN/'independent-delta/review.md'),'origin_fidelity_review':ref(ORIGIN,ORIGIN/'independent-origin-review/review-final.md')}
js(RUN/'delivery-audit.json',out)
lines=['# Command and tool evidence','', 'All commands below ran from `C:/Projects/DevForgeAI`. Exact argument arrays, pre-execution input snapshots, timestamps, separate stdout/stderr, expected/actual exits, and readback are retained in the linked command directories. Commands used 120-second subprocess limits. No required evaluation failed or required a retry.','', '| Start UTC | Command | Exit | Receipt |','| --- | --- | --- | --- |']
for c in commands:
    link=Path(c['attempt']).relative_to(ROOT).as_posix()
    lines.append('| '+c['started']+' | `'+json.dumps(c['command'])+'` | '+str(c['exit_code'])+' | ['+Path(c['attempt']).parent.name+']('+str(Path(c['attempt']).as_posix())+') |')
lines+=['','## Primary orchestration and authoring','', 'The primary session executed these commands with `python -B -X utf8`, each returning exit 0: `preflight.py`, `prepare_origin.py`, then `workflow.py adoption-prepare`, `adoption-publish`, `contract`, `candidate`, `deliver`, `publish`, and `environment`. All scripts live in this build run. The live package was written only by the bounded `deliver` stage. `delivery-before.json` and `delivery-attempt-001.json` retain the preceding live readback and each actual mutation. Tool-based authoring used apply_patch for external run scripts/origin documents; the exact patches and combined shell outputs remain in the session transcript.','', 'Initial read-only intake used PowerShell Get-Content/Get-FileHash/Get-ChildItem and rg to inspect the explicitly selected skills, packet, related references, Python availability and known evidence. Some broad tool output was truncated; later targeted reads and machine parsing consumed the complete selected inputs. Those exploratory outputs were combined streams in the tool transcript, not fabricated separate stdout/stderr files. Independent history, origin and delta reviews retain their own commands and measurements in their assigned directories.','', 'The origin reviewer identified one draft-only CONFLICT/PARTIAL summary imprecision; the initial origin and review are retained, and the corrected origin received a new exact-digest review before adoption. This was not a target edit or failed adoption.','', 'CLI identification exited 0 and reported codex-cli 0.154.0. It emitted access-denied warnings for cleanup/PATH alias preparation under the personal temp path; stderr is retained. This identification did not provide native activation or runtime qualification. No dependency installation or permission escalation was performed.','', 'Every required evaluator case file and complete evaluator/input snapshot was retained before execution, and subsequent readback found no changes. The delivered-stage PARTIAL schema record is explicitly an intermediate pre-evaluation state; successful final APPLIED/COMPLETE records were published only after actual delivery checks and readback. Earlier stage bytes remain intact.','']
(RUN/'command-log.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'status':out['status'],'package_digest':digest,'commands':len(commands),'profiles':profiles,'delta':delta},indent=2))
