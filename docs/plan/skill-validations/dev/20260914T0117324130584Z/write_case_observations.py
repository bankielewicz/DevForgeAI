"""Record manually selected outcomes with exact existing evidence references."""
import json
from pathlib import Path
import hashlib
import sys
RUN = Path(__file__).resolve().parent


def ref(path):
    return {'path': path.relative_to(RUN).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    selected = json.loads((RUN / sys.argv[1]).read_bytes())
    cases = []
    manifest = json.loads((RUN / 'source-manifest.json').read_bytes())
    plans = json.loads((RUN / 'native-plan.json').read_bytes())['trials']
    for cid in [f'DV-{i:02d}' for i in range(1, 19)] + [f'RV-{i:02d}' for i in range(2, 7)]:
        decision = selected.get(cid, {'result': 'NOT_RUN', 'reason': 'Required case is pending completed execution and separate manual adjudication.'})
        evidence = [ref(RUN / 'bundle/expected-results.json')]
        trials = [p['trial_id'] for p in plans if p['case_id'] == cid]
        attempts = {}
        for name in trials:
            base = RUN / 'trials' / name
            evidence.append(ref(base / 'plan.json'))
            completed = sorted(base.glob('attempt-*/result.json'))
            if completed:
                attempt = completed[-1].parent.name.removeprefix('attempt-')
                attempts[name] = attempt
                for file in completed[-1].parent.iterdir():
                    if file.is_file():
                        evidence.append(ref(file))
                command = RUN / 'commands' / (name + '-' + attempt)
                for file in command.iterdir():
                    if file.is_file():
                        evidence.append(ref(file))
                plan = json.loads((base / 'plan.json').read_bytes())
                final = Path(plan['permitted_write_root']) / '.trial-output' / ('final-' + attempt + '.txt')
                if final.exists():
                    evidence.append(ref(final))
        if cid == 'DV-15':
            evidence += [ref(RUN / 'semantic-review-initial.json'), ref(RUN / 'source-manifest.json')]
        if cid == 'DV-16':
            evidence += [ref(RUN / 'commands/intake/stdout.txt'), ref(RUN / 'bundle/artifact-manifest.json'), ref(RUN / 'commands/audit-dv17-rv02/stdout.txt')]
        # Only completed attempts are submitted for deterministic termination checks.
        cases.append({'case_id': cid, 'result': decision['result'], 'reason': decision['reason'],
                      'method': 'deterministic' if cid in ('DV-15', 'DV-16') else 'behavioral',
                      'native_trials': list(attempts), 'native_attempts': attempts, 'evidence': evidence})
    value = {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev', 'package_digest': manifest['package_digest'],
             'adjudication_source': ref(RUN / sys.argv[1]), 'cases': cases}
    with (RUN / sys.argv[2]).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
