"""Operational-validator-owned retained implementation checks."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parent
STAGE = RUN.parents[3] / 'src/agents/skills' if 'delivered' in sys.argv[2:] else RUN / 'candidate'
SERIES = RUN / sys.argv[1]
SERIES.mkdir()
TEMP = SERIES / 'disposable'
TEMP.mkdir()
tempfile.tempdir = str(TEMP)
os.environ['TMP'] = str(TEMP)
os.environ['TEMP'] = str(TEMP)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['AUTHORING_BUILDER_ROOT'] = str(STAGE / 'skill-builder')
for name in ('skill-builder', 'skill-validator'):
    shutil.copytree(STAGE / name, SERIES / 'input-packages' / name)
shutil.copy2(__file__, SERIES / 'runner-input.py')
(SERIES / 'plan.json').write_text(json.dumps({'executor':'operational skill-validator implementation assessment', 'implementation':str(RUN / 'inputs/operational-validator'), 'cases':'exact input-packages/skill-validator/tests', 'expected':'Regression assertions from preserved legacy cases plus new user-contract custody/handoff cases; no failure expected', 'timeout_seconds':120, 'write_root':str(SERIES)}, indent=2))

class RetainedTemporaryDirectory:
    def __init__(self, suffix=None, prefix=None, dir=None, **kwargs):
        self.name = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir or TEMP)
    def cleanup(self):
        pass
    def __enter__(self):
        return self.name
    def __exit__(self, *args):
        pass
tempfile.TemporaryDirectory = RetainedTemporaryDirectory
real_run = subprocess.run
counter = 0
def retained_run(command, *args, **kwargs):
    global counter
    counter += 1
    evidence = SERIES / 'commands' / ('%04d' % counter)
    evidence.mkdir(parents=True)
    command = [str(x) for x in command]
    inputs = {}
    flags = {'--package-root','--candidate-root','--cases','--snapshot-root','--source','--manifest','--run-root','--file','--spec','--contract'}
    for i, token in enumerate(command[:-1]):
        if token in flags:
            source = Path(command[i+1])
            if source.exists():
                dest = evidence / ('input-' + str(i))
                if source.is_dir():
                    shutil.copytree(source, dest)
                    inputs[token] = {'path': str(source), 'snapshot': str(dest)}
                else:
                    shutil.copy2(source, dest)
                    inputs[token] = {'path': str(source), 'snapshot':str(dest), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    (evidence / 'plan.json').write_text(json.dumps({'command':command,'cwd':str(Path.cwd()),'inputs':inputs,'start':start,'timeout_seconds':kwargs.get('timeout',120)}, indent=2))
    kwargs.setdefault('timeout', 120)
    result = real_run(command, *args, **kwargs)
    for name in ('stdout','stderr'):
        value = getattr(result,name)
        if value is not None:
            (evidence / (name + '.txt')).write_bytes(value.encode('utf-8') if isinstance(value,str) else value)
    (evidence / 'result.json').write_text(json.dumps({'exit_code':result.returncode,'end':dt.datetime.now(dt.timezone.utc).isoformat()}, indent=2))
    return result
subprocess.run = retained_run
suite = unittest.defaultTestLoader.discover(str(STAGE / 'skill-validator/tests'))
with (SERIES / 'unittest-output.txt').open('w', encoding='utf-8') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
value = {'tests':result.testsRun, 'failures':len(result.failures), 'errors':len(result.errors), 'skipped':len(result.skipped), 'successful':result.wasSuccessful(), 'subprocess_attempts':counter}
(SERIES / 'result.json').write_text(json.dumps(value, indent=2))
print(json.dumps(value))
for _, reason in result.failures + result.errors:
    print(reason)
sys.exit(not result.wasSuccessful())
