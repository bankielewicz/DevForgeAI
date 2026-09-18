"""External maintenance JSONL runner. Evidence only, not skill qualification."""
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
sys.path.insert(0, str(RUN))
sys.path.insert(0, str(ROOT / 'src/agents/skills/skill-validator/tests'))
os.environ['AUTHORING_BUILDER_ROOT'] = str(ROOT / 'src/agents/skills/skill-builder')

class JsonResult(unittest.TextTestResult):
    def startTest(self, test):
        self.started = time.monotonic()
        super().startTest(test)

    def emit(self, test, status, detail=''):
        self.stream_file.write(json.dumps({'case': test.id(), 'status': status,
            'seconds': time.monotonic() - self.started, 'detail': detail}, ensure_ascii=False) + '\n')
        self.stream_file.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.emit(test, 'PASS')

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.emit(test, 'FAIL', self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.emit(test, 'ERROR', self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.emit(test, 'SKIP', reason)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.emit(test, 'FAIL', self._exc_info_to_string(err, subtest))

def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item.id()

parser = argparse.ArgumentParser()
parser.add_argument('attempt')
parser.add_argument('--design-only', action='store_true')
args = parser.parse_args()
out = RUN / args.attempt
out.mkdir(exist_ok=False)
os.environ['ADAPTIVE_TEST_ROOT'] = str(out / 'adaptive-fixtures')
modules = ['test_design'] if args.design_only else ['test_design', 'test_authoring', 'test_authoring_safeguards', 'test_builder_adaptive']
suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
inventory = list(cases(suite))
(out / 'expected.json').write_text(json.dumps({name: 'PASS' for name in inventory}, indent=2))
(out / 'runtime.json').write_text(json.dumps({'python': sys.version, 'executable': sys.executable,
    'platform': platform.platform(), 'cwd': str(Path.cwd()), 'argv': sys.argv,
    'source': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (ROOT / 'src/agents/skills/skill-builder').rglob('*') if p.is_file()}}, indent=2))
with (out / 'results.jsonl').open('x', encoding='utf-8') as stream:
    JsonResult.stream_file = stream
    result = unittest.TextTestRunner(resultclass=JsonResult, verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
