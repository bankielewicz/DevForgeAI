---
# QA Recommendations Template Metadata
template_version: "1.0"
last_updated: "2026-04-14"
format_version: "1.0"
template_purpose: "AI-optimized spec for post-QA recommendations consumed by /dev remediation cycles"
---

<!-- SECTION_MANIFEST
last_verified: "2026-04-14"
sections:
  - name: "Summary"
    header_level: 2
    status: "Required"
    validation:
      required_fields: ["story_id", "qa_result", "cycle_number", "total_count", "by_severity"]
      enforcement: "halt"
  - name: "Blocking Recommendations"
    header_level: 2
    status: "Required"
    validation:
      allowed_severities: ["CRITICAL", "HIGH"]
      entry_schema: "recommendation_entry"
      empty_allowed: true
      enforcement: "halt"
  - name: "Advisory Recommendations"
    header_level: 2
    status: "Required"
    validation:
      allowed_severities: ["MEDIUM", "LOW"]
      entry_schema: "recommendation_entry"
      empty_allowed: true
      enforcement: "halt"
  - name: "Deferred Recommendations"
    header_level: 2
    status: "Required"
    validation:
      required_per_entry: ["deferral_marker", "user_approval_ref"]
      empty_allowed: true
      enforcement: "halt"
  - name: "Verification Plan"
    header_level: 2
    status: "Required"
    validation:
      required_per_entry: ["rec_id", "command", "expected"]
      cross_reference: "every rec_id in Blocking + Advisory must appear"
      enforcement: "halt"
  - name: "Cycle History"
    header_level: 2
    status: "Required"
    validation:
      append_only: true
      required_fields: ["cycle", "started", "completed_or_null", "rec_ids_attempted", "rec_ids_closed"]
      enforcement: "halt"
  - name: "Provenance"
    header_level: 2
    status: "Required"
    validation:
      required_fields: ["qa_phase_source", "classification_per_rec"]
      enum: ["GROUNDED", "DERIVED", "INCONCLUSIVE"]
      enforcement: "halt"

# Anti-ambiguity validators run automatically on generated files:
#   - detect-aspirational-language: blocks "should", "might", "could", "probably", "approximately" in non-quoted prose
#   - detect-ambiguous-qualifiers: blocks "good", "clean", "proper", "appropriate", "reasonable", "maintainable"
#   - detect-stub-references: blocks "TODO", "TBD", "see above", "as appropriate"
# Exit 1 on any hit. Template authors MUST populate concrete values or use deferred section.

# Recommendation entry YAML schema — used by Blocking and Advisory sections:
#   required:
#     - id (format: REC-{STORY}-{severity-initial}-{3-digit-seq})
#     - severity (enum: CRITICAL, HIGH, MEDIUM, LOW)
#     - provenance (enum: GROUNDED, DERIVED, INCONCLUSIVE)
#     - title (string, 10-120 chars, no aspirational language)
#     - file (relative path from project root)
#     - line (integer) OR line_range ([start, end] integers)
#     - category (enum: correctness, security, performance, test_quality, coverage, anti_pattern, documentation)
#     - blocking_release (boolean; true for CRITICAL/HIGH, false for MEDIUM/LOW by default)
#     - remediation (exactly one of: before_code+after_code pair OR remediation_steps list)
#     - verification ({command: string, expected: string})
#     - estimated_effort_minutes (integer)
#     - dependencies (list of REC-IDs; may be empty)
#   optional:
#     - references (list of {source: string, line_range?: [int, int], url?: string})
#     - cycle_first_seen (integer; auto-populated by /qa)
#     - classification (enum: REGRESSION, PRE_EXISTING; for anti_pattern category only)
END_SECTION_MANIFEST -->

# QA Recommendations: {{STORY_ID}}

> **This file is AI-optimized.** Consumed by `/dev STORY-XXX --fix` to drive targeted remediation cycles. Human prose lives in `devforgeai/qa/reports/{{STORY_ID}}-qa-report.md`. CI-consumable JSON lives in `devforgeai/qa/reports/{{STORY_ID}}-gaps.json`. This file is the third artifact — structured Markdown + YAML for downstream Claude sessions.
>
> **Fidelity contract:** every recommendation MUST include concrete file paths, line numbers, exact remediation (code-block diff or numbered steps), measurable verification command, and GROUNDED or DERIVED provenance. The template validator (`devforgeai-validate validate-qa-recommendations`) refuses to emit this file with any field missing or containing aspirational/ambiguous language.

---

## Summary

| Field | Value |
|-------|-------|
| Story ID | `{{STORY_ID}}` |
| QA Result | `{{QA_RESULT}}` <!-- enum: PASSED, PASS_WITH_WARNINGS, FAILED --> |
| Cycle Number | `{{CYCLE_NUMBER}}` <!-- integer; 1 for initial QA; increments per re-QA after remediation --> |
| Generated At | `{{TIMESTAMP_ISO8601}}` |
| Total Recommendations | `{{TOTAL_COUNT}}` |
| Blocking Release | `{{BLOCKING_COUNT}}` <!-- count of entries with blocking_release: true --> |
| By Severity | CRITICAL: `{{CRITICAL_COUNT}}`, HIGH: `{{HIGH_COUNT}}`, MEDIUM: `{{MEDIUM_COUNT}}`, LOW: `{{LOW_COUNT}}` |
| Open (unresolved) | `{{OPEN_COUNT}}` |
| Closed in prior cycles | `{{CLOSED_COUNT}}` |

---

## Blocking Recommendations

<!-- Entries here MUST have severity CRITICAL or HIGH. These block release per quality-gates.md Gate 3.
     If no CRITICAL/HIGH findings exist for this story, this section contains the literal text "_None._" —
     NEVER omit the section entirely. The validator requires the section to be present. -->

{{#each BLOCKING_RECOMMENDATIONS}}
### {{this.id}} — {{this.title}}

```yaml
- id: "{{this.id}}"
  severity: {{this.severity}}
  provenance: {{this.provenance}}
  title: "{{this.title}}"
  file: "{{this.file}}"
  line: {{this.line}}                         # integer; OR use line_range: [start, end]
  category: {{this.category}}
  blocking_release: {{this.blocking_release}}
  before_code: |
{{indent this.before_code 4}}
  after_code: |
{{indent this.after_code 4}}
  remediation_steps: null                     # null when using before_code/after_code pair
  verification:
    command: "{{this.verification.command}}"
    expected: "{{this.verification.expected}}"
  estimated_effort_minutes: {{this.estimated_effort_minutes}}
  dependencies: {{this.dependencies}}         # e.g. ["REC-STORY-646-H-002"] or []
  references:
{{#each this.references}}
    - source: "{{this.source}}"
{{#if this.line_range}}      line_range: {{this.line_range}}{{/if}}
{{#if this.url}}      url: "{{this.url}}"{{/if}}
{{/each}}
  cycle_first_seen: {{this.cycle_first_seen}}
```

{{/each}}

{{#if BLOCKING_EMPTY}}
_None._
{{/if}}

---

## Advisory Recommendations

<!-- Entries here MUST have severity MEDIUM or LOW. These do NOT block release but are tracked
     and addressed in remediation cycles. Same schema as Blocking. If empty, section contains "_None._". -->

{{#each ADVISORY_RECOMMENDATIONS}}
### {{this.id}} — {{this.title}}

```yaml
- id: "{{this.id}}"
  severity: {{this.severity}}
  provenance: {{this.provenance}}
  title: "{{this.title}}"
  file: "{{this.file}}"
  line: {{this.line}}
  category: {{this.category}}
  blocking_release: false
  {{#if this.before_code}}
  before_code: |
{{indent this.before_code 4}}
  after_code: |
{{indent this.after_code 4}}
  remediation_steps: null
  {{else}}
  before_code: null
  after_code: null
  remediation_steps:
{{#each this.remediation_steps}}
    - "{{this}}"
{{/each}}
  {{/if}}
  verification:
    command: "{{this.verification.command}}"
    expected: "{{this.verification.expected}}"
  estimated_effort_minutes: {{this.estimated_effort_minutes}}
  dependencies: {{this.dependencies}}
  references:
{{#each this.references}}
    - source: "{{this.source}}"
{{#if this.line_range}}      line_range: {{this.line_range}}{{/if}}
{{/each}}
  cycle_first_seen: {{this.cycle_first_seen}}
```

{{/each}}

{{#if ADVISORY_EMPTY}}
_None._
{{/if}}

---

## Deferred Recommendations

<!-- Recommendations the user explicitly deferred. Each MUST include a deferral_marker
     (from quality-gates.md Gate 3 approval protocol) and a user_approval_ref. Deferral of
     CRITICAL/HIGH requires a linked ADR. Deferral of MEDIUM/LOW requires user approval marker only. -->

{{#each DEFERRED_RECOMMENDATIONS}}
### {{this.id}} — {{this.title}} (deferred in cycle {{this.deferred_in_cycle}})

```yaml
- id: "{{this.id}}"
  severity: {{this.severity}}
  deferral_marker: "<!-- AUDIT-DEFERRED: {{this.id}} -->"
  user_approval_ref: "{{this.user_approval_ref}}"  # e.g. "session SC-2026-04-15-002, turn 47"
  adr_ref: "{{this.adr_ref}}"                      # required for CRITICAL/HIGH deferrals; null for MEDIUM/LOW
  justification: "{{this.justification}}"          # one-sentence concrete reason (validator rejects aspirational text)
  deferred_in_cycle: {{this.deferred_in_cycle}}
  revisit_by: "{{this.revisit_by}}"                # sprint or date; null if indefinite
```

{{/each}}

{{#if DEFERRED_EMPTY}}
_None._
{{/if}}

---

## Verification Plan

<!-- Every rec_id from Blocking + Advisory MUST appear here with a concrete command + expected result.
     This is what /dev Phase 02 (Red) converts into test cases. Cross-reference validator enforces
     that every recommendation has a verification entry. -->

| REC-ID | Command | Expected Output |
|--------|---------|-----------------|
{{#each VERIFICATION_ENTRIES}}
| `{{this.rec_id}}` | `{{this.command}}` | `{{this.expected}}` |
{{/each}}

---

## Cycle History

<!-- Append-only log. Each /dev remediation cycle appends an entry. /qa re-runs do NOT modify
     prior cycle entries; they only add new open recommendations to Blocking/Advisory and append
     a new cycle entry (for the /qa run itself, marked source: "qa-validation"). -->

{{#each CYCLE_HISTORY}}
### Cycle {{this.cycle}} — {{this.source}}

- **Started:** `{{this.started}}`
- **Completed:** `{{this.completed_or_null}}`
- **Source:** `{{this.source}}` <!-- enum: initial-qa, qa-validation, remediation-cycle -->
- **Trigger:** `{{this.trigger}}` <!-- e.g. "/qa STORY-646" or "/dev STORY-646 --fix" -->
- **Recommendations attempted:** {{this.rec_ids_attempted}}
- **Recommendations closed:** {{this.rec_ids_closed}}
- **Recommendations deferred:** {{this.rec_ids_deferred}}
- **New recommendations surfaced:** {{this.rec_ids_new}}
- **Notes:** {{this.notes}}

{{/each}}

---

## Provenance

<!-- Every recommendation in Blocking + Advisory sections MUST be classified per
     .claude/rules/core/epistemic-integrity.md. Classification rules:
       GROUNDED — backed by file content, test output, or direct citation from context file
       DERIVED — inferred from heuristics or cross-reference; requires one-sentence justification
       INCONCLUSIVE — evidence insufficient; flagged for manual review

     Aggregate provenance counts across Blocking + Advisory sections: -->

| Provenance | Count |
|------------|-------|
| GROUNDED | `{{GROUNDED_COUNT}}` |
| DERIVED | `{{DERIVED_COUNT}}` |
| INCONCLUSIVE | `{{INCONCLUSIVE_COUNT}}` |

**QA phase sources:**

| Recommendation | QA Phase |
|----------------|----------|
{{#each PROVENANCE_ENTRIES}}
| `{{this.rec_id}}` | {{this.qa_phase}} <!-- enum: Phase-02-Test-Quality, Phase-03-Coverage, Phase-04-Code-Review, Phase-05-Reporting --> |
{{/each}}

**DERIVED justifications:** <!-- one sentence per DERIVED finding, per epistemic-integrity.md -->

{{#each DERIVED_JUSTIFICATIONS}}
- `{{this.rec_id}}`: {{this.justification}}
{{/each}}

**INCONCLUSIVE reasons:** <!-- one sentence per INCONCLUSIVE finding explaining evidence gap -->

{{#each INCONCLUSIVE_REASONS}}
- `{{this.rec_id}}`: {{this.reason}}
{{/each}}

---

<!--
  Template authoring notes (not rendered — for humans updating the template):

  1. Every {{placeholder}} is consumed by the /qa Phase 05 Step 5.6 generator.
  2. The validator (devforgeai-validate validate-qa-recommendations STORY-XXX) enforces:
     - SECTION_MANIFEST integrity (every Required section present)
     - Every recommendation entry has all required schema fields populated (no null for required)
     - Every verification entry cross-references an existing REC-ID
     - Ambiguity scanners (detect-aspirational-language, detect-ambiguous-qualifiers,
       detect-stub-references) return zero hits in non-code sections
     - Deferred entries have user_approval_ref populated
     - Deferred CRITICAL/HIGH entries have adr_ref populated
  3. Exit codes: 0 = valid; 1 = validation failure (HALT recommended); 2 = IO error.
  4. Downstream /dev Phase 01 Step 1.9.6 consumes this file via qa-recommendations-preflight
     CLI and spawns a remediation cycle if open_count > 0.
  5. Multi-cycle pattern: on /qa re-run after remediation, append new Cycle History entry and
     any newly-surfaced recommendations to Blocking/Advisory. Previously-closed recommendations
     remain in Cycle History.rec_ids_closed but are NOT re-listed in Blocking/Advisory.
  6. This template intentionally mirrors story-template.md's SECTION_MANIFEST pattern (ADR-047
     schema-authority contract) so the same tooling (parse-manifest, section-presence checks)
     applies. ADR-048 drift protections apply identically.

  Anti-patterns forbidden in generated files (validator-enforced):
    - Aspirational: "should improve", "consider refactoring", "could be cleaner"
    - Ambiguous: "better handling", "more robust", "appropriate validation"
    - Unquantified: "approximately 500ms" (must cite baseline), "several files", "a few tests"
    - Stub: "TBD", "TODO", "see above", "as appropriate"
    - Missing evidence: DERIVED claim without a one-sentence justification
-->
