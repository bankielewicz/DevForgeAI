# Advisor streaming progress delivery

## Outcome and scope

Implemented and published the selected development package at `C:\Projects\DevForgeAI\src\agents\skills\advisor`. Authoring state: **AUTHORED**. Independent validation: **PASS for the selected offline source-package scope**. The [independent skill-validator report](../../skill-validations/advisor/20260916T140000Z-streaming-final/validation-report.md) records the behavior, regression, coverage, test-integrity and final source-readback results separately from authoring.

The installed `.agents/skills/advisor` remains unchanged. Live Claude qualification and Codex implicit skill activation were not run. Framework acceptance is **NOT_EVALUATED** and is not established by these supporting scripts, tests, authoring records or reports.

## Delivered behavior

- `scripts/advisor.ps1` is a run-only PowerShell 5.1/7 launcher with `-Request`, `-Briefing`, `-RunDir`, optional `-Reason`, `-Python` and `-ShowProgress`. Python continues to own the request, authentication selection, attempt limits, command construction, response validation and evidence.
- `--show-progress` selects Claude `stream-json --verbose`. Safe elapsed-time, session, allowed tool-name, assistant-activity and waiting messages appear on stderr. Final machine-readable JSON stays on stdout. Model text and tool arguments are not displayed as progress.
- The streaming transport concurrently captures raw stdout/stderr, uses a monotonic reviewer deadline through pipe completion and child exit, and bounds cleanup separately to five seconds. Receipts distinguish observed direct-child exit and reader completion; detached process-tree cleanup is not qualified.
- Strict JSONL validation rejects malformed/non-object events, duplicate keys, nonfinite values, missing/duplicate terminal results and events after the result. Failed, interrupted, timed-out or incompletely cleaned-up attempts cannot yield valid advice.
- New `advisor-execution-v2` receipts bind raw streams, `started.json`, `preflight.json`, a strictly parsed `result.json` and the extracted response when valid. Follow-ups verify the recorded observations and derived artifacts. Original quiet JSON commands and `advisor-execution-v1` interpretation remain supported without rewriting historical evidence.
- Streaming receipts retain finite reported cost even on a failed budget result and flag a reported amount above the CLI cap. This observes Claude's report; it does not independently enforce billing or replenish an attempt allocation.

## Candidate identity and ownership

- No Git metadata exists in this checkout.
- Published package: 19 files; 11 selected paths changed or added.
- Canonical package digest: `ce037407bfe1bb636b42dc468595a93b5837a2788837fc436c4bfc615f1d033f`.
- Validation packet SHA256: `e0258f0795b8a8558f9aacf804128bc184e9b43504a66177cad14b029a888985`.
- [Authoring publication](../../skill-authorings/advisor/20260916T134000Z-streaming/publication-readback.json) binds the selected contract, design, source and delivered files.
- [Final readback](final-readback.json) verifies the published files against the frozen candidate, all 16 operational files against their before hashes, and the unchanged user-owned `advisor-test.ps1`.
- The developer freeze used Windows Path ordering for its custom digest. Its file map matches publication exactly; final readback records the builder's canonical case-sensitive relative-path ordering and digest. The original freeze is preserved.

## Executed checks

| Check | Observed result | Evidence |
| --- | --- | --- |
| Pre-change behavior Red | Quiet JSON control passed; new streamed behavior failed as expected | `../../skill-validations/advisor/20260916T134000Z-streaming/prechange-red-result-002.json` |
| Full developer regression | 81/81 passed | [Captured command and output](regression-final/receipt.json) |
| Retained deterministic JSONL evaluation | 38/38 passed | [Summary](jsonl-final/summary.json), [rows](jsonl-final/results.jsonl) |
| PowerShell launcher development checks | PowerShell 5.1 and 7 passed argument, channel, failure and exit-code cases | `launcher/green-result.json` |
| PSScriptAnalyzer 1.25.0 | Zero warnings/errors | [Receipt](launcher-static/receipt.json) |
| Installed Claude help/version only | Exit 0, required profile advertised; no reviewer call | [Receipt](cli-capability-preflight/receipt.json) |
| Independent selected behavior | 30/30 passed | `../../skill-validations/advisor/20260916T140000Z-streaming-final/independent-cases-003-coverage.json` |
| Independent Python regression / JSONL | 81/81 and 38/38 passed | Independent run `unit-tests.txt` and `evaluation-console.txt` |
| Independent Python executed lines | 604/635 = 95.1181102362% | Independent run `coverage/coverage.json` |
| Independent Python branches | 240/258 = 93.0232558140%, reported separately | Independent run `coverage/coverage.json` |
| Standard Pester launcher coverage | Each shell: 4/4 tests, 14/14 commands, 13/13 executable lines (100%) | Independent run `coverage-independent/ps5.json` and `ps7.json` |

The Python source denominator includes every executable `.py` file under package `scripts/` and `evals/`; tests/fixtures and declarative resources are excluded. The launcher is measured separately under each native PowerShell runtime. The coverage.py table's combined line-and-branch percentage is not the mandatory executed-line metric. Required behavior, regression, JSONL and launcher counts are reported separately because their exercised behaviors overlap; retries are not new passing cases.

Environment: native Windows AMD64 at `C:\Projects\DevForgeAI`; Python 3.10.11, coverage.py 7.9.0, Windows PowerShell 5.1.26100.9444 and PowerShell 7.6.6. Standard Pester used existing 3.4.0 and 5.7.1 installations. The independent final Pester runs used no execution-policy bypass; Pester 5's unrelated TestRegistry fixture was disabled. No dependencies were installed.

## Retained failures and limitations

Development Red/Green evidence is under `tests/`, `transport/` and `launcher/`. It includes the retained stream/envelope and evidence-binding failures repaired before publication. Unit fault injection is distinguished from real subprocess tests; it does not qualify real Claude behavior or detached descendants.

The first publication command stopped before target writes because a development tool generated `scripts/__pycache__` inside staging. Those generated bytes were moved, with hashes, to `generated-bytecode-preserved/`. The original failure is retained in `authoring-publication/`; the successful corrected publication is in `authoring-publication-002/`. No source/test assertion was changed to recover from that packaging issue.

The independent evaluator retained its initial CRLF oracle failure and Pester collection attempts. Its earlier hybrid PowerShell coverage analysis is superseded by direct standard Pester measurements in `coverage-independent/`; no ancestor-line inference is used for the final launcher coverage claim. These were evaluation-harness issues, not demonstrated product failures. Read the independent report for their classification and exact retained evidence.

Neither a new paid reviewer call nor operational installation was selected. The historical exhausted review was not rerun. Rust worker development, its native trials, and protected acceptance-authority implementation remain outside this advisor integration.

## Using the development launcher

Prepare a fresh, complete request and briefing as described in [execution.md](../../../../src/agents/skills/advisor/references/execution.md), then run the development launcher from the repository root:

```powershell
.\src\agents\skills\advisor\scripts\advisor.ps1 `
  -Request 'C:\path\intake\request.json' `
  -Briefing 'C:\path\intake\briefing.md' `
  -RunDir 'C:\path\advisor-runs\new-review-id' `
  -ShowProgress
```

The paths above are examples. An authorized follow-up uses the existing immutable request and run directory with an allowed `-Reason`; it cannot reset a consumed review's attempt count. Installation is a separate action against the operational package.
