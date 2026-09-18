"""Recover a byte-identical read-only assessment snapshot after companion drift."""
import json
from pathlib import Path
import preserve

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
expected = json.loads((RUN / 'companion-before.json').read_text())
operational = ROOT / '.agents/skills/skill-validator'
current = preserve.capture(operational)
if current != expected:
    raise SystemExit('No byte-identical baseline available; do not infer compatibility.')
copied = preserve.capture(operational, RUN / 'assessment-owner/skill-validator')
assert copied == expected
preserve.save(RUN / 'assessment-owner/source-receipt.json', {'method': 'Read-only operational bytes independently equal the initial inspected development package.', 'initial_development_manifest': str(RUN / 'companion-before.json'), 'snapshot_manifest': copied, 'no_source_restoration': True})
print(copied['package_digest'])
