# Skill-validator enhancement evidence

This directory retains one development-only maintenance campaign. The selected contract is `docs/specs/skill-validator-postmvp-spec.md`; `specification.md` retains the original intake. The source contract was clarified to allow protected candidate files inside disposable workspaces while requiring plans and evaluator assertions outside them. This clarification did not rewrite previous evidence.

## Reproduction and interpretation

Run from `C:\Projects\DevForgeAI` with native Windows Python 3.10 or newer and the package's declared dependencies. This run used Python 3.10.11, PyYAML and coverage 7.9.0 already installed. No WSL checkout or environment was used. `environment.json` records the denominator before execution.

- `campaign.py ATTEMPT` runs the declared unittest inventory and writes one JSONL record per method; failing subtests never inflate the case count. Use a fresh attempt name. Each attempt records exact source identities, expected results and runtime details before running.
- `grade_campaign.py ATTEMPT_PATH` checks frozen inventory completeness and dispositions against `expected-results.json`. `result.schema.json` describes each JSONL row.
- `measure.py freeze NAME` creates a fresh coverage directory and refreshes the development evaluation manifest. `measure.py combine NAME` combines only measured files with captured hashes equal to the declared final source, using per-process identities captured by `sitecustomize.py`. Executions without matching captured identities receive no coverage credit. All 14 first-party script files remain in the denominator, including unexecuted lines.
- Set `COVERAGE_PROCESS_START` to the selected directory's `coverage.ini`, `PYTHONPATH` to this evidence directory, and `SV_COVERAGE_IDENTITIES` to its `identities` directory for the campaign process. These are per-process settings, not persistent machine configuration.
- `check_delivery.py FRESH_DIRECTORY` verifies protected-file hashes, source syntax, supplied standards digests and the build manifest, then retains exact source/specification copies and a change inventory.

The authoritative paths for this maintenance result are identified in `implementation-report.md`. Earlier provisional coverage and failed attempts remain available but do not qualify the final bytes. The `before` directory is the initial development source. `standards-inputs` contains all eight selected raw documents. Delivered test modules include real temporary fixtures, with existing reusable fixture constructors retained alongside them. `bundle-manifest.json` binds the retained artifacts; it is editable evidence, not protected provenance.

## Retained failures and scope

Initial metadata failures, runner-integrity failures, oracle counterexamples, quoted-link resource failures, and Windows console Unicode failures were retained before their repairs. Setup failures from newly written test fixtures are explicitly distinct from valid red results. The initial advisory organization helper was authored before its first test; no pre-implementation red evidence exists for that helper, and later tests do not retroactively establish it.

Regression-001 included stale-manifest failures; regression-002 and regression-003 exposed the Windows CLI path in stages. Regression-004 was 401/401 PASS with 95.37085744345082% executed-line coverage. A subsequently confirmed analogous advisory-CLI Unicode defect has separate red/green evidence and requires the final regression-005 result. No historical failures were removed or converted into passing cases.

`long-budget` is a real 121-second process probe, not a native skill scenario. `independent/forward-001` contains actual Codex cold trials and separate semantic adjudication. Read-only actor permissions prevented delivery; startup failures and approved continuations are retained. The separately user-authorized `forward-002` final-source campaign used explicit workspace-write: the positive report-delivery trial qualified, while the adverse trial timed out at 600 seconds before report/handoff delivery. Its native completion rate is 1/2, separately reported from unit tests.

Linux native qualification, implicit skill discovery, optional no-skill/previous-version comparisons, installation and compiled-Rust framework acceptance are not established by this campaign. The QA skill's historical 42-scenario evaluation was not selected for replay and its status is unchanged.
