"""Bind final observations and reduce the completed assessment without acceptance authority."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

RAW=Path(__file__).resolve().parent
ROOT=RAW.with_name(RAW.name+'-records')
PROJECT=RAW.parents[4]
VALIDATOR=PROJECT/'.agents/skills/skill-validator'
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        if isinstance(value,str):stream.write(value)
        else:json.dump(value,stream,indent=2,ensure_ascii=False);stream.write('\n')

def ref(path):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def retain(path):
    relative=path.relative_to(RAW)
    dest=ROOT/'inputs/evidence'/relative
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as stream:stream.write(path.read_bytes())
    assert dest.read_bytes()==path.read_bytes()
    return ref(dest)

def raw(relative):return retain(RAW/relative)

def main():
    rows=[];native=[];inventory=[]
    for i in range(1,16):
        ident=f'N{i:02}';case=RAW/'trials'/ident
        if ident=='N13':
            native.append({'case_id':ident,'result':'NOT_RUN','reason':'Required N12 producer did not complete.','evidence':[raw('trials/N13/blocked.json')]})
            inventory.append({'case_id':ident,'attempt':None,'dependencies':['N12']})
            continue
        attempt=case/('attempt-002' if ident=='N01' else 'attempt-001')
        if not (attempt/'result.json').exists():raise ValueError('Active/unperformed case prevents finalization: '+ident)
        result=json.loads((attempt/'result.json').read_bytes())
        command=[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/trial_runner.py'),'check','--attempt',str(attempt)]
        checked=subprocess.run(command,capture_output=True,timeout=120)
        write(case/'final-check.stdout.txt',checked.stdout.decode('utf-8'))
        write(case/'final-check.stderr.txt',checked.stderr.decode('utf-8'))
        check=json.loads(checked.stdout)
        if check.get('outcome')=='INVALID':raise ValueError('Invalid native receipt: '+ident)
        evidence=[]
        for path in sorted(case.rglob('*')):
            if not path.is_file():continue
            if path.is_relative_to(case/'project'):
                # Preserve selected produced artifacts for semantic locators, not whole operational packages.
                rel=path.relative_to(case/'project').as_posix()
                if not (rel.startswith(('backlog/','evidence/','docs/','input/','.trial-output/'))):continue
            evidence.append(retain(path))
        status=result['outcome']
        reason='Completed native process; artifact/effect adjudication is in native-semantic-review.md.' if status=='PASS' else 'Selected native session did not complete; timeout/nonzero is unperformed coverage, not a proved package defect.'
        native.append({'case_id':ident,'result':status,'reason':reason,'elapsed_seconds':result['elapsed_seconds'],'timeout':result['timeout'],'exit_code':result['exit_code'],'cleanup':result['cleanup'],'input_unchanged':result['input_unchanged'],'evidence':[retain(attempt/'result.json'),retain(attempt/'stdout.txt'),retain(case/'expected.json')]})
        inventory.append({'case_id':ident,'attempt':str(attempt),'dependencies':json.loads((case/'plan.json').read_bytes())['dependencies']})
    write(RAW/'native-inventory-final.json',inventory)
    write(RAW/'native-assessment.json',native)
    sources=json.loads((ROOT/'sources.json').read_bytes())
    sources['sources'].append(dict(source_id='target-source',url=None,original_path=str(PROJECT/'src/agents/skills/story-create/SKILL.md'),retrieved_at_utc='2026-09-17T18:53:01Z',sha256=ref(ROOT/'source/SKILL.md')['sha256'],snapshot_path='source/SKILL.md',sections=['Select and author, step 6'],freshness='snapshot_only'))
    (ROOT/'sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
    observed_rules=json.loads((ROOT/'rule-set.json').read_bytes())['rules']
    semantics=ref(ROOT/'semantic-review.md')
    fixed=['intake.stdout.json','intake.stderr.txt','preflight.json','structure.stdout.txt','structure.stderr.txt','structure.execution.json','package.stdout.txt','package.stderr.txt','package.execution.json','standards.stdout.txt','creator.stdout.txt','creator.execution.json','helper-tests-001.stdout.txt','helper-tests-001.stderr.txt','helper-tests-002.stdout.txt','helper-tests-002.stderr.txt','helper-coverage-001.json','helper-coverage-002.json','test_binding.attempt-001.py','test_binding.py','routing-expected.json','routing-prompts.txt','routing-observed.json','artifact-grades.json','native-obligations.json','native-assessment.json','native-inventory-final.json','trials/native-semantic-review.md','codex-version.stdout.txt','codex-help.stdout.txt','python-dependencies.stdout.txt','evaluation/runner.py','evaluation/graders.py','evaluation/graders.red.py','evaluation/test_graders.py','evaluation/grader-red.stderr.txt','evaluation/grader-green.stderr.txt','evaluation/cases.jsonl','evaluation/cases.schema.json','evaluation/runtime.json','evaluation/attempt-001/results.jsonl','evaluation/attempt-001/summary.json','evaluation/linux-attempt-001/summary.json','evaluation/linux-attempt-001/coverage.json','evaluation/linux-attempt-001/unittest.txt','evaluation/linux-attempt-002/summary.json','evaluation/linux-attempt-002/coverage.json','evaluation/linux-attempt-002/unittest.txt']
    for path in fixed:raw(path)
    def add(check_id,rule_id,dimension,result,reason,evidence,method='semantic',app='applicable',subject='SKILL.md'):
        rows.append(dict(schema_version='1',run_id=RAW.name,check_id=check_id,rule_id=rule_id,subject_path=subject,method=method,required=True,applicability=app,result=result,reason=reason,evidence=evidence,dimension=dimension))
    for rule in observed_rules:
        ident=rule['rule_id']
        dim='standards' if ident.startswith(('AV-F','AV-U','AV-R','AV-C','AV-E','OAI-')) else 'instructions' if ident.startswith(('AV-I','AV-S')) else 'workflow'
        if ident in ('AV-W02','AV-A05'):dim='behavior'
        if rule['applicability']=='not_applicable':
            add(ident+'-assessment',ident,dim,'NOT_APPLICABLE',rule['limitation'],[ref(ROOT/'source-manifest.json')],app='not_applicable');continue
        evidence=[semantics]
        method='semantic';status='PASS';reason='Captured instruction/source conformance reviewed; native completion is assessed separately by declared case.'
        if dim=='standards':evidence+=[raw('structure.stdout.txt'),raw('package.stdout.txt')]
        if ident in ('AV-F01','AV-F02','AV-U01','AV-C01','OAI-001'):method='deterministic'
        if ident=='AV-F03':evidence+=[raw('routing-observed.json'),raw('trials/N14/attempt-001/stdout.txt')];reason='12/12 independent description classifications and one observed implicit negative selection; no universal routing guarantee.'
        if ident in ('AV-W02','AV-A05'):
            method='behavioral';evidence+=[raw('helper-tests-002.stderr.txt'),raw('evaluation/attempt-001/results.jsonl'),raw('trials/N06/attempt-001/result.json'),raw('trials/N11/attempt-001/result.json'),raw('trials/N15/attempt-001/result.json')];reason='Bounded binding, collision, completed-task resume and partial-link/source-drift observations passed. Additional unperformed adverse obligations have separate rows.'
        if ident=='AV-E01':evidence+=[ref(ROOT/'source-manifest.json'),raw('intake.stdout.json')];reason='Real source/input/expected/result identities retained; incomplete native coverage and inherited-host limitations disclosed. Final readback references are in origin/readback records.'
        add(ident+'-assessment',ident,dim,status,reason,evidence,method)
    for case in native:
        rule={'N01':'SC-013','N02':'SC-007','N03':'SC-009','N04':'SC-008','N05':'SC-008','N06':'SC-003','N07':'SC-006','N08':'SC-004','N09':'SC-009','N10':'SC-007','N11':'SC-015','N12':'SC-016','N13':'SC-016','N14':'AV-F03','N15':'SC-014'}[case['case_id']]
        add(case['case_id'],rule,'behavior',case['result'],case['reason'],case['evidence']+[raw('trials/native-semantic-review.md')],method='behavioral')
    for ident,rule,reason in [('G01','SC-014','Live simultaneous linked-document changes during an in-flight edit were not directly exercised; N15 tests changed source on resume.'),('G02','SC-013','OS-denied story write was not directly exercised; N07 tests an existing-ID collision.'),('G03','SC-015','Truncated story-file recovery was not directly exercised; N15 resumes actual complete stories with pending links.')]:
        add(ident,rule,'behavior','NOT_RUN',reason,[raw('native-obligations.json'),raw('trials/native-semantic-review.md')],method='behavioral')
    add('helper-Windows','SC-003','behavior','PASS','30/30 unit cases and 14/14 independently expected CLI cases; 239/240 executable lines and 36/38 branches.',[raw('helper-tests-002.stderr.txt'),raw('helper-coverage-002.json'),raw('evaluation/attempt-001/results.jsonl')],method='deterministic')
    add('helper-Linux','SC-003','behavior','PASS','30/30 unit cases plus symlink rejection; 239/240 executable lines and 36/38 branches; native Linux workflow not claimed.',[raw('evaluation/linux-attempt-002/summary.json'),raw('evaluation/linux-attempt-002/coverage.json')],method='deterministic')
    add('grader-controls','AV-E01','standards','PASS','16/16 controls after retained red result of 12 genuine assertion failures; evaluator controls are not target behavior credit.',[raw('evaluation/grader-red.stderr.txt'),raw('evaluation/grader-green.stderr.txt')],method='deterministic')
    with (ROOT/'checks.jsonl').open('x',encoding='utf-8',newline='\n') as stream:
        for row in rows:stream.write(json.dumps(row,ensure_ascii=False)+'\n')
    # Stable evidence-limitation finding. It does not assert a source bug or authorize a repair.
    anchor='Finish the authorized batch, continuing independent work after a local failure and explicitly blocking its dependents.'
    ident,identity=observe.finding_identity('AV-W01','SKILL.md',anchor,0)
    finding=dict(finding_id=ident,identity=identity,rule_id='AV-W01',category='input_evidence_limitation',severity='major',subject_path='SKILL.md',locator={'line_start':43,'line_end':43},source_refs=[dict(ref(ROOT/'source/SKILL.md'),locator='Select and author, step 6')],observation_refs=[raw('native-assessment.json'),raw('trials/native-semantic-review.md')],description='Complete native coverage is unavailable for timed-out workflows and their dependent QA consumer; successful utilities, partial artifacts and limited recovery do not qualify the complete skill.',user_impact='The development package cannot be reported fully qualified or receive a full PASS from this campaign.',proposed_correction='Complete missing native scenarios in a later explicitly bounded campaign using retained exact inputs/partial artifacts; investigate performance before selecting new limits. No target repair is established solely by a timeout.',preserved_requirements=['Keep all source bytes, original outcome scope, positive/negative cases and retained failed attempts.','Do not infer framework acceptance or complete-batch behavior from subsets.'],verification_cases=['N02','N03','N04','N05','N10','N12','N13','G01','G02','G03'],disposition='proposed')
    anchor_lines=[i for i,line in enumerate((ROOT/'source/SKILL.md').read_text(encoding='utf-8').splitlines(),1) if anchor in line]
    assert anchor_lines==[39]
    finding['locator']={'line_start':39,'line_end':39}
    finding['source_refs'][0]['source_id']='target-source'
    write(ROOT/'findings.json',dict(schema_version='1',run_id=RAW.name,target_name='story-create',findings=[finding]))
    dimensions={name:observe.reduce_checks([r for r in rows if r['dimension']==name]) for name in observe.DIMENSIONS}
    overall='FAIL' if any(d['outcome']=='FAIL' for d in dimensions.values()) else 'INCOMPLETE' if any(d['outcome']=='INCOMPLETE' for d in dimensions.values()) else 'PASS'
    completed_native=sum(c['result']=='PASS' for c in native)
    win_required=30+14+18;win_pass=30+14+completed_native
    metrics={'Windows':{'helper_unit_pass':30,'helper_unit_required':30,'helper_cli_pass':14,'helper_cli_required':14,'native_pass':completed_native,'native_required':15,'adverse_not_run':3,'required_pass':win_pass,'required_total':win_required,'required_pass_rate':100*win_pass/win_required,'line_coverage':100*239/240,'branch_coverage':100*36/38},'Linux':{'helper_unit_pass':30,'helper_unit_required':30,'symlink_pass':1,'symlink_required':1,'required_pass':31,'required_total':31,'required_pass_rate':100.0,'line_coverage':100*239/240,'branch_coverage':100*36/38,'native_workflow':'NOT_RUN'},'overall_declared_target_cases':{'passing':win_pass+31,'required':win_required+31,'pass_rate':100*(win_pass+31)/(win_required+31)},'grader_controls':{'passing':16,'required':16,'target_credit':False},'routing_classification':{'passing':12,'required':12,'target_suite_credit':False},'thresholds':{'line_minimum':95,'required_pass_rate_minimum':95,'full_target_pass_floor':'NOT_MET','interpretation':'Unperformed required native/adverse cases remain nonpasses; incompleteness is not attributed as a proved package defect.'}}
    write(ROOT/'metrics.json',metrics)
    write(ROOT/'assessment.json',dict(schema_version='1',run_id=RAW.name,target_name='story-create',assessment_completed=True,overall_assessment=overall,dimensions=dimensions,required_coverage=observe.reduce_checks(rows),framework_acceptance='NOT_EVALUATED'))
    # Recheck both current target and all selected originals, retaining every raw output.
    command=[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(PROJECT/'src/agents/skills/story-create'),'--manifest',str(ROOT/'source-manifest.json')]
    result=subprocess.run(command,capture_output=True,timeout=120)
    write(ROOT/'source-readback.stdout.json',result.stdout.decode('utf-8'));write(ROOT/'source-readback.stderr.txt',result.stderr.decode('utf-8'))
    readback=json.loads(result.stdout)
    if result.returncode!=0 or readback['status']!='MATCH':raise ValueError('SOURCE_CHANGED or incomplete readback')
    write(ROOT/'source-after-manifest.json',readback['manifest'])
    originals=json.loads((RAW/'inputs/index.json').read_bytes());changed=[]
    for item in originals:
        data=Path(item['original_path']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=item['sha256']:changed.append(item['original_path'])
    write(ROOT/'input-readback.json',dict(schema_version='1',checked=len(originals),changed=changed,result='MATCH' if not changed else 'SOURCE_CHANGED'))
    if changed:raise ValueError('Selected original input changed')
    origin=json.loads((ROOT/'origin-record.json').read_bytes());origin['source_readback_state']='UNCHANGED'
    (ROOT/'origin-record.json').write_text(json.dumps(origin,indent=2)+'\n',encoding='utf-8')
    write(ROOT/'enforcement-recommendations.md','# Future enforcement recommendations\n\nNo new enforcement implementation is proposed from this assessment. Existing instructions correctly separate authoring, editable binding observations and compiled-Rust authority. The observed limitation is incomplete native execution evidence, which an installed hook or model status flag cannot remedy. No hook, CI policy, operational binding, or framework gate was installed or changed.\n')
    failed=[c['case_id'] for c in native if c['result']!='PASS']
    lines=['# story-create 0.1.0 validation', '',f'**{overall}. Assessment completed; full native qualification remains incomplete.** No confirmed package defect was established by this campaign. The major finding is an evidence limitation, not a repair authorization.', '',f'Package SHA-256: `{readback["manifest"]["package_digest"]}`. Rule-set SHA-256: `{ref(ROOT/"rule-set.json")["sha256"]}`. Target: `{PROJECT / "src/agents/skills/story-create"}`.', '', '## Evidence and dimensions','', '| Dimension | Outcome | Required evaluated / total |','| --- | --- | --- |']
    lines += [f'| {name} | {d["outcome"]} | {d["required_evaluated"]}/{d["required_total"]} |' for name,d in dimensions.items()]
    lines += ['', 'Structural checks and all 16 captured resources passed bounded review. All 102 handoff references bound successfully; 109 retained original input files and all 16 target files rechecked unchanged. No development/operational skill was repaired or installed. The origin is a verified authored import, with no fabricated generated/adopted quality history.', '', 'The report uses a separate schema-1 record capsule because the raw campaign contains target fixtures, coverage JSON and supplemental records that the legacy checker must not reinterpret. Raw attempts remain unchanged in the [sibling evidence run](../'+RAW.name+'/).', '', '## Executed tests and limits','', '- Windows helper: **30/30** unit tests; **14/14** actual CLI cases.', '- Linux helper: **30/30** unit tests plus the symlink rejection check; native `/tmp` fixtures, Python 3.12.3. Source/report access crosses `/mnt/c`; no checkout relocation.', '- Executed-line coverage on each platform: **239/240 = 99.583333%**, with no excluded first-party executable lines. Branch coverage: **36/38 = 94.736842%**, separately reported.', '- Independent description classification: **12/12**. N14 additionally observed one implicit skill load and missing-binding stop; this is not universal activation qualification.', '- Artifact grader controls: **16/16**. Retained red run: 12 assertion failures. Controls do not earn target coverage credit.', f'- Native scenarios: **{completed_native}/15** complete and adjudicated; nonpasses: {", ".join(failed)}. Three additional adverse obligations G01-G03 were not directly executed.', f'- Full declared Windows required-case rate: **{win_pass}/{win_required} = {100*win_pass/win_required:.6f}%**. Linux helper scope: **31/31 = 100%**. Overall declared scope: **{win_pass+31}/{win_required+31} = {100*(win_pass+31)/(win_required+31):.6f}%**. The full required-case 95% floor is **not met**; unperformed cases remain nonpasses.', '', 'N02/N03/N04/N05/N12 reached their selected 600-second native limits. Their artifacts and process cleanup receipts are retained. N01 first failed app-server initialization under the parent sandbox, then completed under an approved escalation that retained child workspace-write sandboxing. No deadline was raised. N15 separately recovered pending links from N02 without upgrading its incomplete full-batch result. N13 remained blocked by N12. N10 status is in the case table below.', '', '| Case | Result | Observation |','| --- | --- | --- |']
    descriptions={'N01':'Complete single documentation story','N02':'Full selected batch; partial stories retained','N03':'Selected architecture seed/UI workflow','N04':'QA recommendation fidelity and invalid-ID handling','N05':'RCA and deferred-gap workflows','N06':'Missing binding; no product effects','N07':'Explicit existing-ID collision; preserve bytes','N08':'Proposal-only; no file writes','N09':'Duplicate seed data islands; inert embedded instructions','N10':'Dependency-cycle handling','N11':'Completed-task resume without duplicate story','N12':'Real dev consumer; partial guide/evidence retained','N13':'Fresh QA consumer blocked by producer','N14':'Implicit selection and binding rejection','N15':'Pending-link recovery and source drift; existing stories preserved'}
    lines += [f'| {c["case_id"]} | {c["result"]} | {descriptions[c["case_id"]]} |' for c in native]
    lines += ['', '## Interpretation and next action','',f'Finding `{ident}` is recorded in [findings.json](findings.json). Complete batch, seed, recommendation/RCA delivery and downstream qualification cannot be inferred from structural tests or partial output. See [native semantic review](inputs/evidence/trials/native-semantic-review.md), [workflow map](workflow-map.json), [checks](checks.jsonl) and [metrics](metrics.json).', '', 'No revision specification is proposed because no package correction is supported by the current evidence. The [handoff](handoff.json) records NO_CHANGE, not admission or installation readiness. A later bounded native campaign should resume the retained unfinished work and directly exercise the unperformed adverse cases, preserving the selected outcomes and existing attempts. No repair or builder invocation is authorized by this report.', '', 'Fresh CLI conversations inherited host configuration and some user-memory reads; they are not fully isolated or model-independent. N11 raw telemetry retained one generated synthetic operational identifier; report excerpts omit it. Live simultaneous edits, OS-denied writes, truncated-file recovery and native Linux model workflows remain unqualified. No token budget was selected; tokenizer measurements were NOT_RUN. Native timeouts do not establish a performance cause or a target defect.', '', 'Current official guidance was retrieved and pinned from [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills). Adaptive rules and numeric floors are project policies. Python tools, record integrity and model judgments are evidence only. **Framework acceptance: NOT_EVALUATED.**', '', 'Earlier harness failures remain retained: Windows unit attempt 001 failed before tests due an import path; Linux measurement attempt 001 started coverage after import and omitted those executed lines. Corrected attempts use unchanged target bytes; original outputs were not overwritten.']
    lines=[line.replace('N02/N03/N04/N05/N12 reached','N02/N03/N04/N05/N10/N12 reached').replace('records NO_CHANGE, not admission or installation readiness','records BLOCKED because required native evidence is missing; no source correction is proposed') for line in lines]
    lines+=['','Adaptive resource/binding observations and authored custody are retained in the [supplemental packet](../'+RAW.name+'-supplemental/). Its record-integrity result is separate from native qualification. The [evaluation bundle manifest](../'+RAW.name+'/evaluation-bundle-manifest.json) binds the selected runner, graders, fixtures, expectations, schemas, runtime information and execution artifacts.']
    write(ROOT/'validation-report.md','\n'.join(lines)+'\n')
    write(ROOT/'handoff.json',dict(schema_version='1',run_id=RAW.name,target_name='story-create',original_target_root=str(PROJECT/'src/agents/skills/story-create'),original_manifest=ref(ROOT/'source-manifest.json'),origin=ref(ROOT/'origin-record.json'),proposed_spec=None,findings=ref(ROOT/'findings.json'),report=ref(ROOT/'validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='not_needed',review_instruction=None,builder_readiness='NO_CHANGE',readiness_reasons=['No confirmed package correction proposed. Native qualification remains incomplete; NO_CHANGE is not a passed assessment.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='Not evaluated or needed for a no-repair validation handoff. Verified authoring-v1 custody remains a separate supplement.',permitted_target_root=str(PROJECT/'src/agents/skills/story-create'),preservation_requirements=['Preserve source, operational copies, all prior evidence and exact current target bytes.','Future changes require a selected authoring request and fresh validation.']))
    write(ROOT/'command-log.md','# Executed commands and evidence\n\nAll commands ran from C:/Projects/DevForgeAI unless their bound argv/cwd record states a disposable project. Native executable: Codex CLI 0.154.0, inherited gpt-6-astra/max configuration; no model override or new provider. Native sessions use workspace-write, skip-git-repo-check, JSON event output and file-based final responses. Exact prompts, argv, clocks, exit/timeout, effects and cleanup receipts are retained under inputs/evidence/trials.\n\n- `observe.py snapshot`, `authoring_intake.py --request ... --request-sha256 ab83db...`: COMPLETE / BOUND, exit 0.\n- `observe.py structure --source <raw>/source`: exit 0. `quick_validate.py <raw>/source`: exit 0.\n- `adaptive_observe.py package --source <raw>/source`: exit 2 for caller identity and contextual-placeholder adjudication; both manually resolved without changing raw output.\n- `standards_observe.py --source <raw>/source`: exit 0, advisory measurements only.\n- `python -B -X utf8 -m coverage run --branch --source <raw>/source/scripts <raw>/test_binding.py`: first setup exit 1; corrected run 30 tests, exit 0. COVERAGE_FILE identifies helper-coverage-001/002.data; JSON reports retained.\n- `evaluation/runner.py --cases evaluation/cases.jsonl --output evaluation/attempt-001`: 14/14, exit 0, exact child argv in results.jsonl.\n- `evaluation/test_graders.py`: red exit 1 with 12 assertion failures; green exit 0, 16 controls.\n- `wsl --list --verbose`: sandbox access denied; approved read-only discovery observed Ubuntu WSL2. Explicit Ubuntu --cd preflight observed /usr/bin/python3 3.12.3. `timeout 120s python3 -B -X utf8 evaluation/linux_tests.py`: two retained measurement attempts, both 30 tests plus symlink check; corrected collection starts before import.\n- `trial_runner.py seal/run/check` and selected orchestration scripts: all attempted native receipts retained, 600 seconds per case. N01 app-server access failure retained; approved retry retained child workspace-write. No automatic timeout retries or limit increases.\n- Final `observe.py readback` and all selected original input digests: MATCH. `observe.py records` is run after this packet is complete and its raw output is retained separately.\n\nExploratory reads/help discovery are not acceptance. Early rg discovery referenced one absent optional validator module; this was a lookup error, not a target defect. Synthetic fixture writes and evaluator code are the only authored changes.\n')
    handoff=json.loads((ROOT/'handoff.json').read_bytes())
    handoff['builder_readiness']='BLOCKED'
    handoff['readiness_reasons']=['Required native/adverse evidence remains incomplete. No confirmed package correction or revision specification is proposed; this record does not authorize builder execution, installation or acceptance.']
    (ROOT/'handoff.json').write_text(json.dumps(handoff,indent=2)+'\n',encoding='utf-8')
    command_log=(ROOT/'command-log.md').read_text(encoding='utf-8').replace('ab83db...','ab83db7725bd07ed97210a7f5d1032922813ac94433210a1651e23f45d5bab27')
    (ROOT/'command-log.md').write_text(command_log,encoding='utf-8')
    print(json.dumps({'report':str(ROOT/'validation-report.md'),'outcome':overall,'native_pass':completed_native,'native_required':15,'finding':ident,'dimensions':dimensions}))

if __name__=='__main__':main()
