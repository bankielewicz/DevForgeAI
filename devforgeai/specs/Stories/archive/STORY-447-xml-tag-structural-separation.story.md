---
id: STORY-447
title: "Introduce XML Tag Structural Separation"
epic: EPIC-069
status: QA Approved
priority: High
points: 8
type: documentation
created: 2026-02-18
sprint: Sprint-2
---

# STORY-447: Introduce XML Tag Structural Separation

## Description

Introduce XML tags for instruction structure, phase handoffs, and multi-source context per Anthropic `use-xml-tags.md`. Addresses findings 5.3 (FAIL, High), 3.2 (PARTIAL, Medium), 6.3 (PARTIAL, Medium), 8.3 (PARTIAL, Low). Currently all structure uses markdown headers only. XML tags improve Claude's parsing of instruction boundaries and reduce ambiguity in multi-source context assembly.

## Business Value

Improves Claude's ability to parse instruction boundaries, reducing misinterpretation of phase transitions and context handoffs. Directly addresses 4 conformance findings from the Anthropic best-practices audit.

<acceptance_criteria>

### AC#1: SKILL.md Key Sections Wrapped in Semantic XML Tags
- SKILL.md key sections wrapped in semantic XML tags (`<instructions>`, `<context>`, `<output_format>`)
- Tags applied to discovering-requirements SKILL.md as the pilot skill
- Existing markdown content preserved inside XML wrappers

### AC#2: Phase Transition XML Handoff Schemas
- Phase transitions use `<phase-N-output>` XML handoff schemas defining data passed between phases
- Each phase documents its output schema in XML format
- Downstream phases reference the upstream output schema

### AC#3: Command-to-Skill Handoff Uses XML Tags
- Command-to-skill handoff replaces `**Business Idea:**` markdown markers with `<ideation-context>` XML tags
- XML tags contain `<business-idea>`, `<brainstorm-id>`, `<project-mode>` elements
- ideate.md updated to emit XML context markers

### AC#4: Skill Detection Logic Parses XML Tags
- Skill Phase 1 Step 0 detection logic updated to parse XML tags instead of markdown bold matching
- Backward compatibility: skill still detects legacy markdown markers with deprecation warning

### AC#5: Multi-Source Inputs Use XML Wrappers
- Multi-source inputs wrapped in `<brainstorm_context>`, `<user_input>`, `<project_context>` XML tags
- Each source clearly delineated for Claude's parsing

### AC#6: SKILL.md Line Count Constraint
- SKILL.md remains under 500 lines after XML additions
- Any content exceeding budget extracted to reference files

### AC#7: Round-Trip Handoff Test
- Round-trip handoff test: command sets XML context markers, skill correctly parses them
- Test covers: brainstorm mode, fresh mode, and project mode handoffs

</acceptance_criteria>

## Technical Specification

### Files to Modify
- `src/claude/skills/discovering-requirements/SKILL.md` — Add XML tag wrappers around key sections, update detection logic
- `src/claude/commands/ideate.md` — Replace markdown context markers with XML tags
- `src/claude/skills/discovering-requirements/references/discovery-workflow.md` — Add phase output XML schemas
- `src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md` (if exists) — Update for XML context parsing

### Approach
1. Identify all structural boundaries in SKILL.md (instructions, context, output format)
2. Wrap each boundary in semantic XML tags without changing content
3. Define `<phase-N-output>` schemas for each phase transition
4. Update ideate.md to emit `<ideation-context>` XML instead of markdown bold markers
5. Update skill Phase 1 detection to parse XML tags with markdown fallback
6. Verify line count stays under 500

### Risk
XML tag changes break context marker detection. Mitigate by updating command AND skill simultaneously and maintaining backward-compatible markdown fallback.

## Definition of Done

- [x] XML tags present in SKILL.md (`<instructions>`, `<context>`, `<output_format>`)
- [x] Phase handoff schemas defined with `<phase-N-output>` tags
- [x] ideate.md emits `<ideation-context>` XML markers
- [x] Skill detection logic parses XML tags with markdown fallback
- [x] Multi-source XML wrappers in place
- [x] SKILL.md under 500 lines
- [x] Round-trip handoff verified manually

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] XML tags present in SKILL.md (`<instructions>`, `<context>`, `<output_format>`) - Completed: Wrapped Your Role in `<instructions>`, Purpose/When to Use in `<context>`, Reference Files in `<output_format>`
- [x] Phase handoff schemas defined with `<phase-N-output>` tags - Completed: Added `<phase-1-output>` through `<phase-4-output>` schemas after each phase heading
- [x] ideate.md emits `<ideation-context>` XML markers - Completed: Replaced markdown bold markers with `<ideation-context>` containing `<business-idea>`, `<brainstorm-id>`, `<project-mode>` elements
- [x] Skill detection logic parses XML tags with markdown fallback - Completed: Updated Phase 1 Step 0 to parse XML first, fall back to deprecated markdown markers with warning
- [x] Multi-source XML wrappers in place - Completed: Added `<brainstorm_context>`, `<user_input>`, `<project_context>` wrappers in brainstorm handoff section
- [x] SKILL.md under 500 lines - Completed: SKILL.md at 400 lines (well under 500 limit)
- [x] Round-trip handoff verified manually - Completed: 31/31 tests pass including brainstorm, fresh, and project mode handoffs

<!-- IMPORTANT: When completing DoD items, list them as a FLAT list directly under
     this section. Do NOT place them under ### subsections. The extract_section()
     validator stops at the first ### header.
     Reference: .claude/skills/implementing-stories/references/dod-update-workflow.md -->

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 31 tests written, 25 FAIL / 6 PASS |
| Green | ✅ Complete | All 31 tests PASS |
| Refactor | ✅ Complete | No refactoring needed |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/SKILL.md | Modified | 344 → 400 |
| src/claude/commands/ideate.md | Modified | 571 → 575 |
| tests/STORY-447/test-xml-tag-structural-separation.sh | Created | 179 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| YYYY-MM-DD HH:MM | .claude/story-requirements-analyst | Created | Story created | STORY-XXX.story.md |
| 2026-02-18 | .claude/qa-result-interpreter | QA Deep | PASSED: 31/31 tests, 0 violations, 100% traceability | STORY-447-qa-report.md |

---

## Notes
