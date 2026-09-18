from record import ROOT, REPO, digest, write
import json

historical = REPO / 'docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity'
paths = [REPO / 'AGENTS.md', REPO / '.agents/skills/dev/SKILL.md',
         *sorted((REPO / 'docs/specs/framework/runtime').glob('codex-worker-*.md')),
         *sorted(p for p in historical.rglob('*') if p.is_file()),
         REPO / 'docs/plan/framework-worker-source-identity/20260916T021843Z-dev/candidate-manifest.json',
         REPO / 'docs/plan/framework-worker-source-identity-qa/20260916T021843Z-retest/qa-report.md']
write(ROOT / 'input-bindings.json', [{'path':str(p), 'bytes':p.stat().st_size,'sha256':digest(p)} for p in paths])
previous = json.loads(paths[-2].read_text())
baseline = json.loads((ROOT / 'baseline-manifest.json').read_text())
assert {e['path']:e['sha256'] for e in previous} == {e['path']:e['sha256'] for e in baseline}
write(ROOT / 'baseline-comparison.json', {'files':len(baseline),'matches_prior_candidate':True,
      'historical_manifest_sha256':digest(paths[-2]),'current_baseline_manifest_sha256':digest(ROOT / 'baseline-manifest.json')})
print('Bound inputs and 91 historical native evidence files; baseline exactly matches historical 56-file candidate.')
