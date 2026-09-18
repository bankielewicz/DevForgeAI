"""Fail when the selected unchanged fixture emits a ResourceWarning."""
import gc
import io
import sys
import unittest
import warnings
from pathlib import Path

package = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(package / 'tests'))
import test_streaming

suite = unittest.TestSuite([test_streaming.StreamProcessTests(
    'test_continuously_filled_queue_still_obeys_cleanup_ceiling')])
with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter('always', ResourceWarning)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    gc.collect()
leaks = [str(item.message) for item in observed if issubclass(item.category, ResourceWarning)]
print('ResourceWarnings:', leaks)
assert result.wasSuccessful(), 'The underlying fixture failed'
assert not leaks, 'The fixture leaked a resource: ' + repr(leaks)
