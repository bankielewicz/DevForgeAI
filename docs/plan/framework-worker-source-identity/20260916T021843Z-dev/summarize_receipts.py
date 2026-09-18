"""Read back retained command streams and exact counts; descriptive evidence only."""
import json
import re
from pathlib import Path
import record

root = Path(__file__).resolve().parent
rows = []
errors = []
for path in sorted(root.rglob('receipt.json')):
    receipt = json.loads(path.read_text(encoding='utf-8'))
    row = {'receipt': path.relative_to(root).as_posix(),
           'native_exit_code': receipt.get('native_exit_code'),
           'timed_out': receipt.get('timed_out'),
           'duration_monotonic_ns': receipt.get('duration_monotonic_ns')}
    for stream in ('stdout', 'stderr'):
        file = path.parent / (stream + '.bin')
        if not file.is_file() or record.sha256(file) != receipt.get(stream + '_sha256'):
            errors.append(str(file))
    rows.append(row)
counts = []
for label in ('13-full-tests', '16-full-coverage'):
    text = (root/label/'stdout.bin').read_text(encoding='utf-8')
    cases = re.findall(r'^test (\S+) \.\.\. (ok|FAILED|ignored)$', text, re.M)
    results = re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored;', text)
    totals = [sum(int(result[i]) for result in results) for i in range(3)]
    assert totals == [123, 0, 0], (label, totals)
    assert len(cases) == 123 and len({name for name, result in cases}) == 123
    counts.append({'label': label, 'passed': totals[0], 'failed': totals[1],
                   'ignored': totals[2], 'unique_named_cases': len(cases),
                   'unit': 37, 'integration': 86})
installed_equal = ((root/'06-installed-baseline/stdout.bin').read_bytes() ==
                   (root/'17-installed-final/stdout.bin').read_bytes())
assert installed_equal
assert not errors, errors
result = {'receipts': rows, 'stream_readback_errors': errors,
          'test_executions': counts, 'installed_observation_bytes_unchanged': installed_equal,
          'note': 'Instrumented executions are not additional unique required cases. Earlier Red/setup/lint failures remain retained.'}
with (root/'receipt-readback.json').open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'receipts': len(rows), 'errors': errors, 'test_executions': counts,
                  'installed_observation_bytes_unchanged': installed_equal}))
