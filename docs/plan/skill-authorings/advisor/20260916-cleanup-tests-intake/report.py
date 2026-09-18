"""Bind executed maintenance evidence to the delivered bytes and scope."""
import ast
import hashlib
import json
import platform
import re
import sys
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
RUN = HERE.parent / '20260916-cleanup-tests'
EVIDENCE = RUN / 'maintenance'
SOURCE = ROOT / 'src/agents/skills/advisor'
OPERATIONAL = ROOT / '.agents/skills/advisor'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): digest(p)
            for p in sorted(root.rglob('*')) if p.is_file()}


before = json.loads((HERE / 'preservation-before.json').read_text())
current = inventory(SOURCE)
operational = inventory(OPERATIONAL)
assert operational == before['operational'], 'Operational drift'
assert digest(ROOT / 'AGENTS.md') == before['policy']['sha256'], 'Policy drift'
assert current == inventory(RUN / 'candidate'), 'Candidate/delivered mismatch'
changed = sorted(k for k in current.keys() | before['source'].keys()
                 if current.get(k) != before['source'].get(k))
assert changed == ['artifact-manifest.json', 'tests/test_cleanup.py'], changed
manifest = json.loads((SOURCE / 'artifact-manifest.json').read_text())
assert set(manifest['files']) == set(current) - {'artifact-manifest.json'}
assert all(current[k] == value for k, value in manifest['files'].items())
assert not list(SOURCE.rglob('*.pyc'))
ast.parse((SOURCE / 'tests/test_cleanup.py').read_text())

regression = (EVIDENCE / 'regression.txt').read_text(encoding='utf-8-sig')
assert re.search(r'Ran 100 tests in ', regression)
assert re.search(r'\nOK\s*$', regression)
assert '... FAIL' not in regression and '... ERROR' not in regression
assert (EVIDENCE / 'regression-exit.txt').read_text(encoding='utf-8-sig').strip() == '0'
jsonl = json.loads((EVIDENCE / 'jsonl/summary.json').read_text())
assert jsonl['passed'] == jsonl['required'] == 38
assert (EVIDENCE / 'jsonl-exit.txt').read_text(encoding='utf-8-sig').strip() == '0'
mutations = json.loads((EVIDENCE / 'mutations/results.json').read_text())
assert len(mutations) == 4 and all(row['assertion_detected'] for row in mutations)

coverage = json.loads((EVIDENCE / 'coverage.json').read_text())
rows = []
for name, value in coverage['files'].items():
    summary = value['summary']
    rows.append({'file': name.replace('\\', '/'),
                 'covered_lines': summary['covered_lines'], 'lines': summary['num_statements'],
                 'line_percent': 100 * summary['covered_lines'] / summary['num_statements'],
                 'covered_branches': summary['covered_branches'], 'branches': summary['num_branches'],
                 'branch_percent': 100 * summary['covered_branches'] / summary['num_branches'],
                 'missing_lines': value['missing_lines'], 'missing_branches': value['missing_branches']})
total = coverage['totals']
line_percent = 100 * total['covered_lines'] / total['num_statements']
branch_percent = 100 * total['covered_branches'] / total['num_branches']
assert line_percent >= 95
summary = {'scope': 'Windows development advisor Python maintenance', 'changed_paths': changed,
           'source_manifest': current, 'operational_files_unchanged': len(operational),
           'production_and_policy_unchanged': True, 'unit_passed': 100, 'unit_required': 100,
           'jsonl_passed': 38, 'jsonl_required': 38, 'pass_rate': 100,
           'mutation_assertions_detected': 4, 'mutation_cases': 4,
           'line_percent': line_percent, 'branch_percent': branch_percent, 'per_file': rows,
           'independent_skill_validation': 'NOT_PERFORMED', 'native_claude': 'NOT_RUN',
           'framework_acceptance': 'NOT_EVALUATED'}
(EVIDENCE / 'readback.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
table = '\n'.join(
    f"| `{Path(row['file']).name}` | {row['covered_lines']}/{row['lines']} ({row['line_percent']:.2f}%) | "
    f"{row['covered_branches']}/{row['branches']} ({row['branch_percent']:.2f}%) | "
    f"{', '.join(map(str, row['missing_lines']))} |" for row in rows)
report = f'''# Focused cleanup and failure tests

Added 11 tests in `src/agents/skills/advisor/tests/test_cleanup.py`; updated its required artifact-manifest entry. Production code, existing tests, documentation, evaluation fixtures, coverage policy, and all {len(operational)} operational files remain byte-identical to intake. Source readback matches the published candidate, with all {len(manifest['files'])} manifest entries verified.

## Executed results

- Initial focused run against unchanged production: 11/11 passed, exit 0. No production defect was demonstrated, so production red/green repair was not required or claimed.
- Assertion sensitivity: 4/4 isolated intentionally broken copies were caught by assertion failures, not setup errors. Mutations suppressed read errors, lost wait-interruption state, suppressed close errors, and hid an undrained queue. Mutated files exist only under `maintenance/mutations`; no mutant was published.
- Final regression: 100/100 unit tests (89 existing plus 11 new), exit 0.
- Existing deterministic JSONL suite: 38/38 passed, exit 0.
- Declared final QA pass rate: 138/138 = 100%, counting each required case once. Focused runs and mutation cases are separate evidence and do not inflate that denominator.
- Python AST syntax check passed. Diff and hash review found exactly the two authorized changed paths.

## Coverage and remaining gaps

The existing requirement remains >=95% aggregate executed-line coverage across all executable first-party Python in `scripts/` plus `evals/`. No first-party behavior was excluded; tests and fixtures remain outside that source denominator. No branch or per-file gate was added.

| File | Executed lines | Branches | Uncovered lines |
| --- | --- | --- | --- |
{table}
| **Total** | **{total['covered_lines']}/{total['num_statements']} ({line_percent:.2f}%)** | **{total['covered_branches']}/{total['num_branches']} ({branch_percent:.2f}%)** | |

Aggregate line coverage increased from the retained 615/644 (95.4968944099%) to {total['covered_lines']}/644 ({line_percent:.10f}%). The source denominator and production bytes did not change. Branch coverage is reported independently and is not a 95% acceptance floor.

`advisor_stream.py` still has uncovered parser input rejection at lines 69 and 78, plus the empty-queue retry at line 230. Its remaining branches also include ignored progress metadata shapes. Runner history/preflight validation and evaluator input-shape gaps remain listed in `coverage.json`; they were not hidden or waived. This run's cleanup scheduling did not enter line 230 even though an older run had covered it, so per-run coverage is reported from the fresh data only.

An existing flood-reader test emitted `ResourceWarning: unclosed file` while passing. Its prior evidence has the same warning. It is retained in the regression log; the new tests own their real children and pipes with unconditional cleanup. This task does not claim elimination of every prior resource-lifetime issue.

## What the new assertions establish

- Real child pipe closed before reading: reports read failure, reaches reader completion without timeout, and denies advice.
- Injected OS read failure after bytes from a real child: retains exact bytes, records the failure, and denies otherwise well-formed advice.
- OS error or keyboard interrupt at pipe close: retains stdout/stderr, closes the other real pipe, records failure/interruption, and denies advice.
- Missing working directory: exercises a real spawn error and produces no advice or invented process exit.
- Interrupted wait: retries the wait and reaps the actual child, while retaining interruption state.
- Process exits during a kill error, or before cleanup: does not invent a still-live-child failure or kill an already exited child.
- Interruptions during reader and final queue draining: retain all queued bytes and EOF observations and record interruption.
- Cleanup deadline with remaining queued bytes: records incomplete draining, preserves consumed bytes and leaves the remaining event observable.

Fault injection is limited to one pipe/process/queue boundary at a time. No test replaces `execute_stream` or `_cleanup` with a fabricated successful result. Direct helper cases use real child processes, queues and threads, but they do not prove a live Claude or Codex UI interaction. Tests use a short cleanup ceiling only for the explicit exhausted-queue fixture; the production ceiling is unchanged.

## Reproduction

Host: {platform.platform()}; native PowerShell; Python {platform.python_version()} at `{sys.executable}`; cwd `{ROOT}` on the Windows filesystem. coverage.py 7.9.0. No dependency installation, network call or WSL checkout was used.

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:COVERAGE_FILE = 'C:/Projects/DevForgeAI/docs/plan/skill-authorings/advisor/20260916-cleanup-tests/maintenance/.coverage'
python -B -X utf8 -m coverage run --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals -m unittest discover -s src/agents/skills/advisor/tests -v
python -B -X utf8 -m coverage run --append --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/skill-authorings/advisor/20260916-cleanup-tests/maintenance/jsonl
python -B -X utf8 -m coverage json -o docs/plan/skill-authorings/advisor/20260916-cleanup-tests/maintenance/coverage.json
python -B -X utf8 -m coverage report -m
```

All final commands exited 0. Use fresh evidence paths for a subsequent run. Initial focused and mutation commands and outputs are retained under this run and its sibling intake. The package publication is AUTHORED, with source action edited. Authoring records retain their authoring-only status fields; this separate report records user-authorized executed maintenance tests on exactly the delivered bytes.

Independent skill validation: NOT_PERFORMED. Live Claude qualification: NOT_RUN. PowerShell launcher requalification: NOT_RUN (launcher unchanged). Installation: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED. The earlier native advisor smoke test does not establish new live coverage.

Final custody record: `{RUN / 'authoring-record.json'}`. Design capture: `{RUN / 'design-capture.json'}`. Optional independent validation handoff: `{RUN / 'validator-request.md'}`; next owner is skill-validator if the user selects independent package validation. No such invocation is required to complete this focused test-maintenance request.
'''
(EVIDENCE / 'report.md').write_text(report, encoding='utf-8')
print(json.dumps({k: v for k, v in summary.items() if k not in ('source_manifest', 'per_file')}, indent=2))
for row in rows:
    print(json.dumps(row))
