"""Retained JSONL maintenance evidence; each unittest method counted once."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import unittest

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
TARGET = ROOT / 'src/agents/skills/skill-validator'


def write(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')


class Result(unittest.TextTestResult):
    def startTest(self, test):
        self.tick = time.monotonic(); self.status = 'PASS'; self.details = []
        super().startTest(test)

    def addFailure(self, test, err):
        self.status = 'FAIL'; self.details.append(self._exc_info_to_string(err, test)); super().addFailure(test, err)

    def addError(self, test, err):
        self.status = 'ERROR'; self.details.append(self._exc_info_to_string(err, test)); super().addError(test, err)

    def addSkip(self, test, reason):
        self.status = 'NOT_RUN'; self.details.append(reason); super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err:
            self.status = 'FAIL'; self.details.append(self._exc_info_to_string(err, subtest))
        super().addSubTest(test, subtest, err)

    def stopTest(self, test):
        row = dict(case_id=test.id(), result=self.status, seconds=time.monotonic()-self.tick, details=self.details)
        self.records.append(row)
        self.output.write(json.dumps(row) + '\n'); self.output.flush()
        super().stopTest(test)


parser = argparse.ArgumentParser()
parser.add_argument('attempt'); parser.add_argument('--pattern', default='test_*.py')
args = parser.parse_args()
out = RUN / args.attempt; out.mkdir(exist_ok=False)
temp = out / 'temp'; temp.mkdir()
os.environ['TEMP'] = os.environ['TMP'] = str(temp)
sys.path.insert(0, str(TARGET / 'tests'))
suite = unittest.defaultTestLoader.discover(str(TARGET / 'tests'), pattern=args.pattern)
def inventory(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite): yield from inventory(test)
        else: yield test.id()
write(out / 'expected-results.json', {case:'PASS' for case in inventory(suite)})
write(out / 'runtime.json', dict(python=sys.version, executable=sys.executable, platform=platform.platform(), cwd=str(ROOT), argv=sys.argv,
                               source={str(p.relative_to(TARGET)):hashlib.sha256(p.read_bytes()).hexdigest() for p in TARGET.rglob('*') if p.is_file()}))
Result.records = []
with (out / 'results.jsonl').open('x', encoding='utf-8') as stream:
    Result.output = stream
    result = unittest.TextTestRunner(resultclass=Result, verbosity=2).run(suite)
rows = Result.records
write(out / 'summary.json', dict(required=len(rows), passed=sum(r['result']=='PASS' for r in rows), failures=[r for r in rows if r['result']!='PASS']))
sys.exit(0 if result.wasSuccessful() else 1)
