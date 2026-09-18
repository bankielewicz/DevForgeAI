# Local execution contract

Supported implementation target: native Windows with Python 3.10+ standard library and a native Claude CLI executable. Linux behavior is unqualified. No MCP or GUI dependency. Claude authentication must already be configured. The runner passes a copy of the environment to its children according to the selected auth mode; it never records credential values or modifies the parent environment. Do not install or change saved authentication as a recovery step.

`scripts/advisor.ps1` is a thin run-only launcher for Windows PowerShell 5.1 and PowerShell 7. It accepts mandatory `-Request`, `-Briefing`, and `-RunDir` paths; optional `-Reason`, `-Python`, and `-ShowProgress`; then invokes the sibling Python runner with an argument array. It contains no review policy, credential handling, process transport, model selection, or hardcoded review path. Child stdout and stderr remain separate and the launcher exits with the child's native status. A launcher failure before Python starts exits 2. Use the Python command directly for preflight.

Resolve executable paths using `Get-Command claude`. All request paths are absolute. Run the following from the selected repository, substituting the actual skill path if installed elsewhere:

```powershell
python -B -X utf8 C:/Projects/DevForgeAI/src/agents/skills/advisor/scripts/advisor_run.py preflight --claude C:/Users/bryan/.local/bin/claude.exe --auth-mode subscription
```

The probe calls only `--version` and `--help`. It requires the documented restriction, output, budget, and permission flags. The hidden append-system-prompt-file flag may be advertised by the help's `--append-system-prompt[-file]` notation. Help is not proof of authentication, model entitlement, tool access, filesystem confinement, or prompt delivery.

## Request file

Use JSON schema [request.schema.json](../assets/request.schema.json). All defaults are normalized into the retained request. Example, with a contract digest that must be freshly verified before use:

```json
{
  "schema": "advisor-request-v1",
  "ask": "Does the current implementation satisfy the selected specification?",
  "type": "done",
  "model": "opus",
  "effort": "high",
  "auth_mode": "subscription",
  "repo_root": "C:/Projects/DevForgeAI",
  "claude_path": "C:/Users/bryan/.local/bin/claude.exe",
  "contract_path": "C:/Users/bryan/.codex/advisor/contract.md",
  "contract_sha256": "eec3af8fa530175c1da9f31fcf05cab59c591dd30456be13ee9deb2ba234934e",
  "total_budget_usd": "2.00",
  "timeout_seconds": 300
}
```

Unknown fields are rejected. Model/effort options are the skill's narrow interface, not a complete catalog of Claude capabilities. Budget is a decimal string, 0.02 to 100.00 with at most two decimal places; values above the default require existing user authorization. Timeout is an integer from 1 to 1800 seconds. Contract digest is lowercase hex. Defaults: approach/opus/high, USD 2.00 total, 300 seconds.

`auth_mode` accepts `inherit` or `subscription`. The skill explicitly selects `subscription` for newly prepared requests unless `auth=inherit` is requested. For compatibility, omitted JSON fields and omitted standalone preflight `--auth-mode` retain `inherit`. Inherit copies all environment entries. Subscription removes only `ANTHROPIC_API_KEY`, matching its name case-insensitively for Windows, from a child-only copy. The same selection applies to version/help probes and the reviewer process. All other environment entries remain unchanged; other provider settings or credentials may still affect Claude. This is an environment policy, not proof of subscription identity or billing. See [Anthropic's API key guidance](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code).

No mode is selected automatically in response to a 401 or other execution failure. Authentication mode is immutable within a run. Legacy stored requests and receipts without the field mean `inherit`; their original bytes and hashes remain unchanged during follow-ups. New started/execution receipts and preflight results record the selected mode without credential values.

Choose a unique UTC timestamp plus random suffix under a writable evidence parent, for example `docs/plan/advisor-runs/20260915T180000Z-a1b2`. Keep inputs in a sibling intake directory. Do not assume the historical home-directory run location is writable in the active sandbox.

```powershell
python -B -X utf8 C:/Projects/DevForgeAI/src/agents/skills/advisor/scripts/advisor_run.py run --request C:/path/intake/request.json --briefing C:/path/intake/briefing.md --run-dir C:/path/runs/unique-id
```

The equivalent development-package launcher command is:

```powershell
& C:/Projects/DevForgeAI/src/agents/skills/advisor/scripts/advisor.ps1 -Request C:/path/intake/request.json -Briefing C:/path/intake/briefing.md -RunDir C:/path/runs/unique-id
```

Add `-ShowProgress` only when interactive progress is useful. The wrapper translates it to `--show-progress`; progress records go to stderr while the Python helper's final machine-readable result stays on stdout. `-Python` selects the Python executable only and defaults to `python`. Paths are passed as separate native arguments, including Windows paths with spaces and Unicode characters.

This performs exactly one reviewer invocation. For an authorized follow-up use the same request and run directory, a new complete briefing, and `--reason context`, `citation`, `reconcile`, or `retry` (or the PowerShell `-Reason` equivalent). Never automatically repeat a failed tool call. If sandbox escalation is needed after a retained spawn failure, escalation consumes the remaining attempt.

## Files and budgets

The run stores immutable normalized `request.json`. An exclusive `.lock` serializes cooperating helper processes; a crash leaves it for operator investigation. Each `attempt-001` / `attempt-002` stores `briefing.md`, `started.json`, `preflight.json`, raw `stdout.txt`, raw `stderr.txt`, and `execution.json`. A strictly framed progress stream additionally stores its parsed final envelope as `result.json`; a valid successful response additionally produces extracted `response.md`. Started records reserve the attempt before invoking. An incomplete or corrupt prior attempt blocks another call. Follow-ups validate the prior receipt's schema, request/contract/cap/command binding, artifact hashes, transport observations, and agreement with raw output, parsed result, and extracted response. JSON is serialized before an output file is opened. Deliberately rewriting an entire consistent history is outside this helper's trust model; these files are not a protected ledger.

Quiet attempts preserve the original JSON command and `advisor-execution-v1` receipt interpretation. `--show-progress` selects `--output-format stream-json --verbose` and `advisor-execution-v2`. The stream parser drains stdout and stderr concurrently and retains their raw bytes. It requires each nonempty stdout line to be one JSON object, exactly one terminal `type: result` object, and that result to be the final event. Malformed JSON, duplicate JSON member names, nonfinite values, non-object events, a missing or duplicate result, or events after the result make the response invalid. When strict framing identifies one final result, it is retained in `result.json` even when the process or result reports failure. A nonzero exit, timeout, interrupted cleanup, malformed stream, or failed result never yields `response.md` or valid advice.

Interactive progress is an allowlist derived from parsed events. It prints elapsed time, the session UUID, assistant activity, Read/Grep/Glob tool names, final-result receipt and periodic waiting messages to stderr. After evidence is saved, the runner prints the validated execution status, response status, verdict and any reported-cost/cap discrepancy to stderr. It does not print assistant text, tool arguments, file paths, credential values, arbitrary event values, or untrusted terminal control characters. Progress is observational and does not change limits, policy, receipt interpretation, or the final stdout value.

Each invocation receives half the total budget, rounded down to cents. Conservatively reserve that allocation even on spawn failure or unknown actual cost. Thus total configured caps never exceed the request limit; this relies on Claude's implementation of `--max-budget-usd` and is not an independent billing guarantee. For version 2 streaming attempts, a finite nonnegative reported cost in a strictly parsed terminal envelope is retained even for a failed result or nonzero exit. The receipt identifies a reported cost above the reserved cap as a discrepancy; it does not reinterpret the process as successful, replenish the budget, or prove the provider's final charge. Quiet version 1 attempts retain their original cost interpretation.

The command uses `shell=False`, no inline briefing, explicit cwd, safe mode, restricted mode, strict MCP configuration, only Read/Grep/Glob tools and read permissions, dontAsk, no permission prompts, no persistence, and JSON output. Only the current attempt directory is added to the selected repository's read scope. The external contract is read by the CLI flag rather than granting its entire directory to file tools. Managed host policy still applies. CLI incidental files are not covered by the reviewer tool allowlist.

The quiet transport uses Python's bounded subprocess timeout. The streaming transport applies one monotonic reviewer deadline through stdout/stderr draining, pipe completion and observed child exit. On timeout or interruption it terminates the direct child and allows at most a separate five seconds for direct-child and pipe cleanup. Receipts record whether the direct child stopped, whether both pipe readers finished, and any transport error. These observations do not prove termination of detached descendants or independently prove EOF for each pipe; uncertain cleanup blocks advice and requires investigation before another attempt. Do not relax flags, switch to acceptEdits, or enable shell/write tools to recover. Report actual errors without guessing that empty output means a budget or authentication problem.

Receipts retain raw output hashes, contract and briefing hashes, prior receipt hash, cwd, full non-secret argument list, executable path/version, timestamps, exit status, response framing and cleanup observations. Version 2 follows version 1 history without rewriting it; prior version 1 receipts remain subject to their original command and interpretation. Receipts do not capture an entire repository snapshot, guarantee atomic contract reads by another process, prove detached process-tree cleanup, or record credentials. Avoid editing the contract while a review runs; detected drift invalidates advice.

Sources checked during authoring: [Claude CLI reference](https://code.claude.com/docs/en/cli-reference), local Claude 2.1.273 `--help`, and [Codex skills](https://learn.chatgpt.com/docs/build-skills). Supported flags are checked at runtime rather than inferred from a version number.
