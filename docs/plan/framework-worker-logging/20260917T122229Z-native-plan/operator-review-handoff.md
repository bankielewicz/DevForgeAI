# Operator-review handoff

**Review pending. No operator finding or launch approval has been recorded.** Read the [diagnostic plan](native-diagnostic-plan.md), current root AGENTS.md, the [independent QA report](../20260917T105456Z-qa-retest/qa-report.md) and its sealed specifications. The user selected planning only. This packet proposes one `preflight` diagnostic with no thread or turn, using the QA-built corrected candidate and fixed v3 launch policy.

## Decisions that require actual attribution

| Decision | Present state | Required record before dependent work |
| --- | --- | --- |
| Native diagnostic selection | Not selected in this planning task | Exact user instruction, one-attempt/no-retry limit and reference to this sealed handoff. |
| `gpt-6-astra` / `high` | Proposed; availability unobserved | User selection; subsequent Rust model-list result. No substitution. |
| Child environment | `ANTHROPIC_API_KEY` observed by name; no values inspected/logged | Explicit selection to omit only that name from a child copy; actual names-only receipt. Other guarded names or alternate CODEX_HOME stop preparation. |
| Reviewer | Unassigned | Actual named operator and review time; never impersonate the operator. |
| Exact fixture and control sources | Future root absent; live Rust inventory not collected | Fresh schema-2 compiled inventory, digest and semantic review for that fixture. |
| Supervisor | Command and deadline contract proposed | New immutable recorder identity, exact argv and offline evidence for held stdin, stream capture, deadline and owned-process containment. No native worker may be used to test the recorder. |

A diagnostic preflight permits false review findings under the bound preflight contract. False means **unqualified for work** and may honestly represent an unresolved condition, with rationale outside the closed review JSON. It does not claim the empirical opposite is proven. Do not populate true values merely to pass admission. The future `run` operation requires all four supported true findings and a new native selection; it is outside this handoff.

## Finding worksheet

| Exact ReviewV2 field | Current state | Evidence the operator must assess |
| --- | --- | --- |
| `native_read_only_available` | UNRESOLVED | Source-bound Windows/native sandbox selection and actual supported runtime read-only/never state. A configured `windows.sandbox` mode, executable hash or offline synthetic test does not demonstrate arbitrary workload isolation. |
| `no_external_tool_or_hook_effects` | UNRESOLVED | Applicable hooks/rules/plugins/MCP/apps, exact fixed disables, complete source inventory and current runtime config/features/hooks/plugin/app/MCP observations. Empty lists or an inventory digest alone do not prove inactivity. |
| `codex_managed_chatgpt` | UNRESOLVED | Source/provider/auth selection and sanitized account/read observation with refreshToken false showing the required ChatGPT/Pro mode. Do not inspect/copy credentials or account identifiers. |
| `no_custom_provider` | UNRESOLVED | Source semantics, inherited credential/provider variable names, exact policy and supported runtime config origins/provider/base-URL state. Missing arbitrary config keys alone do not prove internal endpoint selection. |

These cells are a worksheet, not booleans submitted to Rust. The [review template](review.template.json) intentionally contains nulls for the reviewer, selection, source bindings/digest and findings; strict deserialization will reject it. The operator must produce a separate final schema-2 review, plus an attributed rationale identifying the evidence or reason each condition remains unqualified. Preflight observations can inform a later review; they never silently revise this immutable review or authorize model work.

## Source and identity review

The compiled inventory derives `ancestor_root` as `C:\`, `workspace_root` as `C:\Projects\DevForgeAI`, user Codex as the actual USERPROFILE plus `.codex`, ProgramData Codex as the actual ProgramData plus `OpenAI\Codex`, and plugin cache beneath that user Codex root. Verify the actual environment-derived paths at preparation; no caller-selected scope. Inventory covers ancestor AGENTS/overrides/config/requirements/hooks, user defaults and rules, system controls, plugin controls, directory membership and explicit absences. It excludes credential file contents. Bounds: 1 MiB/file, 8 MiB aggregate file bytes, 2,048 entries, 1,024 members/directory, 32 ancestor levels and eight rule levels.

Only the compiled plugin junction is allowed in this source scope: `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest` to `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816`, tag `0xa0000003`. Inventory schema 2 also binds source-identity digest `d2f9f1952262dae524930873688c54eef9fd8959ca7fa1c26e7a311ddc089b69` and the exact observed mapping. Read physical sources once; do not recursively traverse the alias. Any added, missing or changed source/membership, unexpected reparse, inaccessible file or unknown runtime origin blocks qualification. Do not fix installed state to satisfy inventory.

The native launcher mappings are separately pinned in the candidate's [native identity](../../../../devforgeai/experiments/codex-worker-probe-logging-qa-fixes/src/native-executable-identity.json). Planning verified the physical executable hash and the displayed targets of both junctions. The full Windows identity/reparse verification must run in unchanged Rust immediately before spawn. Do not launch through the alias, resolve a new release or alter a junction.

Review all relevant semantics without saving arbitrary config contents, headers, environment values, credentials or account identifiers. Record paths/digests, absences, membership and narrowly sanitized reasoning. Source freshness alone is not semantic review. Supported installed-profile and runtime conclusions remain unresolved until actual observations exist.

## Finalization order and closed shapes

1. Record the separate selection and prepare the exact fresh fixture. Collect `sources-001` via the planned compiled `profile-sources` command for operator review of the inventory and source semantics. Retain its exact stdout bytes and exit receipt. Inventory collection itself does not launch Codex.
2. Under the actual launch permission context, collect `sources-002-prelaunch` before finalizing the review. The template references this final observation. Return any material difference to the operator; retain initial observations and any draft input versions. In the final schema-2 review use every field from the template, an actual nonempty reviewer and selection reference, exact worker digest, fixture, model/effort and v3 policy identity. `profile_sources` must contain exactly the physical file entries from the final inventory, each with `path` and `sha256`, no missing/extra/duplicate entries. Bind the exact inventory bytes by absolute reference and SHA256. Keep review at most 64 KiB and inventory at most 1 MiB. Put rationale outside the closed schema; no extra fields.
3. Preserve exact [diagnostics config](inputs/diagnostics.json) bytes in future `inputs-001/diagnostics.json`. Finalize a new schema-3 request from the [template](request.template.json), inserting the actual finalized review digest. Its task hash remains the 307-byte fixture hash. Bind the complete input set and selected probe/worker binaries; request/review paths and bytes must be immutable.
4. Verify all final inputs and maintain the same launch permission context. If a later approval changes source bytes, membership or relevant environment policy, stop the dependent launch, preserve old versions, collect another distinct source observation and return changed material to the operator. Do not auto-carry forward findings. Rust still independently rechecks source and executable identity immediately before spawn.
5. Only after all prerequisites and selection match, execute the single planned preflight through the reviewed supervisor. Capture the process guard, profile observations, mandatory capture and exit consistency, optional diagnostic completeness, fixture immutability and stopped-tree evidence. Recollect sources afterward and inspect the immutable run.

The [command plan](command-plan.json) has exact paths and bounds, but no recorder implementation has been claimed ready. Never invoke the JSON templates or a bare native Codex command as a shortcut. Any startup/profile/identity failure ends dependent work and is retained; no automatic retry, framework acceptance or WN-01/WN-02 launch follows.

## Review return packet

Return the attributed selection, completed review and separate rationale; inventory and all input/build digests; reviewed recorder and offline checks; names-only environment decision; and unresolved predicates. If proceeding is not supportable, return the concrete missing prerequisite without fabricating true findings or editing installed state. Use the [separate trial request](next-native-trial-prompt.txt) only after choosing that step.
