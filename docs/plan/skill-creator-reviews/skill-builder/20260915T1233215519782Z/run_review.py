"""Retain bounded command receipts and independently inventory reviewed bytes."""
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

ROOT = Path(r'C:\Projects\DevForgeAI')
RUN = Path(__file__).resolve().parent
PACKAGE = ROOT / 'src/agents/skills/skill-builder'


def save(name, value):
    (RUN / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def inventory(root):
    rows = []
    for p in sorted(root.rglob('*')):
        if p.is_file():
            raw = p.read_bytes()
            rows.append({'path': p.relative_to(root).as_posix(), 'bytes': len(raw),
                         'sha256': hashlib.sha256(raw).hexdigest()})
    rows.sort(key=lambda row: row['path'])
    return {'files': rows, 'package_digest': hashlib.sha256(json.dumps(rows, ensure_ascii=False,
            separators=(',', ':')).encode()).hexdigest()}


before = inventory(PACKAGE)
operational_before = inventory(ROOT / '.agents/skills/skill-builder')
save('source-before.json', before)
save('operational-before.json', operational_before)
save('environment.json', {'os': platform.platform(), 'shell': 'PowerShell',
    'python': sys.version, 'executable': sys.executable, 'cwd': str(ROOT),
    'filesystem': 'Windows C: native filesystem', 'git_present': (ROOT / '.git').exists()})
py_files = sorted(str(p.relative_to(PACKAGE)).replace('\\', '/') for p in PACKAGE.rglob('*.py'))
save('scope.json', {'scope': 'Focused skill-creator review; no repair or full acceptance',
    'required_cases': 8, 'coverage_source': str(PACKAGE), 'coverage_files': py_files,
    'coverage_exclusions': [], 'coverage_note': 'All executable Python including shipped runtime asset; separate from Rust authority.',
    'commands_timeout_seconds': 120, 'retries': 0,
    'not_covered': ['Full legacy/adaptive/import/adoption suite', 'Linux', 'Native implicit discovery',
                    'Generated skill execution', 'Framework acceptance']})
manifest = json.loads((PACKAGE / 'package-manifest.json').read_bytes())['artifacts']
actual = {row['path']: row['sha256'] for row in before['files'] if row['path'] != 'package-manifest.json'}
broken = []
for p in PACKAGE.rglob('*.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):
            local = target.split('#')[0]
            if local and not (p.parent / local).exists():
                broken.append({'source': str(p.relative_to(PACKAGE)), 'target': target})
syntax = []
for name in py_files:
    try:
        ast.parse((PACKAGE / name).read_text(encoding='utf-8'))
    except SyntaxError as exc:
        syntax.append({'file': name, 'error': str(exc)})
save('structural.json', {'manifest_exact': manifest == actual,
    'manifest_missing': sorted(set(manifest) - set(actual)),
    'manifest_extra': sorted(set(actual) - set(manifest)),
    'manifest_mismatched': [p for p in manifest if p in actual and manifest[p] != actual[p]],
    'broken_markdown_links': broken, 'python_syntax_errors': syntax})
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['COVERAGE_FILE'] = str(RUN / '.coverage')
receipts = []


def command(name, args):
    start = time.monotonic()
    try:
        result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, timeout=120)
        code, out, err = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        code, out, err = None, exc.stdout or b'', exc.stderr or b''
    (RUN / (name + '.stdout.txt')).write_bytes(out)
    (RUN / (name + '.stderr.txt')).write_bytes(err)
    receipts.append({'name': name, 'argv': args, 'cwd': str(ROOT), 'exit_code': code,
                     'timeout': code is None, 'seconds': time.monotonic() - start})
    save('command-receipts.json', receipts)
    print(name, code, flush=True)


command('quick-validate', [sys.executable, '-B', '-X', 'utf8',
    r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py', str(PACKAGE)])
command('publication-tests', [sys.executable, '-B', '-X', 'utf8', '-m', 'coverage', 'run',
    '--branch', '--source=' + str(PACKAGE), str(RUN / 'test_publication.py')])
command('coverage-json', [sys.executable, '-B', '-X', 'utf8', '-m', 'coverage', 'json',
    '-o', str(RUN / 'coverage.json')])
command('coverage-text', [sys.executable, '-B', '-X', 'utf8', '-m', 'coverage', 'report', '-m'])
after = inventory(PACKAGE)
save('source-after.json', after)
save('preservation.json', {'source_unchanged': before == after,
    'operational_unchanged': operational_before == inventory(ROOT / '.agents/skills/skill-builder')})
