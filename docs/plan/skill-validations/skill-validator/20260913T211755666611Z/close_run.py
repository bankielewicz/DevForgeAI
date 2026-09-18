"""Finalize retained command indexes and truthful delivery receipts."""
import json
from pathlib import Path
import re
from harness import RUN, ROOT, TARGET, LOADED, SPECS, read, write, save, ref, inventory, sha, now

BUILD=ROOT/'docs/plan/skill-adaptive-implementations/skill-validator/20260913T211315150947Z'
candidate=json.loads(read(BUILD/'candidate-manifest.json'))
assert inventory(TARGET)['files']==candidate['files']
assert inventory(LOADED)['files']==json.loads(read(BUILD/'inputs/loaded-evaluator-before.json'))['files']
assert inventory(ROOT/'src/agents/skills/skill-builder')['files']==json.loads(read(BUILD/'inputs/companion-before.json'))['files']
for name,digest in SPECS.items(): assert sha(read(ROOT/'docs/plan'/name))==digest
for case in ('LEGACY-RECORDS','ADAPTIVE-RECORDS','STRUCTURAL','BOUND-EVALUATOR','READBACK'):
    assert json.loads(read(RUN/'commands'/case/'receipt.json'))['exit']==0
assert sha(read(ROOT/'AGENTS.md'))==sha(read(BUILD/'inputs/AGENTS.md'))

def index(base):
    commands=[json.loads(read(p/'receipt.json')) for p in sorted((base/'commands').iterdir()) if (p/'receipt.json').exists()]
    # The implementation directory is a separately authorized write root; use
    # explicit native paths, never move or rewrite any previous run.
    payload=json.dumps(commands,ensure_ascii=False,indent=2)+'\n'
    with (base/'command-log.json').open('x',encoding='utf-8',newline='\n') as stream: stream.write(payload)
    lines=['# Exact command/results log','', 'See each plan/receipt for temporary roots, timestamps and stream digests. The full regression failure and pre-repair reproduction are retained. No failed command was silently retried.','']
    for r in commands:
        cid=r['case_id']
        lines += [f'## {cid}','', '```json',json.dumps(r['argv'],ensure_ascii=False),'```','',f"Cwd: `{r['cwd']}`. Start {r['start']}; end {r['end']}; elapsed {r['elapsed_seconds']:.3f}s; exit {r['exit']}; timed out {r['timed_out']}.",f'[stdout](commands/{cid}/stdout.txt) · [stderr](commands/{cid}/stderr.txt) · [receipt](commands/{cid}/receipt.json)','']
    with (base/'command-log.md').open('x',encoding='utf-8',newline='\n') as stream: stream.write('\n'.join(lines))
    return len(commands)

command_count=index(RUN)
index(BUILD)
summary=json.loads(read(RUN/'coverage-summary.json'))
delta=json.loads(read(BUILD/'candidate-delta.json'))
report=f'''# Four confirmed defects repaired

The four selected fixes are implemented and independently revalidated. The delivered development package has **76 files**, SHA-256 `{candidate['package_digest']}`. Operational copies were not updated.

## Changes

- `scripts/adaptive_observe.py`: one artifact/execution registry covers member and integration checks; native case normalization prevents Windows alias reuse. Repeated execution identities are rejected without banning shared supporting citations. Required handoffs cannot be hidden behind required N/A rows, including beside a passing row.
- `scripts/text_resources.py`: literal JSON/JSONL protocol-version spans receive located unresolved Unicode candidates. Fence closing rules preserve examples and correctly resume real link/anchor extraction. Public interfaces and closed schemas are unchanged.
- `tests/test_confirmed_findings.py`: 20 new regression methods cover the defects and discriminating controls. All existing tests are unchanged.
- `evals/build-manifest.json`: exact complete artifact digests refreshed; profile/grader definitions preserved. Generated JSON was serialized with LF line endings. No required evaluator artifacts were removed.

## TDD and QA

Red: 20 new methods executed before production edits; 13 requirement failures, no setup errors. Green: all 20 passed. Refactor: removed one unused test import; no unrelated production restructuring. Full QA reran the new methods with the preserved suite.

Fresh QA: all 37 retained cases matched; separate review contributed 16 passing contextual probes and static record-integrity review. Installed structural checker, actual bound evaluator profile, and legacy/new record checks passed. Tests of target helpers are self-review supplemented by independent expectations and a separate agent context.

Full discovery: 249 methods (229 preserved plus 20 added). 248 passed; one existing method failed in seven message-assertion subtests. The exact failures reproduce on unchanged pre-repair validator bytes with the same companion. These tests were not weakened and companion code was not repaired. Line coverage is {summary['line']['percent']:.4f}% over all nine first-party support scripts, below 95%; branch coverage is {summary['branch']['percent']:.4f}%.

**Selected repair verification: PASS. Full package acceptance: FAIL** because a required regression and the coverage floor remain unmet. Unperformed native/resume/activation/lifecycle/tokenizer/Rust qualification remains separate.

## Preservation and remaining work

Only the four listed development paths changed; no files were removed. The frozen proposal and both specifications matched preflight. An exact observed scoped-edit base and previous implementation receipt were retained; no generated/adopted provenance was fabricated. Current authorization selected these maintenance edits. Final target readback matches the candidate; operational evaluator and companion byte inventories match their pre-edit states.

The requested [workflow plan](../../../skill-validator-confirmed-findings-remediation-workflow.md) is saved. [Fresh QA](../../../skill-validations/skill-validator/{RUN.name}/qa-report.md), [stable-finding resolution](../../../skill-validations/skill-validator/{RUN.name}/resolution-map.json), [change manifest](candidate-delta.json), [candidate patch](candidate.patch) and [TDD commands](command-log.md) are retained.

Next scope: reconcile the existing authoring-test error-message contract; add meaningful coverage for the declared uncovered denominator; complete the separate native acceptance gaps. No further repair to the four selected issues is supported by current evidence.
'''
with (BUILD/'implementation-report.md').open('x',encoding='utf-8',newline='\n') as stream: stream.write(report)

links=[]
for base,names in [(RUN,['qa-report.md','command-log.md']),(BUILD,['implementation-report.md','command-log.md'])]:
    for name in names:
        for target in re.findall(r'\]\(([^)]+)\)',read(base/name).decode()):
            if target.startswith(('http://','https://')): continue
            assert (base/target.split('#')[0]).exists(), (name,target)
            links.append({'document':str(base/name),'target':target,'exists':True})
save(RUN/'final-link-audit.json',{'links':links,'manual_review':'Original/fresh fixture outcomes, source line changes, unchanged source comparison, regression subtest units and coverage arithmetic reviewed. Record integrity alone is not semantic approval.'})
save(RUN/'final-receipt.json',{'completed_at':now(),'assessment_completed':True,'selected_findings':'QA-01 through QA-04 RESOLVED','selected_repair_verification':'PASS','full_package_acceptance':'FAIL','target_digest':candidate['package_digest'],'target_files':76,'required_probes':{'pass':37,'total':37},'independent_contextual_probes':{'pass':16,'total':16},'regression':summary['regression_methods'],'coverage':summary,'source_readback':'UNCHANGED since candidate freeze','loaded_evaluator_readback':'UNCHANGED','companion_readback':'UNCHANGED','specifications':'UNCHANGED','operational_installation':'NOT_PERFORMED','rust_qualification':'NOT_RUN','native_acceptance':'NOT_RUN','qa_report':ref(RUN/'qa-report.md'),'resolution_map':ref(RUN/'resolution-map.json'),'independent_review':ref(RUN/'independent-review/independent-review.md'),'command_log':ref(RUN/'command-log.json'),'final_readback':ref(RUN/'final-input-readback.json'),'followup':'Existing authoring assertion mismatch, coverage floor, separate native qualification gaps.'})
receipt={'completed_at':now(),'implementation':'DELIVERED','selected_defects':'RESOLVED','verification':'PASS for four selected defects; full acceptance FAIL','package_files':76,'package_digest':candidate['package_digest'],'changed_paths':delta['changed'],'removed':[],'qa_receipt':ref(RUN/'final-receipt.json'),'report':ref(BUILD/'implementation-report.md'),'authorization':ref(BUILD/'authorization.json'),'workflow':ref(ROOT/'docs/plan/skill-validator-confirmed-findings-remediation-workflow.md')}
with (BUILD/'final-receipt.json').open('x',encoding='utf-8',newline='\n') as stream: json.dump(receipt,stream,indent=2)
print(json.dumps({'workflow':str(ROOT/'docs/plan/skill-validator-confirmed-findings-remediation-workflow.md'),'implementation':str(BUILD/'implementation-report.md'),'qa':str(RUN/'qa-report.md'),'qa_commands':command_count,'selected_repairs':'PASS','full_acceptance':'FAIL','digest':candidate['package_digest']}))
