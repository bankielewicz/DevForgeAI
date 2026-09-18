# Advisor authentication repair and native completion

Implemented in `C:/Projects/DevForgeAI/src/agents/skills/advisor` and published to `C:/Projects/DevForgeAI/.agents/skills/advisor`. Installation readback and all manifest-listed source/installed hashes match. Backups are retained in `source-before/` and `installed-before/`.

New skill requests explicitly select `auth_mode: subscription` unless the user chooses `auth=inherit`. Subscription mode copies the environment and removes only ANTHROPIC_API_KEY, case-insensitively, for version/help probes and the reviewer child. JSON requests and standalone preflight that omit the mode retain inherited authentication. Neither parent environment nor saved credentials are changed. Mode changes within a run are rejected. Legacy requests and receipts retain their bytes and hashes.

## Executed evidence

- RED: the focused subscription request test failed because the original runner rejected the new field. `red.txt`, exit 1, one expected assertion failure.
- GREEN: nine initial authentication tests passed, including real local subprocesses. `green-auth.txt`, exit 0.
- Refactor review: environment policy is isolated in a pure helper and shared across probes/reviewer. No additional behavioral restructuring was needed. Full regression follows the final changes.
- QA: 51 unique unittest cases passed; `qa-tests.txt`, exit 0. These include 11 authentication cases after adding failure/no-retry and missing-mode receipt negatives.
- Mandatory JSONL evaluation: 27/27 independent fixture expectations passed; `evaluation-001/results.jsonl` and `summary.json`, exit 0. Five fixtures cover authentication environment behavior using synthetic values only.
- Combined declared cases: 78/78, 100%; repeated red/green and internally repeated corpus evaluations do not increase the denominator. Mandatory negative cases passed.
- Coverage denominator: all first-party executable Python in scripts/ and evals/, excluding tests and fixtures only. No coverage exclusions. Executed lines 289/291 = 99.3127147766323%; branches 110/112 = 98.21428571428571%. Preserve `coverage.data` and `coverage.json`.
- Syntax, JSON/JSONL, relative Markdown links, dependency hash and complete package-manifest checks passed; `source-checks.json`. The initial PowerShell display of coverage JSON failed because coverage includes an empty property name; readback with ConvertFrom-Json -AsHashtable succeeded. Coverage generation itself exited 0 and was not rerun.
- Installation: `installation.json` records 12 copied paths, backup location and successful hash readback. No unrelated operational files were changed.

## Native Claude result

The approved changed-package qualification completed on its first attempt, using installed advisor, native Windows Claude Code 2.1.273, Opus/high, subscription mode, the original restricted read-only flags, USD 1.00 cap and 300-second timeout.

- execution_status: SUCCEEDED; helper/Claude exit 0.
- response_status: VALID; verdict: PROCEED_WITH_CHANGES; all_unverified: false.
- CLI envelope: is_error false, 11 turns, no reported permission denials; duration 124153 ms; reported cost USD 0.490801 (CLI estimate, not independently verified billing).
- Raw stdout, empty stderr, receipt and extracted response: `native-subscription/attempt-001/`.
- Parent ANTHROPIC_API_KEY was still present after completion; its value was never printed. The Rust source hash was unchanged and both package manifests still matched.

The old exhausted run `C:/Projects/DevForgeAI/docs/plan/advisor-runs/20260916T032132Z-3c7857` remains intact. This qualification was explicitly authorized with the repair plan; it did not reopen or reset that run. No second repaired-package attempt was needed.

## Assessed Claude summary

Claude summarized `devforgeai/src/protocol.rs` as the indexing daemon's protocol-v1 module. It defines request/response and error types, 17 daemon/project/index/job operations, strict request validation, mutation classification, and length-prefixed framing helpers. Requests have a 1 MiB limit, UUID-shaped identifiers and a 100–120000 ms timeout range; response limit is 8 MiB.

Codex checked its load-bearing citations directly against numbered source. The indexing crate identity is confirmed at Cargo.toml:6. Request validation is at protocol.rs:167 and typed_operation at :197. Mutation classification is at :243. Framing helpers at :307/:322 use four-byte big-endian lengths; their async counterparts are in client.rs:11/:26. This distinction matters when describing production transport. UUID validation checks shape, not UUID version/variant. Response::exit_code depends on the optional error, not the ok boolean.

Accept Claude's requested qualification that this is indexing-daemon source, not the protected acceptance authority. Its characterization of “self-contained” as contradicted is too broad: the file is suitable for a bounded summary, but does not alone describe production transport. Accordingly the summary above avoids that runtime claim. Its advice to avoid all further file writes does not override the user's authorized evidence delivery. Its request for a child-environment dump is unnecessary and would risk recording credentials; synthetic real-child tests already supply bounded evidence of filtering. No Rust repair was requested or applied.

The valid, detailed source-grounded response contains facts not supplied in the briefing. The retained JSON envelope does not include a complete tool-call transcript, so this establishes the exercised native summary scenario, not an independent audit of every internal read. No Rust build/runtime behavior, full advisor native matrix, Linux qualification, account identity, billing mechanism, or framework acceptance is claimed.

## Commands and host

All commands ran from C:/Projects/DevForgeAI using native Windows PowerShell and the C: filesystem. Python: C:/Program Files/Python310/python.exe, version 3.10.11. Coverage.py 7.9.0. Claude: C:/Users/bryan/.local/bin/claude.exe, version 2.1.273. Git metadata absent.

Commands below show the commands executed; log redirections are described above. Install and native model invocation used approved host escalation. No dependency installation was performed.

```powershell
python -B -X utf8 -m unittest discover -s src/agents/skills/advisor/tests -p test_auth.py -k test_subscription_request_excludes_key_from_every_child -v
python -B -X utf8 -m unittest discover -s src/agents/skills/advisor/tests -p test_auth.py -v
python -B -X utf8 -m coverage run --branch --source=src/agents/skills/advisor/scripts,src/agents/skills/advisor/evals --data-file=docs/plan/advisor-auth-fix/20260916T033234Z/coverage.data -m unittest discover -s src/agents/skills/advisor/tests -v
python -B -X utf8 -m coverage json --data-file=docs/plan/advisor-auth-fix/20260916T033234Z/coverage.data -o docs/plan/advisor-auth-fix/20260916T033234Z/coverage.json
python -B -X utf8 src/agents/skills/advisor/evals/run_evaluation.py --output docs/plan/advisor-auth-fix/20260916T033234Z/evaluation-001
python -B -X utf8 docs/plan/advisor-auth-fix/20260916T033234Z/finalize_source.py
& 'C:/Projects/DevForgeAI/docs/plan/advisor-auth-fix/20260916T033234Z/install-validated.ps1'
python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/advisor/scripts/advisor_run.py preflight --claude C:/Users/bryan/.local/bin/claude.exe --auth-mode subscription
python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/advisor/scripts/advisor_run.py run --request C:/Projects/DevForgeAI/docs/plan/advisor-auth-fix/20260916T033234Z/native-request.json --briefing C:/Projects/DevForgeAI/docs/plan/advisor-auth-fix/20260916T033234Z/native-briefing.md --run-dir C:/Projects/DevForgeAI/docs/plan/advisor-auth-fix/20260916T033234Z/native-subscription
```

All commands above except the expected red test exited 0. Native execution arguments, timestamps, binding hashes and exit status are in its execution.json. Source checks and installed verification are supporting evidence only. Framework acceptance: NOT_EVALUATED.
