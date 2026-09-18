# Review, delivery and resumption

## Review the authored story

Read the assembled document against the original selected request, governing sources and current template. Inspect actual content, not merely the presence of headings. Account for every selected clause and scenario, source/decision locator, AC, component/rule/NFR, UI obligation, prerequisite and unresolved question. Confirm that technical requirements map back to ACs or canonical shared clauses and that all selected ACs have concrete verification observations.

Check unique identity, valid metadata types, well-formed XML/YAML, accurate source quotations, resolving local links and actual conditional-section applicability. Replace accidental template examples, contradictory field values, vague mandatory outcomes and empty required content. For facts about existing files/interfaces, read the current source rather than treating an author's claim as proof. Record unavailable parsing tools or uninspected dependencies as limitations. No tool invocation or author checklist confers protected acceptance.

For a new story, correct authoring defects within the selected requirements; do not silently change the governing rule to make a discrepancy disappear. If a material product decision is unresolved, record it and its affected work. Report a drafted story with gaps when that is the actual delivered state. A proposed scope reduction or future deferral needs the corresponding user decision.

## Write and read back

Resolve exact paths from intake. Recheck binding if package/binding state changed, selected source identities, reserved IDs and live destination state immediately before a write. Use native tools with literal arguments. For a new story use exclusive creation; if the tool cannot express this, use an available safe terminal file API that can, rather than risk overwrite. Do not follow a symlink/junction into another scope. Create only the selected output directories and files.

Read every delivered file back in full, compare its content to the intended story and repeat relevant source/traceability checks on those actual bytes. Confirm the path, ID, format version, required/conditional content and unresolved decisions. An announced path or successful write return alone is not the completed artifact. Record a content digest when retaining a session record so later resumption can detect changes.

If creation is denied, interrupted, truncated or readback fails, retain the actual known output and report the literal path/error. Do not relocate output, overwrite unrelated files, delete partial work or claim rollback. Determine existing content and ownership before retry. An absent/unread output is not delivered; a partial file remains partial. Do not update upstream links until story delivery is established.

## Related-document updates

Story creation may include ordinary selected epic/sprint linkage when that association and effect are part of the request. A plan-only request or story-only write restriction overrides it. Read the current exact epic/sprint and locate its actual story/coverage/backlog tables. Do not create an epic or sprint, change its goals or reverse-engineer an assignment from sibling files.

Add or update one row keyed by the new story ID with its relative link, outcome/feature mapping, points and planning state, following the current table schema. Preserve other rows, formatting and unrelated content. Recompute derived story/point totals from current rows when the documented schema requires them; do not blindly increment on retry. Keep completed counts unchanged by new Backlog stories. Maintain the selected document's existing change-log convention.

Reread before each edit and stop that edit on drift. Read back the actual changed document to confirm the exact row/link and preserved context. Apply recommendation/RCA planning links under [their source contract](recommendations-and-gaps.md). Do not equate a planning link with a fixed finding, passed test or accepted epic.

Multi-file delivery is not atomic. If a story succeeds and a later link fails, report the story as delivered and the link as pending with the exact target/error. Preserve successful work. Retry only the unfinished idempotent update after inspecting current bytes; never recreate the story to repeat the whole workflow.

## Interruption and partial batches

Use the [session record](../assets/templates/session-record.md) when a batch, interruption or partial update needs durable context. Resolve its external destination before first write, retain actual inputs/identities, current decisions, reserved IDs, delivered files/digests, applied/pending link changes, failures, process ownership and next safe action. Save useful completed state at natural boundaries. Do not manufacture a checkpoint per sentence or claim a measured context percentage.

On resume, read the user-selected session, current request and rules; rerun the binding prerequisite and compare selected inputs/outputs with recorded identities. A checkpoint is editable evidence, not approval or proof that a step happened. Resolve changed requirements or outputs before relying on old mappings. Preserve original decisions and append current corrections. Do not overwrite or rerun a completed operation merely because it is listed in an old plan.

If an owned operation's outcome is uncertain, inspect the same live handle or actual file effects. Do not launch a duplicate solely because observation timed out. Record supplied execution ceilings faithfully; exhausting one leaves incomplete work. Do not invent a universal deadline or raise limits automatically. No background worker is necessary for ordinary authoring; record none when none was started.

## Final report and next consumer

Report literal delivered story paths, IDs and brief outcomes, selected source scope, important inferred defaults, actual related-document changes, content-review observations, and unresolved behavior/dependency/verification obligations. For a batch include all delivered/partial/blocked/omitted members and remaining integration work. An output announced but unwritten must be called unsaved, not delivered.

Separate story authoring/content review from product implementation, executed tests, independent QA, native/visual qualification and protected framework acceptance. State which checks actually occurred and which did not. Checkboxes, model judgments, Python observations and historical evidence cannot authorize a protected transition.

When appropriate, return a concrete manual handoff naming the actual story files, governing source documents and selected implementation or assessment scope. Discover the available consumer before naming an invocation. Do not auto-run development/QA, create a PR, merge, publish, install skills or alter startup configuration. The user's current request can select subsequent work separately; completion of this story-writing workflow does not imply those effects.
