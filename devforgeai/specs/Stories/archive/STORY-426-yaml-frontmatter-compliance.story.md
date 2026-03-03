---
id: STORY-426
title: "Fix YAML Frontmatter Compliance in devforgeai-ideation Skill"
type: feature
epic: EPIC-067
sprint: Sprint-1
status: Deferred
points: 2
depends_on: []
priority: High
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Fix YAML Frontmatter Compliance in devforgeai-ideation Skill

## Description

**As a** DevForgeAI framework maintainer,
**I want** to fix the YAML frontmatter in the devforgeai-ideation skill and ideate command to comply with Anthropic's Agent Skills specification,
**so that** the skill passes `skills-ref validate` and follows the platform vendor's official schema.

**Context:** This story addresses conformance analysis findings 1.1-1.5 from Category 1: YAML Frontmatter Compliance. Key issues: allowed-tools uses YAML array instead of space-delimited string, includes invalid tools (Skill, Bash(git:*)), and model field format is inconsistent between skill and command.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Category 1, Findings 1.1-1.5

## Acceptance Criteria

### AC#1: Convert allowed-tools to Space-Delimited Format

```xml
<acceptance_criteria id="AC1" implements="FINDING-1.1">
  <given>SKILL.md has allowed-tools as YAML array (lines 4-14)</given>
  <when>The frontmatter is updated</when>
  <then>allowed-tools uses space-delimited string format: "allowed-tools: Read Write Edit Glob Grep AskUserQuestion WebFetch Bash"</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-426/test_ac1_allowed_tools_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Remove Invalid Tools from allowed-tools

```xml
<acceptance_criteria id="AC2" implements="FINDING-1.2,FINDING-1.3">
  <given>SKILL.md allowed-tools includes Skill and Bash(git:*)</given>
  <when>The frontmatter is updated</when>
  <then>Skill tool is removed (not in Agent Skills spec), Bash(git:*) is simplified to Bash (scoped patterns not in spec)</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-426/test_ac2_valid_tools.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Fix Command allowed-tools Delimiter

```xml
<acceptance_criteria id="AC3" implements="FINDING-1.4">
  <given>ideate.md uses comma-delimited allowed-tools (line 6)</given>
  <when>The frontmatter is updated</when>
  <then>Command uses space-delimited format matching Agent Skills spec</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-426/test_ac3_command_tools_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Standardize Model Field Format

```xml
<acceptance_criteria id="AC4" implements="FINDING-1.5">
  <given>SKILL.md uses "model: claude-opus-4-6" and command uses "model: opus"</given>
  <when>Model fields are standardized</when>
  <then>Both files use consistent model format (either both shorthand "opus" or both full model name), and the chosen format is documented</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
      <file hint="Command file">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-426/test_ac4_model_format.sh</test_file>
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
      name: "SKILL.md Frontmatter"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      required_keys:
        - key: "allowed-tools"
          type: "string"
          example: "Read Write Edit Glob Grep AskUserQuestion WebFetch Bash"
          required: true
          validation: "Space-delimited, no commas, no YAML array"
          test_requirement: "Test: Frontmatter allowed-tools is single-line space-delimited"
        - key: "model"
          type: "string"
          example: "opus"
          required: false
          test_requirement: "Test: Model field matches command model field"

    - type: "Configuration"
      name: "ideate.md Frontmatter"
      file_path: ".claude/commands/ideate.md"
      required_keys:
        - key: "allowed-tools"
          type: "string"
          example: "Read Write Edit Glob Skill AskUserQuestion"
          required: true
          validation: "Space-delimited, no commas"
          test_requirement: "Test: Command allowed-tools is space-delimited"

  business_rules:
    - id: "BR-001"
      rule: "allowed-tools format must be space-delimited per Agent Skills spec"
      trigger: "When validating frontmatter"
      validation: "Regex: ^allowed-tools:\\s+[A-Za-z]+( [A-Za-z]+)*$"
      error_handling: "Fail if commas or YAML array syntax detected"
      test_requirement: "Test: Grep for comma in allowed-tools line returns empty"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Frontmatter must pass skills-ref validate"
      metric: "Exit code 0 from validation"
      test_requirement: "Test: skills-ref validate returns success"
      priority: "High"
```

---

## Dependencies

### Prerequisite Stories
- None (Sprint 1 parallel with STORY-425)

---

## Definition of Done

### Implementation
- [ ] SKILL.md allowed-tools converted to space-delimited format
- [ ] Skill tool removed from SKILL.md allowed-tools
- [ ] Bash(git:*) simplified to Bash in SKILL.md
- [ ] Git-only restriction documented in SKILL.md body text
- [ ] ideate.md allowed-tools converted to space-delimited format
- [ ] Model field standardized between SKILL.md and ideate.md

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] No regression in skill functionality
- [ ] Frontmatter passes YAML syntax validation

### Testing
- [ ] Test: allowed-tools space-delimited format
- [ ] Test: No invalid tools in allowed-tools
- [ ] Test: Model field consistency

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 4 | STORY-426.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). Target SKILL.md frontmatter may change with rename — re-evaluate after EPIC-068 Sprint 3. | STORY-426.story.md |

## Notes

**Anthropic Reference:**
- Agent Skills spec: `.claude/skills/claude-code-terminal-expert/references/skills/agent-skills-spec.md` (lines 173-198 for allowed-tools)

**Quick Win:** This story is 2 points because changes are simple find-and-replace operations in frontmatter. Low risk, high conformance impact.

---

Story Template Version: 2.9
Last Updated: 2026-02-17
