"""Run unittest and fail explicitly on captured ResourceWarnings, including GC."""
import argparse
import gc
import json
from pathlib import Path
import sys
import unittest
import warnings

parser = argparse.ArgumentParser()
parser.add_argument('--start', required=True)
parser.add_argument('--summary', required=True)
args = parser.parse_args()
with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter('always', ResourceWarning)
    suite = unittest.defaultTestLoader.discover(args.start)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    gc.collect()
leaks = [str(item.message) for item in observed if issubclass(item.category, ResourceWarning)]
summary = {'tests_run': result.testsRun, 'failures': len(result.failures),
           'errors': len(result.errors), 'skipped': len(result.skipped),
           'resource_warnings': leaks, 'successful': result.wasSuccessful() and not leaks}
Path(args.summary).write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary))
raise SystemExit(0 if summary['successful'] else 1)
