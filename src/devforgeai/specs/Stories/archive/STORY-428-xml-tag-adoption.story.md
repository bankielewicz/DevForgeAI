---
id: STORY-428
title: "Adopt XML Tags for Instruction Structure and Context Handoffs"
type: feature
epic: EPIC-067
sprint: Sprint-2
status: Deferred
points: 5
depends_on: ["STORY-427"]
priority: High
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Adopt XML Tags for Instruction Structure and Context Handoffs

## Description

**As a** DevForgeAI framework maintainer,
**I want** to introduce XML tags for instruction structure, context markers, and inter-phase handoffs,
**so that** Claude can parse prompts more accurately and the command-skill handoff becomes reliable as recommended by Anthropic's prompt engineering guidance.

**Context:** This story addresses conformance analysis findings 5.1 (High), 5.2 (Medium), 7.1 (Medium), and 9.3 (Medium). The skill and command currently use markdown formatting (bold, code fences) where XML tags would improve parsing reliability and data separation.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Categories 5, 7, 9

## Acceptance Criteria

### AC#1: Execution Model Wrapped in XML Tags

```xml
<acceptance_criteria id="AC1" implements="FINDING-5.1">
  <given>SKILL.md Execution Model section uses markdown formatting</given>
  <when>XML tags are introduced</when>
  <then>The execution model is wrapped in &lt;execution-model&gt; tags, providing stronger parsing signal to Claude</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-428/test_ac1_execution_model_xml.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Context Markers Use XML Tags

```xml
<acceptance_criteria id="AC2" implements="FINDING-5.2,FINDING-9.3">
  <given>Command uses markdown bold for context markers (e.g., **Business Idea:**)</given>
  <when>Context markers are converted to XML</when>
  <then>Command emits &lt;ideation-context&gt; XML block with child elements (business-idea, brainstorm-id, project-mode); skill detects and parses these XML tags instead of markdown patterns</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/ideate.md</file>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-428/test_ac2_context_markers_xml.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase Output Handoff Tags Added

```xml
<acceptance_criteria id="AC3" implements="FINDING-7.1">
  <given>Phase handoffs rely on implicit session state variables</given>
  <when>Structured handoff tags are introduced</when>
  <then>Each phase workflow reference file ends with &lt;phase-N-output&gt; XML structure documenting the data passed to the next phase; next phase workflow file references these tags</then>
  <verification>
    <source_files>
      <file hint="Discovery workflow">.claude/skills/devforgeai-ideation/references/discovery-workflow.md</file>
      <file hint="Requirements workflow">.claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-428/test_ac3_phase_handoff_xml.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Skill Context Detection Updated

```xml
<acceptance_criteria id="AC4">
  <given>SKILL.md Phase 1 Step 0 detects context via markdown pattern matching</given>
  <when>Context detection is updated for XML</when>
  <then>Phase 1 Step 0 detects &lt;ideation-context&gt; XML tags; extract_xml() or similar function parses child elements; markdown fallback remains for backward compatibility</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-428/test_ac4_context_detection.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "XML Tag Schema"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      required_keys:
        - key: "execution-model"
          type: "xml"
          example: "<execution-model>...</execution-model>"
          required: true
          test_requirement: "Test: SKILL.md contains <execution-model> tags"
        - key: "ideation-context"
          type: "xml"
          example: "<ideation-context><business-idea>text</business-idea></ideation-context>"
          required: true
          test_requirement: "Test: Command contains <ideation-context> structure"
        - key: "phase-output"
          type: "xml"
          example: "<phase-1-output><problem-statement>...</problem-statement></phase-1-output>"
          required: true
          test_requirement: "Test: Phase workflow files contain phase-N-output tags"

  business_rules:
    - id: "BR-001"
      rule: "Context markers must use XML tags for reliable parsing"
      trigger: "Command-to-skill handoff"
      validation: "Command emits <ideation-context>, skill parses <ideation-context>"
      error_handling: "Skill falls back to markdown detection if XML not found"
      test_requirement: "Test: Both command and skill use ideation-context tags"
      priority: "Critical"

    - id: "BR-002"
      rule: "Phase handoffs use structured XML output tags"
      trigger: "Phase transitions"
      validation: "Each phase emits <phase-N-output>, next phase references it"
      error_handling: "Log warning if phase output not found"
      test_requirement: "Test: Phase workflow files contain output/input references"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "XML parsing more reliable than markdown pattern matching"
      metric: "Zero false positives in context detection"
      test_requirement: "Test: Context detection succeeds with user text containing **bold**"
      priority: "High"
```

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-427:** Command-Skill Separation (must complete first to reduce command size before adding XML)

---

## Definition of Done

### Implementation
- [ ] SKILL.md execution model wrapped in <execution-model> tags
- [ ] ideate.md emits <ideation-context> XML block
- [ ] <ideation-context> contains business-idea, brainstorm-id, project-mode elements
- [ ] SKILL.md Phase 1 Step 0 updated to parse XML context
- [ ] Markdown fallback preserved for backward compatibility
- [ ] discovery-workflow.md emits <phase-1-output> at end
- [ ] requirements-elicitation-workflow.md references <phase-1-output>
- [ ] At least Phases 1-3 have structured output/input tags

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] No regression in context detection
- [ ] XML tags properly nested and closed

### Testing
- [ ] Test: <execution-model> tags in SKILL.md
- [ ] Test: <ideation-context> in command and skill
- [ ] Test: Phase handoff tags in workflow files
- [ ] Test: Context detection works with XML format

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 2 | STORY-428.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). Target files (SKILL.md, ideate.md, reference files) will be restructured and moved — re-evaluate after EPIC-068 Sprint 3. | STORY-428.story.md |

## Notes

**Anthropic Reference:**
- XML tags: `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/use-xml-tags.md`
- Quote: "XML tags help Claude parse your prompts more accurately, leading to higher-quality outputs"

**Risk Mitigation:** Update BOTH command and skill simultaneously to ensure XML emission matches XML detection. Test with `/ideate test idea` after each change.

**Backward Compatibility:** Markdown fallback ensures existing brainstorm documents still work during transition period.

---

Story Template Version: 2.9
Last Updated: 2026-02-17
