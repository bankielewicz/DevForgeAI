"""Verify final custody and summarize evidence without altering old attempts."""
import ast
import hashlib
import json
import platform
from pathlib import Path
import sys

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
RUN = HERE.parent / '20260916-integrity-tests'
EVIDENCE = RUN / 'maintenance'
SOURCE = ROOT / 'src/agents/skills/advisor'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in root.rglob('*') if p.is_file()}


before = json.loads((HERE / 'preservation-before.json').read_text())
current = inventory(SOURCE)
assert inventory(ROOT / '.agents/skills/advisor') == before['operational']
assert digest(ROOT / 'AGENTS.md') == before['policy']['sha256']
assert current == inventory(RUN / 'candidate')
changes = sorted(k for k in current.keys() | before['source'].keys()
                 if current.get(k) != before['source'].get(k))
assert changes == ['artifact-manifest.json', 'evals/coverage-entrypoints.ini',
                   'references/evaluation.md', 'tests/test_integrity.py', 'tests/test_streaming.py']
assert all(current[k] == value for k, value in before['source'].items()
           if k.startswith('scripts/'))
manifest = json.loads((SOURCE / 'artifact-manifest.json').read_text())
assert manifest['files'] == {k: v for k, v in current.items() if k != 'artifact-manifest.json'}
assert not list(SOURCE.rglob('*.pyc'))
for name in ('tests/test_integrity.py', 'tests/test_streaming.py'):
    ast.parse((SOURCE / name).read_text())
unit = json.loads((EVIDENCE / 'unit-summary.json').read_text())
assert unit == {'tests_run': 105, 'failures': 0, 'errors': 0, 'skipped': 0,
                'resource_warnings': [], 'successful': True}
jsonl = json.loads((EVIDENCE / 'jsonl/summary.json').read_text())
assert jsonl['passed'] == jsonl['required'] == 38
mutations = json.loads((EVIDENCE / 'mutations/results.json').read_text())
assert len(mutations) == 5 and all(r['guard_removal_detected'] for r in mutations)
assert (EVIDENCE / 'warning-red-exit.txt').read_text(encoding='utf-8-sig').strip() == '1'
for name in ('warning-green-exit.txt', 'integrity-focused-02-exit.txt',
             'regression-exit.txt', 'jsonl-exit.txt'):
    assert (EVIDENCE / name).read_text(encoding='utf-8-sig').strip() == '0'

coverages = {name: json.loads((EVIDENCE / f'coverage-{name}.json').read_text())
             for name in ('unit-only', 'baseline', 'entrypoints')}
stats = {}
for name, coverage in coverages.items():
    t = coverage['totals']
    stats[name] = {'covered_lines': t['covered_lines'], 'lines': t['num_statements'],
                   'line_percent': 100 * t['covered_lines'] / t['num_statements'],
                   'covered_branches': t['covered_branches'], 'branches': t['num_branches'],
                   'branch_percent': 100 * t['covered_branches'] / t['num_branches']}
assert stats['baseline']['line_percent'] >= 95
assert coverages['baseline']['totals']['excluded_lines'] == 0
delta = {}
for name, data in coverages['baseline']['files'].items():
    previous = coverages['unit-only']['files'][name]
    delta[name] = {
        'added_lines': sorted(set(data['executed_lines']) - set(previous['executed_lines'])),
        'added_branches': sorted(set(map(tuple, data['executed_branches'])) - set(map(tuple, previous['executed_branches'])))}
summary = {'changes': changes, 'source_manifest': current, 'runtime_unchanged': True,
           'operational_files_unchanged': len(before['operational']), 'repository_policy_unchanged': True,
           'unit': unit, 'jsonl_passed': 38, 'jsonl_required': 38,
           'selected_guard_mutations_detected': 5, 'coverage': stats, 'jsonl_execution_delta': delta,
           'independent_skill_validation': 'NOT_PERFORMED', 'native_qualification': 'NOT_RUN',
           'framework_acceptance': 'NOT_EVALUATED'}
(EVIDENCE / 'readback.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
table = []
for name, item in coverages['baseline']['files'].items():
    s = item['summary']
    table.append(f"| `{name.replace(chr(92), '/').split('/')[-1]}` | {s['covered_lines']}/{s['num_statements']} ({100*s['covered_lines']/s['num_statements']:.2f}%) | {s['covered_branches']}/{s['num_branches']} ({100*s['covered_branches']/s['num_branches']:.2f}%) | {', '.join(map(str,item['missing_lines']))} |")
views = '\n'.join(f"| {name} | {s['covered_lines']}/{s['lines']} ({s['line_percent']:.2f}%) | {s['covered_branches']}/{s['branches']} ({s['branch_percent']:.2f}%) |" for name, s in stats.items())
report = f'''# Evidence-integrity and resource-ownership test maintenance

Implemented the five listed rejection tests, repaired the flood-reader fixture's resource ownership, and added an optional entry-point-excluded coverage configuration. Development source only; all {len(before['operational'])} operational files, production scripts and repository policy are unchanged. Source readback matches the authored candidate; all {len(manifest['files'])} artifact-manifest entries match.

## Executed verification

- Five new tests accept a pristine synthetic attempt before tampering. Each makes one semantic change and asserts the exact `ValueError` directly and through the normal follow-up path. Rehashed launch/final-envelope artifacts update only the dependent digest so an unrelated hash failure cannot satisfy the test. Rejection also preserves prior files, leaves no second attempt, and makes no new preflight/reviewer calls.
- Five corresponding isolated guard-removal mutants are all detected by `AssertionError: ValueError not raised`, not by setup errors or another rejection guard. The final-envelope guard was already mutation-detected in the user's report; it is included because all five table entries were explicitly selected. This does not claim mutation coverage for every other integrity check.
- Warning reproduction before repair: original fixture passed but the ResourceWarning probe failed (exit 1) on an unclosed BufferedReader. After repair, the same probe passed (exit 0) with no warnings. The fixture now retains its real child, waits for its deliberately overlong reader, joins both readers and closes both pipes in `finally`. Existing timeout assertions are unchanged; elapsed time is measured before fixture-owned cleanup. No warning suppression was introduced.
- Full regression: **105/105 unit tests**, zero failures/errors/skips; **zero captured ResourceWarnings**, including after explicit garbage collection.
- JSONL regression: **38/38** cases passed. Final declared case rate: **143/143 = 100%**. Focused runs and mutant failures are separate evidence and are not counted again.
- The first integrity-focused run had four fixture setup errors because the production JSON writer intentionally refuses overwrites. The test helper was corrected to rewrite only its temporary fixtures; the original output is retained as `integrity-focused.txt`. Those errors were not product failures or valid red results. The next focused run passed 5/5.
- Python syntax and source/hash checks passed. The only changed paths are {', '.join(changes)}.

## Coverage reconciliation

The evaluator discrepancy is execution scope, not a source or denominator mismatch. The unit-only run measures **70/72 lines (97.22%) and 20/22 branches (90.91%)** in `run_evaluation.py`. Appending the separate JSONL runner invocation additionally executes **line 90** and **branch 89->90**, giving **71/72 (98.61%) and 21/22 (95.45%)**. No other executable file gains coverage from that invocation. Unit-only data is retained as `.coverage-unit-only` and `coverage-unit-only.json` before append, so both views are reproducible.

Required baseline: all first-party executable Python in scripts/ plus evals/, with no excluded first-party lines. Tests and fixtures remain outside the denominator. The >=95% aggregate line requirement is unchanged; branch/per-file figures remain separately reported.

| View | Line coverage | Branch coverage |
| --- | --- | --- |
{views}

`entrypoints` is an optional diagnostic report from the exact same combined data, using `evals/coverage-entrypoints.ini` and `exclude_also`. It excludes only runner lines 426-427 and evaluator lines 89-90. It is not substituted for the required baseline and is not used to rescue a failing threshold.

| Baseline file | Lines | Branches | Uncovered lines |
| --- | --- | --- | --- |
{chr(10).join(table)}

Remaining gaps are recorded without classifying them all as low risk: runner lines 244 and 294-295 still include malformed-receipt shape and unexpected-final-envelope rejection paths beyond the five selected cases. Other runner gaps are unsuccessful terminal-envelope handling and its CLI entry point. Streaming parser/type and queue timing gaps were left unchanged as requested. No full tamper-proof ledger, native confinement, or framework acceptance claim follows from these tests.

## Reproduction and retained artifacts

Host: {platform.platform()}, native PowerShell, Python {platform.python_version()} at `{sys.executable}`, cwd `{ROOT}` on the Windows filesystem. coverage.py 7.9.0. No installation, operational mutation or live Claude invocation.

All final commands exited 0; the warning red probe and all five deliberately broken copies exited 1 as expected. Raw command outputs, mutation receipts and per-case JSONL outputs are retained under this maintenance directory. The test wrapper explicitly fails on ResourceWarnings; it does not suppress them.

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:COVERAGE_FILE = 'C:/Projects/DevForgeAI/docs/plan/skill-authorings/advisor/20260916-integrity-tests/maintenance/.coverage'
python -B -X utf8 -m coverage run --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals docs/plan/skill-authorings/advisor/20260916-integrity-tests-intake/run_tests.py --start src/agents/skills/advisor/tests --summary docs/plan/skill-authorings/advisor/20260916-integrity-tests/maintenance/unit-summary.json
# Preserve unit-only data and coverage JSON here, before append.
python -B -X utf8 -m coverage run --append --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/skill-authorings/advisor/20260916-integrity-tests/maintenance/jsonl
python -B -X utf8 -m coverage json -o docs/plan/skill-authorings/advisor/20260916-integrity-tests/maintenance/coverage-baseline.json
python -B -X utf8 -m coverage report -m
python -B -X utf8 -m coverage json --rcfile=src/agents/skills/advisor/evals/coverage-entrypoints.ini -o docs/plan/skill-authorings/advisor/20260916-integrity-tests/maintenance/coverage-entrypoints.json
python -B -X utf8 -m coverage report --rcfile=src/agents/skills/advisor/evals/coverage-entrypoints.ini -m
```

Use fresh evidence paths on replay. Source authoring: AUTHORED and delivered. Maintenance tests: PASS for the declared Windows Python scope. Independent skill validation: NOT_PERFORMED. Native Claude and PowerShell launcher qualification: NOT_RUN. Installation: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED.

Custody record: `{RUN / 'authoring-record.json'}`. Design capture: `{RUN / 'design-capture.json'}`. Optional manual validation handoff: `{RUN / 'validator-request.md'}`. Authoring-only status fields are not overwritten by this separate executed maintenance evidence.
'''
(EVIDENCE / 'report.md').write_text(report, encoding='utf-8')
print(json.dumps({k: v for k, v in summary.items() if k != 'source_manifest'}, indent=2))
