# PASS — advisor streaming development package

## Identity and conclusion

This independent offline assessment **PASSes** the selected streaming-progress and PowerShell-launcher change in `C:\Projects\DevForgeAI\src\agents\skills\advisor`.

- Exact package: 19 files, canonical package digest `ce037407bfe1bb636b42dc468595a93b5837a2788837fc436c4bfc615f1d033f`.
- Builder handoff: `docs/plan/skill-authorings/advisor/20260916T134000Z-streaming/validation-request.json`, SHA-256 `e0258f0795b8a8558f9aacf804128bc184e9b43504a66177cad14b029a888985`.
- Requirements: the user-selected advisor progress integration captured in `inputs/requirements-matrix.json`, with the deadline and PowerShell coverage clarification in `inputs/requirements-matrix-amendment-001.json`.
- Required platforms: native Windows Python 3.10.11, Windows PowerShell 5.1.26100.9444, and PowerShell 7.6.6.
- Assessment completed: yes. Outcome: PASS for the selected offline source-package scope.
- Builder readiness: `NO_CHANGE`. No repair proposal is justified by the frozen candidate results.

Live Claude behavior, operational installation, native Codex skill routing, and compiled-Rust framework acceptance were outside this selected run and remain separately reported below.

## Required cases and coverage

The mandatory denominator was declared before final execution and contains 30 distinct requirements-derived cases.

| Scope | Passing | Required | Pass rate |
|---|---:|---:|---:|
| Shared Windows-native cases | 28 | 28 | 100% |
| Windows PowerShell 5.1 launcher case | 1 | 1 | 100% |
| PowerShell 7 launcher case | 1 | 1 | 100% |
| **Overall** | **30** | **30** | **100%** |

`independent-cases-002.json` is the qualifying result. The coverage repeat in `independent-cases-003-coverage.json` also passed 30/30 and exists only to collect subprocess execution; it does not increase the denominator.

Executed-line coverage meets the required 95% minimum on every declared executable-source denominator:

| Runtime/source denominator | Executed | Executable | Line coverage |
|---|---:|---:|---:|
| Python `scripts/*.py` and `evals/*.py` | 604 | 635 | 95.1181% |
| Windows PowerShell 5.1 `scripts/advisor.ps1` | 13 | 13 | 100% |
| PowerShell 7 `scripts/advisor.ps1` | 13 | 13 | 100% |
| **Summed declared platform scope** | **630** | **661** | **95.3101%** |

Python branch coverage is reported separately: 240/258 branches, **93.0233%**. The `94.5129%` value shown by coverage.py combines statements and branches; it is not the executed-line metric. No executable Python source file or uncovered first-party behavior was excluded. Tests, fixtures, Markdown, YAML, JSON, the standard library, and the PowerShell runtime are outside the executable-source denominator declared before execution.

## Findings

No required defect was observed in the frozen 19-file package.

One pre-freeze review issue was resolved before publication: the initial v2 draft did not bind every derived evidence file or reject unknown v2 receipt fields. The published candidate binds `started.json`, `preflight.json`, raw streams, `result.json`, transport observations, and closed receipt fields. Independent cases `SV-SP-019` and `SV-SP-020` passed, including a tampered preflight that blocked follow-up before another reviewer invocation.

The independent PowerShell peer report says execution-policy enum value `5` means `Bypass`. That prose is incorrect on this host: the retained readable controls show `Process=Undefined`; enum `5` serialized that state. The peer commands did not pass `-ExecutionPolicy`, and separate positive wrapper runs under both shells also completed without that command-line override.

## Assessment dimensions

### Standards and structure — PASS

- Builder intake independently bound the current target to package digest `ce0374…d033f`.
- The validator structure observer passed all 14 emitted structure/link/configuration checks.
- The installed Skill Creator checker returned `Skill is valid!`.
- `artifact-manifest.json` contains and hashes every package file other than itself; independent case `SV-SP-030` passed.
- The final source snapshot has no excluded boundaries and no generated cache files.

### Workflow correctness — PASS

The public CLI retained quiet v1 behavior and added opt-in v2 streaming. Independent runs established:

- `--show-progress` selects `stream-json --verbose` while retaining every restricted read-only flag.
- Progress appears on stderr; the final receipt is one JSON value on stdout.
- Model text, tool arguments, raw child stderr, disallowed tool names, and terminal escapes do not enter progress output.
- Malformed, missing, duplicate, and nonterminal result streams are rejected without `response.md`.
- A deadline covers stream collection through EOF and actual direct-child exit; cleanup uses its separate bounded ceiling.
- Real two-megabyte stdout and stderr streams drain without deadlock or truncation.
- Failed budget envelopes retain finite reported cost and cap discrepancy while withholding advice.

### Instruction quality — PASS

`SKILL.md` and the execution/evaluation references describe the development and operational invocation paths, v1/v2 receipt compatibility, progress disclosure limits, cleanup boundary, evidence artifacts, coverage denominator, installation boundary, and framework-authority limitation. They do not present Python evidence as protected acceptance.

### Behavioral evaluation — PASS

- Independent mandatory cases: 30/30.
- Package regression tests: 81/81 in 13.606 seconds.
- Deterministic JSONL evaluation: 38/38, exact case digest `6f70d0daa0ac7b761404d08b0df8514b1c6863e1f916c9aafd378eda70770735`.
- Native launcher Pester cases: 4/4 under PowerShell 5.1 and 4/4 under PowerShell 7.
- Wrapper controls without an `-ExecutionPolicy` override: 2/2.
- Final source readback: unchanged package digest, 19/19 files.

### Enforcement recommendations — no candidates

This change is a developer tool and evidence helper. No new hook, phase gate, mutation broker, or acceptance authority is justified by the observed behavior. Existing guidance that Python advice and receipts are evidence only remains necessary.

## Test-integrity review

No skipped/ignored cases, coverage pragmas, unconditional passes, swallowed required exit codes, duplicate denominator cases, or source exclusions were found.

Some delivered unit tests inject queue, pipe, wait, kill, and progress-sink faults with `unittest.mock.patch`. Those tests prove deterministic error handling at the unit boundary, not native process behavior by themselves. The package also contains real local subprocess timeout/backpressure tests, and the independent suite separately exercised actual process I/O, timeout, direct-child stop verification, native CLI receipts, evidence tampering, and both PowerShell launchers.

`test_wait_failure_is_retained_after_actual_child_stop` uses a proxy whose final child state can be timing-sensitive. It passed in this run; its specific injected assertion is not used as the sole evidence for cleanup. Independent cases `SV-SP-015` through `SV-SP-018` provide the real-process evidence.

## Preserved attempts and limitations

- The initial pre-change Red attempt was a harness path error and is retained as non-product evidence. Attempt 002 established the valid Red: quiet JSON passed, while `--show-progress` and a valid JSONL terminal event failed on the old package.
- Final independent attempt 001 reported 29/30 because its oracle expected LF record terminators while the synthetic Windows text process emitted CRLF. Raw product bytes were correct. The corrected byte-level oracle preserved CRLF and attempt 002 passed 30/30; `response.md` was still compared byte-for-byte to the exact UTF-8 result text.
- Early PowerShell coverage probes mixed command inventory with debug-trace inference and are retained under `coverage/` as measurement-development failures. They are excluded from qualification. Standard Pester evidence under `coverage-independent/` directly measures the exact source and supersedes them.
- Pester 5 initially attempted to create an unrelated test-registry fixture on the managed host. The qualifying run set `TestRegistry.Enabled=false`; the launcher fixtures contain no registry behavior. No registry key or host policy was changed.
- The final broad `observe.py records` audit returned `MISMATCH` because this heterogeneous run retains raw BOM-bearing Pester JSON and raw coverage/readback manifests outside the observer's excluded `source/`, `inputs/`, and `trials/` boundaries. Its output is preserved at `trials/records-audit-001.json`. This is an aggregate-record tooling/layout limitation; it did not invalidate the separately verified artifact hashes or source-package observations, and the evidence was not relocated to force a pass.

## NOT_RUN and separate statuses

- Live authenticated Claude review: **NOT_RUN**; no model call or budget was selected for this package validation.
- Native Codex implicit skill activation: **NOT_RUN**.
- Operational `.agents/skills/advisor` installation/update: **NOT_PERFORMED**.
- Compiled-Rust framework acceptance: **NOT_EVALUATED and not established**. No qualified Rust authority issued a protected receipt.

These exclusions do not reduce the selected offline source-package verdict. They prevent claims about installed or live-provider behavior.

## Evidence and next action

Primary evidence is in this directory:

- `source-manifest.json`, `source/`, `source-readback-final.json`, and `source-after-manifest.json`
- `independent-cases-002.json` and `trials/independent-002/`
- `unit-tests.txt`, `evaluation/summary.json`, and `evaluation/results.jsonl`
- `coverage/coverage.json`, `coverage/coverage-report.txt`, and the raw `.coverage` data
- `coverage-independent/ps5.json`, `coverage-independent/ps7.json`, and `coverage-independent/command-receipts.json`
- `structure.json`, `skill-creator-check.txt`, `authoring-intake.json`, and `command-log.md`

No source remediation is required. A later installation or live Claude qualification must use a separate explicit selection and fresh evidence. Neither would establish compiled-Rust framework acceptance by itself.
