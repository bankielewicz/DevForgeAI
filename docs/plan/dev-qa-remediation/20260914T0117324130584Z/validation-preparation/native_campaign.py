"""Fresh current-byte dev cold trials. No retries or target mutation."""
import concurrent.futures
import json
from pathlib import Path
import shutil
import sys
import qa_harness as h

RUN = Path(__file__).resolve().parent
h.RUN = RUN


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def setup():
    package = json.loads((RUN / 'source-manifest.json').read_bytes())
    intake = json.loads((RUN / 'commands/intake/stdout.txt').read_bytes())
    if intake.get('status') != 'BOUND' or package['package_digest'] != intake['package_digest']:
        raise ValueError('Current exact package requires successful intake before trial setup')
    cases = [json.loads(line) for line in (RUN / 'bundle/scenarios.jsonl').read_bytes().splitlines()]
    plans = []
    for case in cases:
        cid = case['case_id']
        if cid in ('DV-15', 'DV-16'):
            continue
        for variant in (['python', 'javascript'] if cid == 'DV-03' else [None]):
            name = cid + ('-' + variant if variant else '')
            base = RUN / 'trials' / name
            fixture = RUN / 'bundle/fixtures' / cid
            if variant:
                fixture = fixture / variant
            project = base / ('project space Ω $literal' if cid == 'DV-18' else 'project')
            if cid == 'DV-18':
                fixture = fixture / 'project space Ω $literal'
            fixture_manifest = h.inventory(fixture, project)
            h.inventory(RUN / 'source', project / 'trial-skill/dev')
            (project / '.trial-output').mkdir()
            specs = ['spec [input] Ω.md'] if cid == 'DV-18' else ['spec.md']
            if cid == 'DV-02':
                specs.append('consumer.md')
            if cid == 'DV-06':
                specs.append('conflict.md')
            scope = case.get('scope', 'plan only' if cid == 'DV-14' else 'analyze supplied synthetic QA evidence only' if cid == 'DV-11' else 'resume selected checkpoint.json' if cid == 'DV-13' else 'implement through applicable QA')
            if cid == 'RV-04':
                scope = 'resume selected delivery-draft.md and finish selected product through applicable QA'
            evidence = case.get('selected_evidence_value', 'custom receipts/' if cid == 'DV-17' else 'evidence/')
            evidence_prompt = json.dumps(evidence, ensure_ascii=False) if cid == 'RV-02' else evidence
            prompt = (f'Use $dev at {project / "trial-skill/dev/SKILL.md"}. Selected disposable project: {project}. '
                      f'Selected specification documents: {json.dumps(specs, ensure_ascii=False)}. Requested scope: {scope}. '
                      f'Evidence destination: {evidence_prompt}. Read the raw local inputs. '
                      'All product changes must remain in this disposable project. The trial-skill package, specification inputs, unrelated sentinel, '
                      'any prior evidence or supplied checkpoint/draft, and any file blocking a selected directory are read-only. '
                      'No product network, credential inspection, installation, external connectors or external writes. '
                      'Do not use earlier conversation history or memories. Deliver the resulting artifacts or precise remaining gap.')
            plan = dict(case, trial_id=name, permitted_write_root=str(project), task_prompt=prompt,
                        fixture_origin=str(fixture), fixture_manifest=fixture_manifest, selected_specs=specs,
                        selected_evidence_value=evidence, timeout_seconds=360, package_digest=package['package_digest'])
            save(base / 'plan.json', plan)
            save(base / 'prompt.txt', prompt)
            plans.append({'trial_id': name, 'case_id': cid, 'project': str(project), 'plan': str(base / 'plan.json'), 'prompt_sha256': h.sha(prompt.encode('utf-8'))})
    save(RUN / 'native-plan.json', {'trials': plans, 'unique_required_cases': 23, 'native_session_count': len(plans),
                                  'alias': {'RV-01': 'DV-17'}, 'maximum_concurrent': 2, 'timeout_seconds': 360,
                                  'retry_policy': 'One fresh attempt per session; no automatic retries.',
                                  'isolation_limit': 'Separate process and disposable assigned root; shared inherited config. Scope is not independently proven OS isolation.'})


def trial(name):
    base = RUN / 'trials' / name
    plan = json.loads((base / 'plan.json').read_bytes())
    project = Path(plan['permitted_write_root'])
    attempt = base / 'attempt-001'
    attempt.mkdir(exist_ok=False)
    before = h.inventory(project)
    save(attempt / 'before.json', before)
    cmd = [shutil.which('codex'), 'exec', '--cd', str(project), '--sandbox', 'workspace-write', '--skip-git-repo-check',
           '--json', '--output-last-message', str(project / '.trial-output/final-001.txt'), '-']
    result = h.execute(name + '-001', cmd, cwd=project, stdin=plan['task_prompt'], timeout=360)
    after = h.inventory(project)
    save(attempt / 'after.json', after)
    old = {r['path']: r for r in before['files']}
    new = {r['path']: r for r in after['files']}
    changed = [p for p in sorted(old.keys() | new.keys()) if old.get(p) != new.get(p)]
    immutable = ['trial-skill/', 'spec.md', 'consumer.md', 'conflict.md', 'spec [input] Ω.md', 'unrelated.txt',
                 'checkpoint.json', 'delivery-draft.md', 'old-evidence.txt', 'old receipts/', 'evidence/sentinel.txt', 'unavailable receipts']
    save(attempt / 'effects.json', {'changed_paths': changed, 'immutable_changes': [p for p in changed if any(p == x or p.startswith(x) for x in immutable)],
                                   'exclusions': after['exclusions'], 'command_receipt': str(RUN / 'commands' / (name + '-001') / 'command.json')})
    save(attempt / 'result.json', result)
    print('COMPLETED', name, result['termination'], result.get('exit_status'), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'batch':
        names = sys.argv[2:] or [p['trial_id'] for p in json.loads((RUN / 'native-plan.json').read_bytes())['trials']]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = {pool.submit(trial, name): name for name in names}
            for future in concurrent.futures.as_completed(futures):
                future.result()
    else:
        trial(sys.argv[1])
