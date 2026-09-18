# Template Upgrade Snippet Library

**Purpose:** Literal text bodies inserted by procedures in `template-upgrade-procedures.md`. Each snippet is delimited by the canonical markers `<!-- SNIPPET: {key} -->` and `<!-- END_SNIPPET -->` for programmatic extraction.

**Read by:** `read_snippet(key)` helper defined in `template-upgrade-procedures.md`. The helper reads this file, locates the marker pair for the requested key, and returns the body text between the markers (exclusive of marker lines).

**Convention:** snippet bodies are inserted verbatim into target story files by the fix procedures. They contain placeholder text in parentheses (e.g., `(populate from brainstorm source)`) signaling content that requires manual completion. The accompanying `AUDIT-DEFERRED` marker inserted by P1 makes this explicit.

---

<!-- SNIPPET: provenance_scaffold -->
```xml
<provenance>
  <!-- Origin: link to source brainstorm or epic with quoted evidence -->
  <origin document="UNKNOWN" section="unknown">
    <quote>(populate from brainstorm/epic source)</quote>
    <line_reference>(populate)</line_reference>
    <quantified_impact>(populate)</quantified_impact>
  </origin>
</provenance>
```
<!-- END_SNIPPET -->

---

<!-- SNIPPET: implementation_guide_scaffold -->
### Architecture Decisions

(Populate with key architectural decisions affecting this story.)

### Cross-Cutting Concerns

(Populate with concerns spanning multiple ACs — logging, auth, error handling.)

### Implementation Sequence

(Populate with recommended order of AC implementation.)

### Task Prompt Templates

(Populate with subagent task prompt templates if applicable.)

### Anti-Patterns

(Populate with anti-patterns specific to this story's implementation.)

### Patterns and References

(Populate with patterns and reference materials.)
<!-- END_SNIPPET -->

---

<!-- SNIPPET: technical_limitations_scaffold -->
```yaml
limitations:
  - id: TL-001
    title: (populate)
    severity: (low|medium|high)
    description: (populate)
    decision: (documented|pending|deferred)
    decision_reference: (ADR-NNN or N/A)
```
<!-- END_SNIPPET -->

---

<!-- SNIPPET: change_log_table_header -->
**Current Status:** (preserved from frontmatter)

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
<!-- END_SNIPPET -->

---

<!-- SNIPPET: ac_verification_checklist_scaffold -->
**Real-time AC progress tracker. Update sub-items as TDD phases complete.**

- [ ] AC#1: (mirror AC#1 header text)
  - [ ] Red phase: failing test written
  - [ ] Green phase: implementation passing test
  - [ ] Refactor phase: code cleaned
- [ ] AC#2: (mirror AC#2 header text)
  - [ ] Red phase: failing test written
  - [ ] Green phase: implementation passing test
  - [ ] Refactor phase: code cleaned

(Replicate the AC#N: pattern for each AC in this story.)
<!-- END_SNIPPET -->

---

<!-- SNIPPET: edge_cases_scaffold -->
(Document edge cases discovered during implementation. Examples: null inputs, empty collections, concurrent access, network failures.)
<!-- END_SNIPPET -->

---

<!-- SNIPPET: notes_scaffold -->
(General notes, design decisions, or context not captured elsewhere.)
<!-- END_SNIPPET -->

---

<!-- SNIPPET: generic_section_scaffold -->
(Section auto-added by /fix-story --upgrade. Populate with content matching the canonical template's structure for this section. See src/claude/skills/spec-driven-stories/assets/templates/story-template.md for the canonical layout of every Required and Conditional section.)
<!-- END_SNIPPET -->

---

## Verification

To audit snippet pairing:

```bash
grep -c '<!-- SNIPPET:' src/claude/skills/spec-driven-remediation/assets/templates/template-upgrade-snippets.md
grep -c '<!-- END_SNIPPET -->' src/claude/skills/spec-driven-remediation/assets/templates/template-upgrade-snippets.md
```

Both counts must be equal and `>= 8` (7 named keys + 1 generic fallback).
