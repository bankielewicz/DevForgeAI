"""Evidence-only suite runner; never a native dispatch authority."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent
TRIAL = ROOT.parents[1] / "framework-worker-trials/20260917T122229Z-logging-diagnostic"
sys.path.insert(0, str(TRIAL))
from supervisor import binding, write_new

output = Path(sys.argv[1])
os.environ["HARNESS_UNDER_TEST"] = str(TRIAL / "operator-harness-001/diagnostic.py")
os.environ["RECORDER_TEST_MODULE"] = str(TRIAL / "operator-harness-001/recorder.py")
files = [ROOT / "tests/test_operator_harness.py", TRIAL / "test_supervisor.py"]
suite = unittest.TestSuite()
for index, path in enumerate(files):
    spec = importlib.util.spec_from_file_location("suite_" + str(index), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))


def cases(group):
    for item in group:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item.id()


identifiers = list(cases(suite))
write_new(output / "suite-definition.json", dict(
    platform=sys.platform, python=sys.version, cwd=str(Path.cwd()), required_cases=identifiers,
    runtime_sources=[binding(TRIAL / "operator-harness-001/diagnostic.py"), binding(TRIAL / "operator-harness-001/recorder.py")],
    tests=[binding(path) for path in files],
    denominator="All executed lines of diagnostic.py and derived recorder.py; no runtime exclusions",
    excluded="Tests, synthetic fixtures, evidence-only runner and preserved historical supervisor; PowerShell measured separately",
    live_integration="Two live preparation cases separately blocked by externally changed config.toml; not credited as passing"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
failed = {test.id().split(" (")[0] for test, _ in result.failures + result.errors}
skipped = {test.id() for test, _ in result.skipped}
passing = [case for case in identifiers if case not in failed | skipped]
write_new(output / "test-results.json", dict(required=len(identifiers), executed=result.testsRun,
    passing=len(passing), pass_rate=100 * len(passing) / len(identifiers),
    failed=sorted(failed), skipped=sorted(skipped), passed=passing,
    successful=result.wasSuccessful(), native_codex="NOT_RUN", framework_acceptance="NOT_EVALUATED"))
raise SystemExit(0 if result.wasSuccessful() else 1)
