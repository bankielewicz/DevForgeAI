"""Retain exact command attempts; each label is exclusive."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
run = root / sys.argv[1]
run.mkdir(exist_ok=False)
inputs = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))}
command = [sys.executable, '-B', '-X', 'utf8', *sys.argv[2:]]
(run / 'plan.json').write_text(json.dumps({'command': command, 'cwd': str(root), 'inputs': inputs, 'timeout': 120}, indent=2))
for p in root.glob('*.py'):
    (run / p.name).write_bytes(p.read_bytes())
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
cp = subprocess.run(command, cwd=root, capture_output=True, timeout=120)
(run / 'stdout.txt').write_bytes(cp.stdout)
(run / 'stderr.txt').write_bytes(cp.stderr)
(run / 'receipt.json').write_text(json.dumps({'command': command, 'start': start, 'end': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'exit_code': cp.returncode}, indent=2))
print(cp.stdout.decode(errors='replace'))
print(cp.stderr.decode(errors='replace'))
print('Exit code:', cp.returncode)
