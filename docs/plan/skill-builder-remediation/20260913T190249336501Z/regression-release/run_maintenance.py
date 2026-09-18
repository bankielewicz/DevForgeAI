"""Fresh maintenance execution; historical independent oracles, not new audit."""
import json
import sys
from pathlib import Path
import test_followup as f
t = f.t
original_run = t.run


def measured(case, argv, **kwargs):
    if len(argv) > 4 and Path(str(argv[4])).is_relative_to(t.BUILDER):
        argv = argv[:4] + ['-m', 'coverage', 'run', '--append', '--branch', '--data-file='+str(t.RUN/'coverage-data'), '--source='+str(t.BUILDER), t.RUN/'coverage_driver.py'] + argv[4:]
    return original_run(case, argv, **kwargs)


t.run = measured
f.main()
t.SUITE = t.RUN/'fixtures/extra'
t.SUITE.mkdir(parents=True, exist_ok=False)
t.binding_cases()
t.record_cases()
results = list(t.RESULTS)
import test_extended as e
e.OUT.mkdir(parents=True, exist_ok=False)
e.check = lambda case, *args, **kwargs: e.original('ext-'+case, *args, **kwargs)
t.check = e.check
e.linked()
e.legacy()
e.updates()
e.metadata()
results.extend(t.RESULTS)
t.put(t.RUN/'maintenance-results.json', results)
print(json.dumps({'cases':len(results),'failed':[r['case'] for r in results if r['status']!='PASS']}))
sys.exit(1 if any(r['status']!='PASS' for r in results) else 0)
