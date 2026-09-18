"""Read-only input identity collection; writes only into this new QA root."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path('C:/Projects/DevForgeAI')
CANDIDATE = REPO / 'devforgeai/experiments/codex-worker-probe-logging'
DEV = REPO / 'docs/plan/framework-worker-logging/20260917T014842Z-dev'
OLD = REPO / 'docs/plan/framework-worker-diagnostics/20260916T181820Z-dev'

def digest(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(path.read_bytes()).hexdigest()

def identity(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)}

def save(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as out:
        json.dump(value, out, indent=2, ensure_ascii=True)
        out.write('\n')

expected = json.loads((DEV / 'candidate-manifest.json').read_text())
actual = [identity(p) for p in sorted(CANDIDATE.rglob('*')) if p.is_file()]
relative = {str(Path(v['path']).relative_to(CANDIDATE)).replace('\\', '/'): v for v in actual}
problems = []
for item in expected:
    observed = relative.get(item['path'].replace('\\', '/'))
    if observed is None or observed['sha256'] != item['sha256'] or observed['bytes'] != item['bytes']:
        problems.append({'candidate_mismatch': item, 'actual': observed})
if set(relative) != {v['path'].replace('\\', '/') for v in expected}:
    problems.append({'candidate_inventory_mismatch': list(relative)})
preserved = []
for base in [REPO / 'devforgeai/experiments/codex-worker-probe', OLD / 'candidate-v2-snapshot']:
    for item in json.loads((OLD / 'candidate-v2-manifest.json').read_text()):
        p = base / item['path']
        observed = identity(p)
        preserved.append(observed)
        if observed['sha256'] != item['sha256']:
            problems.append({'preservation_mismatch': observed})
inputs = []
for item in json.loads((DEV / 'input-bindings.json').read_text()):
    observed = identity(Path(item['path']))
    inputs.append(observed)
    if observed['sha256'] != item['sha256']:
        problems.append({'input_mismatch': item, 'actual': observed})
for name in ['delivery.md','qa-handoff.md','candidate-manifest.json','candidate.patch','traceability.md','test-analysis.json','suite-summary.json','coverage-analysis.json','coverage.json','input-bindings.json']:
    inputs.append(identity(DEV / name))
for name in ['SKILL.md','references/intake-planning.md','references/execution-integrity.md','references/assessment.md','references/reporting-handoff.md','assets/test-plan-template.md','assets/qa-report-template.md','assets/qa-fix-template.md']:
    inputs.append(identity(REPO / '.agents/skills/qa' / name))
for p in sorted((DEV / 'qa-harness').rglob('*')):
    if p.is_file() and 'target' not in p.relative_to(DEV / 'qa-harness').parts:
        inputs.append(identity(p))
save('candidate-manifest.json', actual)
save('preserved-manifest.json', preserved)
save('input-manifest.json', inputs)
save('identity-check.json', {'candidate_files': len(actual), 'preserved_files': len(preserved), 'inputs':len(inputs), 'problems':problems, 'git_present': (REPO / '.git').exists()})
baseline = json.loads((DEV / 'test-analysis.json').read_text())['required_cases']
save('required-cases.json', [{'id':f'PKG-{i+1:03}', 'name':n, 'category':'unit' if '::' in n else 'integration', 'provenance':'developer-authored, independently executed by QA', 'platform':'Windows x64', 'readiness':'READY', 'status':'NOT_RUN'} for i,n in enumerate(baseline)] + [{'id':'SUP-01','name':'real_windows_invalid_utf8_and_unterminated_line_preserve_exact_bytes','category':'integration','provenance':'developer supplemental harness, QA execution','platform':'Windows x64','readiness':'READY','status':'NOT_RUN'}] + [{'id':f'QA-{i:02}', 'category':'acceptance','provenance':'independent QA','platform':'Windows x64','readiness':'READY','status':'NOT_RUN'} for i in range(1,14)])
save('source-denominator.json', [v for v in actual if Path(v['path']).parent == CANDIDATE / 'src' and Path(v['path']).suffix == '.rs'])
print(json.dumps({'candidate_files': len(actual), 'preserved_files':len(preserved), 'required_cases':len(baseline)+14,'required_units':sum('::' in n for n in baseline),'problems':problems}))
if problems:
    raise SystemExit(2)
