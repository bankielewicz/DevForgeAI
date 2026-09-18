# Local execution contract

Supported implementation target: native Windows with Python 3.10+ standard library and a native Claude CLI executable. Linux behavior is unqualified. No MCP or GUI dependency. Claude authentication must already be configured. The runner passes a copy of the environment to its children according to the selected auth mode; it never records credential values or modifies the parent environment. Do not install or change saved authentication as a recovery step.

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

This performs exactly one reviewer invocation. For an authorized follow-up use the same request and run directory, a new complete briefing, and `--reason context`, `citation`, `reconcile`, or `retry`. Never automatically repeat a failed tool call. If sandbox escalation is needed after a retained spawn failure, escalation consumes the remaining attempt.

## Files and budgets

The run stores immutable normalized `request.json`. An exclusive `.lock` serializes cooperating helper processes; a crash leaves it for operator investigation. Each `attempt-001` / `attempt-002` stores `briefing.md`, `started.json`, `preflight.json`, raw `stdout.txt`, raw `stderr.txt`, and `execution.json`. A valid response additionally produces extracted `response.md`. Started records reserve the attempt before invoking. An incomplete or corrupt prior attempt blocks another call. Follow-ups validate the prior receipt's schema, request/contract/cap/command binding, artifact hashes, and agreement with raw output and extracted response. JSON is serialized before an output file is opened. Deliberately rewriting an entire consistent history is outside this helper's trust model; these files are not a protected ledger.

Each invocation receives half the total budget, rounded down to cents. Conservatively reserve that allocation even on spawn failure or unknown actual cost. Thus total configured caps never exceed the request limit; this relies on Claude's implementation of `--max-budget-usd` and is not an independent billing guarantee. The reported cost, if present, is evidence only and never replenishes the budget.

The command uses `shell=False`, no inline briefing, explicit cwd, safe mode, restricted mode, strict MCP configuration, only Read/Grep/Glob tools and read permissions, dontAsk, no permission prompts, no persistence, and JSON output. Only the current attempt directory is added to the selected repository's read scope. The external contract is read by the CLI flag rather than granting its entire directory to file tools. Managed host policy still applies. CLI incidental files are not covered by the reviewer tool allowlist.

Python terminates and waits for the direct child on timeout. It does not prove termination of detached descendants; investigate an uncertain process before another attempt. Do not relax flags, switch to acceptEdits, or enable shell/write tools to recover. Report actual errors without guessing that empty output means a budget or authentication problem.

Receipts retain raw output hashes, contract and briefing hashes, prior receipt hash, cwd, full non-secret argument list, executable path/version, timestamps and exit status. They do not capture an entire repository snapshot, guarantee atomic contract reads by another process, or record credentials. Avoid editing the contract while a review runs; detected drift invalidates advice.

Sources checked during authoring: [Claude CLI reference](https://code.claude.com/docs/en/cli-reference), local Claude 2.1.273 `--help`, and [Codex skills](https://learn.chatgpt.com/docs/build-skills). Supported flags are checked at runtime rather than inferred from a version number.
