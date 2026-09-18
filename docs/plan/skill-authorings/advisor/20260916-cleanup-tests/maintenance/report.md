# Focused cleanup and failure tests

Added 11 tests in `src/agents/skills/advisor/tests/test_cleanup.py`; updated its required artifact-manifest entry. Production code, existing tests, documentation, evaluation fixtures, coverage policy, and all 19 operational files remain byte-identical to intake. Source readback matches the published candidate, with all 19 manifest entries verified.

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
| `run_evaluation.py` | 71/72 (98.61%) | 21/22 (95.45%) | 29 |
| `advisor_run.py` | 311/320 (97.19%) | 137/148 (92.57%) | 228, 244, 265, 272, 287, 294, 295, 297, 427 |
| `advisor_stream.py` | 249/252 (98.81%) | 90/94 (95.74%) | 69, 78, 230 |
| **Total** | **631/644 (97.98%)** | **248/264 (93.94%)** | |

Aggregate line coverage increased from the retained 615/644 (95.4968944099%) to 631/644 (97.9813664596%). The source denominator and production bytes did not change. Branch coverage is reported independently and is not a 95% acceptance floor.

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

Host: Windows-10-10.0.26200-SP0; native PowerShell; Python 3.10.11 at `C:\Program Files\Python310\python.exe`; cwd `C:\Projects\DevForgeAI` on the Windows filesystem. coverage.py 7.9.0. No dependency installation, network call or WSL checkout was used.

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

Final custody record: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-cleanup-tests\authoring-record.json`. Design capture: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-cleanup-tests\design-capture.json`. Optional independent validation handoff: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-cleanup-tests\validator-request.md`; next owner is skill-validator if the user selects independent package validation. No such invocation is required to complete this focused test-maintenance request.
