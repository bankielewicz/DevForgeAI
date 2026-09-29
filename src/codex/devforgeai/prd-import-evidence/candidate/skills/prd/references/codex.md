# Codex host mapping and contract limits

Read this at entry. SPEC-002 v1 remains the authority; these provider mappings do not
establish framework acceptance. Relative assets and references resolve from the actual
loaded PRD skill directory, and `../architecture/SKILL.md` resolves in that same package.
Do not search other worktrees, installed caches or another provider to make a handoff work.

## Invocation and tools

Select PRD in Codex, invoke `$devforgeai:prd BRN-001` (or the catalog's actual PRD name),
or use a matching natural-language request. The argument is an ID, never a path.
There is no Claude `$ARGUMENTS` expansion or Claude Skill tool. Use the file, patch and
shell tools the host actually exposes. Shell reads stay in the workflow's named folders.
Do not invoke a `devforgeai` executable. No connector or extra runtime library is needed.

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
write `"unknown"` for that field in a provisional new/draft PRD and explain the missing value
in the current Change Log row and reply. This is an explicit disclosure, not compliant
provenance: self-check item 3 remains unresolved under BEH-10/VER-09. Do not report validation
success, approval readiness or successful downstream handoff. Never retry a missing capability
as if it were a repairable formatting error. Ask for a supported integration or owner decision
before claiming full conformance; do not modify the governing specification.

## Unresolved validation wording

BEH-12 says "Fix and check again, at most three attempts." ERR-06 says "after three fix
attempts". The source carries both wordings. Do not claim an exact exhaustion count is
qualified until the owner resolves whether the initial check counts. Stop after at most
three repair attempts, retain the initial check and every real repair/readback, and report
the count and unresolved errors without claiming this resolves the ambiguity.

BEH-09 returns an approved extension to `in-review` and clears approval. ERR-06 requires
the previous status after failure; for an approved input that would label altered content
approved, conflicting with BEH-06 and the output contract. Before changing an approved PRD,
show this conflict and obtain a concrete failure disposition from the owner, unless already
decided explicitly for this run. Keep the original file unchanged while that decision is open.
Do not restore `approved` onto changed content by implication. Other independent PRD work
can continue. The comparison report proposes resolutions; none is approved by this import.
