# Evidence and safe resumption

Use current filesystem and execution observations, not reconstructed success narratives. Records are editable development evidence, never protected acceptance or an authority gate.

## Logical records and locations

Resolve the evidence root through [context.md](context.md) before creating records. Select concrete paths there and record their mapping. Reuse a suitable existing evidence system if it preserves the required fields. Consolidate human-readable sections where useful; do not create empty files to satisfy a list.

| Logical record | Template and use |
| --- | --- |
| Context | [context.md](../assets/context.md): authorization, exact inputs, rules/decisions, tools, outputs, gaps. |
| Requirement traceability | [traceability.md](../assets/traceability.md): all source-qualified requirements, implementation, checks, statuses. |
| Slice plan | [slice-plan.md](../assets/slice-plan.md): dependency order, ownership, reuse decisions, verification and state. |
| Execution evidence | [execution-record.jsonl](../assets/execution-record.jsonl): one actual attempt per append-only JSONL line. |
| Checkpoint | [checkpoint.md](../assets/checkpoint.md): meaningful progress, live jobs, pending work and next safe action. |
| Delivery | [delivery.md](../assets/delivery.md): scope, outputs, requirement accounting, metrics, remaining gaps and acceptance. |

These are templates, not preexisting observations. Replace placeholder values only with observed facts; omit inapplicable optional detail with reasons. Never append an unexecuted template row as a real execution receipt.

Execution records must retain unique attempt/slice/check IDs, stage, exact command and working directory, platform/tool identities, start/end times, exit/timeout or unknown outcome, stdout/stderr locators, candidate identity, and interpretation. Use raw-byte SHA-256 for retained inputs and outputs; bind candidate source, tests, relevant configuration and prerequisites with scoped manifests/hashes, plus Git identity when available. HEAD alone is insufficient for dirty/untracked work. Record secret redaction explicitly; a redacted command is not an exact unredacted command. Retain a protected original locator only when required and permitted.

Use distinct attempt IDs/outputs on retries; never overwrite earlier failures. Equivalent references into an existing project evidence system must preserve the same observable fields. After commands, inspect actual outputs before assigning check status. Record interrupted/unknown outcomes honestly and reconcile later with new observations.

## Checkpoint and resume

Write a checkpoint after meaningful verified progress and before yielding with unfinished work. Preserve the context/input references, completed/pending slices, last verified candidates, observed source changes, owned jobs, decisions/failures, and next safe action. Update traceability with evidence locators. Keep historical checkpoints inspectable.

On a user-selected resume:

1. Locate the selected project, checkpoint, and context; verify their actual identity rather than restoring old source.
2. Re-read selected specification/instruction hashes, relevant current source/test/config hashes, toolchain identity, permissions, and jobs/process state.
3. Compare changed specifications, shared contracts, source, tools, and test definitions with dependent decisions/results. Mark those results stale and plan the necessary reruns; retain unaffected evidence only if candidate and prerequisites still match.
4. Reconcile owned jobs using observable process/output state. Inspect an unknown outcome before a retry; do not blindly replay commands, migrations, or long-running work.
5. Preserve another actor's changes. Resolve overlapping edits before mutation; never copy an old snapshot over current work. Cancel/clean only resources this run owns and is authorized to manage.
6. Record drift, affected requirements/slices, carried-forward evidence and reasons, gaps, and the next safe action. Continue independent work and write a fresh checkpoint as progress resumes.

A checkpoint is navigation, not unquestioned truth. Do not claim rollback, recovery, or completion without actual evidence. Follow [failure-delivery.md](failure-delivery.md) for changed-input and blocked outcomes.

