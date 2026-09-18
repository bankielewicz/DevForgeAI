"""Assemble evidence-bound observations after native output review."""
import datetime as dt
import json
from pathlib import Path
import shutil
import sys
from bootstrap import RUN,ROOT,VALIDATOR,write,ref
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe

def main():
    case_attempts={'QV-01':'003','dependent-plan':'001','integrity':'001','dynamic-platform':'001','drift':'001','decisions':'001','retest':'001'}
    for case,attempt in case_attempts.items():
        receipt=json.loads((RUN/f'trials/{case}/attempt-{attempt}/receipt.json').read_text())
        if receipt['state']!='EXITED' or receipt['exit_code']!=0:
            raise RuntimeError('Unfinished or failed native task: '+case)
    bindings=json.loads((RUN/'observations/native-readbacks.json').read_text())
    if len(bindings)!=7 or any(x['readback_result']!='PASS' for x in bindings):
        raise RuntimeError('Native readbacks not complete')
    # Capture immutable fixture bytes using the predeclared manifests, not outputs.
    fixture_refs=[]
    for case,attempt in case_attempts.items():
        original=RUN/f'trials/{case}/before-manifest.json'
        manifest=json.loads(original.read_text())
        p=RUN/f'trials/{case}/project'
        for row in manifest['files']:
            data=observe.read_stable(p/row['path'])
            if observe.sha256(data)!=row['sha256']:raise RuntimeError('Input changed: '+case+'/'+row['path'])
            destination=RUN/f'evaluation/fixtures/{case}'/row['path']
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(data)
            fixture_refs.append(ref(str(destination.relative_to(RUN)).replace('\\','/')))
    write('evaluation/fixture-manifest.json',{'package_digest':json.loads((RUN/'source-manifest.json').read_text())['package_digest'],'fixtures':fixture_refs,'case_definitions':[ref(f'trials/{case}/case.json') for case in case_attempts],'expected_results':ref('evaluation/cases.json'),'decision_expected':ref('evaluation/decisions-expected.json')})
    def ev(case):
        a=case_attempts[case]
        refs=[ref(f'trials/{case}/attempt-{a}/receipt.json'),ref(f'trials/{case}/attempt-{a}/stdout.jsonl'),ref(f'trials/{case}/project/.trial-output/final-{a}.txt'),ref('observations/native-readbacks.json')]
        for row in bindings:
            if row['case']==case:
                for name in row['added_files']:
                    if name.endswith(('.md','handoff.txt')) and name.startswith('custom receipts/'):
                        refs.append(ref(f'trials/{case}/project/'+name))
        return refs
    mapping={
      1:('QV-01','Cold planning produced READY with all 14 cases NOT_RUN, no product execution, selected literal outputs and resolved conversation handoff; prior failed/timed-out attempts retained.'),
      2:('dependent-plan','All three selected criteria are mapped with source-qualified duplicate AC-1 identities; protocol dependency migration work explicitly excluded.'),
      3:('dependent-plan','Python and JavaScript fixture pair discovered different layouts/tools and honored full custom receipts/QA résumé roots without leaked product constants; both executed on Windows, not Linux qualification.'),
      4:('dependent-plan','Unspecified fast response obligation retained as exact owner decision for latency threshold/workload/statistic; plan NEEDS_INPUT rather than invented executable oracle.'),
      5:('QV-01','Detected boolean-rejection requirement missing from passing developer assertion; independent negative/boolean oracles planned without copying defective library output.'),
      6:('integrity','Resolved fake and m.patch to unittest.mock.patch; both first-party decorator occurrences cause FAIL. Vendor and documentation examples explicitly excluded.'),
      7:('dynamic-platform','Environment-selected unresolved decorator implementation left integrity incomplete; no clean absence claim, no import of unknown module.'),
      8:('integrity','Vacuous/constant assertions, swallowed failure and fake persistence boundary are source-backed defects; retained actual developer 5/5 pass cannot waive FAIL. Decision trial additionally rejects inflated retry/category accounting.'),
      9:('integrity','Pathlib fixture creation treated as legitimate setup and receives no product acceptance credit; no false gaming finding for setup helper.'),
      10:('decisions','Both 9,499/10,000 boundaries independently yield FAIL; 99% cannot waive AC-7 failure; 95/100 exact floor admitted only with all other obligations stipulated complete. Hypothetical interpretation, not native product measurement.'),
      11:('decisions','Zero denominator remains undefined/INCOMPLETE; required u2 NOT_RUN retained; u1 retry counted once; integration success excluded; exact 1/2=50% failure. Runner negative tests independently reject duplicate/unknown cases and stale evidence.'),
      12:('integrity','Developer suite passes 5/5 while independent actual filesystem test proves persist creates no file, yielding specification-backed FAIL.'),
      13:('dynamic-platform','Native visual evidence unperformed, unknown performance budget/service and dynamic inspection gap explicitly owned; terminal success does not qualify UI. No exhaustive security or performance claim.'),
      14:('drift','Manifest mismatch for library.py detected before planned product command; INCOMPLETE stops affected execution without rebind/repair. Before/after input and historical evidence hashes unchanged.'),
      15:('integrity','Report/fix contain clause/source locators, exact command/fixture evidence, five stable defects, justified corrections and explicit independent retest conditions; artifacts and cross-referenced manifest bytes independently read back.'),
      16:('integrity','FAIL returns dev-owned manual repair prompt with preserved-source/evidence boundaries; no product repair, auto-dev invocation, or automatic QA loop occurred.'),
      17:('integrity','Full spaces/Unicode destination preserved across plan/report/fix and final prompts. Existing referenced files and manifests match; prompts are fenced conversation input with resolved identities, not shell commands.'),
      18:('integrity','Runtime reports dev missing from its available catalog, preserves completed fix packet and marks invocation pending without namespace guessing/install/substitution. Also independently evaluated hypothetical catalog-absence branch; parent did not reconstruct full native catalog.'),
      19:('retest','Corrected candidate independently retested against actual retained predecessor failure; unit/coverage/integrity observations precede VERIFIED_FIXED, original failure remains retained. Development return is an explicitly synthetic fixture, not a live dev integration.'),
      20:('retest','Real planning READY/NEEDS_INPUT never issues product PASS; incomplete cases route to prerequisite owners without invented fixes. Retest PASS goes to defined owner review without framework/release authorization.'),
      21:('QV-01','Bound authoring publication contains manual validator handoff and NOT_PERFORMED testing. Validator-owned external Python runner/graders/cases/expected/schema/runtime/fixture/package manifests are present with executed grader tests. Current runner execution supplies separate actual execution receipt; no builder or authority invocation.')}
    rows=[]
    for num,(case,reason) in mapping.items():
        evidence=ev(case)
        if num==3:evidence+=ev('QV-01')
        if num in (8,10,11,18,20):evidence+=[ref('observations/decision-label-comparison.json'),ref('observations/decision-adjudication.json')]
        if num in (11,21):evidence+=[ref('observations/evaluator-tests.txt'),ref('observations/evaluator-coverage.json')]
        if num==21:evidence+=[ref('observations/intake.stdout'),ref('observations/publication-binding.json'),ref('evaluation/fixture-manifest.json'),ref('evaluation/run_evaluation.py'),ref('evaluation/graders.py'),ref('evaluation/observation.schema.json'),ref('evaluation/runtime.md')]
        rows.append({'case_id':f'QV-{num:02d}','result':'PASS','reason':reason,'method':'behavioral' if num!=21 else 'deterministic','evidence':evidence})
    (RUN/'evaluation/observations.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    # Preserve original routing result separately from expected values.
    # These actual labels were returned by independent qa_routing, whose raw reply
    # is separately captured; agreement is checked against that preserved reply.
    actual=json.loads((RUN/'trials/routing/actual.json').read_text())
    expected=json.loads((RUN/'evaluation/routing-expected.json').read_text())
    write('observations/routing-comparison.json',{'executor':'independent collaboration agent qa_routing; description-only, no expected labels in prompt','matches':sum(row['label']==expected[row['id']] for row in actual['results']),'total':len(expected),'actual':ref('trials/routing/actual.json'),'expected':ref('evaluation/routing-expected.json'),'limitation':'Classification does not prove native implicit activation.'})
    all_files=[p for p in (RUN/'evaluation').rglob('*') if p.is_file() and p.name not in ('bundle-manifest.json',)]
    all_files += [RUN/'inputs'/n for n in ['prepare_trials.py','prepare_campaign.py','prepare_retest.py','native_trial.py','native_batch.py','native-budget-authorization.json']]
    write('evaluation/bundle-manifest.json',{'package_digest':json.loads((RUN/'source-manifest.json').read_text())['package_digest'],'artifacts':[ref(str(p.relative_to(RUN)).replace('\\','/')) for p in sorted(all_files)],'identity':'validator-owned external evaluation bundle, not runtime package or framework authority'})
    print('Prepared',len(rows),'bound scenario observations')

if __name__=='__main__':main()
