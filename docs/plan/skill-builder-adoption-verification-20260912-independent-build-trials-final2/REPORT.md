# Independent legacy forward trials on the final package

The unchanged independent trial harness completed synthetic import, reviewed
Markdown build, and generated-baseline regeneration in a fresh disposable
project. All earlier trial artifacts remain unchanged.

The final builder manifest is
`11457297985c7768faaec1846e54e0bcf4538fd8e064fb0d1099f9da6c7e8620`.

| Observation | Executed result |
| --- | --- |
| Import, specification build, and conflict/resolved regeneration | Complete |
| Evaluator invocations | 13, all exit 0 |
| Grader observations | 35 PASS: import-v2 9, spec-v1 8, revision-spec-v1 18 |
| Skill Creator structural checks | 9 passed |
| Receipt-script executions | 63, expected outputs/exits observed |
| Conflict proposal | Exit 1, no destination change or baseline advancement |
| Resolved revision | Only scripts/summarize.py changed; user-edited SKILL.md and unrelated personal-note.txt retained |
| Readback audit | All emitted candidate/case hashes and 553 retained file hashes verified; live source file set and hashes unchanged |
| Trial subprocess commands | 89; no unexpected exit codes |

Script executions observed exact `13.30` total and `0.30` travel subtotal, the
declared four-field JSON output, header-only zeros, and exit-2/no-stdout
rejections for nonfinite, missing, excess-precision, malformed-column, and
blank-category input. Task input bytes remained unchanged. Source Python was
preserved during import; the source-host model override was removed from the
entrypoint. The Markdown build retained the equivalent capability and mappings.

The real conflict and the separate authorized resolution remain distinct runs.
The retry used the original successful B, retained the edited entrypoint through
N=B, rechecked package and per-path current bytes before mutation, and advanced
the new generated baseline only after delivered checks and readback. Every
evaluator invocation has a distinct retained input snapshot and exact case file.

Evidence entry points:

- [Task and exact top-level commands](original-agent-task.md).
- [Synthetic task prompts](raw-task-prompts.md) and [subprocess log](commands.jsonl).
- [Final audit](final-readback-audit.json).
- [Import report](retained-project/docs/plan/skill-imports/receipt-summary/initial/conversion-report.md).
- [Specification build report](retained-project/docs/plan/skill-builds/receipt-summary-spec/initial/build-report.md).
- [Conflict report](retained-project/docs/plan/skill-builds/receipt-summary-spec/conflict/conflict-report.md).
- [Resolved revision report](retained-project/docs/plan/skill-builds/receipt-summary-spec/resolved-retry/build-report.md) and [actual mutation log](retained-project/docs/plan/skill-builds/receipt-summary-spec/resolved-retry/mutation-log.json).

The worker made no builder-source edits and performed no installation. These
are development observations: framework enforcement is NOT_IMPLEMENTED; Rust
qualification, native implicit activation, and operational installation are
NOT_PERFORMED. This revision trial changes a script clarification and exercises
the unchanged task behavior; it does not establish general semantic merging or
all recovery cases. Independent routing was delivered separately in the earlier
evidence directory for the parent's final evaluation.
