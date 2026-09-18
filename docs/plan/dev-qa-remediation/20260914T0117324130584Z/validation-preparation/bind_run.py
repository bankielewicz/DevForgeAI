"""Create a fresh exact-byte validator run after an explicit authoring packet."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

PREP = Path(__file__).resolve().parent
PROJECT = PREP.parents[4]
VALIDATOR = PROJECT / '.agents/skills/skill-validator'
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe
import qa_harness as h


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', required=True)
    p.add_argument('--packet', required=True)
    p.add_argument('--sha256', required=True)
    args = p.parse_args()
    run = observe.safe_path(args.run, must_exist=False)
    packet = observe.safe_path(args.packet)
    if run.exists() or not run.is_relative_to(PROJECT / 'docs/plan/skill-validations/dev'):
        raise ValueError('fresh selected dev run required')
    raw = observe.read_stable(packet)
    if observe.sha256(raw) != args.sha256:
        raise ValueError('selected request digest mismatch')
    request = observe.strict_json(raw)
    target = observe.safe_path(request['target_root'])
    result, code = observe.snapshot(argparse.Namespace(source=str(target), output=str(run)))
    save(run / 'snapshot-observation.json', result)
    if code:
        raise ValueError('incomplete snapshot')
    h.RUN = run
    h.execute('intake', [sys.executable, '-B', '-X', 'utf8', str(VALIDATOR / 'scripts/authoring_intake.py'),
                        '--request', str(packet), '--request-sha256', args.sha256], cwd=PROJECT)
    intake = observe.strict_json((run / 'commands/intake/stdout.txt').read_bytes())
    if intake.get('status') != 'BOUND':
        raise ValueError('mandatory intake rejected; retain run and stop dependent assessment')
    save(run / 'authorization.json', {'source': 'User: Implement the plan; selected root task separately assigned validator assessment after new packet.',
                                     'scope': 'Fresh dev assessment, disposable native fixtures, existing authenticated model connection.',
                                     'restrictions': ['No target repair', 'No installation', 'No operational edits', 'No product network/credential/external writes'],
                                     'timeout_seconds': 360, 'maximum_concurrent_native_sessions': 2, 'automatic_retries': False})
    captured = []
    originals = [packet, Path(request['authoring_record']['path']), Path(request['target_manifest']['path']),
                 *[Path(x['path']) for x in request['specification_refs']], PROJECT / 'docs/specs/dev-skill-spec.md',
                 PROJECT / 'docs/plan/skill-validations/dev/20260913T2310456388212Z/revision-spec.md',
                 PROJECT / 'AGENTS.md', PROJECT / 'docs/plan/dev-qa-remediation-plan.md',
                 VALIDATOR / 'SKILL.md', VALIDATOR / 'references/adaptive-validation.md',
                 VALIDATOR / 'references/rules.md', VALIDATOR / 'assets/rules-snapshot.json']
    record = observe.strict_json(observe.read_stable(Path(request['authoring_record']['path'])))
    originals.append(Path(record['contract']['path']))
    seen = set()
    for original in originals:
        original = observe.safe_path(original)
        if str(original) in seen:
            continue
        seen.add(str(original))
        dest = run / 'inputs' / (f'{len(captured):02d}-' + original.name)
        data = observe.read_stable(original)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(data)
        captured.append({'original_path': str(original), 'snapshot': {'path': dest.relative_to(run).as_posix(), 'sha256': observe.sha256(data)}})
    save(run / 'inputs/input-index.json', captured)
    save(run / 'inputs/evaluator-manifest.json', h.inventory(VALIDATOR / 'scripts', run / 'inputs/evaluator'))
    for name in ['qa_harness.py', 'native_campaign.py', 'bound_runner.py']:
        shutil.copyfile(PREP / name, run / ('runner.py' if name == 'bound_runner.py' else name))
    bundle = run / 'bundle'
    bundle.mkdir()
    shutil.copytree(PREP / 'legacy-bundle/fixtures', bundle / 'fixtures')
    for path in (PREP / 'revision-fixtures').iterdir():
        shutil.copytree(path, bundle / 'fixtures' / path.name)
    shutil.copyfile(PREP / 'legacy-bundle/graders.py', bundle / 'graders.py')
    shutil.copyfile(PREP / 'legacy-bundle/evidence.schema.json', bundle / 'evidence.schema.json')
    shutil.copyfile(PREP / 'bound_runner.py', bundle / 'runner.py')
    scenarios = [observe.strict_json(line) for line in (PREP / 'legacy-bundle/scenarios.jsonl').read_bytes().splitlines()]
    revision = observe.strict_json((PREP / 'revision-case-plan.json').read_bytes())
    scenarios.extend(revision['cases'])
    for case in scenarios:
        cid = case['case_id']
        case['fixture_refs'] = [{'path': p.relative_to(bundle).as_posix(), 'sha256': observe.sha256(p.read_bytes())}
                                for p in sorted((bundle / 'fixtures' / cid).rglob('*')) if p.is_file()]
        case['timeout_seconds'] = 360
        case['permitted_write_root'] = str(run / 'trials' / cid)
        case['budget'] = 'One initial attempt; no automatic retry.'
    save(bundle / 'scenarios.jsonl', ''.join(json.dumps(case, ensure_ascii=False) + '\n' for case in scenarios))
    save(bundle / 'expected-results.json', {'case_oracles': {s['case_id']: s['expected'] for s in scenarios},
                                          'case_count': 23, 'alias': {'RV-01': 'DV-17'},
                                          'grading_policy': 'Independent semantic adjudication plus observed native receipts. No PASS from keyword matches, prior results, or model completion text alone.'})
    save(bundle / 'runtime.json', {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
                                 'dependencies': 'stdlib only for runner/graders; PyYAML for separately executed validator structure; existing Codex CLI for native sessions',
                                 'authority': 'Evaluation evidence only. Framework acceptance NOT_EVALUATED.'})
    # Rules are selected before observations, using exact original/revision passages.
    sources = []
    def source(original, ident):
        row = next(c for c in captured if Path(c['original_path']) == original)
        ref = dict(row['snapshot'], source_id=ident)
        sources.append({'source_id': ident, 'original_path': str(original), 'retrieved_at_utc': h.now(),
                        'sha256': ref['sha256'], 'snapshot_path': ref['path'], 'sections': 'complete captured input', 'freshness': 'current_local'})
        return ref
    spec_ref = source(PROJECT / 'docs/specs/dev-skill-spec.md', 'dev-spec')
    rev_ref = source(PROJECT / 'docs/plan/skill-validations/dev/20260913T2310456388212Z/revision-spec.md', 'revision-spec')
    av_ref = source(VALIDATOR / 'references/adaptive-validation.md', 'av-catalog')
    rules_ref = source(VALIDATOR / 'assets/rules-snapshot.json', 'dated-rules')
    rules = []
    for ref, prefix in [(spec_ref, 'DEV'), (rev_ref, 'REV')]:
        text = (run / ref['path']).read_text(encoding='utf-8')
        matches = list(re.finditer(r'\*\*(' + prefix + r'-\d{3})\s+[—–-]\s+(.+?)\*\*', text))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else text.find('\n## ', match.end())
            passage = text[match.start():end if end >= 0 else len(text)].strip()
            rules.append({'rule_id': match[1], 'revision': '1', 'title': match[2], 'source_refs': [dict(ref, locator=match[1])],
                          'authority_class': 'project_policy', 'applicability': 'applicable', 'method': 'semantic',
                          'expected_observation': passage, 'required': True, 'limitation': 'Instruction review is separate from native behavior.'})
    text = (run / av_ref['path']).read_text(encoding='utf-8')
    for line in text.splitlines():
        match = re.match(r'\| (AV-[A-Z]\d{2}) \| (.*?) \| (.*?) \|', line)
        if not match:
            continue
        adaptive = match[1].startswith('AV-A')
        rules.append({'rule_id': match[1], 'revision': '2026-09-12', 'title': match[2], 'source_refs': [dict(av_ref, locator=match[1]), dict(rules_ref, locator='rules')],
                      'authority_class': 'project_policy', 'applicability': 'not_applicable' if adaptive else 'applicable',
                      'method': 'semantic', 'expected_observation': match[3], 'required': True,
                      'limitation': 'Ordinary standalone skill has no adaptive or selected-set contract.' if adaptive else 'Deterministic candidates require semantic adjudication.'})
    for case in scenarios:
        rules.append({'rule_id': case['case_id'], 'revision': '1', 'title': case.get('name', case['case_id']),
                      'source_refs': [dict(rev_ref if case['case_id'].startswith('RV') else spec_ref, locator=case['case_id'])],
                      'authority_class': 'project_policy', 'applicability': 'applicable', 'method': 'behavioral',
                      'expected_observation': case['expected'], 'required': True, 'limitation': 'Only observed disposable Windows sessions and declared variants qualify.'})
    save(run / 'sources.json', {'schema_version': '1', 'run_id': run.name, 'target_name': 'dev', 'sources': sources})
    save(run / 'rule-set.json', {'schema_version': '1', 'run_id': run.name, 'target_name': 'dev', 'rules': rules})
    artifacts = [{'path': p.relative_to(bundle).as_posix(), 'sha256': observe.sha256(p.read_bytes())} for p in sorted(bundle.rglob('*')) if p.is_file()]
    save(bundle / 'artifact-manifest.json', {'schema_version': 'dev-evaluation-bundle-v1', 'package_digest': request['package_digest'],
                                          'artifacts': artifacts, 'input_refs': [dict(c['snapshot']) for c in captured] +
                                          [{'path': 'rule-set.json', 'sha256': observe.sha256((run / 'rule-set.json').read_bytes())}]})
    print(json.dumps({'run': str(run), 'package_digest': request['package_digest'], 'case_count': len(scenarios), 'rule_count': len(rules), 'intake': intake['status']}))


if __name__ == '__main__':
    main()
