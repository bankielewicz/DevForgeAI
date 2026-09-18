"""Run predeclared local observations; never fabricate cold-session execution.

Input: bound run-local bundle. Output: fresh output directory, JSONL results and
append-only receipts. No network, subprocess, target import or production write.
Exit 0: all required cases passed; 1: FAIL; 2: incomplete; 3: binding/error.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import platform
import sys
import graders

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    bundle=Path(__file__).resolve().parent
    run=bundle.parent
    output=Path(args.output).absolute()
    if output.exists() or not output.is_relative_to(run/'trials'):
        print('Output must be fresh under this run/trials',file=sys.stderr); return 3
    started=dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        manifest=graders.load((bundle/'artifact-manifest.json').read_bytes())
        graders.verify_refs(bundle,manifest['artifacts'])
        package=graders.load((run/'source-manifest.json').read_bytes())
        if graders.verify_package(run/'source',package)!=manifest['package_digest']: raise ValueError('package binding mismatch')
        graders.verify_refs(run,manifest['input_refs'])
        scenarios=[graders.load(line) for line in (bundle/'scenarios.jsonl').read_bytes().splitlines()]
        if [s['case_id'] for s in scenarios]!=[f'DV-{i:02d}' for i in range(1,19)]: raise ValueError('case accounting mismatch')
        output.mkdir(parents=True)
        results=[]
        for scenario in scenarios:
            graders.verify_refs(bundle,scenario['fixture_refs'])
            result='NOT_RUN'
            reason='Cold authenticated model execution not authorized by selected packet; no behavioral attempt fabricated.'
            if scenario['case_id']=='DV-15':
                matches=graders.portable_scan(run/'source',package)
                result='FAIL' if matches else 'PASS'
                reason='Bound complete package scan found '+str(len(matches))+' prohibited concrete-path/product/binding patterns. Separate semantic portability review required.'
            elif scenario['case_id']=='DV-16':
                reason='External evaluation artifact bindings verified, but authoring handoff was rejected by mandatory intake; full scenario prerequisite remains unresolved. Product QA behavior is unperformed.'
            row={'schema_version':'dev-evaluation-v1','case_id':scenario['case_id'],'required':True,'result':result,'method':'deterministic' if scenario['case_id']=='DV-15' else 'unperformed','reason':reason,'package_digest':package['package_digest'],'scenario_sha256':graders.sha(graders.compact(scenario)),'started_at':started,'ended_at':dt.datetime.now(dt.timezone.utc).isoformat()}
            results.append(row)
            with (output/'results.jsonl').open('a',encoding='utf-8',newline='\n') as stream: stream.write(json.dumps(row,ensure_ascii=False)+'\n')
            print(json.dumps(row,ensure_ascii=False))
        summary=graders.metrics(results)
        summary.update(bundle_binding='MATCH',package_binding='MATCH',framework_acceptance='NOT_EVALUATED',cold_trials_executed=0,platform=platform.platform(),python=sys.version)
        (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
        return 1 if summary['counts']['FAIL'] else 2 if summary['passing']!=summary['required'] else 0
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(str(error),file=sys.stderr); return 3

if __name__=='__main__': raise SystemExit(main())
