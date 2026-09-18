# Proposed next selection: explain the native profile denial

Status: **proposal/handoff only**. The approved junction amendment is complete and independently PASS. This document does not authorize another launch, product repair, policy relaxation, operational edit, or framework acceptance.

## Exact retained evidence

- Frozen 56-file worker manifest: `../../framework-worker-source-identity/20260916T021843Z-dev/candidate-manifest.json`, SHA256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`.
- Independent QA: [report](../../framework-worker-source-identity-qa/20260916T021843Z-retest/qa-report.md), 123/123 tests, 3,191/3,339 lines.
- Current-rule native no-work preflight: [receipt](current-rules-preflight/preflight-001/receipt.json), [journal](current-rules-preflight/preflight-001/stdout.bin), [request](current-rules-preflight/preflight-request.json), [false-findings review](current-rules-preflight/preflight-review.unqualified.json).
- Final compiled inspector and source readback: [summary](final-readback.json). The source inventory before/after is identical.

## Problem to investigate

Real Codex process creation succeeded, then the harness returned native exit3 `profile_unqualified` before recording a successful effective-config observation. Cleanup and fixture preservation succeeded. The journal does not identify whether rejection came from post-spawn source review, initialize/config RPC process accounting, or config validation. `worker_exit_code:1` follows the stop request and is not an independent crash diagnosis.

No native model trial ran. Do not conclude that Pro authentication, gpt-6-astra/high availability, hooks, plugins, apps, MCP, network isolation or custom-provider policy passed or failed from this result.

## Bounded proposed development work

1. Derive a closed, non-sensitive diagnostic contract for the existing denial branches before changing behavior. Preserve all rejection predicates, fixed launch vector, source/executable identities and all-false preflight semantics.
2. With retained Red/Green tests, add compiled-Rust observations identifying the failed stage and approved predicate category. Cover post-spawn source verification; initialize/config RPC process accounting (total/active counts, without arbitrary process command lines); and closed config-validator rejection categories. Do not retain raw config, credential material, user identifiers, arbitrary server error text or unknown payload fields.
3. Independently verify that diagnostics distinguish these branches, cannot authorize work, preserve cleanup/deadlines/cancellation, and do not leak unknown fields. Repeat required offline regressions, negative paths, formatting, Clippy and full first-party executed-line coverage with both 95% floors. Preserve the current original failure and candidate; do not edit historical evidence.
4. After independent QA, prepare exact fresh fixture/request/review/inventory digests and select one bounded no-work native diagnostic launch. Refresh source bindings after any host permission changes; retain every attempt. A diagnostic launch remains separate from WN-01/WN-02 and must not dispatch a thread/turn or generate true operator findings.
5. Use the newly observed predicate to decide whether there is a product defect, unsupported host/profile prerequisite, or contract gap. Any repair/contract or installed-state change must have its corresponding selection. Do not preselect an allowlist relaxation as the answer.

## Unchanged boundaries

Windows-native selected checkout; no install/login, alternate CODEX_HOME, operational-copy changes, cache edits, junction refresh or authority provisioning. Parent credentials remain unchanged; any child-only environment choice must be recorded explicitly. Preserve native model-trial limits and require independently supported human operator findings before them. Framework acceptance stays NOT_EVALUATED until a separately qualified compiled-Rust authority issues an applicable protected decision.
