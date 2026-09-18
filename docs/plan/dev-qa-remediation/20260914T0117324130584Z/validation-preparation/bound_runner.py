"""Verify exact external bundle and independently adjudicated real trial evidence.

Writes a fresh JSONL results directory. Never imports target code or creates a
behavioral verdict from instruction keywords. Stdlib only; evidence, not authority.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import graders


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--observations', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    bundle = Path(__file__).resolve().parent
    run = bundle.parent
    output = Path(args.output).absolute()
    if output.exists() or not output.is_relative_to(run / 'trials'):
        raise ValueError('Output must be a fresh run-local trials directory')
    manifest = graders.load((bundle / 'artifact-manifest.json').read_bytes())
    graders.verify_refs(bundle, manifest['artifacts'])
    graders.verify_refs(run, manifest['input_refs'])
    package = graders.load((run / 'source-manifest.json').read_bytes())
    if graders.verify_package(run / 'source', package) != manifest['package_digest']:
        raise ValueError('package binding mismatch')
    scenarios = [graders.load(line) for line in (bundle / 'scenarios.jsonl').read_bytes().splitlines()]
    ids = [f'DV-{i:02d}' for i in range(1, 19)] + [f'RV-{i:02d}' for i in range(2, 7)]
    if [s['case_id'] for s in scenarios] != ids:
        raise ValueError('Unique case accounting mismatch')
    observations = graders.load(Path(args.observations).read_bytes())
    if observations['package_digest'] != package['package_digest']:
        raise ValueError('semantic observations package mismatch')
    by_id = {c['case_id']: c for c in observations['cases']}
    if len(by_id) != len(observations['cases']) or set(by_id) != set(ids):
        raise ValueError('Missing/duplicate/unselected case observation')
    results = []
    for case in scenarios:
        cid = case['case_id']
        observed = by_id[cid]
        graders.verify_refs(bundle, case['fixture_refs'])
        graders.verify_refs(run, observed['evidence'])
        if observed['result'] == 'PASS' and not observed['evidence']:
            raise ValueError('PASS without observed evidence')
        for trial in observed.get('native_trials', []):
            command = graders.load((run / 'commands' / (trial + '-001') / 'command.json').read_bytes())
            effects = graders.load((run / 'trials' / trial / 'attempt-001/effects.json').read_bytes())
            if observed['result'] == 'PASS' and (command['termination'] != 'exited' or command['exit_status'] != 0 or effects['immutable_changes']):
                raise ValueError('PASS conflicts with native termination or immutable effects: ' + trial)
        if cid == 'DV-15' and observed['result'] == 'PASS' and graders.portable_scan(run / 'source', package):
            raise ValueError('Portability PASS conflicts with deterministic forbidden-path matches')
        if cid == 'DV-16' and observed['result'] == 'PASS':
            intake = graders.load((run / 'commands/intake/stdout.txt').read_bytes())
            if intake.get('status') != 'BOUND' or intake['package_digest'] != package['package_digest']:
                raise ValueError('DV16 requires current accepted intake')
        # Exact existence supplements, never replaces, semantic placement review.
        if observed['result'] == 'PASS' and cid in ('DV-17', 'RV-02', 'RV-03', 'RV-06'):
            trial = observed['native_trials'][0]
            plan = graders.load((run / 'trials' / trial / 'plan.json').read_bytes())
            project = Path(plan['permitted_write_root'])
            expected = project / plan['selected_evidence_value']
            if not expected.is_dir() or not any(p.is_file() for p in expected.rglob('*')):
                raise ValueError('PASS without exact selected evidence root: ' + cid)
        results.append({'schema_version': 'dev-evaluation-v1', 'case_id': cid, 'required': True,
                        'result': observed['result'], 'reason': observed['reason'], 'method': observed['method'],
                        'package_digest': package['package_digest'], 'scenario_sha256': graders.sha(graders.compact(case)),
                        'evidence': observed['evidence'], 'evaluated_at': dt.datetime.now(dt.timezone.utc).isoformat()})
    summary = graders.metrics(results)
    summary.update(bundle_binding='MATCH', package_binding='MATCH', alias={'RV-01': 'DV-17'}, framework_acceptance='NOT_EVALUATED')
    output.mkdir(parents=True)
    with (output / 'results.jsonl').open('x', encoding='utf-8', newline='\n') as stream:
        for row in results:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            print(json.dumps(row, ensure_ascii=False))
    with (output / 'summary.json').open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
    return 1 if summary['counts']['FAIL'] else 2 if summary['passing'] != summary['required'] else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(3)
