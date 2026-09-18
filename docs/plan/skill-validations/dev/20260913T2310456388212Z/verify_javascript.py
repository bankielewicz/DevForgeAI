"""Separate validator observation of the already inspected disposable Node test suite."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs'))
import qa_harness as h
h.RUN = ROOT / 'verification'
project = ROOT / 'trials/DV-03-javascript/project'
attempt = sys.argv[1]
before = h.inventory(project)
h.save(h.RUN / ('node-' + attempt + '-before.json'), before)
record = h.execute('node-' + attempt, [shutil.which('node'), '--test'], cwd=project, timeout=120)
after = h.inventory(project)
h.save(h.RUN / ('node-' + attempt + '-after.json'), after)
assert before['files'] == after['files'], 'Product fixture changed during verification'
raise SystemExit(record['exit_status'] if record['exit_status'] is not None else 3)
