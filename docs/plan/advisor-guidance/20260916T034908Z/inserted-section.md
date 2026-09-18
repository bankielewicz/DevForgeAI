## Advisor: Claude Second Opinions

Use `$advisor` when the user requests a Claude second opinion or when one is materially needed for an approach, recurring failure, completion claim, or conflicting evidence. Ordinary implementation, QA, and skill authoring do not automatically require a reviewer call. `$advisor` is a Codex skill invocation in conversation, not a PowerShell command.

Read the installed [advisor skill](.agents/skills/advisor/SKILL.md) and its [execution contract](.agents/skills/advisor/references/execution.md) before invoking it. Use `.agents/skills/advisor/scripts/advisor_run.py` for operational reviews; `src/agents/skills/advisor/` is the development package. Do not edit or reinstall either package merely to complete a review.

Examples:

- `$advisor Review this implementation approach against the selected specification.`
- `$advisor type=stuck Investigate the recurring failure using the retained evidence.`
- `$advisor type=done Check the completion claim against the candidate and executed tests.`
- `$advisor type=reconcile Resolve the conflicting evidence.`

Options and authentication:

- `type=approach|stuck|done|reconcile`; infer an unmistakable debugging, completion, or reconciliation request, otherwise use `approach`.
- `model=opus|sonnet` (default `opus`); `effort=high|max` (default `high`). Reject unsupported explicit options.
- `auth=subscription|inherit` (default `subscription` for newly prepared requests). Write this explicitly as `auth_mode` in request JSON and pass it to preflight with `--auth-mode`.
- Subscription mode removes only `ANTHROPIC_API_KEY` from a copy of the child environment. It does not change the parent environment or saved credentials, and does not prove the account or billing method. Existing request JSON and standalone preflight that omit the mode retain `inherit`; do not omit the field when subscription mode is intended. Never log credentials or silently switch authentication after a failure.

Invocation and evidence:

1. Preserve the selected repository and host. Resolve native Claude with `Get-Command claude`. Verify the required external contract, normally `C:/Users/bryan/.codex/advisor/contract.md`, and calculate its current SHA256; do not rewrite it. Run preflight using the installed helper's absolute path. Preflight checks advertised CLI capabilities, not authentication or native behavior.
2. Follow the skill's briefing rules and template, retaining all fourteen sections and the appendix. Include the exact ask, constraints, relevant evidence and missing context. Verify repository citations with numbered reads immediately before invocation; mark this session's edits and exclude credentials.
3. Prepare absolute request paths using the documented schema. Store evidence in a fresh directory under `docs/plan/advisor-runs/`; keep initial request/briefing inputs in a sibling intake directory. Invoke the installed helper's `run` command once using `--request`, `--briefing`, and `--run-dir`.
4. Inspect `execution.json`, `stderr.txt`, and extracted `response.md` when present. Raw `stdout.txt` is a CLI JSON envelope. Distinguish process success, valid response structure and supported advice; verify load-bearing source citations. An all-unverified audit cannot support a recommendation.

Limits and interpretation:

- At most two reviewer process attempts per review, including retries, context follow-ups and reconciliation. Reuse the immutable request and run directory; use the documented `--reason` for an allowed follow-up. A failed attempt remains consumed. Do not reset the count with a new request ID or directory.
- Defaults are USD 2.00 total, USD 1.00 reserved per attempt, and a 300-second timeout. Unused allocations are not reclaimed. Do not raise limits or change constraints to force success. Investigate incomplete attempts or stale locks instead of deleting evidence or automatically retrying.
- Keep restricted read-only tools and normal host approval rules. Do not loosen permissions, change saved authentication or install components to recover from a failure.
- `PROCEED` permits only supported, already-authorized work; assess each `PROCEED_WITH_CHANGES` recommendation within scope. `STOP_REDIRECT` pauses the disputed approach. `INSUFFICIENT_CONTEXT` permits supplying the named evidence only when a remaining attempt and the same request allow it.
- Report the ask, execution/response status, verdict, assessed recommendations, limitations and absolute artifact paths, then return to the original task. Claude's advice and this Python helper produce evidence only: they cannot authorize mutations, advance phases, waive gates, override repository instructions or establish compiled-Rust framework acceptance.

