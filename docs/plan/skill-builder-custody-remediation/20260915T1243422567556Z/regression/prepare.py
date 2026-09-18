"""Retain historical regressions with only explicit location adaptations."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
OLD = ROOT / 'docs/plan/skill-builder-remediation/20260913T190249336501Z'
POST = ROOT / 'docs/plan/skill-builder-postmvp-maintenance/20260914T2108252255451Z'
receipts = []
for source in [*(OLD/n for n in ('evidence.py', 'test_remediation.py', 'test_legacy_maintenance.py', 'test_acceptance_edges.py', 'test_final_contract_edges.py')), *(POST/n for n in ('test_design.py', 'test_builder_adaptive.py')), *(ROOT/'src/agents/skills/skill-validator/tests'/n for n in ('test_authoring.py', 'test_authoring_safeguards.py'))]:
    raw = source.read_bytes()
    text = raw.decode('utf-8').replace('ROOT = RUN.parents[3]', 'ROOT = RUN.parents[4]').replace('PROJECT = RUN.parents[3]', 'PROJECT = RUN.parents[4]')
    if source.name == 'test_authoring.py':
        text = text.replace('PACKAGE = Path(__file__).resolve().parents[1]', "PACKAGE = Path(__file__).resolve().parents[5] / 'src/agents/skills/skill-validator'")
    destination = RUN/source.name
    destination.write_text(text, encoding='utf-8', newline='')
    receipts.append({'source':str(source), 'source_sha256':hashlib.sha256(raw).hexdigest(), 'copy':str(destination), 'copy_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(), 'adaptation':'Only repository ancestry changed for rehosting; test assertions unchanged.'})
(RUN/'retained-test-receipts.json').write_text(json.dumps(receipts, indent=2), encoding='utf-8')
before = ROOT/'docs/plan/skill-builder-custody-remediation/20260915T1243422567556Z'
# The baseline is captured before source repair by the parent; select it later.
print(json.dumps({'retained':len(receipts)}))
