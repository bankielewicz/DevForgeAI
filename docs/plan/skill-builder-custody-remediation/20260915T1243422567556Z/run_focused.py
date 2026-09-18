import json
from pathlib import Path
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
attempt = RUN / sys.argv[1]
attempt.mkdir(exist_ok=False)
command = [sys.executable, '-B', '-X', 'utf8', str(RUN / 'test_stage_integrity.py')]
start = time.monotonic()
result = subprocess.run(command, cwd=Path.cwd(), capture_output=True, timeout=120)
(attempt / 'stdout.txt').write_bytes(result.stdout)
(attempt / 'stderr.txt').write_bytes(result.stderr)
(attempt / 'receipt.json').write_text(json.dumps({'argv': command, 'cwd': str(Path.cwd()),
    'exit_code': result.returncode, 'seconds': time.monotonic() - start}, indent=2))
print(result.stderr.decode('utf-8')[-7000:])
sys.exit(result.returncode)
