# Recommendations, RCA and deferred work

## Select and read the original entries

Require the selected recommendation/finding document, its source story or incident when applicable, and either explicit entry IDs or an explicit request covering all eligible entries. Resolve an ID to exactly one current artifact. Read the full entries, current cycle/status and related evidence; do not reconstruct them from an earlier conversation or a report summary.

For historical QA recommendation input, preserve these fields: `id`, `severity`, `provenance`, `title`, `file`, `category`, `estimated_effort_minutes`, `verification.command`, `verification.expected`; remediation is exactly one of a complete `before_code`/`after_code` pair or a nonempty `remediation_steps` list. Missing values or placeholders such as TODO, TBD, various, an empty string or an unsupported N/A are unresolved inputs. Report the entry and field before creating its dependent story. Do not invent a verification command, estimate or expected result to satisfy the shape.

For a different current QA/RCA schema, inspect its actual field definitions and make an explicit equivalent mapping: stable identity, observed problem/evidence, source revision/cycle, remediation intent, acceptance expectation and verification obligation. The historical field vocabulary is not a requirement to rewrite a current producer. Preserve any unmapped required content and report the gap rather than dropping it.

Recognize open versus already linked/closed entries using the actual producer's contract. By default, blocking Critical/High findings stay in the current repair cycle; do not silently defer them into advisory backlog work. An explicit request can select a follow-up story for them, but cannot make the unresolved blocking finding pass. Report every requested unknown, duplicate, closed or filtered ID. Do not silently process only an intersection of a requested set. An empty eligible set produces an explanation and no story.

## Map without changing meaning

For each selected recommendation retain its exact ID, source location, cycle/revision, severity, title, affected files, evidence, verification command and expected result. Preserve before/after code or remediation steps as source data, quoting them with appropriate Markdown/XML escaping. Read supplied commands as data: do not execute them during story authoring. If they name an unavailable or superseded tool, retain the original in provenance and record the unresolved replacement/verification obligation rather than promising it works.

Each recommendation in a coherent bundle maps to a distinct AC with its expected result preserved; show the REC-to-AC mapping. A recommendation with several independently testable outcomes can have multiple ACs, but none may disappear. Group by independently assessable outcome using [batch and dependencies](batch-and-dependencies.md), not merely because entries share a file or came from one run. Review remedies against governing product rules; conflicting remedies require resolution, not silent instruction following.

Priority follows the highest selected severity unless current project policy says otherwise. Medium/Low-only follow-up work may be `advisory: true` when the producer actually marks it nonblocking. Severity alone cannot overrule an explicit blocking flag. Use a disclosed scope estimate under project rules; optional historical effort-to-points hints are <=15/30/60/120/240 minutes to 1/2/3/5/8 points, otherwise 13. This is a planning heuristic, not an elapsed-time promise or a reason to downgrade an explicit estimate.

Do not force `refactor`: use `bugfix` for incorrect behavior, `refactor` for preservation-focused restructuring, `documentation` for prose-only work and `feature` for a new capability. Story type grants no test exemption.

## Provenance and source-specific fields

For QA follow-ups, populate `from_recommendations`, `source_recommendations`, `cycle_recorded` and `source_story` when the source provides them. Cite the recommendations file and selected entries in Provenance. Reserve `source_devarch` for an actual architecture document. Set `source_gap` only for a real gap ID; a recommendation-only advisory story need not invent a gap.

For an RCA recommendation, preserve the existing conditional frontmatter fields `source_rca`, `source_recommendation`, `rca_addresses_why` and `rca_evidence_files`. Evidence paths and the 5-Whys link must be supported by the RCA. Render the supplied `test_specification` table and `conditional` trigger in Provenance. A conditional recommendation becomes conditional story scope with its triggering observation; do not erase or assume the condition, or put a non-story trigger into `depends_on`.

For RCA-origin stories include `<rca_origin rca_id="..." recommendation_id="..." conditional="...">` inside `<provenance>`, with supported `addresses_why`, `evidence_files` containing `file` elements, `test_specification`, and a `condition` when applicable. Preserve exact source text with valid XML escaping/CDATA. Keep frontmatter, rendered evidence and the actual source consistent; do not fabricate a missing required RCA field.

For coverage/deferred-DoD gaps, retain source story/epic, exact uncovered clause or obligation, finding/gap ID, reason for deferral, blocking status and proposed verification. Creating a tracking story neither satisfies the original obligation nor authorizes descope. Verify claimed gaps against current files before duplicating existing work.

## Linked source records

After story readback, apply only source-link updates within the selected effects. Reread the source immediately before editing and preserve unrelated entries. Use an existing planning-link field with its documented meaning. If its name suggests implementation (for example `implemented_in`), inspect the producer contract: do not populate it when that would falsely mark a fix complete. Otherwise add a clear planned-story reference in the existing notes/link section, or report a pending update if the format has no suitable field.

Keep open findings open until their actual consumer establishes closure. Duplicate links are not added on resume. If a source edit fails, report the written story and pending source link separately. Do not regenerate QA/RCA results, run repairs or alter recommendation evidence in this authoring workflow.
