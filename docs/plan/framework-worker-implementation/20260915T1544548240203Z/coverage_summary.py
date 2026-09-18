"""Report the declared src denominator without excluding runtime files."""
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
report = json.loads(path.read_bytes())
files = [f for d in report['data'] for f in d['files'] if '/codex-worker-probe/src/' in f['filename'].replace('\\', '/')]
rows = []
for f in files:
    summary = f['summary']['lines']
    source = pathlib.Path(f['filename'])
    rows.append({'path': str(source), **summary})
    if len(sys.argv) > 2:
        lines = source.read_text(encoding='utf-8').splitlines()
        missing = sorted({s[0] for s in f['segments'] if s[2] == 0 and s[3] and not s[5]})
        print(source.name, [(i, lines[i-1].strip()) for i in missing if i <= len(lines)])
total = sum(r['count'] for r in rows)
covered = sum(r['covered'] for r in rows)
result = {'files': rows, 'covered': covered, 'count': total, 'percent': covered*100/total,
          'branches': 'NOT_RUN - stable collection, unstable branch flag not selected',
          'exclusions': ['tests/support/fixtures', 'generated/vendor/dependency code'], 'runtime_exclusions': []}
path.with_suffix('.summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
