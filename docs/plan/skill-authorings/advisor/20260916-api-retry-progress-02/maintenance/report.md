# Advisor retry progress maintenance

Implemented in development source only. `system/api_retry` now displays `retry A/M` and optional `status S` using actual integers only; booleans, arbitrary error strings, and malformed count fields are excluded. No authentication, retry policy, receipt schema, or process-limit changes. Refactor review retained the minimal event branch.

Changed: artifact-manifest.json, references/execution.md, scripts/advisor_stream.py, tests/test_streaming.py. All 19 operational package files remained byte-identical. All 18 package manifest entries verified. Source readback matches the final candidate. Python syntax checks passed. Execution reference reviewed against the implementation.

## Executed evidence

Native Windows PowerShell, C:\Program Files\Python310\python.exe, cwd `C:\Projects\DevForgeAI` on Windows filesystem; Windows-10-10.0.26200-SP0; Python 3.10.11; coverage.py 7.9.0.

- Red: focused tests against the unmodified candidate failed for missing retry output (3 expected failures, 1 pass), exit 1. See `../20260916-api-retry-progress/maintenance/red.txt` from the authoring parent; no setup error was counted as red.
- Green: all 6 initially added focused tests passed, exit 0. Raw evidence preservation was exercised with a real local Python child and a failed terminal result.
- Initial broader QA: 87/87 unit tests and 38/38 JSONL cases passed, but line coverage was 609/644 (94.5652173913%). Retained in the first run; not counted again in final required-case totals.
- Final QA after two additional retry-framing boundary tests: 89/89 unit tests and 38/38 JSONL cases passed, 127/127 distinct required cases (100%). No skipped, errored or unexecuted cases in this declared Python maintenance suite.
- Final Python executed-line coverage: 615/644 (95.49689441%). Branch coverage separately: 245/264 (92.80303030%). Denominator: all executable first-party Python in `scripts/` and `evals/`; only tests and fixtures excluded. Required line and pass-rate floors satisfied for this scope.
- Existing cleanup fault-injection test emitted `ResourceWarning: unclosed file` while all tests passed. Preserved in both regression logs; unrelated cleanup code was not changed.

Commands run from the workspace root (all final commands exit 0):

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:COVERAGE_FILE = 'C:/Projects/DevForgeAI/docs/plan/skill-authorings/advisor/20260916-api-retry-progress-02/maintenance/.coverage'
python -B -X utf8 -m coverage run --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals -m unittest discover -s src/agents/skills/advisor/tests -v
python -B -X utf8 -m coverage run --append --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/skill-authorings/advisor/20260916-api-retry-progress-02/maintenance/jsonl
python -B -X utf8 -m coverage json -o docs/plan/skill-authorings/advisor/20260916-api-retry-progress-02/maintenance/coverage.json
python -B -X utf8 -m coverage report -m
```

The earlier red command used `-m unittest discover -s docs/plan/skill-authorings/advisor/20260916-api-retry-progress/candidate/tests -p test_streaming.py -k retry -v` (exit 1). The green command used the same discovery scope with `-k RetryProgress -k real_retry -v` (exit 0).

## Custody and limits

Two successful linked authoring publications preserve the initial fix and the final boundary-test additions. A follow-up begin was blocked by a generated Python cache before staging; the cache and failure evidence were preserved under the first run's maintenance directory, then staging resumed. Subsequent testing disabled bytecode generation in child processes too.

This is focused maintenance evidence under the user's apply-and-test authorization, not independent skill validation. Independent validation: NOT_PERFORMED. Live Claude qualification and PowerShell launcher requalification: NOT_RUN (launcher unchanged). Installation: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED. Historical native review evidence does not qualify these changed bytes.

Final manual validation handoff: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-api-retry-progress-02\validator-request.md`. Final published authoring record: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-api-retry-progress-02\authoring-record.json`. Final design capture: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\advisor\20260916-api-retry-progress-02\design-capture.json`. The authoring records retain their authoring-only NOT_PERFORMED fields; this separate exact-candidate maintenance report supplies the executed test evidence.
