---
id: STORY-141
title: Question Duplication Elimination
epic: EPIC-029
sprint: Backlog
status: Backlog
points: 6
depends_on: ["STORY-130", "STORY-131", "STORY-132"]  # EPIC-028 refactoring must complete first
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Question Duplication Elimination

## Description

**As a** user executing the /ideate command,
**I want** to answer each question only once (in the skill, not repeated in the command),
**so that** the workflow feels streamlined and I'm not asked the same question twice.

## Acceptance Criteria

### AC#1: Remove Project Type Question from Command

**Given** the current /ideate command asks for project type in Phase 1
**When** the command is refactored
**Then** the project type question is removed from the command:
- Command Phase 1 only validates business idea argument
- Skill Phase 1 Step 1 asks all discovery questions including project type
- Single source of truth for discovery questions: skill only

**Test Requirements:**
- Grep command file for "project type" - should not appear
- Verify skill asks project type
- Verify no duplicate question in workflow

---

### AC#2: Remove All Discovery Questions from Command

**Given** the /ideate command contains discovery-related AskUserQuestion calls
**When** the command is refactored
**Then** all discovery questions are delegated to skill:
- Command responsibilities limited to:
  - Argument validation (business idea non-empty)
  - Brainstorm detection and selection
  - Skill invocation
- Skill responsibilities include ALL:
  - Project type (greenfield/brownfield)
  - Complexity assessment inputs
  - Domain-specific questions
  - Priority clarifications

**Test Requirements:**
- Count AskUserQuestion in command (should be minimal: brainstorm selection only)
- Count AskUserQuestion in skill (should include all discovery questions)
- End-to-end test: no repeated questions

---

### AC#3: Skill Owns Question Templates

**Given** discovery questions need to be asked
**When** the ideation workflow executes
**Then** all question templates reside in skill reference files:
- `references/discovery-workflow.md` contains question templates
- `references/requirements-elicitation-workflow.md` contains domain questions
- Command does NOT contain question templates (except brainstorm selection)

**Test Requirements:**
- Verify question templates in skill references
- Verify command has no question templates (grep for AskUserQuestion patterns)
- Verify templates are complete and well-formatted

---

### AC#4: Command Passes Context to Skill

**Given** the command detects a brainstorm file to continue from
**When** the skill is invoked
**Then** context is passed via conversation markers:
- `**Business Idea:** {user-provided description}`
- `**Brainstorm Context:** {brainstorm-id}` (if continuing from brainstorm)
- `**Brainstorm File:** {path}` (if continuing from brainstorm)
- Skill extracts context from conversation, not from re-asking user

**Test Requirements:**
- Verify context markers in conversation before skill invocation
- Verify skill reads markers correctly
- Verify no re-asking of context already provided

---

### AC#5: Zero Duplicate Questions in End-to-End Flow

**Given** a user runs `/ideate "Build a task management app"`
**When** the complete ideation workflow executes
**Then** each question is asked exactly once:
- No "What type of project?" asked twice
- No "What is the primary domain?" asked twice
- No "How complex is this project?" asked twice
- User feedback: "No repetitive questions"

**Test Requirements:**
- Record all AskUserQuestion invocations in workflow
- Verify each question topic appears once
- Manual verification with test user

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  reference_files:
    command_to_modify: ".claude/commands/ideate.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    discovery_workflow: ".claude/skills/devforgeai-ideation/references/discovery-workflow.md"
    requirements_elicitation: ".claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md"
    user_input_guidance: ".claude/skills/devforgeai-ideation/references/user-input-guidance.md"

  prerequisite_stories:
    description: "This story builds on EPIC-028 refactoring which simplifies the command structure"
    stories:
      - id: "STORY-130"
        title: "Delegate Artifact Verification to Skill"
        relevance: "Removes duplicate verification, enabling cleaner question flow"
      - id: "STORY-131"
        title: "Delegate Summary Presentation to Skill"
        relevance: "Removes duplicate summary, reducing command question scope"
      - id: "STORY-132"
        title: "Delegate Next Action Determination to Skill"
        relevance: "Removes duplicate next-action question from command"

  components:
    - name: CommandPhase1Simplified
      type: Configuration
      description: "Simplified command Phase 1 with argument validation only"
      location: ".claude/commands/ideate.md"
      responsibilities:
        - "Validate business idea argument non-empty"
        - "Detect brainstorm files"
        - "Offer brainstorm selection (if found)"
        - "Set context markers"
        - "Invoke skill"
      not_responsible_for:
        - "Discovery questions"
        - "Project type classification"
        - "Domain detection"
      test_requirement: "Command simplification verification"

    - name: SkillDiscoveryOwnership
      type: Configuration
      description: "Skill Phase 1 owns all discovery questions"
      location: ".claude/skills/devforgeai-ideation/SKILL.md"
      responsibilities:
        - "All discovery questions"
        - "Project type classification"
        - "Domain detection"
        - "Complexity assessment"
      test_requirement: "Verify all questions in skill"

    - name: ContextMarkerProtocol
      type: Configuration
      description: "Protocol for passing context from command to skill"
      location: ".claude/commands/ideate.md"
      markers:
        - "**Business Idea:** {text}"
        - "**Brainstorm Context:** {id}"
        - "**Brainstorm File:** {path}"
      test_requirement: "Context marker parsing tests"

  business_rules:
    - id: BR-001
      description: "Command MUST NOT contain discovery question templates"
      test_requirement: "Grep command for discovery patterns"

    - id: BR-002
      description: "Skill MUST be single source of truth for all questions"
      test_requirement: "Question template location verification"

    - id: BR-003
      description: "Context passed via markers, not re-asking"
      test_requirement: "Context marker flow test"

  non_functional_requirements:
    - id: NFR-001
      category: User Experience
      description: "Zero duplicate questions in workflow"
      metric: "Duplicate question count"
      target: "0"
      test_requirement: "End-to-end question audit"

    - id: NFR-002
      category: Maintainability
      description: "Question templates in single location"
      metric: "Template locations"
      target: "1 location (skill references)"
      test_requirement: "Template location audit"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# None identified at Architecture phase
```

---

## Edge Cases

| # | Scenario | Expected Behavior | Test Approach |
|---|----------|-------------------|---------------|
| 1 | Brainstorm has project type, skill asks again | Skill checks brainstorm context first, skips if present | Pre-set context marker test |
| 2 | User provides project type in business idea | NLP extraction in skill, confirm with user | "Build a greenfield task app" test |
| 3 | Command context markers missing | Skill asks all questions (no crash) | Clear context before skill invoke |
| 4 | Multiple brainstorms with different project types | Use selected brainstorm's type | Multi-brainstorm test |

---

## UI Specification

**Not applicable** - Workflow refactoring with no new UI elements.

---

## Definition of Done

### Implementation
- [ ] Project type question removed from command
- [ ] All discovery questions removed from command
- [ ] Question templates moved to skill references
- [ ] Context marker protocol implemented
- [ ] Skill updated to read context markers

### Quality
- [ ] All acceptance criteria verified with tests
- [ ] Code follows coding-standards.md patterns
- [ ] No CRITICAL or HIGH anti-pattern violations
- [ ] Command line count reduced (target: ≤200 lines)

### Testing
- [ ] Command simplification verified (grep for patterns)
- [ ] Skill ownership verified
- [ ] Context marker flow tests
- [ ] End-to-end duplicate question audit
- [ ] Coverage meets thresholds (95%/85%/80%)

### Documentation
- [ ] Question ownership documented
- [ ] Context marker protocol documented
- [ ] Migration notes for existing workflows

---

## Implementation Notes

### Architecture Decisions
- **Decision:** Skill owns all discovery questions, command only orchestrates
- **Rationale:** Single source of truth prevents duplication, aligns with lean orchestration
- **Reference:** EPIC-028 Feature 1-3, lean-orchestration-pattern.md

### Related Stories
- **EPIC-028 STORY-130:** Delegate Artifact Verification to Skill
- **EPIC-028 STORY-131:** Delegate Summary Presentation to Skill
- **EPIC-028 STORY-132:** Delegate Next Action Determination to Skill

This story complements the EPIC-028 refactoring by eliminating duplicate questions specifically.

---

## Workflow Status

- [ ] Story created
- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

**Created:** 2025-12-22
**Source:** /create-missing-stories EPIC-029 (batch mode)
**Epic Reference:** EPIC-029 Feature 6: Question Duplication Elimination
