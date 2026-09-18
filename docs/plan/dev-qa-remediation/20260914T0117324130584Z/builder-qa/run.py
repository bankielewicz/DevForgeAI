"""Bounded local QA execution; retains each attempt and exact test/source inputs."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
project = root.parents[4]
label = sys.argv[1]
run = root / label
run.mkdir(exist_ok=False)
tests = project / 'src/agents/skills/skill-validator/tests'
source = project / 'src/agents/skills/skill-builder/scripts/authoring.py'
inputs = {}
for p in [source, *sorted(tests.glob('test_authoring*.py'))]:
    b = p.read_bytes()
    (run / p.name).write_bytes(b)
    inputs[str(p)] = hashlib.sha256(b).hexdigest()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
(run / 'tmp').mkdir()
env['TMP'] = env['TEMP'] = str(run / 'tmp')
commands = [
    [sys.executable, '-B', '-X', 'utf8', '-m', 'coverage', 'run', '--branch', '--data-file', str(run / 'coverage.data'), '--include', str(source), '-m', 'unittest', 'discover', '-s', str(tests), '-p', 'test_authoring*.py', '-v'],
    [sys.executable, '-B', '-m', 'coverage', 'json', '--data-file', str(run / 'coverage.data'), '-o', str(run / 'coverage.json')],
]
(run / 'plan.json').write_text(json.dumps({'inputs': inputs, 'commands': commands, 'timeout_seconds': 120, 'cwd': str(project), 'platform': sys.platform, 'python': sys.version, 'source_denominator': str(source), 'exclusions': [], 'expected': 'All declared authoring regression cases pass; >=95% executed-line coverage. No Rust acceptance claim.', 'allowed_writes': [str(run), 'synthetic temporary fixtures only']}, indent=2))
for i, command in enumerate(commands):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    result = subprocess.run(command, cwd=project, env=env, capture_output=True, timeout=120)
    (run / f'{i}-stdout.txt').write_bytes(result.stdout)
    (run / f'{i}-stderr.txt').write_bytes(result.stderr)
    (run / f'{i}-receipt.json').write_text(json.dumps({'command': command, 'start': start, 'end': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': time.monotonic()-tick, 'exit_code': result.returncode}, indent=2))
    print(result.stdout.decode(errors='replace'))
    print(result.stderr.decode(errors='replace'))
