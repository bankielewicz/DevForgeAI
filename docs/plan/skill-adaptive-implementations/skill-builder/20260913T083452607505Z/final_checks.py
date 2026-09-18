"""Final read-only existing-validator observations with retained command receipts."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
from preserve import capture, save, sha

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
OUT = RUN / 'assessment'
OWNER = RUN / 'assessment-owner/skill-validator'
BUILDER = ROOT / 'src/agents/skills/skill-builder'
commands = {
    'readback': ['readback', '--source', str(BUILDER), '--manifest', str(OUT / 'source-manifest.json')],
    'records': ['records', '--run-root', str(OUT)]}
for name, args in commands.items():
    command = [sys.executable, '-B', '-X', 'utf8', str(OWNER / 'scripts/observe.py')] + args
    result = subprocess.run(command, capture_output=True, cwd=ROOT, timeout=120)
    (RUN / ('final-' + name + '-stdout.json')).write_bytes(result.stdout)
    (RUN / ('final-' + name + '-stderr.txt')).write_bytes(result.stderr)
    save(RUN / ('final-' + name + '-receipt.json'), {'command': command, 'exit_code': result.returncode, 'ended_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')})
    observation = json.loads(result.stdout)
    print(name, result.returncode, observation.get('status'), observation.get('errors', []), observation.get('overall_assessment', ''))
    assert result.returncode == 0
actual = capture(BUILDER)
expected = json.loads((RUN / 'builder-final.json').read_text())
assert actual == expected
inputs = json.loads((RUN / 'input-hashes.json').read_text())
assert {p: sha((ROOT / p).read_bytes()) for p in inputs} == inputs
for name in ['builder', 'validator']:
    actual_operational = capture(ROOT / '.agents/skills' / ('skill-' + name))
    assert actual_operational == json.loads((RUN / ('operational-' + name + '-before.json')).read_text())
save(RUN / 'FINAL-RECEIPT.json', {
    'run_id': RUN.name, 'package_digest': actual['package_digest'], 'file_count': len(actual['files']),
    'source_readback': 'UNCHANGED', 'input_readback': 'UNCHANGED', 'operational_readback': 'UNCHANGED',
    'companion': 'Changed concurrently by another session; no task-owned writes.',
    'implementation': 'DELIVERED', 'verification': 'INCOMPLETE', 'installation': 'NOT_PERFORMED',
    'rust_qualification': 'NOT_PERFORMED', 'enhanced_validator_integration': 'NOT_RUN',
    'assessment_report_sha256': sha((OUT / 'validation-report.md').read_bytes()),
    'rule_set_sha256': sha((OUT / 'rule-set.json').read_bytes()),
    'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')})
print(actual['package_digest'])
