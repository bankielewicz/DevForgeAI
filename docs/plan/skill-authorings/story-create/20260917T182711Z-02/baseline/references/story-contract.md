# Story document contract

## Version and canonical template

The [bundled template](../assets/templates/story-template.md) owns the current story/template version and `SECTION_MANIFEST`. Read its metadata and manifest during assembly; derive required/conditional sections from them rather than keeping another hardcoded list or stale line ranges. Copy only the generated-story portion into the output, not template metadata/instructions. Fill every applicable placeholder and remove illustrative rows/comments. Re-read a changed template before continuing.

Initial `story-create` package, template and story format version are **0.1.0**. This is a new adaptive output contract derived from the former single-file shape. The nested structured technical block retains its own `format_version: "2.0"` vocabulary. Neither stamp asserts compatibility with historical parsers. Existing stories are not migrated automatically.

One story has one complete Markdown file containing its metadata, requirements, technical/UI specification and verification obligations. Referencing a canonical shared specification is permitted and preferred to copying competing clauses. Do not move required story content into notes/spec/API sidecars. External session evidence contains progress and identities, never the only copy of normative story requirements.

## Frontmatter

Use one valid YAML mapping as the generated file's opening frontmatter. Keys are unique and values have the meanings below; quote titles/strings where YAML syntax requires it. Project-defined additional fields may be retained with their documented meaning.

| Fields | Meaning |
| --- | --- |
| `id`, `title`, `type` | Unique selected story identity, outcome and one of feature/bugfix/refactor/documentation |
| `epic`, `sprint`, `status` | Actual selected epic or null; selected sprint or Backlog; new-story status Backlog |
| `points`, `priority`, `depends_on` | Selected/disclosed estimate (or explicit unknown null), priority, and array of resolved story-ID dependencies |
| `assigned_to`, `created`, `format_version` | Owner or Unassigned, creation date and current story format from template metadata |
| `advisory`, `source_gap`, `source_story` | Whether a source finding is nonblocking, its actual gap ID if applicable, and actual source story; missing facts remain null |
| `from_recommendations`, `source_recommendations`, `cycle_recorded` | Recommendation origin, exact selected IDs and actual source cycle when applicable |
| `feature_ref`, `source_devarch` | Source architecture feature and project-relative document path; empty strings when inapplicable |
| `branch`, `pr_base`, `worktree_path`, `pr_number`, `pr_url`, `pr_merged`, `merged_sha`, `merged_at` | Reserved delivery facts; initialize to null/false, not a proposed branch, fabricated PR or performed merge |

Conditional RCA frontmatter preserves `source_rca`, `source_recommendation`, `rca_addresses_why` and `rca_evidence_files` as described in [recommendations and gaps](recommendations-and-gaps.md). A recommendation-only advisory story has no fabricated `source_gap`. `source_devarch` never stores a QA report. Dates, counters, booleans and arrays have their intended types; do not encode booleans as misleading strings.

## Body semantics

Description contains the actor/outcome/value, explicit scope/exclusions and observable deliverables. Provenance records actual source decisions and clause ownership. XML origins can use `document`/`section`, exact `quote`, verified `line_reference`, supported `quantified_impact`, optional `decision`, `stakeholder` and `hypothesis` elements. Unknown optional details are omitted; source claims are not fabricated to meet a count. For a direct request, a concrete request/decision record is adequate provenance.

Acceptance Criteria uses the XML form and IDs in [acceptance criteria](acceptance-criteria.md). Technical Specification follows [technical detail](technical-specification.md); applicable UI and implementation guidance follow their conditional template entries. Document relevant NFR categories, including Performance, Security, Scalability, Reliability and Observability, with explicit non-applicability reasons where appropriate. Additional grounded categories are allowed.

Dependencies identifies prerequisite stories, external dependencies and technology dependencies, each with required artifact/decision, owner and satisfaction observation. Test Strategy gives meaningful unit/document, integration and conditional end-to-end/platform cases. The AC Verification Checklist is a planned traceability table/list with unchecked results; it cannot replace actual future evidence. Edge Cases identifies denied/invalid/recovery behavior, including its AC or test mapping.

DoD contains concrete unchecked implementation, quality, testing and documentation outcomes. TDD Workflow Summary states planned obligations or accurate documentation-only non-applicability. Files Created/Modified lists intended product paths, clearly marked planned; story-authoring delivery is recorded in Change Log/Notes. New story creation does not tick future product completion items.

Notes owns unresolved questions (question, owner, affected clauses and effect on readiness), estimates/assumptions, UI non-applicability, review observations and a manual next action. `Backlog` does not resolve these questions. Do not call a story implementation-ready while an essential behavior, authority, interface or dependency decision remains unresolved.

## Consumer boundary

The current development and QA responsibilities accept explicitly selected specifications/stories and governing references. Return this artifact and scope as a manual handoff; a consumer must still inspect its own current contract and candidate. This authoring contract does not guarantee compatibility with an uninspected parser, mark independent QA passed, advance a protected phase or authorize deployment.
