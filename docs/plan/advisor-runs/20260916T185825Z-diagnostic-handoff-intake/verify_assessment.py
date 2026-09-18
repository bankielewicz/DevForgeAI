import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

repo = Path('C:/Projects/DevForgeAI')
dev = repo / 'docs/plan/framework-worker-diagnostics/20260916T181820Z-dev'
run = repo / 'docs/plan/advisor-runs/20260916T185825Z-diagnostic-handoff'
package = repo / 'devforgeai/experiments/codex-worker-probe'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root, entries):
    failures = []
    for entry in entries:
        path = root / entry['path']
        if not path.is_file() or path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
            failures.append(entry['path'])
    return {'checked': len(entries), 'mismatches': failures}

manifest = dev / 'candidate-v2-manifest.json'
entries = json.loads(manifest.read_text())
index = json.loads((dev / 'artifact-index.json').read_text())['entries']
coverage = json.loads((dev / 'final-coverage-analysis.json').read_text())
raw = json.loads((dev / 'final-coverage.json').read_text())
segments = []
for data in raw['data']:
    for file in data['files']:
        if file['filename'].replace('\\', '/').endswith('/src/protocol.rs'):
            segments.extend(s for s in file['segments'] if 257 <= s[0] <= 259)
tests = re.findall(r'test result: ok\. (\d+) passed; (\d+) failed; (\d+) ignored',
                   (dev / 'attempts/21-final-offline/stdout.txt').read_text())
result = {
    'scope': 'Readback of retained development evidence; no test execution or acceptance',
    'observed_utc': datetime.now(timezone.utc).isoformat(),
    'manifest_sha256': digest(manifest),
    'candidate': verify(package, entries),
    'snapshot': verify(dev / 'candidate-v2-snapshot', entries),
    'historical_artifact_index': verify(dev, index),
    'coverage_files': len(coverage['files']),
    'covered': sum(f['covered'] for f in coverage['files']),
    'count': sum(f['count'] for f in coverage['files']),
    'protocol_segments_lines_257_259': segments,
    'suite_totals': dict(zip(['passed', 'failed', 'ignored'], map(sum, zip(*(map(int, t) for t in tests))))),
    'suite_result_records': len(tests),
    'original_handoff_sha256': digest(dev / 'qa-handoff.md'),
}
assert result['manifest_sha256'] == '419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540'
assert all(not result[key]['mismatches'] for key in ('candidate', 'snapshot', 'historical_artifact_index'))
with (run / 'assessment-evidence.json').open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps(result, indent=2))
