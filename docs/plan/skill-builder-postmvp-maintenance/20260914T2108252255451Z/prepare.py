import hashlib
import json
from pathlib import Path
import shutil
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'

def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

shutil.copytree(PACKAGE, RUN / 'before/skill-builder')
protected = [ROOT / '.agents/skills/skill-builder', ROOT / 'src/agents/skills/skill-validator', ROOT / 'docs/specs']
(RUN / 'preservation-before.json').write_text(json.dumps({str(p): inventory(p) for p in protected}, indent=2))
(RUN / 'before-manifest.json').write_text(json.dumps(inventory(PACKAGE), indent=2))
for name in ('skill-builder-postmvp-spec.md',):
    shutil.copyfile(ROOT / 'docs/specs' / name, RUN / name)
(RUN / 'plan.md').write_text('''# Maintenance scope declared before changes

Implement SBP-001 through SBP-016 in development skill-builder only. No installation,
validator modification, generated-skill campaign, or Rust authority change.

Executable coverage denominator: all executed-line statements in authoring.py and
record_schema.py, the changed custody implementation and its schema dependency;
no excluded lines. Branch coverage reported separately. Other unchanged builder
modules are exercised by applicable retained regression tests but are not claimed
as fully covered by this focused maintenance measurement. Platform: native Windows.
Linux and cold native skill qualification remain separate NOT_RUN obligations.

Required maintenance inventory: every unittest case in test_design.py plus retained
test_authoring.py and test_authoring_safeguards.py; adaptive regression inventory
will be frozen before execution after reviewing current fixture setup. Expected
red failures are retained as TDD evidence; green/QA case counts are separate, and
failed attempts are never deleted or averaged away. 95% line coverage and case pass
rate are independently required for the declared maintenance scope.

Use disposable local fixtures with spaces/Unicode, file-delivery/readback assertions,
invalid input and mutation probes, legacy calls and unchanged validator intake.
Each maintenance command has a 120-second execution ceiling, no product timeout
claim, no automatic retry. No network, native agent invocation, or external effect.
The separate validator task owns SBPV-01 through SBPV-18 behavioral qualification,
including two end-to-end generated skills and independent oracles.
''', encoding='utf-8')
print(RUN)
