---
id: STORY-159
title: Create /create-stories-from-rca Command Shell
type: feature
epic: EPIC-032
priority: Medium
points: 5
depends_on: ["STORY-155", "STORY-156", "STORY-157", "STORY-158"]
status: Backlog
created: 2025-12-25
---

# STORY-159: Create /create-stories-from-rca Command Shell

## User Story

**As a** DevForgeAI developer,
**I want** a lean `/create-stories-from-rca` slash command,
**So that** I can invoke RCA-to-Story automation with a simple command following DevForgeAI orchestration patterns.

## Acceptance Criteria

### AC#1: Create Command File with YAML Frontmatter

**Given** the need for a new slash command
**When** creating the command
**Then** a file is created at `.claude/commands/create-stories-from-rca.md` with valid YAML frontmatter (name, description, argument-hint, allowed-tools)

### AC#2: Implement Argument Parsing and Validation

**Given** a user runs `/create-stories-from-rca RCA-022`
**When** the command executes
**Then** the RCA ID argument is parsed, validated (format RCA-NNN), and the corresponding file is located in `devforgeai/RCA/`

### AC#3: Implement Help Text

**Given** a user runs `/create-stories-from-rca --help` or `/create-stories-from-rca help`
**When** the command executes
**Then** comprehensive help text is displayed with usage, examples, and related commands

### AC#4: Handle Invalid Arguments

**Given** a user provides an invalid RCA ID or missing argument
**When** the command executes
**Then** a clear error message is displayed with format guidance and list of available RCAs

### AC#5: Orchestrate to Story Creation Components

**Given** valid RCA ID is provided
**When** the command executes
**Then** the command orchestrates: Parse RCA (STORY-155) → Select Recommendations (STORY-156) → Create Stories (STORY-157) → Link Back (STORY-158)

## Technical Specification

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Configuration
      name: CommandFrontmatter
      path: .claude/commands/create-stories-from-rca.md
      description: YAML frontmatter for slash command
      fields:
        - name: name
          value: create-stories-from-rca
        - name: description
          value: Create user stories from RCA recommendations
        - name: argument-hint
          value: "RCA-NNN [--help]"
        - name: model
          value: sonnet
        - name: allowed-tools
          value: [Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite]
      test_requirement: Command registered and invocable via /create-stories-from-rca

    - type: Service
      name: CommandOrchestrator
      path: .claude/commands/create-stories-from-rca.md
      description: Lean orchestration shell for RCA-to-Story workflow
      dependencies:
        - RCAParser (STORY-155)
        - RecommendationSelector (STORY-156)
        - BatchStoryCreator (STORY-157)
        - RCAStoryLinker (STORY-158)
      test_requirement: Command orchestrates all 4 phases in sequence

  business_rules:
    - id: BR-001
      name: Lean Orchestration
      description: Command delegates to skills/subagents, contains no business logic
      test_requirement: Command file < 15,000 characters (per lean orchestration standard)

    - id: BR-002
      name: RCA ID Format
      description: Accept case-insensitive RCA ID (rca-022 → RCA-022)
      test_requirement: Both RCA-022 and rca-022 locate same file

    - id: BR-003
      name: File Existence Check
      description: Verify RCA file exists before proceeding
      test_requirement: Non-existent RCA ID displays error with available RCAs

  non_functional_requirements:
    - category: Architecture
      requirement: Command size < 15K characters
      metric: character_count < 15000
      test_requirement: Command file measured at < 15,000 characters

    - category: Usability
      requirement: Clear error messages with actionable guidance
      metric: All error messages include next steps
      test_requirement: Error messages tested for clarity

    - category: Compliance
      requirement: Follow DevForgeAI command patterns
      metric: Matches /create-missing-stories structure
      test_requirement: Command structure reviewed against template
```

## Edge Cases

1. **No argument:** Display usage message and list available RCAs.

2. **RCA not found:** Display error with list of valid RCA IDs.

3. **RCA has no recommendations:** Display message and exit (no stories to create).

4. **User cancels selection:** Exit gracefully with message.

5. **All story creations fail:** Display failure summary, RCA not updated.

## Non-Functional Requirements

- **Architecture:** Command size < 15K characters (lean orchestration)
- **Usability:** Clear error messages with actionable guidance
- **Compliance:** Follow DevForgeAI command patterns (matches /create-missing-stories)
- **Documentation:** Help text covers all options and examples

## Definition of Done

### Implementation
- [ ] Command file created at .claude/commands/create-stories-from-rca.md
- [ ] YAML frontmatter with all required fields
- [ ] Argument parsing and validation
- [ ] Help text (--help flag)
- [ ] Error handling with clear messages
- [ ] Orchestration to all 4 component stories

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Command size verified < 15K characters
- [ ] Error messages reviewed for clarity
- [ ] Help text reviewed for completeness

### Testing
- [ ] Unit test for argument parsing
- [ ] Integration test for full workflow
- [ ] End-to-end test with real RCA

### Documentation
- [ ] Command added to commands-reference.md
- [ ] Usage examples in help text

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-25 | DevForgeAI | Story created via /create-missing-stories batch mode |
