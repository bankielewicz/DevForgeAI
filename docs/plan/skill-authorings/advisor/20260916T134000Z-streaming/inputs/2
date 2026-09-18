# Advisor development package handoff

The advisor skill is authored at `src/agents/skills/advisor`. It provides conversational request selection, a fourteen-section briefing template, direct use of the existing external Claude contract, a bounded process runner, preserved attempt evidence, response parsing, and Codex assessment guidance. Automatic discovery policy is left at its normal default. No operational installation was performed.

## Status and limits

| Scope | Result | Evidence |
| --- | --- | --- |
| Development package authoring | COMPLETE | SKILL.md, resources, helper, tests, JSONL evaluation, schemas, runtime declaration and artifact manifest |
| Final unit/integration checks | PASS: 40/40 distinct test methods, 100% | [final test output](final-checks/tests.stderr.txt) |
| Final deterministic JSONL cases | PASS: 22/22 required cases, 100% | [summary](final-checks/evaluation/summary.json), [case results](final-checks/evaluation/results.jsonl) |
| Executed-line coverage | PASS: 280/282, 99.29078014184397% | [coverage JSON](final-checks/coverage.json) |
| Branch coverage | 106/108, 98.14814814814815% | Same coverage JSON; reported separately |
| Skill metadata and local links | PASS | skill-creator quick_validate exit 0; 8 local links verified |
| Independent bounded review | PASS after three findings were repaired and independently retested | [independent report](independent/report.md) |
| Native Windows Claude smoke test | INCOMPLETE: 0/1 completed successfully | [native execution receipt](native/run-001/attempt-001/execution.json) |
| Native Codex discovery/routing, denied mutation and outside-root access scenarios | NOT_RUN | Package was not installed; deterministic command checks do not prove native confinement |
| Installation | NOT_RUN | Development package only |
| Framework acceptance | NOT_EVALUATED | Python and reviewer output are evidence only |

The deterministic groups overlap in exercised code and are reported separately; repeated runs are not added to either denominator. The native failure is not counted as a deterministic pass. Full native qualification remains INCOMPLETE despite passing numeric floors for the declared deterministic scope.

Coverage denominator was declared before implementation in [scope.md](scope.md): all first-party executable Python under advisor/scripts and advisor/evals, no excluded executable lines. Tests and data fixtures are outside this denominator. The two uncovered lines are module entrypoint calls; they remain in the denominator. The combined line-and-branch percentage printed by coverage.py is not substituted for executed-line coverage.

## Native observation

On Windows through PowerShell, the Python 3.10.11 runner launched `C:\Users\bryan\.local\bin\claude.exe` 2.1.273 from the synthetic repository at `C:\Projects\DevForgeAI\docs\plan\advisor-build\20260915-initial\native\repo`, on the native Windows filesystem. The command and exact arguments are in the execution receipt. It requested opus/high with a USD 1.00 CLI cap, out of a USD 2.00 two-attempt request, using the original external contract and only synthetic fixture content.

Start: 2026-09-16T02:33:12.475280+00:00. Finish: 2026-09-16T02:36:12.518970+00:00. The 180-second timeout expired with empty stdout and stderr; the helper exited 1 and recorded TIMEOUT, NOT_EVALUATED, and null verdict. No paid retry was performed. The timeout does not establish a model, authentication, permission, or product defect. No native successful-read, contract-delivery, or confinement claim is made. This trial used an intermediate runner revision; it cannot qualify the final package bytes in any case.

## Corrections and retained evidence

Initial contract/budget tests and runner tests failed before their implementation, retained in red.txt and red-runner.txt. Additional tests reproduced the numeric-vs-string request budget mismatch before its repair. The early extended suite accidentally rediscovered an imported test class; it was corrected before final measurement. Its 38-count exploratory output is retained but is not used as final pass-rate evidence.

Focused grader checks reproduced rejection gaps for empty fixture IDs and type-coercing equality (`false` versus `0`); grading now compares canonical JSON values without that coercion. Their failures remain in grader-red.txt.

Independent review identified acceptance of bulleted `none` under MISSING, unlabeled text after VERDICT, and nonfinite cost causing truncated receipts with insufficient follow-up history checks. Each was reproduced before repair. The runner now rejects those malformed responses, serializes JSON before creating a file, and validates prior receipt structure, bound request/contract/cap/command, raw artifact hashes, and extracted response agreement before a follow-up. Derived-response tampering was separately reproduced and fixed. Red and green outputs remain in this directory; independent retest evidence remains in independent/.

A follow-up outside the selected repository must quote relevant prior response text into its new briefing, since only the current attempt directory is added to Claude's read scope. The instructions now state this explicitly.

## Reproducibility and artifact identity

[Final commands](final-checks/commands.json) record each argument list, working directory, platform, Python executable/version, and exit code. The final verification script is [run_final_checks.py](run_final_checks.py); it uses a fresh directory and does not overwrite previous outputs. Individual command stdout/stderr and coverage data are retained alongside commands.json.

`verify_package.py --publish` created the package manifest; a second `verify_package.py` call read it back and verified exact file hashes, Python/JSON syntax, local links and unchanged original source hashes. Both exited 0. The manifest binds 14 package files and the external contract dependency. Manifest SHA256: `f19f0161efed621d56044cd6242d3f50c625d4f9ec18ee014b3d05a9b4563d29`.

Original prompt SHA256 remains `2bb2e9b5c0d226c4778bc61dc8cd39e2a87aa04611538f541dd4d4cee7719aba`. External contract SHA256 remains `af4cd7f0505c92a186c29edc17328107ac2103f6069109c5aacac04da32b18ab`. These files were read, not modified or copied into the skill as competing authorities.

The runner's caps and checks are local workflow mechanics. Files are not a protected ledger, the CLI budget flag is not an independent billing guarantee, and Python does not grant framework authority. Native qualification and operational installation are the next separate work items.
