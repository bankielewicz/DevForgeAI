# Advisor execution and continuation assessment

## Actual advisor result

The user authorized the newly available [operational advisor skill](../../../../.agents/skills/advisor/SKILL.md) for guidance when stuck. This review asked whether a one-use child-only environment with the unrelated provider key omitted fits the existing worker preflight selection. The exact immutable request is at `../../advisor-runs/20260916T034812Z-8d3c2a/request.json`.

Both permitted attempts are consumed; no third call, increased budget, changed authentication, or relaxed reviewer tools is selected.

| Attempt | Execution | Response / verdict |
| --- | --- | --- |
| 001 | Exit 1; raw envelope reports ConnectionRefused; empty stderr; 181.875 seconds reported CLI duration; zero reported cost | NOT_EVALUATED / none |
| 002, approved host escalation | Exit 1; raw envelope reports `error_max_budget_usd`, `budget_exhausted`, reached $1 cap; empty stderr; 188.252 seconds reported CLI duration | NOT_EVALUATED / none |

The CLI reports $1.015353 for attempt 002 despite the supplied $1 limit. That is retained CLI cost evidence, not a verified bill or a guarantee that the CLI enforces an exact monetary ceiling. Total configured allocations were $2 for the two attempts. No response.md was produced. No Claude recommendation was accepted or applied.

The first briefing's AGENTS.md line88 anchor drifted after the external advisor-guidance edit. The scope clause remains present at line123; the second complete briefing corrects the anchor and records the new source inventory. Original inputs and both attempts remain unchanged. The candidate stayed at manifest SHA256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`.

## Codex assessment of already-authorized preparation

The base worker contract at `docs/specs/framework/runtime/codex-worker-feasibility-v1.md:120` requires rejecting API credentials **in the child environment**. It prohibits another CODEX_HOME, rule bypass, changed operational configuration, credential-store reads/copies, or changing login. It does not require propagating every unrelated parent variable into the trial child. The preflight companion at lines18-20 expressly selects the bounded no-work inspection and allows false findings. The user already selected implementation through independent QA and continuation to those prerequisites; ordinary reversible preparation is authorized by `.agents/skills/dev/SKILL.md:14`.

Select a one-use input environment for the evidence supervisor's worker child that omits exactly `ANTHROPIC_API_KEY` case-insensitively. Preserve every other entry, the parent environment, saved credentials, fixed installed Codex home/profile, fixed launch vector, and compiled guard at `runner.rs:96-100`. Record variable names and the omission only, never credential values. Any other prohibited inherited name remains visible to the Rust guard and can still deny the operation. This is restrictive test-input preparation within the existing preflight scope, not a new framework environment-filter feature, altered guard, policy exemption, login, configuration edit, or operator finding.

Do not execute a predictably denied inherited-environment run merely to consume a fresh native run directory: the inherited-environment denial remains a clearly labeled static inference. The selected compiled preflight itself will validate its actual environment and every remaining source/profile prerequisite. A false-finding review cannot authorize `run`; no true finding is manufactured.

Keep stdin open, retain the exact command and streams, bound the supervisor at 145 seconds, and preserve any denial/failure without automatic retry or policy broadening. WN-01/WN-02 remain untouched and cannot run without their independent human operator findings. Advisor execution is optional supporting evidence and does not qualify this decision or establish protected framework acceptance.

## Current source state

The first successful inventory is historical after AGENTS.md changed. A second compiled collection against the unchanged candidate passed with refreshed AGENTS.md identity, still 137 entries (36 files, 56 indices, 45 absences). Its stdout SHA256 is `2029d7889cd4054d2791fd0e55684dae48ac0c37aac12710e068aad858a1fbad`. Fresh preflight request/review inputs bind these exact bytes. Rust must recollect and reject subsequent source or membership drift.

Developer evidence was sealed with 18,999 entries and zero readback errors; artifact-manifest SHA256 is `c8d537420e79156f5b147789e35948b7577e587bce5b837a9564d21e96b3de9e`. The sealed development and independent QA roots remain immutable.
