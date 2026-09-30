# Codex host mapping and contract limits

Read this at entry. SPEC-002 v2 remains the authority; these provider mappings do not
establish framework acceptance. Relative assets and references resolve from the actual
loaded PRD skill directory, and `../architecture/SKILL.md` resolves in that same package.
Do not search other worktrees, installed caches or another provider to make a handoff work.

## Invocation and tools

Select PRD in Codex, invoke `$devforgeai:prd BRN-001` (or the catalog's actual PRD name),
or use a matching natural-language request. The argument is an ID, never a path.
There is no Claude `$ARGUMENTS` expansion or Claude Skill tool. Use the file, patch and
shell tools the host actually exposes. Shell reads stay in the workflow's named folders.
Do not invoke a `devforgeai` executable. Policy validation requires Python 3, PyYAML and jsonschema. Missing validation capability
with approved policy is ERR-08; do not install dependencies or substitute a handwritten check.

## Questions

Follow the actual tool schema, availability and permitted use. On hosts with Plan-only
`request_user_input`, it is unavailable in Default mode; its common limits are 1–3 questions
and 2–3 options. Do not call it for a required gate when the host permits optional questions
only. An asynchronous question tool also requires an actual user reply before dependent work.

Use numbered plain text and end the turn whenever the permitted tool cannot represent all
choices. Keep must now, should now, later and won't; allow could now, decide later and statement
edits. Keep all four operating contexts and the multi-select ADR applicability question.
Never drop a choice or re-ask an explicitly answered gate. Use at most three questions in
each batch. Count each call or plain-text batch, including gates, toward `interview.max_calls`;
changing tools never resets or increases the budget. If an essential gate is still unanswered
when the budget is exhausted, stop without writing and name it. Ask more only if authorized.

## Runtime provenance

Use `tool: "codex"` for newly authored records. Preserve existing authors, reviews and old
Change Log rows, including Claude authorship. Record the current model and session only if
the running skill can obtain them through a supported production interface exposed by this
host. A configured model is not proof of the model serving this turn. A harness-observed
thread ID is not automatically available to the skill.

Never scrape unrelated session logs, guess environment-variable names, invent IDs, copy the
BRN's identity or consume evaluator-only identity injection. If an exact value is unavailable,
write `"unavailable"` for that field and disclose it in this write's Change Log row and in the
handoff. SPEC-002 v2 explicitly permits that honest disclosure, but the exact-identity obligation
BEH-10 stays open in qualification. Do not turn an unavailable identity into fabricated evidence
or repeatedly rewrite the file to pretend the capability was repaired.

## Validation and extension lifecycle

SPEC-002 v2 settles D-03 to D-09. An approved PRD may be extended after the user's explicit choice;
no additional failure-disposition permission is required. A changed approved PRD stays in-review
with approval cleared, including after failed validation. Preserve earlier item bytes and review
history, and state that the new revision has not been reviewed.

Run one initial readback check and at most three actual repair-and-readback cycles (four checks
maximum). Record each check and repair. An unrepairable error stops early; an unchanged check
or a no-op rewrite is not a repair. ERR-06 produces a failure report with no architecture handoff.
