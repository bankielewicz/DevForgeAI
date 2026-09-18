# Supporting-helper evaluation bundle

This external Python JSONL bundle verifies byte bindings and deterministically
reduces **already executed** helper tests, full validator regressions and helper
coverage. It does not run native skill trials or authorize framework operations.

Use `manifest-v2.json` as the final manifest. It binds the exact current builder
package, current validator source/fixtures, immutable copies of both packages,
retained execution receipts/logs, raw coverage, JSONL scenarios, independently
selected expected counts and threshold, result schema, runtime versions, runner
and synthetic reducer-test fixtures. `results.jsonl` contains the executed final
reduction; `FINAL-RECEIPT.json` additionally binds runner-development evidence.

Runner command from this directory:

```powershell
python -B -X utf8 reduce.py manifest-v2.json 1fe87bc375d32a8c3e02080f1790d63f73bcb705db3b175ec02d70604f47a0dd
```

Eight reducer tests passed in `green-002`, checking exact versus changed hashes,
duplicate case IDs, failed/skipped cases, wrong counts/nonzero exits, exact and
below-threshold coverage, exclusions, and added package files. `red-001` retains
the genuine duplicate-case assertion failure; `red-002` retains the changed-byte
assertion failure. These were corrected before successful reduction.

The first reduction failed a too-strict coverage assumption: coverage.py's raw
executed-line list includes module docstring line 1, whereas its executed-statement
denominator does not. Coverage.analysis2 confirmed all 453 executable statements
and 435 covered statements. The corrected grader intersects traced lines with
that explicit statement set and independently reconciles missing lines. The old
manifest and failed reduction remain retained; no threshold or denominator was
lowered and no source behavior was excluded.

Final reductions: helper tests 71/71 PASS, full regressions 292/292 PASS,
executed-line coverage 435/453 =96.02649006622516%. The 71 helper cases occur
within the 292 full-suite cases, so these counts must not be added. Branch arc
coverage remains separately 225/244 =92.21311475409836%.

Framework acceptance: NOT_EVALUATED. Full skill behavioral qualification is a
separate task; this bundle satisfies the supporting-helper evidence obligation
within its explicitly declared scope.
