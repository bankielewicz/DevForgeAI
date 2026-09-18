"""Readback and delivery observations only; no protected acceptance authority."""
import hashlib
import json
import pathlib
import re
import sys
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
PACKAGE = PROJECT / 'devforgeai/experiments/codex-worker-probe'

def identity(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def write(name, value):
    target = ROOT / name
    if target.exists():
        raise RuntimeError(f'Preserve existing audit: {target}')
    target.write_text(json.dumps(value, indent=2), encoding='utf-8')

if sys.argv[1] == 'candidate':
    candidates = [identity(p) for p in sorted(PACKAGE.rglob('*'))
                  if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    write('source-test-manifest.json', candidates)
    original = json.loads((ROOT / 'input-checks.json').read_bytes())
    checks = []
    for entry in original:
        expected = entry.get('expected', entry.get('preserve'))
        path = pathlib.Path(expected['path'])
        if not path.is_absolute():
            path = PROJECT / path
        actual = identity(path)
        checks.append({'expected': expected, 'actual': actual,
                       'matches': all(expected[k] == actual[k] for k in ('bytes', 'sha256'))})
    write('input-final-checks.json', checks)
    print(json.dumps({'manifest': identity(ROOT / 'source-test-manifest.json'),
                      'matched': sum(c['matches'] for c in checks), 'total': len(checks)}))
elif sys.argv[1] == 'tests':
    reports = []
    for attempt in sys.argv[2:]:
        output = (ROOT / attempt / 'stdout.txt').read_text(encoding='utf-8')
        tests = re.findall(r'^test (\S+) \.\.\. (ok|FAILED|ignored)$', output, re.M)
        mandatory = [t for t in tests if re.fullmatch(r'wf_\d\d', t[0])]
        required = [f'wf_{n:02}' for n in range(1, 21)]
        assert sorted(t[0] for t in mandatory) == required
        reports.append({'attempt': attempt, 'receipt': identity(ROOT / attempt / 'receipt.json'),
                        'mandatory': mandatory, 'mandatory_passes': sum(t[1]=='ok' for t in mandatory),
                        'mandatory_total': 20, 'all_tests': tests,
                        'supplemental_total': len(tests)-20,
                        'case_fixture_roots': sorted(p.name for p in (ROOT / attempt / 'runs').iterdir())})
    write('final-test-inventory.json', reports)
    print(json.dumps([{'attempt':r['attempt'], 'mandatory_passes':r['mandatory_passes'],
                       'supplemental_total':r['supplemental_total']} for r in reports]))
elif sys.argv[1] == 'outputs':
    names = ['context.md', 'input-checks.json', 'traceability.md', 'slices.md', 'executions.jsonl',
             'development-notes.md', 'delivery.md', 'independent-qa-handoff.md',
             'source-test-manifest.json', 'input-final-checks.json', 'final-test-inventory.json',
             'binary-manifest.json', 'checkpoint.md', 'final-source-test-manifest.json',
             'coverage-05.json', 'coverage-05.summary.json', 'candidate-readback.json', 'tool-identities.json']
    write('output-readback.json', [{'required': str(ROOT / n), 'actual': identity(ROOT / n)} for n in names])
    print(json.dumps({'bound_root': str(ROOT), 'read_back': len(names),
                      'original_handoff': identity(PROJECT / 'docs/plan/framework-worker-coding-handoff.md')}))
elif sys.argv[1] == 'final':
    selected = ROOT / '063-clippy/candidate.json'
    data = selected.read_bytes()
    target = ROOT / 'final-source-test-manifest.json'
    if target.exists():
        raise RuntimeError('Preserve prior manifest')
    target.write_bytes(data)
    checks = []
    for entry in json.loads(data):
        actual = identity(pathlib.Path(entry['path']))
        checks.append({'expected': entry, 'actual': actual, 'matches': actual == entry})
    assert all(c['matches'] for c in checks)
    write('candidate-readback.json', checks)
    binaries = []
    for sub in ('debug', 'llvm-cov-target/debug'):
        for name in ('devforgeai-codex-worker-probe.exe', 'protocol-peer.exe', 'console-driver.exe', 'crash-driver.exe'):
            original = PACKAGE / 'target' / sub / name
            copy = ROOT / 'binaries' / sub / name
            copy.parent.mkdir(parents=True, exist_ok=True)
            with copy.open('xb') as stream:
                stream.write(original.read_bytes())
            binaries.append({'original': identity(original), 'retained': identity(copy)})
    write('binary-manifest.json', binaries)
    print(json.dumps({'source_manifest': identity(target), 'source_files': len(checks), 'binaries': len(binaries)}))
elif sys.argv[1] == 'tools':
    observations = []
    for argv in [['rustc', '-Vv'], ['cargo', '-Vv'], ['rustfmt', '--version'],
                 ['cargo', 'clippy', '--version'], ['cargo', 'llvm-cov', '--version']]:
        result = subprocess.run(argv, cwd=PACKAGE, capture_output=True, text=True, check=False)
        observations.append({'argv': argv, 'cwd': str(PACKAGE), 'exit_code': result.returncode,
                             'stdout': result.stdout, 'stderr': result.stderr,
                             'launcher': identity(pathlib.Path(shutil.which(argv[0])))})
    for name in ('cargo', 'rustc', 'rustfmt', 'clippy-driver'):
        result = subprocess.run(['rustup', 'which', name], cwd=PACKAGE, capture_output=True, text=True, check=False)
        observations.append({'argv': ['rustup', 'which', name], 'exit_code': result.returncode,
                             'executable': identity(pathlib.Path(result.stdout.strip()))})
    observations.append({'executable': identity(pathlib.Path(shutil.which('cargo-llvm-cov')))})
    write('tool-identities.json', observations)
    print(json.dumps({'observations': len(observations)}))
elif sys.argv[1] == 'fixtures':
    pinned = [e['expected'] for e in json.loads((ROOT / 'input-checks.json').read_bytes()) if 'expected' in e]
    rows = []
    for path in sorted((PACKAGE / 'tests/fixtures').iterdir()):
        actual = identity(path)
        origins = [e for e in pinned if e['sha256'] == actual['sha256'] and e['bytes'] == actual['bytes']]
        origin_kind = 'manifest-pinned'
        if path.name == 'schema-command.json':
            original = identity(PROJECT / 'docs/plan/framework-worker-contract/20260915T151300Z/schema-command.json')
            origins = [original] if all(original[k] == actual[k] for k in ('bytes', 'sha256')) else []
            origin_kind = 'captured receipt exact readback; not an entry in the 335-input manifests'
        assert origins, f'No exact pinned origin: {path}'
        rows.append({'copy': actual, 'origin_kind': origin_kind, 'origins': origins})
    write('fixture-provenance.json', rows)
    print(json.dumps({'exact_fixture_copies': len(rows)}))
elif sys.argv[1] == 'review':
    readback = json.loads((ROOT / 'output-readback.json').read_bytes())
    for entry in readback:
        assert entry['required'] == entry['actual']['path']
        assert identity(pathlib.Path(entry['required'])) == entry['actual']
    links = []
    for path in [ROOT / 'delivery.md', ROOT / 'independent-qa-handoff.md', PACKAGE / 'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            resolved = (path.parent / target.split('#')[0]).resolve()
            assert resolved.is_file(), f'Missing link: {path}: {target}'
            links.append({'source': str(path), 'target': target, 'resolved': str(resolved)})
    source = json.loads((ROOT / 'final-source-test-manifest.json').read_bytes())
    assert all(identity(pathlib.Path(e['path'])) == e for e in source)
    checks = json.loads((ROOT / 'input-final-checks.json').read_bytes())
    assert all(identity(pathlib.Path(e['actual']['path'])) == e['actual'] for e in checks)
    write('final-review.json', {'output_readbacks': len(readback), 'source_files': len(source),
                               'input_and_preservation_entries': len(checks), 'local_links': links,
                               'delivery': identity(ROOT/'delivery.md'),
                               'handoff': identity(ROOT/'independent-qa-handoff.md'),
                               'output_manifest': identity(ROOT/'output-readback.json')})
    print(json.dumps({'output_readbacks': len(readback), 'source_files': len(source),
                      'input_and_preservation_entries': len(checks), 'local_links': len(links)}))
