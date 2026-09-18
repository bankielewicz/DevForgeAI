"""Fresh source/input readback and origin; no writes to inspected sources."""
import json
import sys
import native_trials as n

ROOT, PROJECT = n.RUN, n.PROJECT
n.h.RUN = ROOT / 'verification'
validator = PROJECT / '.agents/skills/skill-validator'
record = n.h.execute('final-source-readback', [sys.executable, '-B', '-X', 'utf8', str(validator / 'scripts/observe.py'), 'readback', '--source', str(PROJECT / 'src/agents/skills/dev'), '--manifest', str(ROOT / 'source-manifest.json')], cwd=PROJECT)
assert record['exit_status'] == 0
readback = json.loads((ROOT / 'verification/commands/final-source-readback/stdout.txt').read_bytes())
assert readback['status'] == 'MATCH'
n.save(ROOT / 'source-after-manifest.json', readback['manifest'])
def ref(name):
    return {'path': name, 'sha256': n.h.sha((ROOT / name).read_bytes())}
checks = []
for source in json.loads((ROOT / 'sources.json').read_bytes())['sources']:
    if not source.get('original_path'):
        continue
    actual = n.h.sha(n.observe.read_stable(n.observe.safe_path(source['original_path'])))
    checks.append({'source_id': source['source_id'], 'original_path': source['original_path'], 'expected_sha256': source['sha256'], 'actual_sha256': actual, 'result': 'MATCH' if actual == source['sha256'] else 'CHANGED'})
    assert actual == source['sha256'], source['original_path']
for saved in (ROOT / 'inputs/checker-implementation').glob('*.py'):
    if saved.name == 'quick_validate.py':
        original = n.Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    else:
        original = validator / 'scripts' / saved.name
    assert n.h.sha(original.read_bytes()) == n.h.sha(saved.read_bytes()), str(original)
n.save(ROOT / 'input-readback.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'checks': checks, 'checker_sources': 'MATCH', 'rechecked_at': n.h.now()})
n.save(ROOT / 'origin-record.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'original_source_root': str(PROJECT / 'src/agents/skills/dev'), 'manifest': ref('source-manifest.json'), 'specification': ref('inputs/inputs/06-dev-skill-spec.md'), 'origin_kind': 'existing_spec', 'history_kind': 'observed', 'prior_evidence': ref('inputs/static-final-receipt.json'), 'completeness': 'complete', 'uncertainties': ['Selected authoring packet rejected; no generated/adopted baseline inferred', 'Native case DV-17 failed; no passing evaluated-build readiness'], 'source_readback_state': 'UNCHANGED', 'historical_origin': 'unknown'})
# Legacy records recognize source-file inventory rows by manifest filename.
for stage in ('before', 'after'):
    old = ROOT / 'verification' / ('node-001-' + stage + '.json')
    new = ROOT / 'verification' / ('node-001-' + stage + '-manifest.json')
    assert old.is_relative_to(ROOT) and new.is_relative_to(ROOT) and not new.exists()
    digest = n.h.sha(old.read_bytes())
    old.rename(new)
    assert n.h.sha(new.read_bytes()) == digest
print('Source, selected input and checker readback MATCH')
