# Independent forward review of `advisor`

## Conclusion

The completed development package now gives another Codex agent a coherent, bounded workflow for:

`$advisor type=done Check whether the candidate satisfies the selected specification.`

The request routed cleanly to `type=done`; the briefing and request formats were usable; the no-cost native preflight succeeded; and the current helper passed an independently prepared simulated process run over the synthetic repository in this directory. Three concrete response/receipt defects were found during the review, repaired by the package author, and independently retested. No unresolved deterministic runner defect remains from this bounded review.

End-to-end native behavior is still `INCOMPLETE`. The retained real Claude attempt timed out after its configured 180 seconds with empty stdout and stderr and no verdict. That result does not show that Claude can complete this `done` review, and it does not by itself prove a package defect. No retry or other paid Claude invocation was made by this independent review.

## Scope and package binding

- Package: `C:/Projects/DevForgeAI/src/agents/skills/advisor` development source only.
- Operational copies were not changed or installed.
- Synthetic repository, intake, probes, and retained simulated artifacts are under this `independent/` directory.
- Final package manifest SHA256: `f19f0161efed621d56044cd6242d3f50c625d4f9ec18ee014b3d05a9b4563d29`.
- The manifest binds 14 package files. Its bound helper is `scripts/advisor_run.py` SHA256 `4c4fdee77db5865c831cbd607aa6c754424b509f2b1f676636a35c5913347d02`.
- External advisor contract SHA256: `af4cd7f0505c92a186c29edc17328107ac2103f6069109c5aacac04da32b18ab`.
- No package file was edited by this independent reviewer.

## Synthetic forward case

The synthetic repository selects `docs/limit-cli-spec.md` and `src/limit_cli.py` in its `AGENTS.md`. Its specification requires canonical decimal input and exact stdout/stderr behavior. The candidate intentionally strips whitespace, accepts leading zeroes, and prints invalid-input errors to stdout.

The repository's existing happy-path test passed 1/1. The independent negative probe then assessed four required examples and passed only 1/4:

- `LIMIT=7`: PASS.
- `LIMIT= 7`: FAIL; candidate returned exit 0 and `limit=7` on stdout.
- `LIMIT=007`: FAIL; candidate returned exit 0 and `limit=7` on stdout.
- missing `LIMIT`: FAIL; exit 2 was correct, but the error was written to stdout instead of stderr.

This makes the adverse oracle concrete. A valid completion review should reject the candidate's conformance claim. The simulated reviewer result did so with `STOP_REDIRECT`; because that response was independently authored and injected, it validates runner mechanics only, not Claude reasoning.

## Confirmed defects and retests

### IF-01: empty missing-evidence list accepted

The initial parser accepted `VERDICT: INSUFFICIENT_CONTEXT` with `MISSING:\n- none` as valid even though `references/response-format.md` requires actual missing evidence. This could consume the remaining bounded follow-up without an actionable evidence request.

Final retest: PASS. The same response is rejected with `Missing-context verdict requires actual missing items`.

### IF-02: unlabeled content after verdict accepted

The initial parser accepted arbitrary unlabeled text between `VERDICT:` and `ASK RESTATED:`. That classified content outside the defined response sections as valid.

Final retest: PASS. The same response is rejected with `Unexpected content before ASK RESTATED`.

### IF-03: nonfinite cost could corrupt attempt history

An injected successful JSON envelope with `total_cost_usd: NaN` originally passed interpretation. Receipt serialization then failed after creating a truncated `execution.json`. The history check tested only file existence, so attempt 2 was allowed and chained to the corrupt bytes. The retained adverse artifacts are under `nan-cost-run/`.

Final retest: PASS. A nonfinite cost now produces a complete JSON-valid receipt with `response_status: INVALID` and `Reported cost must be finite, nonnegative numeric or null`. A separately corrupted prior receipt blocks before preflight or reviewer execution with zero additional process calls. The final helper also checks the prior response derived from raw stdout before permitting a follow-up.

## Final bounded evidence

All commands ran on native Windows from `C:\Projects\DevForgeAI` with Python 3.10.11 unless a narrower working directory is stated.

| Check | Result | Qualification |
| --- | --- | --- |
| `python -B -X utf8 -m unittest discover -s src/agents/skills/advisor/tests -p test_*.py -v` | PASS, 40/40 | Current deterministic unit/runner tests |
| `python -B -X utf8 src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/advisor-build/20260915-initial/independent/evaluation-final` | PASS, 22/22, 100% | JSONL structural/process corpus; `native_qualification: NOT_RUN`, `framework_acceptance: NOT_EVALUATED` |
| system `skill-creator` `quick_validate.py` | PASS, `Skill is valid!` | Structure/frontmatter only |
| `advisor_run.py preflight --claude C:/Users/bryan/.local/bin/claude.exe` | PASS, Claude Code 2.1.273, help SHA256 `ae85d661e9c086f05637ebcd868f5702b477ff6e55e2e65b8ada7807cd51a4b6` | Advertised flags only; not authentication, model entitlement, confinement, or prompt delivery |
| independently prepared current simulated run | PASS | One restricted reviewer process call, USD 1.00 cap, `Read,Grep,Glob`, `dontAsk`, required retained artifacts; simulated process only |
| parser edge retest | PASS | Both IF-01 and IF-02 rejected after repair |
| receipt integrity retest | PASS | IF-03 repaired; corrupt history blocked before another process call |

The package's final coverage evidence reports 280/282 executed lines (99.2908%) and 106/108 branches (98.1481%) over first-party executable Python in `scripts/` and `evals/`. This review read that final package evidence but did not independently reproduce the coverage run. The independently executed 40/40 tests and 22/22 JSONL cases were run against the same manifest-bound source hashes.

## Native and authority limits

The existing native attempt used Claude Code 2.1.273 from the synthetic native repository and retained a `TIMEOUT` receipt after approximately 180 seconds. `response_status` is `NOT_EVALUATED`; verdict and `all_unverified` are null; stdout and stderr both have the empty-file SHA256. No native response exists to grade for citation quality, contract delivery, read confinement, or discovery of the seeded defect.

Accordingly:

- Development source and bounded deterministic runner evidence: `PASS` after repair.
- Independent simulated workflow over a synthetic repository: `PASS`, helper mechanics only.
- Native Claude forward behavior: `INCOMPLETE`.
- Installation or operational-copy qualification: `NOT_PERFORMED`.
- Framework acceptance: `NOT_EVALUATED`.

## Evidence index

- `synthetic-repo/`: selected specification, flawed candidate, and happy-path test.
- `intake/`: independently prepared request and fifteen-section briefing.
- `probes/candidate_probe.py`: independently authored behavioral oracle.
- `probes/runner_probe.py` and `simulated-run-current/`: retained simulated process path.
- `probes/runner_edge_probe.py`: request and response parser edge cases.
- `probes/nan_cost_probe.py` and `nan-cost-run/`: retained pre-repair receipt-integrity failure.
- `probes/receipt_integrity_retest.py`, `nan-cost-retest/`, and `corrupt-history-retest/`: final receipt-integrity retests.
- `evaluation-final/`: final 22-case JSONL results and summary.
