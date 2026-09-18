"""Retain/rehost inspected prior independent tests as maintenance regressions."""
from pathlib import Path
import sys
from evidence import RUN, ROOT, identity, dump, sha

old = ROOT / 'docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z'
new = RUN / sys.argv[1]
new.mkdir(exist_ok=False)
(new/'run_maintenance.py').write_bytes((RUN/'regression-01/run_maintenance.py').read_bytes())
receipt = []
current = identity()['package_digest']
for name in ('capture.py', 'runner.py', 'test_independent.py', 'test_followup.py', 'test_extended.py', 'coverage_driver.py'):
    raw = (old/name).read_bytes()
    text = raw.decode('utf-8').replace('338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2', current)
    (new/name).write_text(text, encoding='utf-8', newline='')
    receipt.append({'source':str(old/name),'sha256':sha(raw),'copy':str(new/name),'copy_sha256':sha((new/name).read_bytes())})
dump(new/'source-receipts.json', receipt)
