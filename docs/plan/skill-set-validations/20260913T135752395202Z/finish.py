"""Report selected-pair compatibility, validate record families, seal readbacks."""
import datetime
import hashlib
import json
from pathlib import Path
import sys
from run_checks import execute
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
V=ROOT/'.agents/skills/skill-validator'
sys.path.insert(0,str(V/'scripts'))
import observe
import adaptive_observe as ao
PY=[sys.executable,'-B','-X','utf8']
def sha(data): return hashlib.sha256(data).hexdigest()
def ref(path): return {'path':str(path),'sha256':sha(path.read_bytes())}
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream: json.dump(value,stream,indent=2,ensure_ascii=False)
def text(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream: stream.write(value)
members=json.loads((RUN/'member-records.json').read_text())['members']
cases=json.loads((RUN/'compatibility-results-round2.json').read_text())['cases']+json.loads((RUN/'additional-results.json').read_text())['cases']
supp=RUN/'supplemental'
supp.mkdir()
text(RUN/'authorization.txt','Current user request: run checks with the updated skill-validator to understand whether it meets the needs of the updated skill-builder. Selected pair is validator and builder only. Scope is read-only compatibility assessment and fresh bounded synthetic tests; no repair or installation.\n')
packages=[]
for label,path in [('validator',V),('builder',ROOT/'src/agents/skills/skill-builder')]:
    manifest=json.loads((ROOT/'docs/plan/skill-validations'/('skill-'+label)/RUN.name/'source-manifest.json').read_text())
    output=RUN/'integration-inputs'/(label+'-manifest.json')
    write(output,manifest['files'])
    packages.append({'member_id':label,'package':{'name':'skill-'+label,'root':str(path),'manifest':ref(output),'package_digest':manifest['package_digest']},'specifications':[ref(RUN/'inputs'/('skill-'+label+'-adaptive-enhancement-spec.md'))],'adaptive_descriptor':None,'depends_on':[]})
selected={'schema_version':'standalone-set-input-v1','run_id':RUN.name,'authorization':ref(RUN/'authorization.txt'),'members':packages,'handoffs':[],'requirements':[],'gaps':[]}
write(supp/'selected-pair.json',selected)
integration=[]
for case in cases:
    success=case['validator_exit']==case['expected_exit']
    evidence_path=Path(case['validator_evidence'])/'stdout.txt'
    integration.append({'schema_version':'1','run_id':RUN.name,'check_id':case['case'],'rule_id':'AV-R03','subject_path':'members/validator','dimension':'workflow','method':'deterministic','required':True,'applicability':'applicable','result':'PASS' if success else 'FAIL','reason':'Expected validator exit '+str(case['expected_exit'])+'; observed '+str(case['validator_exit'])+'. Case '+case['case']+'.','evidence':[{'path':evidence_path.relative_to(RUN).as_posix(),'sha256':sha(evidence_path.read_bytes())}]})
text(RUN/'integration-checks.jsonl',''.join(json.dumps(row)+'\n' for row in integration))
rows=integration[:]
for member in members.values():
    rows += [json.loads(line) for line in Path(member['checks']['path']).read_text().splitlines()]
counts=ao.reduction(rows)
assessment={'schema_version':'set-assessment-v1','run_id':RUN.name,'input':ref(supp/'selected-pair.json'),'scope':'full_set','omitted_member_ids':[],'omitted_handoff_ids':[],'members':list(members.values()),'integration_checks':ref(RUN/'integration-checks.jsonl'),'outcome':'FAIL','assessment_completed':True,'required_evaluated':counts['required_evaluated'],'required_total':counts['required_total'],'unknown_applicability':counts['unknown_applicability'],'limitations':['Selected diagnostic pair, not a generated product workflow.','Actual prior builder outputs were consumed unchanged for intake, but no completed end-to-end new adaptive authoring/assessment workflow.','Native cold validator noticed role mismatch but timed out before final delivery.','No native implicit discovery or Rust qualification.'],'prior_assessment':None}
write(supp/'set-assessment.json',assessment)

for label in ['validator','builder']:
    receipt=sorted((RUN/'attempts').glob('*-package-'+label+'/receipt.json'))[-1]
    raw=(receipt.parent/'stdout.txt').read_bytes()
    (supp/('raw-package-'+label+'.json')).write_bytes(raw)
    parsed=json.loads(raw)['observations']
    for candidate in parsed['unicode_candidates']:
        candidate.update(disposition='legitimate',reason='Intentional fullwidth command-token negative fixture at tests/test_adaptive.py:102; no source transformation.')
    record={'schema_version':'adaptive-observations-v1','run_id':RUN.name,'target_digest':members[label]['package_digest'],'unicode_candidates':parsed['unicode_candidates'],'resources':parsed['resources'],'edges':parsed['edges'],'context':parsed['context'],'bindings':[],'limitations':['Dynamic Python/script/template use remains unresolved_usage where parser does not establish it.','No observed host token loads or mandatory token budget.','Finalized Unicode/placeholder adjudication is separate from unchanged raw helper stdout.']}
    write(supp/('observations-'+label+'.json'),record)

for label in ['validator','builder']:
    out=ROOT/'docs/plan/skill-validations'/('skill-'+label)/RUN.name
    attempt,receipt=execute('records-'+label,PY+[str(V/'scripts/observe.py'),'records','--run-root',str(out)],'Machine references, shapes and declared reduction agree; exit 0 even for assessment FAIL/INCOMPLETE.')
    assert receipt['exit_code']==0,(attempt/'stdout.txt').read_text()
attempt,receipt=execute('supplemental-records',PY+[str(V/'scripts/adaptive_observe.py'),'records','--run-root',str(supp)],'Closed supplemental observations, selected-pair assessment, exact coverage totals and FAIL reduction accepted; exit 0.')
assert receipt['exit_code']==0,(attempt/'stdout.txt').read_text()

readbacks={}
for label,path in [('validator-loaded',V),('validator-development',ROOT/'src/agents/skills/skill-validator'),('builder-loaded',ROOT/'.agents/skills/skill-builder'),('builder-development',ROOT/'src/agents/skills/skill-builder')]:
    before=json.loads((RUN/'inputs'/(label+'-manifest.json')).read_text())
    after=observe.make_manifest(observe.safe_path(path))
    assert before['files']==after['files'] and before['package_digest']==after['package_digest']
    readbacks[label]=after['package_digest']
for name in ['skill-builder','skill-validator']:
    source=ROOT/'docs/plan'/(name+'-adaptive-enhancement-spec.md')
    assert sha(source.read_bytes())==sha((RUN/'inputs'/source.name).read_bytes())
command_log=['# Actual commands and results\n\nAll attempts are retained. Expected code mismatches are compatibility findings; runner success alone is not PASS.\n']
for path in sorted((RUN/'attempts').glob('*/receipt.json')):
    receipt=json.loads(path.read_text())
    command_log.append('## '+path.parent.name+'\n\n```json\n'+json.dumps(receipt['command'],indent=2)+'\n```\n\nExit '+str(receipt['exit_code'])+'; timed out '+str(receipt['timed_out'])+'. Raw stdout/stderr adjacent.\n')
text(RUN/'command-log.md','\n'.join(command_log))
table='| Case | Expected exit | Builder | Validator | Validator result |\n| --- | --- | --- | --- | --- |\n'+'\n'.join('| '+case['case']+' | '+str(case['expected_exit'])+' | '+str(case.get('builder_exit','not repeated'))+' | '+str(case['validator_exit'])+' | '+('PASS' if case['expected_exit']==case['validator_exit'] else 'FAIL')+' |' for case in cases)
text(RUN/'compatibility-report.md','# Updated validator / builder compatibility\n\n**The updated validator supports basic handoffs, but does not yet fully meet the updated builder contract. Assessment: FAIL.** Five defects are demonstrated by eight differential counterexamples. No package was changed.\n\nValidator digest: `'+readbacks['validator-loaded']+'` (75 files, loaded and development copies identical). Builder development digest: `'+readbacks['builder-development']+'` (43 files, unchanged since the earlier enhancement). The operational builder has the same 43 common files plus 26 legacy evaluation/test files; its distinct digest is `'+readbacks['builder-loaded']+'`. No operational cleanup was attempted.\n\n## Confirmed findings\n\n1. Update review rejects valid changed-input PROPOSED and accepts incorrect NO_CHANGE/nonvariant reviews.\n2. Parent inventory requires references/adaptive-contract.md even for ordinary cores with an explicit complete SKILL.md table.\n3. CRLF fenced parent inventories are rejected.\n4. Delivered descriptor role and parent lineage are not bound to the selected proposal.\n5. A descriptor can name a parent requirement absent from its contract disposition map.\n\nThese are reader implementation gaps: all 14 shared schemas are identical. The default validator test suite passed 229 tests but did not catch these cross-package cases.\n\n## Actual coverage\n\n'+table+'\n\nPositive handoff evidence includes the actual prior cold builder single-skill manual request and the actual per-member-custody partial-set request consumed unchanged by the updated validator. Full-set acceptance is additionally demonstrated with a retained-variant synthetic fixture. Intake is now exercised against the enhanced validator; complete new adaptive authoring-to-assessment and product producer/consumer workflows are still unverified.\n\nThe cold validator task independently detected the role mismatch in a partial message, then timed out at 120 seconds before final delivery. Its first attempt failed parent-sandbox app-server initialization; the approved retry preserved normal child workspace-write controls. Both attempts remain. No completed native or implicit-discovery PASS is claimed.\n\nFinal record checks passed: both schema-1 member runs and the closed supplemental selected-pair report are internally consistent. Overall FAIL takes precedence over retained NOT_RUN coverage. Required evaluated/total: '+str(counts['required_evaluated'])+'/'+str(counts['required_total'])+'; unknown applicability '+str(counts['unknown_applicability'])+'. This is a diagnostic pair, not an installed or generated operational set.\n\n## Evidence and proposed next work\n\n- [Validator report](../../skill-validations/skill-validator/'+RUN.name+'/validation-report.md) and [findings](../../skill-validations/skill-validator/'+RUN.name+'/findings.json).\n- [Proposed complete revision](revision-spec.md): VC-001 through VC-005; no repairs authorized by this report.\n- [Exact commands/results](command-log.md), [differential results](compatibility-results-round2.json), [additional results](additional-results.json), [independent review](independent-review.md), [set assessment](supplemental/set-assessment.json).\n\nInitial differential fixtures used Windows path sort instead of sorted manifest-row paths; that rejected setup is preserved. Corrected fixtures were created under trials-round2, leaving original attempts intact. Source, operational copies, specifications and selected historical inputs were not edited. No installation, hooks, CI, binding setup or Rust qualification. Future revision must use the development validator package and a fresh validation run.\n')
write(RUN/'FINAL-RECEIPT.json',{'schema_version':'1','run_id':RUN.name,'assessment':'FAIL','package_readbacks':readbacks,'source_state':'UNCHANGED','specification_state':'UNCHANGED','finding_count':5,'differential_cases':13,'validator_expected_matches':sum(r['expected_exit']==r['validator_exit'] for r in cases),'regression_tests':229,'regression_result':'PASS','native_result':'TIMEOUT_PARTIAL_OBSERVATION','report':ref(RUN/'compatibility-report.md'),'revision_spec':ref(RUN/'revision-spec.md'),'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print('FAIL; five findings;',counts)
