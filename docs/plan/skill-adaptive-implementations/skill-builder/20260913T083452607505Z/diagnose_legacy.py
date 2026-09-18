"""Read-only companion diagnosis in a fresh disposable copy; retain failures."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

RUN = Path(__file__).resolve().parent
SOURCE = RUN.parents[4] / 'src/agents/skills/skill-validator'
TARGET = RUN / 'legacy-diagnosis/validator'
shutil.copytree(SOURCE, TARGET)
sys.path.insert(0, str(TARGET / 'scripts'))
import run_evaluation
expected = json.loads((TARGET / 'evals/build-manifest.json').read_text())['artifacts']
actual = {p.relative_to(TARGET).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in TARGET.rglob('*') if p.is_file() and p != TARGET / 'evals/build-manifest.json'}
result = {'before_diff': {p: {'expected': expected.get(p), 'actual': actual.get(p)} for p in set(actual) | set(expected) if actual.get(p) != expected.get(p)}}
try:
    result['package_binding'] = str(run_evaluation.package_binding(TARGET)[:2])
except Exception as exc:
    result['error'] = str(exc)
(RUN / 'legacy-diagnosis/observation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
