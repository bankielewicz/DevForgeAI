"""Small Linux check uses selected /mnt/c source and Linux-native temp fixtures."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = RUN / 'linux-focused-001'
OUT.mkdir(exist_ok=False)
env = os.environ.copy()
env.update(BUILDER_REVIEW_PROJECT=str(ROOT), BUILDER_REVIEW_EVIDENCE=str(OUT),
           PYTHONDONTWRITEBYTECODE='1', COVERAGE_FILE=str(OUT / '.coverage'))
package = ROOT / 'src/agents/skills/skill-builder'
source = [{'path': str(p.relative_to(package)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
          for p in sorted(package.rglob('*')) if p.is_file()]
(OUT / 'source-before.json').write_text(json.dumps(source, indent=2))
command = [sys.executable, '-B', '-X', 'utf8', '-m', 'coverage', 'run', '--branch',
           '--source=' + str(package), str(RUN / 'test_stage_integrity.py')]
start = time.monotonic()
result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=120)
(OUT / 'stdout.txt').write_bytes(result.stdout)
(OUT / 'stderr.txt').write_bytes(result.stderr)
(OUT / 'receipt.json').write_text(json.dumps({'argv': command, 'cwd': str(ROOT),
    'os': platform.platform(), 'python': sys.version, 'executable': sys.executable,
    'fixture_filesystem': '/tmp Linux native', 'source_filesystem': '/mnt/c selected Windows source',
    'exit_code': result.returncode, 'seconds': time.monotonic() - start}, indent=2))
import coverage
cov = coverage.Coverage(data_file=str(OUT / '.coverage'))
cov.load()
rows = []
for p in sorted(package.rglob('*.py')):
    _, statements, excluded, missing, _ = cov.analysis2(str(p))
    rows.append({'path': str(p.relative_to(package)), 'statements': len(statements),
                 'covered': len(statements) - len(missing), 'excluded': excluded})
covered = sum(r['covered'] for r in rows)
total = sum(r['statements'] for r in rows)
(OUT / 'coverage.json').write_text(json.dumps({'files': rows, 'covered': covered,
    'total': total, 'line_percent': 100 * covered / total}, indent=2))
print(result.stderr.decode('utf-8'))
sys.exit(result.returncode)
