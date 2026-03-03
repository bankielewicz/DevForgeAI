---
id: STORY-425
title: "Add Role Prompting and Multishot Examples to devforgeai-ideation Skill"
type: feature
epic: EPIC-067
sprint: Sprint-1
status: Deferred
points: 5
depends_on: []
priority: High
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Add Role Prompting and Multishot Examples to devforgeai-ideation Skill

## Description

**As a** DevForgeAI framework maintainer,
**I want** to add a role prompt and multishot examples to the devforgeai-ideation skill,
**so that** Claude adopts a domain-expert persona and produces higher-quality discovery questions, requirements elicitation, and epic decomposition outputs aligned with Anthropic's prompt engineering best practices.

**Context:** This story addresses conformance analysis findings 8.1 (High), 8.2 (High), and 8.3 (Medium) from Category 8: Role Prompting & Examples. The conformance analysis found the skill scored Non-Conformant (the only category with this status) because it lacks both a role prompt and multishot examples.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Category 8, Findings 8.1-8.3

## Provenance

```xml
<provenance>
  <origin document="ideation-anthropic-conformance-analysis.md" section="Category 8: Role Prompting & Examples">
    <quote>"SKILL.md contains no role assignment. The execution model says 'YOU (Claude) execute these instructions' but doesn't establish a domain persona. There is no 'You are a senior business analyst' statement anywhere."</quote>
    <line_reference>Category 8, Finding 8.1</line_reference>
    <quantified_impact>Category 8 scored Non-Conformant (only category at this level); role prompting is "the most powerful way to use system prompts" per Anthropic guidance</quantified_impact>
  </origin>

  <decision rationale="follow-anthropic-best-practices">
    <selected>Add role prompt + multishot examples + completed template example</selected>
    <rejected alternative="role-prompt-only">
      Role prompt alone addresses Finding 8.1 but leaves 8.2 (examples) unresolved; combined approach resolves entire category
    </rejected>
    <trade_off>Increases SKILL.md size by ~30 lines and adds 2 new reference files</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Role Prompt Added to SKILL.md

```xml
<acceptance_criteria id="AC1" implements="FINDING-8.1">
  <given>The SKILL.md file exists without a Role section</given>
  <when>The Role section is added after the Execution Model section (after line 39)</when>
  <then>SKILL.md contains a ## Role section with persona definition including: senior business analyst identity, requirements engineering expertise, and behavioral guidance (apply rigorous thinking, challenge vague requirements, quantify metrics)</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-425/test_ac1_role_prompt.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Multishot Examples Reference File Created

```xml
<acceptance_criteria id="AC2" implements="FINDING-8.2">
  <given>No examples reference file exists in the skill</given>
  <when>A new examples.md file is created in references/</when>
  <then>The file contains 2-3 input/output examples for: (1) Discovery session showing question/answer flow, (2) Epic decomposition showing feature breakdown, with examples wrapped in XML example tags</then>
  <verification>
    <source_files>
      <file hint="Examples reference file">.claude/skills/devforgeai-ideation/references/examples.md</file>
    </source_files>
    <test_file>tests/STORY-425/test_ac2_examples_file.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Completed Epic Template Example Created

```xml
<acceptance_criteria id="AC3" implements="FINDING-8.3">
  <given>The epic-template.md exists but no completed example exists</given>
  <when>A companion example file is created</when>
  <then>The file assets/templates/epic-example-completed.md contains a fully completed epic with high-quality content demonstrating expected output quality, and the original template references this example</then>
  <verification>
    <source_files>
      <file hint="Completed epic example">.claude/skills/devforgeai-ideation/assets/templates/epic-example-completed.md</file>
      <file hint="Original template">.claude/skills/devforgeai-ideation/assets/templates/epic-template.md</file>
    </source_files>
    <test_file>tests/STORY-425/test_ac3_epic_example.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: SKILL.md References Examples File

```xml
<acceptance_criteria id="AC4">
  <given>The examples.md file has been created (AC2)</given>
  <when>Phase 4 epic decomposition section in SKILL.md is updated</when>
  <then>SKILL.md contains a reference pointer: "**For output examples:** → Load `references/examples.md`"</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-425/test_ac4_examples_reference.sh</test_file>
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
      name: "SKILL.md Role Section"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      required_keys:
        - key: "Role.persona"
          type: "string"
          example: "You are a senior business analyst and requirements engineer"
          required: true
          test_requirement: "Test: Grep for 'You are a senior business analyst' in SKILL.md"
        - key: "Role.expertise"
          type: "array"
          example: "['stakeholder discovery', 'requirements elicitation', 'complexity assessment']"
          required: true
          test_requirement: "Test: Role section contains at least 3 expertise areas"
        - key: "Role.behavior"
          type: "string"
          example: "Apply rigorous analytical thinking. Challenge vague requirements."
          required: true
          test_requirement: "Test: Role section contains behavioral guidance"

    - type: "Configuration"
      name: "examples.md Reference File"
      file_path: ".claude/skills/devforgeai-ideation/references/examples.md"
      required_keys:
        - key: "example_count"
          type: "int"
          example: "2"
          required: true
          validation: "Minimum 2 examples required"
          test_requirement: "Test: File contains at least 2 <example> XML blocks"
        - key: "example_format"
          type: "string"
          example: "<example><input>...</input><output>...</output></example>"
          required: true
          test_requirement: "Test: Each example has input/output structure"

    - type: "Configuration"
      name: "epic-example-completed.md"
      file_path: ".claude/skills/devforgeai-ideation/assets/templates/epic-example-completed.md"
      required_keys:
        - key: "epic_structure"
          type: "object"
          required: true
          test_requirement: "Test: File follows epic-template.md structure"

  business_rules:
    - id: "BR-001"
      rule: "Role section must appear after Execution Model section in SKILL.md"
      trigger: "When editing SKILL.md"
      validation: "Grep line numbers to verify Role section follows line 39"
      error_handling: "Fail validation if Role section precedes Execution Model"
      test_requirement: "Test: Role section line number > 39"
      priority: "High"

    - id: "BR-002"
      rule: "Examples must use XML <example> tags per Anthropic guidance"
      trigger: "When creating examples.md"
      validation: "Parse file for <example> XML tags"
      error_handling: "Warn if examples use markdown code fences instead of XML"
      test_requirement: "Test: examples.md contains <example> tags"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Role section must not exceed 15 lines to minimize token overhead"
      metric: "Line count < 15"
      test_requirement: "Test: wc -l on Role section <= 15"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Token Impact:**
- Role section: ~150 tokens additional per skill invocation
- Examples file: Loaded on-demand (progressive disclosure), no upfront cost
- Completed template example: Loaded on-demand, no upfront cost

### Reliability

**Backward Compatibility:**
- Existing ideation workflows continue to work
- Role prompt is additive (no existing content removed)
- Examples are optional reference (no mandatory loading)

---

## Dependencies

### Prerequisite Stories
- None (this is Sprint 1, Feature 1)

### External Dependencies
- None

### Technology Dependencies
- None (changes are to Markdown files only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% for file structure validation

**Test Scenarios:**
1. **Happy Path:** Role section exists with required elements
2. **Edge Cases:**
   - Role section contains minimum required content
   - Examples file has exactly 2 examples
3. **Error Cases:**
   - Missing Role section
   - Examples missing input/output structure

---

## Acceptance Criteria Verification Checklist

### AC#1: Role Prompt Added to SKILL.md

- [ ] Role section added after line 39 - **Phase:** 3 - **Evidence:** SKILL.md
- [ ] Contains "senior business analyst" persona - **Phase:** 3 - **Evidence:** Grep output
- [ ] Contains expertise list (3+ items) - **Phase:** 3 - **Evidence:** Grep output
- [ ] Contains behavioral guidance - **Phase:** 3 - **Evidence:** Grep output

### AC#2: Multishot Examples Reference File Created

- [ ] File references/examples.md created - **Phase:** 3 - **Evidence:** File exists
- [ ] Contains 2+ examples with <example> tags - **Phase:** 3 - **Evidence:** Grep output
- [ ] Each example has input/output structure - **Phase:** 3 - **Evidence:** Parse check

### AC#3: Completed Epic Template Example Created

- [ ] File assets/templates/epic-example-completed.md created - **Phase:** 3 - **Evidence:** File exists
- [ ] Follows epic-template.md structure - **Phase:** 3 - **Evidence:** Structural comparison
- [ ] Original template references the example - **Phase:** 3 - **Evidence:** Grep output

### AC#4: SKILL.md References Examples File

- [ ] Reference pointer added to Phase 4 section - **Phase:** 3 - **Evidence:** Grep output

---

## Definition of Done

### Implementation
- [ ] Role section added to SKILL.md after Execution Model (line 39+)
- [ ] Role section defines business analyst/requirements engineer persona
- [ ] Role section includes expertise areas and behavioral guidance
- [ ] references/examples.md created with 2+ multishot examples
- [ ] Each example uses XML <example> tags with input/output structure
- [ ] assets/templates/epic-example-completed.md created with high-quality content
- [ ] epic-template.md updated to reference completed example
- [ ] SKILL.md Phase 4 references examples.md

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Role section ≤15 lines (token efficiency)
- [ ] Examples demonstrate expected quality level
- [ ] No regression in existing skill functionality

### Testing
- [ ] Test: Role section exists and contains required elements
- [ ] Test: examples.md exists with proper structure
- [ ] Test: epic-example-completed.md follows template structure
- [ ] Test: SKILL.md contains reference pointer

### Documentation
- [ ] SKILL.md changelog updated with v[next] entry
- [ ] examples.md has table of contents (>100 lines rule)

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 1 | STORY-425.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). Target SKILL.md will be restructured — re-evaluate after EPIC-068 Sprint 2 completes. | STORY-425.story.md |

## Notes

**Anthropic Reference:**
- Role prompting: `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/give-claude-a-role.md`
- Multishot examples: `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md`

**Expected Outcome:**
After implementation, Category 8 (Role Prompting & Examples) should move from Non-Conformant to Conformant in the re-run conformance analysis.

---

Story Template Version: 2.9
Last Updated: 2026-02-17
