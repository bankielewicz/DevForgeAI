# Evidence-integrity and resource-ownership test maintenance

Implemented the five listed rejection tests, repaired the flood-reader fixture's resource ownership, and added an optional entry-point-excluded coverage configuration. Development source only; all 19 operational files, production scripts and repository policy are unchanged. Source readback matches the authored candidate; all 21 artifact-manifest entries match.

## Executed verification

- Five new tests accept a pristine synthetic attempt before tampering. Each makes one semantic change and asserts the exact `ValueError` directly and through the normal follow-up path. Rehashed launch/final-envelope artifacts update only the dependent digest so an unrelated hash failure cannot satisfy the test. Rejection also preserves prior files, leaves no second attempt, and makes no new preflight/reviewer calls.
- Five corresponding isolated guard-removal mutants are all detected by `AssertionError: ValueError not raised`, not by setup errors or another rejection guard. The final-envelope guard was already mutation-detected in the user's report; it is included because all five table entries were explicitly selected. This does not claim mutation coverage for every other integrity check.
- Warning reproduction before repair: original fixture passed but the ResourceWarning probe failed (exit 1) on an unclosed BufferedReader. After repair, the same probe passed (exit 0) with no warnings. The fixture now retains its real child, waits for its deliberately overlong reader, joins both readers and closes both pipes in `finally`. Existing timeout assertions are unchanged; elapsed time is measured before fixture-owned cleanup. No warning suppression was introduced.
- Full regression: **105/105 unit tests**, zero failures/errors/skips; **zero captured ResourceWarnings**, including after explicit garbage collection.
- JSONL regression: **38/38** cases passed. Final declared case rate: **143/143 = 100%**. Focused runs and mutant failures are separate evidence and are not counted again.
- The first integrity-focused run had four fixture setup errors because the production JSON writer intentionally refuses overwrites. The test helper was corrected to rewrite only its temporary fixtures; the original output is retained as `integrity-focused.txt`. Those errors were not product failures or valid red results. The next focused run passed 5/5.
- Python syntax and source/hash checks passed. The only changed paths are artifact-manifest.json, evals/coverage-entrypoints.ini, references/evaluation.md, tests/test_integrity.py, tests/test_streaming.py.

## Coverage reconciliation

The evaluator discrepancy is execution scope, not a source or denominator mismatch. The unit-only run measures **70/72 lines (97.22%) and 20/22 branches (90.91%)** in `run_evaluation.py`. Appending the separate JSONL runner invocation additionally executes **line 90** and **branch 89->90**, giving **71/72 (98.61%) and 21/22 (95.45%)**. No other executable file gains coverage from that invocation. Unit-only data is retained as `.coverage-unit-only` and `coverage-unit-only.json` before append, so both views are reproducible.

Required baseline: all first-party executable Python in scripts/ plus evals/, with no excluded first-party lines. Tests and fixtures remain outside the denominator. The >=95% aggregate line requirement is unchanged; branch/per-file figures remain separately reported.

| View | Line coverage | Branch coverage |
| --- | --- | --- |
| unit-only | 634/644 (98.45%) | 251/264 (95.08%) |
| baseline | 635/644 (98.60%) | 252/264 (95.45%) |
| entrypoints | 632/640 (98.75%) | 249/260 (95.77%) |

`entrypoints` is an optional diagnostic report from the exact same combined data, using `evals/coverage-entrypoints.ini` and `exclude_also`. It excludes only runner lines 426-427 and evaluator lines 89-90. It is not substituted for the required baseline and is not used to rescue a failing threshold.

| Baseline file | Lines | Branches | Uncovered lines |
| --- | --- | --- | --- |
| `run_evaluation.py` | 71/72 (98.61%) | 21/22 (95.45%) | 29 |
| `advisor_run.py` | 315/320 (98.44%) | 141/148 (95.27%) | 228, 244, 294, 295, 427 |
| `advisor_stream.py` | 249/252 (98.81%) | 90/94 (95.74%) | 69, 78, 230 |

Remaining gaps are recorded without classifying them all as low risk: runner lines 244 and 294-295 still include malformed-receipt shape and unexpected-final-envelope rejection paths beyond the five selected cases. Other runner gaps are unsuccessful terminal-envelope handling and its CLI entry point. Streaming parser/type and queue timing gaps were left unchanged as requested. No full tamper-proof ledger, native confinement, or framework acceptance claim follows from these tests.

## Reproduction and retained artifacts

Host: Windows-10-10.0.26200-SP0, native PowerShell, Python 3.10.11 at `C:\Program Files\Python310\python.exe`, cwd `C:\Projects\DevForgeAI` on the Windows filesystem. coverage.py 7.9.0. No installation, operational mutation or live Claude invocation.

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

Custody record: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-integrity-tests\authoring-record.json`. Design capture: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-integrity-tests\design-capture.json`. Optional manual validation handoff: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-integrity-tests\validator-request.md`. Authoring-only status fields are not overwritten by this separate executed maintenance evidence.
